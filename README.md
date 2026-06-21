# poo — Discord AI Chatbot

An AI-powered Discord bot built with discord.py and the Groq API. Designed to feel like a casual, humorous companion in a Discord server, with persistent conversation memory and a daily mood system.

## Features
- 🧠 **Conversation memory** — keeps the last 20 messages per channel for context-aware replies
- 🎭 **Daily mood system** — bot's personality shifts slightly day to day
- 🔐 **Admin commands** — restricted commands (e.g. `!reset`) for designated admin users
- 💬 **Casual Bahasa Indonesia responses** — tuned to chat naturally with server members
- ⚡ **Powered by Groq API** — using `llama-3.1-8b-instant` for fast responses

## Tech Stack
- Python
- discord.py
- Groq API

## Setup
1. Clone this repo
2. Install dependencies:
```bash
   pip install discord.py groq python-dotenv
```
3. Create a `.env` file in the root directory:
DISCORD_TOKEN=your_discord_bot_token

GROQ_API_KEY=your_groq_api_key
4. Run the bot:
```bash
   python bot.py
```

## Note
This bot is designed for personal/community Discord servers as a fun, lightweight AI companion — not intended for production-scale deployment.
