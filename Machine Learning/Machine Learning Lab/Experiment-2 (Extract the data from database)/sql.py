import pymysql
def mysqlconnect():
    # To connect MySQL database 
    conn = pymysql.connect( host='localhost', user='root', password = "mysql", db='csd_students_info')
    cur = conn.cursor()
    cur.execute("select @@version")
    output = cur.fetchall()
    print(output)

mysqlconnect()