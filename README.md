# rotation

This project generates a youth soccer substitution/position rotation plan.

The main script is `rotation.py`. It reads a game roster from a JSON file,
applies position preferences from `database/players.json`, rotates players
across periods, and prints the resulting lineup table for each half.

## What `rotation.py` does

1. Loads player position preferences from `database/players.json`.
2. Reads game-day roster data from an input JSON file (`--players_file`):
	- defense players
	- offense players
	- goalkeeper rotation list
	- optional halftime swaps
3. Builds a `Team` with:
	- one goalkeeper on field
	- defense unit (LB, CB, RB)
	- offense unit (LW, ST, RW)
4. Rotates players each period using predefined rotation maps.
5. Applies halftime swaps at period 5.
6. Prints a table showing each player's position by period.

## Input file format

Example (like `input_data/may16_1.json`):

```json
{
  "defense": ["Piero", "Asher", "Ottavio", "Teddy", "Charles"],
  "offense": ["Daniel", "Cal", "Isaac", "Brogan", "Chris"],
  "keepers": ["Anderson", "Isaac", "Ottavio", "Charles"],
  "swaps": [["Ottavio", "Brogan"], ["Charles", "Anderson"]]
}
```

## How to run

From the project root:

```bash
python3 rotation.py --players_file input_data/may16_1.json
```

Optional argument:

```bash
python3 rotation.py --players_file input_data/may16_1.json --num_periods 8
```

## Run tests

```bash
python3 -m unittest discover -s test -p 'test_*.py'
```
