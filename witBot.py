from wit import Wit
#from msSqlTestLocal import queryPolicyTable
import os

witAccessToken = os.environ.get('witAccessToken')

client = Wit(witAccessToken)

def getWitResponse(message_text):
	response = client.message(message_text)
	
	#Returns a dictionary of entities and their values, as well as confidence level
	try:
		entityValueList = {}
		
		entityList = list(response['entities'])

		# Need to add a confidence average
		entity = list(response['entities'])[0]
		#print(response['entities'][entity][0]['confidence'])
		confidence = response['entities'][entity][0]['confidence']

		for element in entityList:
			#print(element)
			#print(response['entities'][element][0]['value'])
			entityValueList[str(element)] = response['entities'][element][0]['value']
			#values = valueList.append(response['entities'][element][0]['value'])

		return (entityValueList, confidence)

	except:
		return (None, None)
		
# result = getWitResponse("Show me policy number 2 premium")
