from wit import Wit
import os

witAccessToken = os.environ.get('witAccessToken')

client = Wit(witAccessToken)

def getWitResponse(message_text):
	response = client.message(message_text)
	#confidence = list(response['confidence'])[0]
	#print('entity------- '+confidence)
	try:
		entity = list(response['entities'])[0]
		
		value = response['entities'][entity][0]['value']

		confidence = response['entities'][entity][0]['confidence']

		return (value, confidence, entity)
	except:
		return (None, None, None)

print(getWitResponse("Show me sports 1"))

#print(        list(client.message('show me sports news'))['confidence'] [0]       )