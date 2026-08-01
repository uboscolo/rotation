# rotation

Generates a youth soccer rotation plan by period, including:

- field position assignment per player
- goalkeeper rotation
- halftime player swaps

The script prints one table per half showing each player's position for each period.

## How it works

`rotation.py` does the following:

1. Loads player position preferences from a player database JSON file.
2. Loads game-day roster data from `--players_file`.
3. Builds a team with defense, offense, and goalkeeper groups.
4. Rotates active players each period using predefined rotation maps.
5. Applies halftime swaps at period 5.
6. Prints the final rotation table.

## Supported formats

### Players file (`--players_file`)

Expected keys:

- `defense`: list of defender names
- `offense`: list of attacker names
- `keepers`: list of goalkeeper names (first name starts in goal)
- `swaps`: optional halftime swaps as `[player_a, player_b]`

Example:

```json
{
	"defense": ["Jules", "Raphael", "Dayot", "Theo", "Aurelien"],
	"offense": ["Adrien", "Ousmane", "Antoine", "Kylian", "Olivier"],
	"keepers": ["Hugo", "Jules", "Theo", "Adrien"],
	"swaps": [["Theo", "Kylian"]]
}
```

### Player database (`--players_db`)

Each player must include unit-specific preferences:

- `defense.favorite` and `defense.alternate`
- `offense.favorite` and `offense.alternate`

Example files in this repo:

- `database/B4_lions.json`
- `database/B5_dynamo.json`

## Supported starter modes

- `--num_starters 7`
	- defense: 3 field starters
	- offense: 3 field starters
	- plus 1 goalkeeper
- `--num_starters 9`
	- defense: 3 field starters
	- offense: 5 field starters
	- plus 1 goalkeeper

## Usage

From the repository root:

```bash
python3 rotation.py --players_file input_data/may16_1.json --players_db database/B4_lions.json --num_starters 7
```

9-starter example:

```bash
python3 rotation.py --players_file input_data/sep12_1.json --players_db database/B5_dynamo.json --num_starters 9
```

Optional flag:

```bash
python3 rotation.py --players_file input_data/may16_1.json --players_db database/B4_lions.json --num_starters 7 --num_periods 8
```

## Tests

```bash
python3 -m unittest discover -s test -q
```
