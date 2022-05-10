import psycopg2


try:
    #establishing the connection
    conn = psycopg2.connect(
            database = 'main',user='root', password='Mam@69853301135803421#', host='localhost', port= '5432'
        )
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Preparing query to create a database
    name_Database = 'booking'
    sql = f"CREATE DATABASE {name_Database};"

    #Creating a database
    cursor.execute(sql)
    print("Database created successfully........")

    #Closing the connection
    conn.close()
except:
    # conn.rollback()
    print("Database created is failed...")
    raise