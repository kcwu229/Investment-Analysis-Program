# A connector by the MYSQL for connecting with Python
import mysql.connector
import SQLconnectSret as secret
import pandas as pd
from sqlalchemy import Column, String, create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData


# Connect to MYSQL
mysql.connector.connect()

df = pd.read_csv("stockList.csv");

conn = mysql.connector.connect(
    host = secret.host, 
    user = secret.user, 
    password = secret.password)

# A collection for iterating set of rows by query and process each row individually.
mycur = conn.cursor()

# One of the function from cursor to excute command

"""Set up database"""
database_ = "STOCKDB"
mycur.execute("""CREATE DATABASE IF NOT EXISTS """ + database_)
conn.close()



conn = mysql.connector.connect(host = secret.host, user = secret.user, password = secret.password, database = database_, port = secret.port)
engine = create_engine("mysql+mysqlconnector://" + secret.user + ":" + secret.password + "@" + secret.host + "/" + database_)

meta = MetaData()

students = Table(
   'stockTransaction', meta, 
   Column('id', Integer, primary_key = True), 
   Column('code', String(2000)), 
   Column('date', String(2000)), 
   Column('codeOpen ($)', String(2000)),
   Column('codeClose ($)', String(2000)),
   Column('codeVolume', Integer)
)

meta.create_all(engine)

df.to_sql(con=engine, name="stocktransaction", if_exists="append", index=False)
