import pypyodbc as pyodbc



connection_string = 'Driver={ODBC Driver 13 for SQL Server};Server=localhost;Database=policyDatabase;UID=user1;PWD=TestPassword123!!;'#trusted_connection=yes;')

db = pyodbc.connect(connection_string)


cursor = db.cursor()

def queryPolicyTable(policyNumber, policyField):

	cursor.execute('SELECT ['+str(policyField)+'] FROM [policyDatabase].[dbo].[policyTable] WHERE [policyNumber] = '+str(policyNumber)+';')

 	return cursor.fetchone()[0]