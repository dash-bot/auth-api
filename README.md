# Dash: Authentication API

#### For more detailed information, check out Dash on [Devpost](https://devpost.com/software/dash-5wq83e)!
#### Created at nwHacks 2018


## What is this API used for?
This is one of three microservices that make up Dash, and provides it with authentication abilities via **Microsoft Cognitive Services' Speaker Recognition**. 

Users are authenticated via biometric identification with users speaking a phrase, which is then verified by the Speaker Recognition API. A level of confidence is returned of how confident the service is that the user attempting to log in is the actual user. This prohibits any unauthenticated access to a customer's account in [banking-api](https://github.com/dash-bot/banking-api).
