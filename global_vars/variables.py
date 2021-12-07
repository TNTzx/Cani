"""Variables."""

import json
import os
import pyrebase

import nextcord as nx


# Bot
global_bot = nx.Client()

# Command Prefix
CMD_PREFIX = "++"


# Initialize database
env = os.environ["CaniDBToken"]
env_dict = json.loads(env)
db_key = env_dict["databaseKey"]
fb = pyrebase.initialize_app(db_key)

db = fb.database()
fb_auth = fb.auth()

env_auth = env_dict["auth"]
fb_user = fb_auth.sign_in_with_email_and_password(env_auth["email"], env_auth["password"])

def get_token():
    """Gets the firebase token."""
    fb_token = fb_user['idToken']
    return fb_token
