from wit import Wit
import os

witAccessToken = os.environ.get('witAccessToken')

client = Wit(witAccessToken)

def getWitResponse(message_text):
	response = client.message(message_text)
	#print(response)
	#entityValueList = {}
	queryFields = []
	whereValues = {}

	try:
		#entityList = list(response['entities'])
		#print(      list(response['entities']['column'])[0]['value']    )
		confidence = 0.7#response['entities'][entity][0]['confidence']
		
		for element in list(response['entities']['column']):
			#print(element['value'])
			#print(list(response['entities']['column'])[element]['value'])
			queryFields.append(element['value'])

		#print(queryFields)
		#print(entityList)
		for element in list(response['entities']):
			if not element == 'column':
				#whereValues.append(element['value'])
				#print(        response['entities'][element][0]['value']        )
				whereValues[element] = response['entities'][element][0]['value']
				# for thing in response['entities']['policyNumberValue'] :
				# 	print(thing)
				#print(    response['entities'][str(element)]['value']   )
		
		return (queryFields, whereValues, confidence)

	except:
		return (None)