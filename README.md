# Current Events Research Agent

A full-stack, LangGraph-powered agent that generates news-style, all-you-need-to-know reports about current events topics.

## Setup

1. Clone the repo
```bash
git clone https://github.com/clayostroff/CERA.git
cd CERA
```

2. Make and activate a new venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the backend dependencies
```bash
pip install -r requirements.txt
```

4. Install the frontend dependencies
```bash
npm install
```

5. Create a `.env` file in the backend directory with your API keys
```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

6. Start the backend server
```bash
npm run start
```
This will start the FastAPI server at http://localhost:8000.

7. In a new terminal, start the frontend server
```bash
npm run dev
```
This will start the Vite development server, typically at http://localhost:5173.

8. Navigate to the URL shown in your terminal (usually http://localhost:5173).

## Stack
- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Python, LangChain, LangGraph, FastAPI