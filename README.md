# GGBOT v2 - Mobile2 Global Bot

A comprehensive Python bot for Mobile2 Global with all the features you requested.

## Features

### Potion Management
- **Red Potion**: Automatically uses red potions based on HP percentage
- **Blue Potion**: Automatically uses blue potions based on MP percentage
- **Stop when no red potions**: Option to stop bot when red potions run out

### Movement & Hacks
- **Wallhack**: Pass through objects, items, and mobs
- **Restart Here**: Restart at current position when you die
- **Movement Speed**: Adjust movement speed multiplier
- **Wait Hack**: Attack without animation at close range
- **Wait Hack Range**: Attack without animation at long range

### Targeting & Farming
- **Farm Range**: Set farming area radius
- **Fixed Position**: Set specific farming area
- **Mob Selection**: Choose which mobs to attack
- **Stone Selection**: Choose which stones to mine
- **Attack Groups**: Attack multiple groups simultaneously
- **Base Skills**: Auto-use non-damaging base items like Air Rage

### Item Management
- **Search Items**: Search for specific items
- **Pickup Filter**: Only pickup listed items
- **Drop No Bonus**: Drop items without bonuses, keep enchanted items
- **File Management**: Save/load item lists

### Player Detection & Whitelist
- **ESP Players**: Show players on screen
- **ESP Stones**: Show stones on screen
- **Player Whitelist**: Add players to whitelist
- **Player Range**: Set detection range
- **Player Actions**: Actions when players enter range
- **GM Actions**: Actions when GMs enter range

### Spambot
- **Auto Message**: Send messages automatically
- **Custom Text**: Set custom message text
- **Timing**: Set message interval in seconds

### Fishing Bot
- **Kill Fish**: Automatically kill fish
- **Grill Fish**: Automatically grill fish
- **Drop Dead Fish**: Drop dead fish
- **Drop Hair Color**: Drop hair color items
- **Dead Alarm**: Sound alarm when you die
- **Delay Settings**: Adjust timing

### Route Recording
- **Record Route**: Record movement patterns
- **Auto Route**: Follow recorded routes
- **Route Management**: Save/load/delete routes
- **Farm Range**: Set farming area for routes

## Installation

1. **Install Python 3.8+**
   ```bash
   # Download from https://python.org
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Bot**
   ```bash
   python mobile2_bot.py
   ```

## Usage

1. **Start the Bot**: Run `mobile2_bot.py`
2. **Configure Settings**: Use the GUI to configure all features
3. **Connect to Game**: Make sure Mobile2 Global is running
4. **Start Bot**: Click "Start Bot" button
5. **Monitor**: Watch the bot work and adjust settings as needed

## Configuration

The bot saves all settings automatically. You can also:
- **Save Settings**: Export current configuration
- **Load Settings**: Import saved configuration
- **Reset Settings**: Restart with default settings

## Safety Features

- **Player Detection**: Stop bot when players enter range
- **GM Detection**: Stop bot when GMs enter range
- **Alarm System**: Sound alerts for important events
- **Configurable Actions**: Set different actions for different situations

## File Structure

```
mobile2_bot/
├── mobile2_bot.py          # Main bot application
├── game_interaction.py     # Game interaction module
├── requirements.txt        # Python dependencies
├── config_template.json    # Configuration template
├── README.md              # This file
├── bot_config.json        # Saved configuration (auto-created)
├── item_files/            # Saved item lists
└── route_files/           # Saved routes
```

## Important Notes

⚠️ **Use at your own risk!** This bot is for educational purposes only.

- Always follow game terms of service
- Use responsibly and don't abuse the game
- Some features may require game-specific memory addresses
- Test in safe areas first
- Keep backups of your configurations

## Troubleshooting

### Bot won't connect to game
- Make sure Mobile2 Global is running
- Run as administrator if needed
- Check if game window title matches

### Features not working
- Some features require specific game versions
- Memory addresses may need updating
- Check game compatibility

### Performance issues
- Reduce bot loop frequency
- Disable unnecessary features
- Close other applications

## Support

This bot is provided as-is. For issues or questions:
1. Check the configuration
2. Verify game compatibility
3. Review the logs for errors

## Disclaimer

This software is for educational purposes only. The authors are not responsible for any consequences of using this software. Use at your own risk and in accordance with the game's terms of service.