import sqlite3
import os
import ast


cxn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "..", "Database", "database.db"))
crsr = cxn.cursor()

crsr.execute("""
    CREATE TABLE IF NOT EXISTS database (
        `guild_id` TEXT,
        `claim_channel_data` TEXT
)
""")

def createData(guildId):
    crsr.execute(f"""
        INSERT IGNORE INTO database
        VALUES (`{guildId}`, `None`)
    """)
    cxn.commit()


def insertData(guildId, **kwargs):
    for key, value in kwargs.items():
        crsr.execute(f"""
            UPDATE database SET {key} = `{value}`
            WHERE guild_id = `{guildId}`
        """)
    cxn.commit()

def getData(guildId, column, type=str):
    crsr.execute(f"""
    SELECT {column} FROM database
    WHERE guild_id = `{guildId}`
    """)
    data = crsr.fetchone()[0]

    if type == dict:
        return ast.literal_eval(data)
    else:
        return type(data)

# createData("beans")
# insertData("beans", claim_channel_data="true")


# cxn.commit()
# cxn.close()