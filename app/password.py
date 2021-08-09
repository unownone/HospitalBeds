import bcrypt
import re
def get_pass(raw_password,salt=None):
    raw_password=bytes(raw_password,'utf8')
    master_secret_key = bytes('1FUH@CKEDU5_G00DJ08','utf8')
    if salt is None:salt = bcrypt.gensalt()
    else: salt=bytes(salt,'utf8')
    combo_password = raw_password + salt + master_secret_key
    hashed_password = bcrypt.hashpw(combo_password, salt)
    return str(hashed_password)[2:62],str(salt)[2:31]

def check_pass(raw_password):
    return re.search('[a-zA-Z0-9\@\!]{6,}',raw_password)
