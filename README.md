# pybot
Bot application for slack. Uses WitAi machine learning to structure queries for MS SQL database and DynamoDB. Also uses my blockchain API to grab variables from personal ethereum blockchain's smart contracts hosted on an AWS EC2 instance. Falls back to Chatterbot retrieval bot when WitAi's confidence in its response is below a certain level. Chatterbot trained with the Ubuntu DialogCoprus.

Speak to the bot either in a private message or addressing it through '@botName'

Current slackbot functionality:
Bot structures SQL Queries from conversational inputs, using WitAi machine learning:
![querygif](https://cloud.githubusercontent.com/assets/5387510/26638562/6b676364-45f0-11e7-8e52-10838e06c448.gif)
