import hashlib, os, binascii
import dbUtils


'''
SUCESS CODE: 0
ERROR CODES:
 * 1: email taken
'''
def add_user(fullname, email, password):
    #limit password length to ~1024 for hmac
    #also maybe email verification would be nice
    if dbUtils.user_in_db(email):
        return 10

    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha512', password, \
                             salt, 25000, 64)
    hashedPass = binascii.hexlify(dk)
    dbUtils.insert_user(fullname, email, hashedPass, \
                        binascii.hexlify(salt))
    return 0


'''
SUCCESS CODE: 0
ERROR CODES:
 *  1: incorrect credentials
'''
def verify_user(email, password):
    if not dbUtils.user_in_db(email):
        return 1
    
    user = dbUtils.get_user_by_col(email, 'email')
    hashedPass_real = user['password']
    salt_b = binascii.unhexlify(user['salt'])
    dk = hashlib.pbkdf2_hmac('sha512', password, \
                             salt_b, 25000, 64)
    hashedPass = binascii.hexlify(dk)
    if hashedPass != hashedPass_real:
        return 1
    
    return 0
