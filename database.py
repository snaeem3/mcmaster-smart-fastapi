from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "mysql+mysqlclient://fastapi_user:your_password@localhost/fastapi_db"
# DATABASE_URL = "mysql+mysqldb://fastapi_user:your_password@localhost/fastapi_db"
DATABASE_URL = "mysql+pymysql://fastapi_user:your_password@localhost/fastapi_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
