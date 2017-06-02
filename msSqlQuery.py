import pypyodbc as pyodbc
from witBot import getWitResponse

connection_string = 'Driver={ODBC Driver 13 for SQL Server};Server=localhost;Database=policyDatabase;UID=user1;PWD=testPassword123!;'#trusted_connection=yes;')

db = pyodbc.connect(connection_string)


cursor = db.cursor()

#Passes variables from witAi into a query string
def queryPolicyTable(queryFields, whereValues):

	selectString = 'SELECT '

	for element in queryFields:
		selectString = selectString + '[' + element + '],'
	selectString = selectString[0:len(selectString)-1]

	whereString = ' WHERE'

	for element in whereValues:
		whereString = whereString + ' ' + element[0:-5] + ' = ' + whereValues[element] + ' AND'
	whereString = whereString[0:-4]

	fromString = ' FROM [policyDatabase].[dbo].[policyTable]'
	queryString = selectString + fromString + whereString


	cursor.execute(queryString + ';')

 	#print(cursor.fetchone())
	return cursor.fetchone()


#queryFields, whereValues = getWitResponse("Show me premium and account number of policy number 2")
#print(result)
#queryPolicyTable(queryFields, whereValues)
