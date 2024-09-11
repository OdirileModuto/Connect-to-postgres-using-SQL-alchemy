import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load envirometal variables
load_dotenv(".env", verbose=True)

print(os.getenv("PGHOST"))

def get_engine():
    db_user = os.environ['PGUSER']
    db_password = os.environ['PGPASSWORD']
    db_host = os.environ['PGHOST']
    db_port = os.environ['PGPORT']
    db_name = os.environ['PGDATABASE']

    url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(url, pool_size=50, echo=False)
    print(f'Conneted to the database')

    if not database_exists(engine.url):
        create_database(engine.url)

    return engine


engine = get_engine()

Base = declarative_base()

class Film (Base):
    __tablename__ = 'film'
    film_id = Column(Integer, primary_key=True)
    title = Column(String)



 # Create the table
Base.metadata.create_all(engine) 



Session = sessionmaker(bind=engine)
session = Session()

data = session.query(Film).filter_by(title="Wrong Behavior").all()



session.commit()

if data:
    for row in data:
        print(row.film_id, row.title)
else:
    print("No films found with title '8'.")







print(engine.url)

