# Telegram Inline AI Bot 🤖

A production-ready Telegram bot with inline query support, powered by DeepSeek AI with multiple personality modes and Wikipedia integration.

## Features

✨ **Inline Query Support**
- Use the bot inline: `@botname your question`
- Get instant AI-powered responses

🧠 **Personality Modes**
- Smart Mode: Intelligent and accurate responses
- Funny Mode: Humorous and entertaining responses
- Savage Mode: Direct and no-nonsense responses

📚 **Wikipedia Integration**
- Automatic Wikipedia context for factual queries
- Enhanced responses with real-world knowledge

⚡ **Fast & Reliable**
- Async/await for optimal performance
- Error handling and fallback responses
- Railway.app ready

## Tech Stack

- **Language**: Python 3.11+
- **Bot Library**: python-telegram-bot v20+
- **AI**: DeepSeek API
- **Knowledge**: Wikipedia API
- **Hosting**: Railway.app

## Commands

- `/start` - Welcome message and current mode display
- `/help` - Help and features information
- `/mode` - Switch personality mode with inline buttons

## Project Structure

```
telegram-inline-ai-bot/
├── main.py              # Main bot logic
├── ai_engine.py         # DeepSeek API wrapper
├── wiki_engine.py       # Wikipedia integration
├── requirements.txt     # Python dependencies
├── Procfile            # Railway configuration
├── runtime.txt         # Python version
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Quick Start

### Local Setup

```bash
# Clone repository
git clone <your-repo>
cd telegram-inline-ai-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run bot
python main.py
```

### Railway Deployment

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway link
git push
```

## Usage

### Inline Queries

Open any chat and type:
```
@yourbot what is machine learning?
```

### Mode Switching

Send `/mode` command to switch between personality modes.

## API Configuration

- **DeepSeek Model**: deepseek-chat
- **Max Tokens**: 300
- **Temperature**: 0.7
- **Timeout**: 30 seconds

## Error Handling

✅ API timeout handling
✅ Wikipedia not found graceful fallback
✅ Invalid queries handling
✅ Network error recovery
✅ User mode persistence

## License

MIT License

## Support

For issues:
- Check README first
- Review error logs
- Contact administrator