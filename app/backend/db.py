from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Указание пути к базе данных
DATABASE_URL = 'sqlite:///taskmanager.db'

# Создание движка
engine = create_engine(DATABASE_URL, echo=True)

# Создание локальной сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

