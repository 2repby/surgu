import psycopg2
import os
from dotenv import load_dotenv

connection = psycopg2.connect(
    host=os.getenv('host'),
    port=os.getenv('port'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('database')
)
# cur = connection.cursor()
# cur.execute("set timezone=05")