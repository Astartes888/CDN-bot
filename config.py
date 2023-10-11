from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных
    redis_url: str


@dataclass
class TgBot:
    token: str      
    admin_id: str 


@dataclass
class WebhookConfig:
    webhook_path: str      
    webhook_url: str


@dataclass
class ApiConfig:
    api_token: str
    api_org_id: str    


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    #webhook: WebhookConfig
    api: ApiConfig

def load_config(path: str = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('TOKEN'),
                                admin_id=env.int('ADMIN_ID')), 
                  db=DatabaseConfig(database=env('DATABASE'),
                                db_host=env('DB_HOST'),
                                db_user=env('DB_USER'),
                                db_password=env('DB_PASSWORD'),
                                redis_url=env('REDIS_URL')),
                  #webhook=WebhookConfig(webhook_path=env('WEBHOOK_PATH'),
                                #webhook_url=env('WEBHOOK_URL')),
                    api=ApiConfig(api_token=env('API_TOKEN'), 
                                  api_org_id=env('API_ORG_ID'))
                    )
