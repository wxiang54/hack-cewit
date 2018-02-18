import sqlite3, csv, time, json, random
from pprint import pprint
from nameparser import HumanName
import apiUtils
'''
if __name__ == "__main__":
    db_url = "../data/db.db"
    schema_url = "../data/db_schema.json"
    cc_url = "../data/fake_credit_cards.json"
else:
'''
db_url = "data/db.db"
schema_url = "data/db_schema.json"
cc_url = "data/fake_credit_cards.json"
    
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
    
def tie_token_to_user(token, email):
    assert user_in_db(email)
    q = "UPDATE user SET cc_token=? WHERE email=?;"
    c.execute(q, (token, email))
    conn.commit()

#this only gets the first instance
def get_user(email):
    q = "SELECT * FROM user WHERE email=?;"
    return c.execute(q, (email,)).fetchone()

def user_in_db(email):
    return get_user(email) != None

def get_vcard(referenceID):
    q = "SELECT * FROM vcard WHERE referenceID=?;"
    return c.execute(q, (email,)).fetchone()

def vcard_in_db(referenceID):
    return get_vcard(referenceID) != None

def insert_vcard(referenceID):
    time_added = int(time.time()) #unix time
    q = "INSERT INTO vcard(referenceID, time_added) VALUES (?, ?);"
    c.execute(q, (referenceID, time_added))
    conn.commit()

def register_new_vcard(email, limit, name):
    #find an empty one
    q = "UPDATE vcard SET user_email=?, money_limit=?, money_used=0, name=? WHERE id IN \
    (SELECT id FROM vcard WHERE user_email IS NULL LIMIT 1);"
    c.execute(q, (email, limit, name))
    
def get_vcard(referenceID):
    q = "SELECT * FROM vcard WHERE referenceID=?"
    return c.execute(q, (referenceID,)).fetchone()

def get_vcards_by_email(email):
    q = "SELECT referenceID FROM vcard WHERE user_email=?"
    all_refID = c.execute(q, (email,)).fetchall()
    #now to actual credit card info
    ret = []
    access_token = apiUtils.request_token()
    for refID in all_refID:
        ret.append(get_vcards_by_email_H(refID, access_token))
    return ret


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

def repopulate_vcards():
    with open(cc_url, 'rb') as f:
        FAKE_CC = json.loads(f.read())
        reset_table('vcard')
        access_token = apiUtils.request_token()
        for card in FAKE_CC:
            refID = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
            while vcard_in_db(refID): #make sure refID is unique
                refID = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
            ccrm = {
                "cardNumber": card["CreditCard"]["CardNumber"],
                "securityCode": "123",
                "expirationMonth": 11,
                "expirationYear": 2020,
                "cardHolderName": "John Doe",
                "billingAddress": {
                    "address1": "1500 Stony Brook Road",
                    "city": "Stony Brook",
                    "state": "NY",
                    "zipCode": "11790"
                },
                "email": "jdoe@example.com",
                "referenceId": refID,
            }
            apiUtils.tokenize(ccrm, access_token)
            insert_vcard(refID)

def init():
    reset_table("user")
    repopulate_vcards()    
        
if __name__ == "__main__":
    init()
