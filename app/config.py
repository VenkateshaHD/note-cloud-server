import os
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

# AWS credentials
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_ACCESS_KEY_ID = "AKIA5EN3ZRDWMS5HB3XQ"
AWS_SECRET_ACCESS_KEY = "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"

# JWT Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_dev_secret_key")
