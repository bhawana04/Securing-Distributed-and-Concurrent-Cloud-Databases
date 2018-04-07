#!/usr/bin/python
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
            print ("table doesn't exists")
            main()
        else:
            select_table(tab_name)
    except:
        e = str(sys.exc_info())
        print("Error: %s" % e)
        db.rollback()
    db.close()
        
def select_table(tab_name):
    key_list=[]
    modeName="CBC"
    mode = AESModeOfOperation.modeOfOperation[modeName]
    genmd=message_digest(tab_name)
    db = pymysql.connect("localhost","pavan","pavan","project" )
    cursor = db.cursor()
    try:
        cursor.execute("select * from table_metadata where message_digest=%s",(genmd)) 
        results=cursor.fetchall()
        ename=results[0][1]
        cursor.execute("SELECT count(*) FROM information_schema.columns WHERE TABLE_NAME=%s",(ename))
        ncol=cursor.fetchall()[0][0]
        masterkey=raw_input("Enter key:")
        for i in range(1,ncol+1):
            cursor.execute("select column"+str(i)+" from table_metadata where message_digest= '"+genmd+"'")
            key=cursor.fetchall()[0][0]
            key=key.lstrip().rstrip()
            key=normalKeyDecrypt(key,masterkey,keysize=16,modeName="CBC")#key is the cleartext that is to be decrypted
            key_list.append(key)
        cursor.execute("SELECT * FROM "+ename)
        results=cursor.fetchall()
        for i in range(len(results)):
            for j in range(len(key_list)):
                res=decryptData(key_list[j], results[i][j], mode)
                print (res)
            print("------------------")
        print ("table selected")
        db.commit()
    except:
        e = str(sys.exc_info())
        print("Error: %s" % e)
        db.rollback()

   # disconnect from server
    db.close()


        
def main():
    tab_name=str(raw_input("Enter table name:"))#enter table name of the sql to be created
    table_exists(tab_name)   #checks if table exist,If doesn't exists creates a table
    
    
main()
