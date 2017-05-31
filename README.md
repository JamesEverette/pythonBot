# pybot
Speak to the bot either in a private message or by addressing it through '@botName'

![gif](https://cloud.githubusercontent.com/assets/5387510/26640759/9d6d203c-45f6-11e7-9545-c9b46790da32.gif)

Current slackbot functionality:
- Executes SQL Queries from conversational inputs, structured using WitAi machine learning.
- Uses my Blockchain API to grab variables from personal ethereum blockchain's smart contracts hosted on an AWS EC2 instance.
- Falls back to Chatterbot retrieval when WitAi is not confident in its response, anything I've not trained WitAi to understand. Chatterbot trained with English Corpus (artificially not-very-intelligent).
