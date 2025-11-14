from pymongo import MongoClient
from config.config import dbSettings

database = MongoClient(
f"mongodb://{dbSettings.DB_USER_NAME}:{dbSettings.DB_PASSWORD}@{dbSettings.DB_HOST}:27017/{dbSettings.DB_NAME}?authSource=admin"
)

