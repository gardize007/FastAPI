from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./marketplace.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True )
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#begin Nataliia
metadata = MetaData()
metadata.reflect(bind=engine) 
#end Nataliia

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
