import sqlite3

def create_db():
    conn = sqlite3.connect("lab.db")
    
    cur = conn.cursor()

    table_create_sql = """ create table if not exists todo (
                id integer primary key autoincrement,
                what text not null,
                category text not null,
                due text not null,
                finished integer);"""

    cur.execute(table_create_sql)

    conn.close()
    

def run_program():
    create_db()
    while(True):
        input_symbol = input("Choose what to do:\n(a: Add todo, l: List todo, m: Modify todo, q: Quit)?")

        if input_symbol == "a" :
            add_todo()
        elif input_symbol == "l" :
            category_type = input("What category are you looking at ?")
            list_type = input("What items are you looking at (a: All, f: Finished only)?")
            while(list_type != "a" and list_type != "f"):
                list_type = input("What items are you looking at (a: All, f: Finished only)?")
            list_todo(filter_todo(list_type,category_type))
        elif input_symbol == "m" :
            modify_todo()
        elif input_symbol == "q" :
            break

def filter_todo(filter, category=""):
    conn = sqlite3.connect("lab.db")
    
    cur = conn.cursor()
    
    if(category == ""):
        if(filter == "f"):
            sql = "select * from todo where finished = 1"
        
        elif(filter == "a"):
            sql = "select * from todo"

        cur.execute(sql)
                    
    else:
        if(filter == "f"):
            sql = "select * from todo where finished = 1 and category = ?"

        elif(filter == "a"):
            sql = "select * from todo where category = ?"
    
        cur.execute(sql,(category,))

    rows = cur.fetchall()

    conn.close()

    return rows



def list_todo(data):

    print("ID  TODO   CATEGORY    DATE                    FINISHED?")
    print("--------------------------------------------------------")
    for row in data:
        print(row[0],row[1],row[2],row[3],row[4])

    print()


def add_todo():
    conn = sqlite3.connect("lab.db")
    
    cur = conn.cursor()
    what = input("Todo?")
    category = input("Category?")
    due = input("Due date?")
    
    sql = "insert into todo (what, category, due, finished) values (?,?,?,?)"

    cur.execute(sql,(what,category,due,0,))

    conn.commit()

    conn.close()

def modify_todo():
    conn = sqlite3.connect("lab.db")
    
    cur = conn.cursor()

    u_id = input("Record id?")
    u_wh = input("Todo?")
    u_ca = input("Category?")
    u_du = input("Due date?")
    u_fi = input("Finished (1: yes, 0: no)?")

    update = "UPDATE todo SET what = ?, category = ?, due = ?, finished = ? WHERE id = ?"

    cur.execute(update,(u_wh,u_ca,u_du,u_fi,u_id,))

    conn.commit()

    conn.close()

if __name__ == "__main__":
    run_program()