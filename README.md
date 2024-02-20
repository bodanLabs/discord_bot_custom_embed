# Custom Discord Embed Bot

This repository contains the source code for a Discord bot designed to create and manage custom embed messages within Discord channels. Utilizing the discord.py library, this bot offers an interactive interface for users to customize embeds through commands and modal inputs.

## Features
- Custom Embed Creation: Users can create custom embed messages with dynamic content, including titles, descriptions, and colors.
- Interactive Modals and Buttons: Leverages Discord's modal and button components for user-friendly interaction and customization of embeds.
- Slash Command Integration: Utilizes slash commands for ease of use and accessibility within Discord servers.

## Components
- bot.py: The main bot script that handles Discord events, commands, and interactions.
- embed_creator.py: A utility module that defines classes and views for creating and customizing embeds through interactive modals and buttons.

## Setup

### Prerequisites
- Python 3.8 or higher
- discord.py library
- A Discord Bot Token

### Installation
1. Clone this repository or download the source files.
2. Install the required Python packages:
```pip install discord```
3. Update the TOKEN variable in bot.py with your Discord Bot Token.
4. Run bot.py to start the bot:
```python bot.py```

## Usage
Once the bot is running and added to your Discord server, use the following command to start creating custom embeds:
```/embed [channel]```
Follow the interactive prompts to customize your embed's title, description, and color. The bot will guide you through each step, providing buttons and modals to input your customizations.

## Contributing
Contributions, bug reports, and feature requests are welcome! Please feel free to fork the repository and submit pull requests with your improvements.
