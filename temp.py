'''
try:
    sqliteConnection = sqlite3.connect(r'C:\Users\darwi\test 6\Assets\gestures.db')
    cursor = sqliteConnection.cursor()
    count = cursor.execute("DELETE FROM chatGPT")
    sqliteConnection.commit()
    print("Records deleted")
    cursor.close()

except sqlite3.Error as error:
    print("Failed to delete data from sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite database is prepared")
'''
'''
try:
    sqliteConnection = sqlite3.connect(r'C:\Users\darwi\test 6\Assets\gestures.db')
    cursor = sqliteConnection.cursor()
    # print("Successfully Connected to SQLite")

    count = cursor.execute("insert into chatGPT (question) values (?)", [response])
    sqliteConnection.commit()
    # print("Record inserted successfully into Sqlite Gestures table ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        # print("The SQLite connection is closed")
'''