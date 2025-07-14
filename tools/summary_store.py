import sqlite3

def init_db():
    conn=sqlite3.connect("data/summaries.db")
    conn.execute(''' create table if not exists summaries (
                 title text,url text,summary text)''')
    conn.commit()
    conn.close()

def save_memory(title, url, summary):
    conn=sqlite3.connect("data/summaries.db")
    conn.execute(''' insert into summaries(title,url,summary) values (?,?,?)''',(title, url, summary))
    conn.commit()
    conn.close()

def query_summaries():
    conn=sqlite3.connect("data/summaries.db")
    cursor=conn.execute("select title,url,summary from summaries")
    result=cursor.fetchall()
    conn.close()
    return result
