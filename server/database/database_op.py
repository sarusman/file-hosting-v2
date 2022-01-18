import sqlite3, os

class Database:
	def __init__(self):
		self.connector=sqlite3.connect(os.getcwd()+"/database/db.sqlite3", check_same_thread=False)
		self.curseur=self.connector.cursor()
		#self.curseur.execute("CREATE TABLE information (name, file_id, size)")
		#self.connector.commit()
	
	def select(self, column):
		return self.curseur.execute(f'SELECT {column} FROM information').fetchall()

	def insert(self, column, values):
		self.curseur.execute(f'INSERT into information {column} VALUES (?,?,?)', (values))
		self.connector.commit()

	def select_file(self, column, nom):
		return self.curseur.execute(f'SELECT name, file_id, size FROM information WHERE name=(?)',  (nom,)).fetchone()

	def delete(self, file_id):
		self.curseur.execute('DELETE FROM information WHERE (file_id)=(?)', (file_id,))
		self.connector.commit()
		return