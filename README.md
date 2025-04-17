# Current Events Research Agent

A multi-node agent that generates a news-like report about current events topics.

## Setup

1. Clone the repo
```bash
git clone https://github.com/clayostroff/CERA.git
cd CERA
```

2. Make and activate a venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies
```bash
pip install -r backend/requirements.txt
```

4. Create a `.env` with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

5. Run the agent
```bash
python main.py
```