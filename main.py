import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



# Load envirometal variables
load_dotenv(".env", verbose=True)

print(os.getenv("PGHOST"))
   

# creates a connection to a PostgreSQL database
def get_engine():
    db_user = os.environ['PGUSER']
    db_password = os.environ['PGPASSWORD']
    db_host = os.environ['PGHOST']
    db_port = os.environ['PGPORT']
    db_name = os.environ['PGDATABASE']


# creates a connection to a PostgreSQL database using the connection string and SQLAlchemy's
    url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(url, pool_size=50, echo=False)
    print(f'Conneted to the database')

#  checks if a database exists at the specified URL
    if not database_exists(engine.url):
        create_database(engine.url)

    return engine

 #  define your database tables
engine = get_engine()

Base = declarative_base()

#  represents a table in a database
class Account (Base):
    __tablename__ = 'account'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email_address = Column (String,unique=True)
    security_code = Column(String)
    jobs = relationship("Account_job", backref="account")



class Account_job (Base):
    __tablename__ = "account_job"
    user_id = Column(Integer, ForeignKey('account.user_id'), primary_key=True)
    job_id = Column(Integer, primary_key=True)
    hire_date = Column(Integer)

class Job_Name (Base):
    __tablename__ = "job_name"
    job_id = Column(Integer, primary_key=True)
    job_name =Column(String)
  
 

 # Create the table
Base.metadata.create_all(engine) 


#  Creates a special tool (Session) to talk to the database.

Session = sessionmaker(bind=engine)

# Uses the tool (Session) to start a conversation with the database.

session = Session()

# data = session.query(Account).all()
data = session.query(Account_job, Account).join(Account).all()



# saves all the changes you've made to the database
session.commit()

if data:
    for account_job, account in data:
        print(f"User ID: {account.user_id}, Username: {account.username}, Email: {account.email_address}")
        print(f"Job ID: {account_job.job_id}, Hire Date: {account_job.hire_date}")
       
else:
    print("No data found.")



print(engine.url)



