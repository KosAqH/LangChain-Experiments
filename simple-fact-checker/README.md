# Fact-Checker Agent

An AI-powered agent that verifies the accuracy of claims using web research and the CRAAP test methodology.

## What It Does

- Takes user input and breaks claims into testable statements
- Searches the internet for evidence using the Tavily API
- Cross-references information and looks for conflicting data
- Evaluates findings using the CRAAP test (Currency, Relevance, Authority, Accuracy, Purpose)
- Generates markdown reports with structured findings, evidence, and confidence scores

## Requirements

- Python 3.13+
- Installed uv
- OpenRouter API key
- Tavily API key

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```
2. Create a `.env` file with your API keys. Use `env.example` file for reference:

   ```
   TAVILY_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ```
3. Run the agent:

   ```bash
   uv run simple-fact-checker/agent.py
   ```

## Usage

```
Enter a query (or 'quit' to exit): Is the Earth flat?
```

The agent will:

- Analyze the claim
- Search for evidence
- Generate a report saved to `reports/` folder
- Save raw search tavily results to `logs/raw_searches/`

## Output

Reports include:

- Original claim
- Evidence summary
- References/sources
- Verdict (True/False/Uncertain)
- Confidence score

## Showcase

https://github.com/user-attachments/assets/dbbb6bd8-1a85-4fe6-8037-468d782814cc

