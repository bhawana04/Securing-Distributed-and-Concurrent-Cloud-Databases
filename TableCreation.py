from aes import *               #importing aes module
def table_exists(tab_name):
    mdname=message_digest(tab_name)
    db = pymysql.connect("localhost","pavan","pavan","project" )
    cursor = db.cursor()
    # Create table as per requirement0
    try:
        a=cursor.execute("select * from table_metadata where message_digest=%s",(mdname))#checking if table exists
        if a==0: 
            create_table(tab_name)
            db.commit()
        else:
            print "Table exists, please enter another name"
            main()
    except:
        e = str(sys.exc_info())
        print("Error: %s" % e)
        db.rollback()
    db.close()
        
def create_table(tab_name):
    columns=[]
    coln=1
    colstring=""
    mdname=message_digest(tab_name)
    masterkey=raw_input("Enter 16 bitkey:")
    ename=testStr(tab_name,masterkey, 16, "CBC") #encoded cipher name for table
    db = pymysql.connect("localhost","pavan","pavan","project" )
    cursor = db.cursor()
    insert_cursor=select_cursor=db.cursor()
    ncolumns=int(raw_input("Enter number of columns:"))
    for i in range(1,ncolumns+1):
        columns.append(raw_input("Enter column"+str(i)+" with datatype:"))
    # Create table as per requirement
    try:
        cursor.execute("""Insert into table_metadata(message_digest,tab_name) values(%s,%s)""",(mdname,ename))
        for cols in columns:
            colname=cols[:cols.find(" ")]   #splitting colname
            coltype=cols[cols.find(" "):]   #splitting data type
            encryptedColName,key=randomKeyEncrypt(colname, keysize=16, modeName = "CBC")
            key=normalKeyEncrypt(key,masterkey, keysize=16, modeName = "CBC")           #encrypting metadata
            cursor.execute("""SELECT count(*) FROM information_schema.columns WHERE TABLE_NAME='table_metadata'""")
            colstring+=encryptedColName+coltype+","
            tmd_cols=cursor.fetchone()[0]#Retrieving number of columns in table_metadata
            if (tmd_cols<len(columns)+2):
                cursor.execute("Alter table table_metadata add column"+str(tmd_cols-1)+" "+"VARBINARY(64)")
            cursor.execute("update table_metadata set column"+str(coln)+" = "+" ' "+ key +" ' " +"where message_digest = '"+mdname+"'")
            coln=coln+1
        colstring=colstring[:-1]
        cursor.execute("create table "+ename+"("+colstring+")")
        print "table created"
        db.commit()
    except:
        e = str(sys.exc_info())
        print("Error: %s" % e)
        db.rollback()
    finally:
        main()
   # disconnect from server
    db.close()


        
def main():
    print "Enter -1 to exit"
    tab_name=raw_input("Enter table name:")#enter table name of the sql to be created
    if tab_name=="-1":
        sys.exit
    else:
         table_exists(tab_name)   #checks if table exist,If doesn't exists creates a table
         
    
    
main()
