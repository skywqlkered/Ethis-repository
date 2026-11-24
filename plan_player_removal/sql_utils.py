import os
import sys

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")



class Database:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
        )
        
        self.mycursor = self.mydb.cursor()
    
    def get_username_of_uuid(self, uuid):
        try:
            self.mycursor.execute("SELECT * FROM plan_users WHERE uuid = %s", (uuid,))
            row = self.mycursor.fetchone()
            return row[3] if row else None #type: ignore
        except Exception as e: 
            print(e) 

    def get_usernames_from_db(self):
        self.mycursor.execute("SELECT * FROM plan_users")
        names = [x[3] for x in self.mycursor]  # type: ignore
        return names


    def get_uuids_from_db(self):
        self.mycursor.execute("SELECT * FROM plan_users")
        uuids = [x[1] for x in self.mycursor]  # type: ignore
        return uuids


    def get_userid_from_db(self, uuid: str):
        try:
            self.mycursor.execute("SELECT * FROM plan_users WHERE uuid = %s", (uuid,))
            row = self.mycursor.fetchone()
            return row[0] if row else None # type:ignore
        except Exception as e: 
            print("Userid could not be found, ",e)
            sys.exit()


    def deleteFromTable(self, tableName: str, uuid: str):
        try:
            self.mycursor.execute(f"DELETE FROM {tableName} WHERE uuid = %s", (uuid,))
        except Exception as e:
            print("SQL execution raised error: ", e)


    def deleteFromUserIdTable(self, tableName: str, uuid: str):
        user_id = self.get_userid_from_db(uuid)
        if user_id is None:
            print(f"No user_id found for uuid {uuid}, skipping {tableName}")
            return
        try:
            self.mycursor.execute(f"DELETE FROM {tableName} WHERE user_id = %s", (user_id,)) # type: ignore
        except Exception as e:
            print("SQL execution raised error: ", e)


    def deleteFromKillsTable(self, uuid: str):
        query = "DELETE FROM plan_kills WHERE killer_uuid = %s OR victim_uuid = %s"
        try:
            self.mycursor.execute(query, (uuid, uuid))
        except Exception as e:
            print("SQL execution raised error: ", e)


    def delete_user_from_db(self, uuid):
        # note: get_userid_from_db(uuid) must still work, so do this BEFORE deleting from plan_users
        self.deleteFromUserIdTable("plan_geolocations", uuid)
        self.deleteFromTable("plan_nicknames", uuid)
        self.deleteFromKillsTable(uuid)
        self.deleteFromUserIdTable("plan_world_times", uuid)
        self.deleteFromUserIdTable("plan_sessions", uuid)
        self.deleteFromUserIdTable("plan_ping", uuid)
        self.deleteFromUserIdTable("plan_user_info", uuid)
        self.deleteFromTable("plan_users", uuid)

        self.deleteFromTable("plan_extension_user_table_values", uuid)
        self.deleteFromTable("plan_extension_user_values", uuid)
        self.deleteFromTable("plan_extension_groups", uuid)

    def close(self):
        self.mydb.commit()
        self.mycursor.close()
        self.mydb.close()
