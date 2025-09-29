import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database= "absen"
)

# if db.is_connected():
#     print("Database connected")