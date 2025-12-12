from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from schemas import ChatRequest
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_players_by_position
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

# @app.post("/chat")
# async def chat_gpt(request: PromptRequest):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4",  # Use "gpt-4.1" if you have access, otherwise "gpt-4" or "gpt-3.5-turbo"
#             messages=[
#                 {"role": "user", "content": request.prompt}
#             ],
#             temperature=0.7
#         )
#         full_text = response.choices[0].message.content
#         print(request)
#         print(full_text)
        
#         # Parse the lineup from the response text
#         lineup = extract_players_by_position(full_text)
        
#         return {"response": full_text, "lineup": lineup}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # @app.post("/extract-lineup")
# # async def extract_lineup(request: ChatRequest):
# #     response = openai.ChatCompletion.create(
# #         model="gpt-4.1",
# #         messages=request.messages
# #     )
# #     full_text = response.choices[0].message.content
# #     players = extract_players_by_position(full_text)
# #     return {"lineup": lineup, "text": full_text}
def find_table_after_header(soup, possible_ids, section_friendly_name):
    for section_id in possible_ids:
        header = soup.find("span", id=section_id)
        if header:
            nxt = header.parent
            while nxt:
                nxt = nxt.find_next_sibling()
                if not nxt:
                    break
                if nxt.name == "table":
                    return nxt
    
    # Fallback: search for table by column headers
    print(f"Could not find header for: {section_friendly_name}. Trying fallback...")
    all_tables = soup.find_all("table")
    for table in all_tables:
        ths = [t.get_text(strip=True) for t in table.find_all("th")]
        if any(col in ths for col in ["Player", "Pos.", "Date of birth (age)"]):
            print(f"Fallback matched table for: {section_friendly_name}")
            return table
    
    return None

def parse_wiki_table(table):
    rows = []
    for row in table.find_all("tr"):
        cells = row.find_all(["td", "th"])
        row_text = [c.get_text(" ", strip=True) for c in cells]
        if row_text:
            rows.append(row_text)
    return rows

@app.post("/chat")
async def chat(request: PromptRequest):
    try:
        # Scrape Wikipedia
        url = "https://en.wikipedia.org/wiki/Argentina_national_football_team"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Get current squad
        current_squad_table = find_table_after_header(
            soup,
            ["Current_squad", "Current squad"],
            "Current Squad"
        )
        current_squad = parse_wiki_table(current_squad_table) if current_squad_table else []
        print(f"Current squad rows: {len(current_squad)}")
        
        # Get recent callups - find all tables and get the second one with player data
        all_tables = soup.find_all("table")
        recent_callups = []
        table_count = 0
        for table in all_tables:
            ths = [t.get_text(strip=True) for t in table.find_all("th")]
            if any(col in ths for col in ["Player", "Pos.", "Date of birth (age)"]):
                table_count += 1
                if table_count == 2:
                    recent_callups = parse_wiki_table(table)
                    break
        print(f"Recent callups rows: {len(recent_callups)}")
        
        # Send to AI with the scraped data
        enhanced_prompt = f"{request.prompt}\n\nCurrent Argentina squad: {current_squad}\n\nRecent call-ups: {recent_callups}\n\n IMPORTANT: Select EXACTLY 11 players total. Do not include substitutes or bench players. Only the starting 11. The players can either be from current squad or recent callups"
        
        print("prompt: ", enhanced_prompt)

        ai_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": enhanced_prompt}],
            temperature=0.7
        )
        print("response: ", ai_response.choices[0].message.content)
        return {"response": ai_response.choices[0].message.content}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
