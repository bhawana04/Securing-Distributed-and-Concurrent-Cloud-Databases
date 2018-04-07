#!/usr/bin/python
import sys
from aes import *
def table_exists(tab_name):
    mdname=message_digest(tab_name)
    db = pymysql.connect("localhost","pavan","pavan","project" )
    cursor = db.cursor()
    insert_cursor=select_cursor=db.cursor()
    # Create table as per requirement0
    try:
        a=cursor.execute("select * from table_metadata where message_digest=%s",(mdname))#checking if table exists
        if a==0: 
            print "table doesn't exists"
            main()
        else:
            insert_table(tab_name)
            
    except:
        #e = str(sys.exc_info())
        print("Error")
        db.rollback()
    db.close()
        
def insert_table(tab_name):
    modeName="CBC"
    mode = AESModeOfOperation.modeOfOperation[modeName]
    colstring=" "
    genmd=message_digest(tab_name)
    db = pymysql.connect("localhost","pavan","pavan","project" )
    cursor = db.cursor()
    try:
        cursor.execute("select * from table_metadata where message_digest=%s",(genmd)) 
        results=cursor.fetchall()
        ename=results[0][1]
        cursor.execute("SELECT count(*) FROM information_schema.columns WHERE TABLE_NAME=%s",(ename))
        results=cursor.fetchall()[0][0]
        masterkey=raw_input("Enter key:")
        for i in range(1,results+1):
            cursor.execute("select column"+str(i)+" from table_metadata where message_digest= '"+genmd+"'")
            keyone=cursor.fetchall()[0][0]
            keyone=keyone.lstrip().rstrip()
            key=normalKeyDecrypt(keyone,masterkey,keysize=16,modeName="CBC")  #retrieves encrypted col key after decrypting with masterkey
            cursor.execute("select column_name from information_schema.columns where table_name=%s",(ename))
            cipher=cursor.fetchall()[i-1][0]
            decr_column = randomColDecrypt(key, cipher, mode)
            colData=raw_input("Enter "+decr_column+":")
            encColData=randomColEncrypt(colData, key,  mode)
            colstring+="'"+encColData+"'"+","
        colstring=colstring[:-1]
        cursor.execute("Insert into "+ename+" values("+colstring+");")
        print "Data inserted in the table"
        db.commit()
        
    except:
        e = str(sys.exc_info())
        print("Error:Something might have gone wrong")
        db.rollback()
    finally:
        main()

   # disconnect from server
    db.close()


        
def main():
    print "Enter -1 to Exit"
    tab_name=str(raw_input("Enter table name:"))#enter table name of the sql to be created
    if tab_name=="-1":
        sys.exit
    else:
        table_exists(tab_name)   #checks if table exist,If doesn't exists creates a table
    
main()
