# Autonomous AI Research Agent

A small, runnable Python project that researches a topic using public web search, gathers source snippets, generates a structured report with numbered citations using an OpenAI model, and lets you download the report as Markdown.

## Features
- Streamlit web interface
- Public web search via `ddgs`
- LLM-generated report when an OpenAI API key is configured
- Numbered source citations and source list
- Markdown report download and local report saving
- Source-digest fallback if no API key is configured

## Requirements
- Python 3.10 or newer (Python 3.11 recommended)
- Internet connection
- OpenAI API key for AI synthesis (API usage may incur charges)

## Windows: step-by-step run instructions

### 1. Install Python
Install Python 3.11 from the official Python website. During setup, enable **Add Python to PATH**.
Check it in Command Prompt:
```bat
python --version
```

### 2. Extract the ZIP
Extract `autonomous_ai_research_agent.zip` to a folder, for example:
`C:\Projects\autonomous_ai_research_agent`

### 3. Open a terminal in the project folder
In File Explorer, open the extracted folder, click the address bar, type `cmd`, and press Enter.

### 4. Create and activate a virtual environment
```bat
python -m venv .venv
.venv\Scripts\activate
```
If PowerShell is being used instead of Command Prompt:
```powershell
.\.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, use Command Prompt or follow Microsoft's execution-policy guidance.

### 5. Install dependencies
```bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Configure the API key
Copy `.env.example` and name the copy `.env`. Open `.env` in a text editor and replace `your_api_key_here` with your OpenAI API key:
```env
OPENAI_API_KEY=your_actual_key
OPENAI_MODEL=gpt-4o-mini
```
Keep `.env` private. Do not upload it to GitHub or share it. You can run without a key, but the app will only show a source digest instead of an LLM-written synthesis.

### 7. Start the app
```bat
streamlit run app.py
```
Streamlit should open the app in your browser. If it does not, use the local address printed in the terminal (usually `http://localhost:8501`).

### 8. Run your first research task
1. Enter a specific research question.
2. Optionally add a focus, such as “prioritize official sources”.
3. Choose how many sources to collect.
4. Click **Run research**.
5. Review the report and open the source links to verify important claims.
6. Click **Download Markdown report** to save the report.

### 9. Stop the app
Return to the terminal and press `Ctrl+C`.

## macOS / Linux quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key
streamlit run app.py
```

## Project structure
```text
autonomous_ai_research_agent/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── reports/                 # created automatically; generated reports are saved here
```

## How it works
1. **Question intake:** receives a research question and optional focus.
2. **Search:** searches the web for the question (and focus, if supplied).
3. **Deduplication:** removes duplicate result URLs.
4. **Synthesis:** sends titles, URLs, and snippets to the configured LLM.
5. **Citation discipline:** asks the model to use numbered references and flag uncertainty.
6. **Export:** displays and saves the report as Markdown.

## Limitations and safety
- This is a practical starter project, not a fully autonomous multi-agent system.
- Search providers may rate-limit or change their response format.
- The LLM receives search-result snippets, not necessarily the complete web pages; it can miss context.
- Numbered citations are based on the supplied search results. Always verify critical claims in the original pages.
- Do not use generated output as the sole basis for medical, legal, financial, or other high-impact decisions.
- API usage may cost money. Check your provider's current pricing and usage limits.

## Troubleshooting
- **`python` not found:** reinstall Python and enable PATH, or try `py` instead of `python`.
- **`streamlit` not found:** activate `.venv`, then run `python -m pip install -r requirements.txt`.
- **API authentication error:** check the key in `.env`, ensure there are no extra spaces, and confirm the key has API access.
- **No search results / search error:** retry later, check your internet connection, or try a more specific query.
- **Port 8501 is busy:** run `streamlit run app.py --server.port 8502`.

## Next upgrades
- Fetch and parse full web pages with domain allowlists and robots-aware retrieval.
- Add planning and reflection loops with bounded tool calls.
- Add a vector database and retrieval over saved research.
- Add evaluation for citation correctness, source diversity, and answer faithfulness.
- Add structured JSON logs, tests, caching, and Docker deployment.
