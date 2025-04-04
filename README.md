# Sorting-Bot

A Discord bot designed to manage and coordinate multiplayer games for your Discord server. Currently supports Among Us sessions and Minecraft Manhunt organization.

## Features

### Among Us Session Management

- Start/stop game sessions
- Player registration system
- Random player selection
- Private code distribution via DM
- Blacklist system for moderation
- Channel-specific command restrictions
- Role-based access control

### Minecraft Manhunt

- Player registration with Minecraft IGN verification
- Integration with Mojang API
- Google Sheets integration for player tracking
- Update/remove registration
- Automated IGN validation

### Utility Commands

- Message purge functionality
- Module management system
- Role-based administrative controls

## Setup

1. Clone the repository:

```bash
git clone https://github.com/0xPiyush/Sorting-Bot.git
cd Sorting-Bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the bot:

   - Add your Discord bot token in `SortingBot.py`
   - Configure Google Sheets credentials in `cogs/GoogleSheetsCreds.json`
   - Customize `config_model.py` settings if needed

4. Run the bot:

```bash
python SortingBot.py
```

## Command Prefix

The bot uses `.sb` as its default command prefix.

## Core Commands

### Among Us Commands

- `.sb au start` - Start an Among Us session
- `.sb au register` - Register for the current session
- `.sb au pick <code> <server> [number]` - Pick random players
- `.sb au blacklist <user>` - Blacklist a user

### Minecraft Manhunt Commands

- `.sb mh register <IGN>` - Register Minecraft username
- `.sb mh update <IGN>` - Update registered username
- `.sb mh unregister` - Remove registration

### Administrative Commands

- `.sb load <module>` - Load a bot module
- `.sb unload <module>` - Unload a bot module
- `.sb clear [amount]` - Clear messages

## Permissions

The bot uses a role-based permission system:

- Management roles can control modules and game sessions
- Public roles can access basic game commands
- Channel restrictions can be configured for both public and management commands

## Requirements

- Python 3.7+
- discord.py
- gspread
- oauth2client
- mojang-api-3

## License

[Add your license information here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Support

[Add support contact information or links here]
