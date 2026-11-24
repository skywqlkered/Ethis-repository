import time

from sql_utils import Database
from whitelist_utils import Whitelist

if __name__ == "__main__":
    whitelist = Whitelist()
    db = Database()
    
    whitelist_uuids = whitelist.uuids
    db_uuids = db.get_uuids_from_db()
    
    res = [x for x in db_uuids if x not in whitelist_uuids]        

    if len(res) == 0:
        db.close()
        exit()

    for uuid in res:
        print(f"Removing user: {db.get_username_of_uuid(uuid)}")    
        db.delete_user_from_db(uuid)
        time.sleep(1)
        
    db.close()