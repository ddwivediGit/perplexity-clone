# Unperplexed

Unperplexed is an AI-powered search tool that delivers web-backed answers and smart follow-up questions. Built with [Tavily](https://tavily.com) for web search and [Groq](https://groq.com) for LLM responses, it’s deployed on [Streamlit Community Cloud](https://streamlit.io/cloud). Think of it as a simpler, open-source take on AI search!

## Features

**Web-Sourced Answers**: Pulls context from Tavily’s search API.
**Model Selection**: Choose from 5 Groq models (e.g., `mixtral-8x7b-32768`, `llama-3.1-8b-instant`).
**Processing Modes**: "Adapts to Question" for quick replies, "Think Hard" for deeper reasoning.
**Follow-Ups**: Generates 3 relevant follow-up questions to explore further.

## Demo

Try it live: [https://unperplexed.streamlit.app]


## Setup

   git clone  https://github.com/ddwivediGit/perplexity-clone.git
   cd unperplexed

   pip install streamlit tavily-python groq

   streamlit run app.py

## Usage
Open the app in your browser.
Select a model and mode.
Ask a question (e.g., "What’s the economic outlook for India?").
Get an answer, sources, and follow-ups to copy-paste.
## Reuse
Feel free to fork this repo, tweak the code, or build on it! Contributions welcome—submit a PR or open an issue.

## Tech Stack
Tavily: Web search API.
Groq: LLM inference.
Streamlit: UI and deployment.

## License
MIT License—free to use, modify, and distribute.

Built with ❤️ by Dib. 