from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from schemas import ChatRequest
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_players_by_position
from openai import OpenAI
import os
from dotenv import load_dotenv

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

@app.post("/chat")
async def chat_gpt(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Use "gpt-4.1" if you have access, otherwise "gpt-4" or "gpt-3.5-turbo"
            messages=[
                {"role": "user", "content": request.prompt}
            ],
            temperature=0.7
        )
        full_text = response.choices[0].message.content
        print(request)
        print(full_text)
        
        # Parse the lineup from the response text
        lineup = extract_players_by_position(full_text)
        
        return {"response": full_text, "lineup": lineup}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/extract-lineup")
# async def extract_lineup(request: ChatRequest):
#     response = openai.ChatCompletion.create(
#         model="gpt-4.1",
#         messages=request.messages
#     )
#     full_text = response.choices[0].message.content
#     players = extract_players_by_position(full_text)
#     return {"lineup": lineup, "text": full_text}
