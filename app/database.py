from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

connection_string = quote_plus(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-8TOH6OI;"
    "DATABASE=todo_app_python;"
    "UID=sa;"
    "PWD=sa123;"
    "TrustServerCertificate=yes;"
)

DATABASE_URL= f"mssql+pyodbc:///?odbc_connect={connection_string}"
 
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()