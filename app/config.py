import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Database URI: Use DATABASE_URL (Railway PostgreSQL), fallback to SQLite
DATABASE_URL = os.getenv('DATABASE_URL')

# Debug logging
print(f"DEBUG: DATABASE_URL = {DATABASE_URL[:50] if DATABASE_URL else 'NOT SET'}", file=sys.stderr)
print(f"DEBUG: All env vars: {list(os.environ.keys())[:10]}", file=sys.stderr)

# Always use DATABASE_URL if available, it means we're on Railway
if DATABASE_URL:
    # Railway PostgreSQL
    db_uri = DATABASE_URL
    # Fix postgres:// to postgresql:// for SQLAlchemy compatibility
    if db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://', 1)
else:
    # Local development: SQLite
    try:
        instance_path = os.path.abspath(r'C:\Users\yeini\.villa_lisanna_tmp')
        os.makedirs(instance_path, exist_ok=True)
        db_file_path = os.path.join(instance_path, 'villalisanna.db')
        if not os.path.exists(db_file_path):
            open(db_file_path, 'a').close()
        db_uri = f'sqlite:///{db_file_path.replace(chr(92), "/")}'
    except:
        # Fallback if path creation fails
        db_uri = 'sqlite:///./villalisanna.db'

class Config:
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL', 'reservas@villalisanna.com')
    SMTP_FROM_NAME = os.getenv('SMTP_FROM_NAME', 'Villa Lisanna')

    VILLA_OWNER_EMAIL = os.getenv('VILLA_OWNER_EMAIL', 'liset@villalisanna.com')
    VILLA_OWNER_NAME = os.getenv('VILLA_OWNER_NAME', 'Liset')
    NIGHTLY_RATE = float(os.getenv('NIGHTLY_RATE', 5))
    CLEANING_FEE = float(os.getenv('CLEANING_FEE', 0))
    DAMAGE_DEPOSIT = float(os.getenv('DAMAGE_DEPOSIT', 0))
    SALES_TAX_RATE = float(os.getenv('SALES_TAX_RATE', 0.12))
    MIN_NIGHTS = int(os.getenv('MIN_NIGHTS', 3))
    MAX_NIGHTS = int(os.getenv('MAX_NIGHTS', 28))
    MAX_GUESTS = int(os.getenv('MAX_GUESTS', 10))
    MIN_AGE = int(os.getenv('MIN_AGE', 25))
    DEPOSIT_PERCENTAGE = float(os.getenv('DEPOSIT_PERCENTAGE', 0.5))
    DEPOSIT_HOLD_HOURS = int(os.getenv('DEPOSIT_HOLD_HOURS', 48))
    BALANCE_DUE_DAYS_BEFORE = int(os.getenv('BALANCE_DUE_DAYS_BEFORE', 30))

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
