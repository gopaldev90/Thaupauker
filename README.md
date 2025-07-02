# Thaupauker

**Thaupauker** is a powerful modding tool for *Plants vs. Zombies 2 (PvZ2)* that allows players to unlock the full potential of their favorite plants. With this tool, you can upgrade any plant to level 1000 and boost individual abilities — creating a truly unstoppable garden!

---

## Features

- **Ultra-Leveling**: Upgrade plants to level 1000 for maximum damage, toughness, and special effects.
- **Skill Enhancement**: Modify and enhance plant-specific abilities like toughness, damage, recharge rate, and more.
- **Batch Editing**:
  - **Sabekam**: Modify all plants in a single file.
  - **Sab Alag**: Modify each plant individually in separate folders.
- **Plant Food Customization**: Enable multiple Plant Food uses (PFPC) to amplify power-ups.
- **Search & Modify**: Use the `khoj` button to find plants quickly and `confirm` to apply changes.
- **Safe Editing**: Creates new folders with modified data, preserving your original files.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/gopaldev90/Thaupauker.git
   cd Thaupauker
   ```

2. Ensure you have Python installed (3.7+ recommended).

3. Install required libraries (if any).

---

## How to Use

### 1. Prepare Your Files
- Locate the `Plantlevels.json` file from your PvZ2 game data.
- Make a backup of the original before editing.

### 2. Run the Tool
```bash
python Thaupauker.py
```

### 3. Select an Option
- **Khoj (Search)**: Enter the plant name or ID to search.
- **PFPC Tick**: Enables infinite Plant Food usage.
- **Confirm**: Apply the modifications.
- **Sabekam**: Modify all plants in one file.
- **Sab Alag**: Modify all plants in separate folders.
- **0 Cooldown**: Modify all plants recharge and cost to 0.

### 4. Export and Use
- Modified files will be saved in a new `edited` folder.
- Replace original game files with your converted RTON files.
- Launch PvZ2 and enjoy!

---

## Example

**Input**: `Peashooter`  
**Output**: A Peashooter with 1000-level stats, enhanced damage, and faster recharge — ready to wipe out any wave of zombies!

---

## File Structure

```
Thaupauker/
├── Thaupauker.py         # Main GUI and logic
├── Aftkr.py              # Core function handlers
├── jsortokhi.py          # Utility functions
├── alrdy.json            # Already hacked plant data
└── README.md             # Project documentation
```

---

## Disclaimer

> This tool is intended for **educational and personal use only**. Modifying game files may violate PvZ2's terms of service and can potentially lead to issues with game stability or bans. Use at your own risk.

---

## License

This project is licensed under the **MIT License**. See `LICENSE` file for details.

---

## Credits

Created by [gopaldev90](https://github.com/gopaldev90)
