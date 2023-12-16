import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd =YOUR_DATABASE_PASSWORD,
    auth_plugin='mysql_native_password'
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE posts")
my_cursor.execute("DROP posts")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)