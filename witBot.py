from wit import Wit
import os

witAccessToken = os.environ.get('witAccessToken')

client = Wit(witAccessToken)

def witResponse(message_text):
	response = client.message(message_text)
	try:
		entity = list(response['entities'])[0]
		value = response['entities'][entity][0]['value']
		return (entity, value)
	except:
		return (None, None)

print(witResponse("Show me policy number 1"))