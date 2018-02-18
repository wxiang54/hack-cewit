import sqlite3, csv, time, json
from pprint import pprint
from nameparser import HumanName

if __name__ == "__main__":
    db_url = "../data/db.db"
    schema_url = "../data/db_schema.json"
else:
    db_url = "data/db.db"
    schema_url = "data/db_schema.json"
    
conn = sqlite3.connect(db_url, check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()
SCHEMA = None #dict
with open(schema_url) as schema_json:
    data = schema_json.read()
    SCHEMA = json.loads(data)

def insert_user(fullname, email, password, salt):
    q = "INSERT INTO user(fullname, displayname, email, password, salt, time_joined) \
    VALUES(?, ?, ?, ?, ?, ?);"
    name = HumanName("fullname")
    print name
    displayname = name.first
    time_joined = int(time.time()) #unix time
    #   print("\n\nTime joined: {}\n\n".format(time_joined))
    
    c.execute(q, (fullname, displayname, email, password, salt, time_joined))
    conn.commit()

def user_in_db(email):
    q = "SELECT 1 FROM user WHERE email=?;"
    return c.execute(q, (email,)).fetchone() != None

#this only gets the first instance
def get_user_by_col(value, col_name):
    q = "SELECT * FROM user WHERE {}=?;".format(col_name)
    return c.execute(q, (value,)).fetchone()

def insert_vcard(user_id, referenceID):
    assert isinstance(user_id, int)
    time_added = int(time.time()) #unix time
    q = "INSERT INTO vcard(user_id, referenceID, time_added) VALUES (?, ?, ?);"
    c.execute(q, (user_id, referenceID, time_added))
    conn.commit()




    
def table_in_db(table):
    q = "SELECT 1 FROM sqlite_master \
    WHERE type='table' AND name='{}';".format(table)
    return c.execute(q).fetchone() != None

def reset_table(table, makeBackup = True):
    if table_in_db(table):
        if makeBackup:
            table_old = "_{}_old".format(table)
            c.execute('DROP TABLE IF EXISTS {};'.format(table_old))
            c.execute('ALTER TABLE {} RENAME TO {};'.format(table, table_old))
        else:
            c.execute('DROP TABLE {};'.format(table))
    
    c.execute( SCHEMA[table] )
    conn.commit()

'''
def repopulate_jewelry(filename):
    with open(filename, 'rb') as f:
        reset_table('jewelry')
        reader = csv.DictReader(f)
        for row in reader:
            insert_jewelry(row['name'], row['photo_url'], row['price'], row['msmts'])
        conn.commit()
'''
            
if __name__ == "__main__":
#    reset_table("cart")
#    repopulate_jewelry("../data/jewelry_data.csv")
#    pprint(get_all_jewelry())
    print "ran dbutils lol"
