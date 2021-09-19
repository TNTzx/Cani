import sqlite3
import os

import json

from Functions import customExceptions as cE


cxn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "..", "Database", "database.db"))
crsr = cxn.cursor()

crsr.execute("""
    CREATE TABLE IF NOT EXISTS database (
        `guild_id` TEXT,
        `claim_channel_data` TEXT
        `claim_channel_embed` TEXT
)
""")

# Get Data
def getData(guildId, column, type=str):
    crsr.execute(f"""
    SELECT {column} FROM database
    WHERE guild_id = '{guildId}'
    """)

    fetched = crsr.fetchone()
    try:
        data = fetched[0]
    except TypeError:
        return None

    if type == dict:
        return json.loads(data)
    else:
        return type(data)

# Check if data already exists
def isDataExists(guildId):
    return getData(guildId, 1) == None


# Create
def createData(guildId):
    if not isDataExists(guildId):
        raise cE.SqlNoEntry(f"Data already found for '{guildId}'.")

    crsr.execute(f"""
            INSERT INTO database
            VALUES ('{guildId}', 'nodata', 'nodata')
    """)
    cxn.commit()

# Edit
def editData(guildId, **kwargs):
    if isDataExists(guildId):
        raise cE.SqlNoEntry(f"Data already found for '{guildId}'.")

    for key, value in kwargs.items():
        if isinstance(value, dict):
            value = json.dumps(value)
        crsr.execute(f"""
            UPDATE database SET {key} = '{value}'
            WHERE guild_id = '{guildId}'
        """)
    cxn.commit()


# Delete
def deleteData(guildId):
    if not isDataExists(guildId):
        raise cE.SqlNoEntry(f"Data being deleted doesn't exist for '{guildId}'.")
    
    crsr.execute(f"""
        DELETE FROM database
        WHERE guildId = '{guildId}'
    """)
    cxn.commit()
    


# createData("beans")
# insertData("beans", claim_channel_data="true")
# print(getData("beans", "claim_channel_data"))


# cxn.commit()
# cxn.close()