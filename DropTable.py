from aes import *

def drop_table(tab_name):
    genmd=message_digest(tab_name)
    db = pymysql.connect("localhost","pavan","pavan","project" )
    cursor = db.cursor()
    try:
        cursor.execute("select * from table_metadata where message_digest=%s",(genmd)) 
        results=cursor.fetchall()
        ename=results[0][0]
        tab_name=results[0][1]
        cursor.execute("delete from table_metadata where message_digest= %s",ename)
        cursor.execute("""drop table """+tab_name)
        print "Table found"
        db.commit()
    except:
        e = str(sys.exc_info())
        #print("Error: %s" % e)
        print "Table Not exists"
    finally:
        print "Drop completed"
        print "Enter -1 to exit"
        main()

   # disconnect from server
    db.close()


        
def main():
    tab_name=str(raw_input("Enter table name:"))#enter table name of the sql to be created
    if tab_name=="-1":
        sys.exit()
    drop_table(tab_name)   #plain table name and cipher name are passed as arguments


main()
