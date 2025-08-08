# --- Code Block ---
#Import packages and create SQL and PostgreSQL Connections
# Import necessary package(s)
# Import necessary package(s)
import pandas as pd
# Establish SQLAlchemy engine for SQL Server
# Establish SQLAlchemy engine for SQL Server
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
# Import necessary package(s)
# Import necessary package(s)
import plotly.express as px
# Import necessary package(s)
# Import necessary package(s)
import configparser

#get credentials
config = configparser.ConfigParser()
# Load credentials from config.ini file
# Load credentials from config.ini file
config.read('config.ini')

evolv_password = config['credentials']['evolv_password']
postgre_password = config['credentials']['postgre_password']
ds_password = config['credentials']['ds_password']

#Myevolve database connection
server = 'myevolv50724rpt.netsmartcloud.com'
database = 'evolv_cs_reports'
username = '50724_ReportUser'
password = evolv_password
driver = 'ODBC Driver 17 for SQL Server'

# Create connection strings
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
# Establish SQLAlchemy engine for SQL Server
# Establish SQLAlchemy engine for SQL Server
sql_conn = create_engine(connection_string)

#axiom database connection
# Import necessary package(s)
# Import necessary package(s)
import psycopg2

# Define connection parameters
params = {
    "dbname": "tscore",
    "user": "ontrak_vvu",
    "password": postgre_password,
    #"host": "ontrak-uat-rds-ro.cnsw1mb6oasc.us-east-1.rds.amazonaws.com", #uat
    "host": "ontrak-prod-tscore-ro.cnsw1mb6oasc.us-east-1.rds.amazonaws.com", #prod
    "port": "5432"  # Default PostgreSQL port
}
# Establish the connection
try:
# Connect to Axiom PostgreSQL database
# Connect to Axiom PostgreSQL database
    psql_conn = psycopg2.connect(**params)
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")

#Set folder path
# Set local file path for analysis artifacts
# Set local file path for analysis artifacts
path = r"\\fs01\Catasys\Data Analysis\vvu\bh_visits"

# --- Code Block ---
# Import necessary package(s)
# Import necessary package(s)
import urllib
# Establish SQLAlchemy engine for SQL Server
# Establish SQLAlchemy engine for SQL Server
from sqlalchemy import create_engine

params = urllib.parse.quote_plus(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER=dwhdevmssqlserver.database.windows.net;'
    f'DATABASE=ds_analytics;'
    f'UID=ds_analytics_user@dwhdevmssqlserver;'
    f'PWD={ds_password}'
)

# Establish SQLAlchemy engine for SQL Server
# Establish SQLAlchemy engine for SQL Server
ds_engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

