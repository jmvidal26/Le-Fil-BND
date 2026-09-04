import sqlite3
import os
import bcrypt
import sys
import asyncio












#===============================================#
#++++++++++CREATE_AND_SEARCH_THE_TABLE++++++++++#
#===============================================#

def create_table(DB_NAME):
    if os.path.exists(DB_NAME):
        pass
    else:
        try:
            conn = sqlite3.connect(DB_NAME)

            cursor=conn.cursor()

            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS users(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT UNIQUE NOT NULL, 
                           password_hash TEXT NOT NULL)""")

            conn.commit()

        except sqlite3.Error as e:
            print({e})
            sys.exit(1)
        
        finally:
            conn.close()
            










#===============================================#
#++++++++++--------REGISTER_USER------++++++++++#
#===============================================#

def register_user(DB_NAME,username,password):

#register new user an encrypt his password

    if not username or not password:

        print("empty")
        return
    
#generate salt and hash password
    salt=bcrypt.gensalt()
    password_hash=bcrypt.hashpw(password.encode("utf-8"),salt)

    try:
        conn = sqlite3.connect(DB_NAME)

        cursor=conn.cursor()

        cursor.execute("INSERT INTO users(username, password_hash) VALUES(?,?)",
                          (username,password_hash.decode("utf-8")))

        conn.commit()

        print(f"User: {username} registered succesfully")    #Debugging#

    except sqlite3.IntegrityError:

        print(f"That user: '{username}' already exists")

    except sqlite3.Error as e:

        print("There is a problem with the database: {e}")

    finally:
        conn.close()

            










#===============================================#
#++++++++++--------VERIFY_USER--------++++++++++#
#===============================================#

def verify_user(DB_NAME,username,password):

#Verify the user and password

    try:
        conn= sqlite3.connect(DB_NAME)

        cursor=conn.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE username =?", (username,))

        row=cursor.fetchone()

    except sqlite3.Error:
        
        print("There is a problem with the database: {e}")
        return False
    
    finally:

        conn.close()

    

    if row is None:

        print("User not found")
        return False
    
    stored_hash=row[0].encode("utf-8")

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        print("Login successful")
        return True
    
    else:
        print("Invalid password.")
        return False    

            













#===============================================#
#++++++++++---RUNNING AND DEBUGGING---++++++++++#
#===============================================#

if __name__=="__main__":

    route = "Access"
    DB_NAME=os.path.join(route, f"memory.db")

    try:
        create_table(DB_NAME)
        
        ask=input("Do you have a count,\n\n if you dont have a count press 1  ")

        if ask=="1":

            user=input("\n Input his user ")
            pwd=input("\n Input his password ")

            register_user(DB_NAME,user,pwd)

        user=input("\n Input his user ")
        pwd=input("\n Input his password ")

        if not verify_user(DB_NAME,user,pwd):
 
            if ask=="1":

                user=input("\n Input his user ")
                pwd=input("\n Input his password ")

                register_user(DB_NAME,user,pwd)

            user=input("\n Input his user ")
            pwd=input("\n Input his password ")

        
    except OSError as e:
        print({e})