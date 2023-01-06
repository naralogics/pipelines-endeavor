import os

import mysql.connector

con = mysql.connector.connect(
    user=os.environ["ENV_PLATFORM_DATABASE_USERNAME"],
    password=os.environ["ENV_PLATFORM_DATABASE_PASSWORD"],
    host=os.environ["ENV_PLATFORM_DATABASE_HOST"],
    port=os.environ["ENV_PLATFORM_DATABASE_PORT_NUMBER"],
)

cursor = con.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS dagster")

cursor.execute("use dagster")

try:
    cursor.execute("alter table asset_keys modify column last_materialization longtext")
    cursor.execute("alter table event_logs modify column event longtext")
except mysql.connector.errors.ProgrammingError:
    pass
