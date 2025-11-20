# Napoleon's Campaign

A text-based strategy CLI game where you play as Napoleon Bonaparte, making historical decisions that shape the fate of Europe.

## Game Overview

Experience Napoleon's rise and fall through strategic decision-making, resource management, and tactical battles. Navigate key historical moments from the French Revolution to Waterloo.

## Features

- **Historical Events**: Make decisions at crucial moments in Napoleon's career
- **Resource Management**: Manage troops, gold, morale, and territories
- **Battle System**: Simple yet engaging tactical combat
- **Diplomacy**: Form alliances and manage international relations
- **Educational Content**: Learn about historical events and their consequences

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. Follow the on-screen menus to:
   - Start a new campaign
   - View game instructions
   - Load a saved game
   - Exit

## Testing

Run the test script to verify functionality:
```bash
python test.py
```

## Game Controls

- Use number keys (1-4) to select menu options
- Follow prompts for decision-making
- Type 'save' at any time to save your game
- Type 'quit' to exit to main menu

## Game Mechanics

### Resources
- **Troops**: Your military strength for battles
- **Gold**: Economy and army maintenance
- **Morale**: Army effectiveness and public support
- **Territories**: Land control and resource generation

### Gameplay Loop
1. View current status
2. Encounter historical events
3. Make strategic decisions
4. Resolve battles (if any)
5. Manage resources
6. Advance to next event

## Project Structure

```
napoleons-campaign/
├── main.py              # Entry point and game loop
├── game_logic.py        # Core game mechanics
├── ui.py               # User interface and display
├── data.py             # Game data and historical events
├── utils.py            # Helper functions
├── test.py             # Test script for verification
├── README.md           # This file
├── QUICKSTART.md       # Quick start guide
├── DEVELOPMENT.md      # Development notes
├── GAME_DESIGN.md      # Game design document
└── requirements.txt    # Python dependencies
```

## Design Principles

This project follows:
- **KISS**: Keep it simple, straightforward
- **Clean Code**: Clear, readable, maintainable
- **Separation of Concerns**: Each module has single responsibility
- **Performance**: Efficient and responsive
- **User-Friendly**: Intuitive interface
- **No Redundancies**: DRY principle applied

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Educational Value

While entertaining, this game also provides:
- Historical context for Napoleon's era
- Understanding of strategic decision-making
- Insight into 19th-century European politics
- Resource management skills

## Version History

- **v1.0**: Complete implementation with all core features
  - 25+ historical events from 1796-1815
  - Full resource management system
  - Battle and diplomacy mechanics
  - Save/load functionality
  - Educational content
- Future versions may include additional features and content

---

*Experience history through the eyes of one of its most influential figures.*