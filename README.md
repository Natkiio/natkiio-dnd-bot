# D&D Discord Bot

A simple Discord bot for D&D dice rolling and character generation.

## Features

- `/roll 2d6` - Roll any dice notation
- `/roll 1d20+5` - Roll with modifiers
- `/advantage 3` - Roll with advantage (2d20, take higher)
- `/disadvantage -1` - Roll with disadvantage (2d20, take lower)
- `/stats` - Roll character stats (4d6 drop lowest, 6 times)

## Setup

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give it a name (e.g., "D&D Dice Bot")
4. Go to "Bot" section
5. Click "Reset Token" and copy the token
6. Enable "Message Content Intent" under Privileged Gateway Intents

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Bot

Create a `.env` file in the project directory:

```
DISCORD_TOKEN=your_token_here
```

Replace `your_token_here` with the token you copied.

### 4. Invite Bot to Server

1. In Discord Developer Portal, go to "OAuth2" > "URL Generator"
2. Select scopes: `bot` and `applications.commands`
3. Select permissions: `Send Messages`, `Embed Links`
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

### 5. Run Bot

```bash
python bot.py
```

You should see: "Bot is now running!"

## Usage

In your Discord server, type:
- `/roll 1d20` - Roll a d20
- `/roll 2d6+3` - Roll 2d6 with +3 modifier
- `/advantage 5` - Roll with advantage, +5 modifier
- `/stats` - Generate character stats

## Deployment (Optional)

Deploy to Render for free 24/7 hosting:

1. Create account on [Render](https://render.com)
2. Create new "Web Service"
3. Connect GitHub repository
4. Add environment variable: `DISCORD_TOKEN`
5. Deploy

## Tech Stack

- Python 3.9+
- discord.py 2.3.2
- python-dotenv 1.0.0

---

Built by Nathan Lyons | [GitHub](https://github.com/nathanlyons)
