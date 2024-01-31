# ThunderBot - Discord Yu-Gi-Oh! Card Bot

ThunderBot is a Discord bot designed to provide information about Yu-Gi-Oh! trading cards using the Yu-Gi-Oh! ProDeck API. Users can retrieve card images, detailed card information, translate card names, search for cards, and view card prices directly within Discord.

## Features

- **!card (lang) (cardName):** Returns the image of the specified card.
- **!info (lang) (cardName):** Provides detailed information about the specified card.
- **!tr (original_lang) (cardName) (translate_lang):** Translates the name of the card from one language to another.
- **!search (lang) (cardName):** Searches for cards based on a character sequence.
- **!prices (lang) (cardName):** Shows the prices of the specified card.

## Getting Started

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ThunderBot.git
   cd ThunderBot
   ```

2. Install dependencies:

   ```bash
   ./setup.sh
   ```

3. Create a `.env` file in the project root and add your Discord API key:

   ```dotenv
   DISCORD_API_KEY=your_discord_api_key
   ```

4. Run the bot:

   ```bash
   python bot.py
   ```

## Usage

- Invite [ThunderBot](https://discord.com/api/oauth2/authorize?client_id=1201190749727887481&permissions=2048&scope=bot) to your Discord server.
- Use the provided commands in Discord to interact with ThunderBot.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the bot.

## Acknowledgments

- Thanks to [Yu-Gi-Oh! ProDeck API](https://db.ygoprodeck.com) for providing card data.
- Thanks to [Kraus](https://www.deviantart.com/kraus-illustration) for bot image in discord.

