# envcheck

Checks your .env file has every variable listed in .env.example
before you run something that needs them.

## Usage

    python3 envcheck.py [directory]

Defaults to the current directory if no path is given.

Reports any variables that are missing entirely, or present but
left blank. Exits with status 1 if anything's wrong, 0 if clean —
so it can be dropped into a script or CI step to actually block
execution instead of just printing a warning.

## Example

    $ python3 envcheck.py
    missing (1):
      DB_URL

## Requirements

Python 3.

## License

MIT