from dotenv import load_dotenv
import os

load_dotenv()

CISCO_CLIENT_ID = os.getenv("CLIENT_ID")
CISCO_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
