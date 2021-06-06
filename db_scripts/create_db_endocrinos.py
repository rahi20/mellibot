"""
data scrapped from http://smedian.ma/endocrinos/

db name : diabetes_chatbot
table name : endorcrinologues

table fields :
id int aut_increment
name varchar(300)
secteur enum ('private','public')
email varchar(255)
tel varchar(15)
address varchar(1000)
city varchar(255)
"""

import mysql.connector as mysql
import json


#fetch mysql credentials 
file_cred = open("db_cred.json")
cred_dic = json.load(file_cred)

db = mysql.connect(
    host = cred_dic["host"],
    user = cred_dic["username"],
    passwd = cred_dic["password"],
    auth_plugin='mysql_native_password'
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS db_dia_chat")
cursor.execute("USE db_dia_chat")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS endorcrinologues(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name TEXT,
    sector ENUM('private','public'),
    email VARCHAR(255),
    tel VARCHAR(15), 
    address TEXT,
    city VARCHAR(255)
    )
    """
)

#SET GLOBAL local_infile=1; 
#local_infile is off by default
cursor.execute("""
    LOAD DATA LOCAL INFILE './endocrinos.csv' 
    INTO TABLE endorcrinologues 
    FIELDS TERMINATED BY ',' 
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;
""")

db.commit()