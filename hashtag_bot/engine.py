import os

from config.create_database import create_database
from models.database import DATABASE_NAME

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_database()
