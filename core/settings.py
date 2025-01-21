import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    secret_key: str = os.environ.get(
        'SECRET_KEY',
        'kjnl3r4nc9opokpd2123i1sada2971owdhp23j093nws10ip5t1dvfv')
    access_token_expires_in_minutes: int = os.environ.get(
        'ACCESS_TOKEN_EXPIRES_IN_MINUTES', 60)

    db_user: str = os.environ.get('DB_USER', 'admin')
    db_password: str = os.environ.get('DB_PASS', '12345678')
    db_name: str = os.environ.get('DB_NAME', 'library_api')
    db_host: str = os.environ.get('DB_HOST', 'localhost')
    db_port: str = os.environ.get('DB_PORT', 5432)


settings = Settings()
