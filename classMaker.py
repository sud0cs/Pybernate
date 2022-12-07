#Imports

import mysql.connector as sql
import sys


class SQLClassMaker():

	def __init__(self,host,user,passwd,port):

		self.cursor = None
		
		if host == '':
			host = 'localhost'
		if user == '':
			user = 'root'
		if port == '':
			port = 3306

		try:

			#Connects to SQL

			self.connection = sql.connect(
				host=host,
				user=user,
				passwd=passwd,
				port=port
				)

			#Create SQL cursor

			self.cursor = self.connection.cursor()

		except sql.Error as error:
			print(f"Error: {error}")

	
	#This method returns a string array with all the db names

	def getDbs(self):
		
		#Get dbs
		try:
			self.cursor.execute("SHOW DATABASES")
			result=self.cursor.fetchall()
			dbnames = []
			
			#Append all the names to the array and returns it

			for db in result:
				dbnames.append(db[0])
		
			return dbnames
		except:
			return None


	#Connect to the db and return the tables in the db

	def getTables(self, dbname): 

		self.cursor.execute(f"USE {dbname}")
		self.cursor.execute("SHOW TABLES")
		result=self.cursor.fetchall()
		
		return result

	#Write the code

	def exportClass(self,tables,package):

		
		
		for table in tables:

			self.cursor.execute(f"describe {table[0]}")

			table_info = self.cursor.fetchall()
			getters = '\n\n//GETTERS\n\n'
			setters = '\n\n//SETTERS\n\n'
			declaration = ''
			constructor_declaration = ''
			constructor = ''
			toString = '\n\n//ToString\n\n@Override\npublic String toString(){\nreturn '

			#Java class start

			table_class = f'package {package};\nimport javax.persistence.*;\n@Entity\n@Table(name="{table[0]}")\npublic class {table[0].capitalize()}'+'{\n' + f'public {table[0].capitalize()}()'+ '{}\n' + f'public {table[0].capitalize()}('
			

			#Still needs more variable types

			for col in table_info:
				if 'int' in col[1]:
					vartype = 'int'
				elif 'varchar'in col[1]:
					vartype = 'String'
				elif 'float' in col[1]:
					vartype = 'float'
				elif 'double' in col[1]:
					vartype = 'double'
				elif 'boolean' in col[1]:
					vartype = 'boolean'
				if 'PRI' in col[3]:
					declaration += '@Id\n'

				
				#Writing java class

				constructor_declaration += f'{vartype} {col[0]},'
				constructor += f'this.{col[0]} = {col[0]};\n'
				declaration += f'@Column(name="{col[0]}")\nprivate {vartype} {col[0]};\n'
				getters += f'\npublic {vartype} get{col[0].capitalize()}()' +  '{\n' + f'return this.{col[0]};\n' + '}\n'
				setters += f'\npublic void set{col[0].capitalize()}({vartype} {col[0]})' +  '{\n' + f'this.{col[0]} = {col[0]};\n' + '}\n'
				toString += f'"[{col[0]}, " + {col[0]} + "]"+'

			toString = toString.strip()
			toString = toString[:len(toString)-1]
			toString = toString.strip()
			toString += ';\n}'
			table_class += constructor_declaration[:len(constructor_declaration)-1] + '){\n' + constructor + '}\n' + declaration + getters + setters + toString + '\n}'
			#Creates file and writes the code
			with open(f'{table[0].capitalize()}.java','w+') as classfile:
				classfile.write(table_class)

	#Close connection

	def closeCon(self):
		self.connection.close()
	def exit(self):
		sys.exit(0)