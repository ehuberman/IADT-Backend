# IADT Backend (POC)

FastAPI backend for generating AI-driven soccer tactics using real-world player data and dynamic prompt construction.

## Architecture

This project is part of a full-stack system:

- Frontend: Angular app for lineup visualization and user interaction  
  👉 https://github.com/ehuberman/IADT-Frontend
- Backend: FastAPI service for data enrichment and AI-powered tactical generation (this repository)

The backend enhances user input with real-world data and generates tactical insights using an LLM.

## Tech Stack

- FastAPI  
- Python  
- OpenAI API (GPT-4)  
- BeautifulSoup (web scraping)  
- Requests  

## Features

- REST API endpoint for tactical generation (`POST /chat`)  
- Scrapes live squad data from Wikipedia (Argentina national team)  
- Extracts structured player data from HTML tables  
- Dynamically enriches prompts with real-world squad + call-up data  
- Generates AI-driven tactical responses using GPT-4  

## How It Works

1. Receives a prompt from the frontend  
2. Scrapes current squad + recent call-ups from Wikipedia  
3. Parses player data into structured format  
4. Enhances the prompt with real-world context  
5. Sends enriched prompt to OpenAI API  
6. Returns AI-generated tactical response  

## Getting Started

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will run locally at `http://localhost:8000`.

## Environment Variables

Create a `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Notes

This project was built to explore:

- Combining web scraping with AI-driven decision making  
- Prompt engineering with dynamic real-world data  
- Full-stack communication between Angular and FastAPI  

## Future Improvements

- Cache scraped data to reduce repeated requests  
- Add structured response schemas (JSON output)  
- Support multiple teams and leagues  
- Improve error handling and fallback logic  
- Deploy as a scalable API service 
