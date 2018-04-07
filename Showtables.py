#!/usr/bin/python
from aes import *        
def show_table(key):
    key_list=[]
    modeName="CBC"
    mode = AESModeOfOperation.modeOfOperation[modeName]
    encryCol=''
    db = pymysql.connect("localhost","pavan","pavan","project" )
    cursor = db.cursor()
    try:
        cursor.execute("select * from table_metadata") 
        results=cursor.fetchall()
        count =cursor.rowcount
        if count==0:
            print "Sorry,No tables exist"
        else:
            print "tables in data base are:"
            for i in range(count):
                data=base64.b32decode(results[i][1])
                data=data[:32]
                print decryptData(key, data, mode=AESModeOfOperation.modeOfOperation["CBC"])
        db.commit()
    except:
        e = str(sys.exc_info())
        print "Sorry,No tables exist"
        print("Error: %s" % e)
        db.rollback()

   # disconnect from server
    db.close()


        
def main():
    key=str(raw_input("Enter key:"))#enter table name of the sql to be created
    show_table(key)  #checks if table exist,If doesn't exists creates a table
    
    
main()
