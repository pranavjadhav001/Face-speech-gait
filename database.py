import sqlite3

class database:

    def __init__(self,database_path='major.db'):
        self.database_path = database_path

    def connection(self):
        self.conn = sqlite3.connect(self.database_path)
        self.c = self.conn.cursor()
            
    def new_profile(self,data_list):
        try:
            self.c.execute("CREATE TABLE IF NOT EXISTS profiles(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,uniq_id INT)")
            insert_data = '''INSERT INTO profiles(name,uniq_id)VALUES(?,?)'''
            self.c.execute(insert_data,[data_list[0],int(data_list[1])])
            self.conn.commit()
            print('dont forget to break connection')
        except AttributeError:
            print('pls connect first')
        except sqlite3.ProgrammingError:
            print('reconnect pls')
    
    def break_connection(self):
        self.c.close()
        self.conn.close()

    def get_profile(self):
        try:
            self.c.execute('select * from profiles')
            self.output = self.c.fetchall()
            return self.output
        except AttributeError:
            print('pls connect first')
        except sqlite3.ProgrammingError:
            print('reconnect pls')
        except sqlite3.OperationalError:
            print('No such table')
    def delete_profile(self,name):
        self.c.execute("DELETE FROM profiles WHERE name=?", (name,))
        self.conn.commit()
        print(self.get_profile())
