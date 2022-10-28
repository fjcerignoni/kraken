from pathlib import Path
import sqlite3

# TODO estudar alembic para construir o banco.

current_path = Path(__file__).parent.absolute()
try:
    with open(current_path / 'kraken_schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    db = sqlite3.connect(current_path / 'kraken.sqlite')
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()
    print('Database running.')
except Exception as e:
    print(e)