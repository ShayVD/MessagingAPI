# Coding Exercise

Imagine we are making a private messaging service for our new company Perry’s Summer Vacation Goods and Services. We need you to design and create a scalable API to be able to handle the many messages this company is going to handle.

### Develop an application meeting the following requirements:

* The application must be able to create and get users.
- We do not expect you do handle any kind of authentication for users.
* The application must allow users to send a message to one other user.
- No need to consider group chats.
* The application must allow editing and deleting messages.
* The application must be able to get all the messages sent between two users.
* The application must allow a user to "like" a message.
* The application must be able to get a list of other users that have sent or received messages to/from a specified user.

### Technical requirements:

* The application should be a REST API (No need for any kind of UI)
* Use what language you are comfortable with, but Typescript, Javascript, Java preferred.
* The source code must be shared in a public repository (Github, Bitbucket, etc).
* The application should be ready to run in the cloud or in a container (You can use any technology available in AWS).
* The application data must be persisted in a database of some type.

### Other notes:

* We do not expect that you spend more than 8 hours on this challenge, so some rough edges are acceptable.
* In terms of testing, implement only what unit/integration testing you find necessary to build it. We will not judge for lack of test coverage.
* Take into consideration how you might scale this application for a large amount of load. No need to implement any kind of stress/load test.
* We do not expect you do handle any kind of authentication for users.
* Treat this as a proof of concept, so documentation is not important.
* Have fun with it!

## SETUP
1. docker-compose pull
2. docker-compose build
3. docker-compose up
4. UI is available at 'localhost:1337' or on 'domain:80' if deployed

## CREATE ADMIN USER (not required)
1. docker exec -it genesys_api_1 bash
2. python manage.py createsuperuser

## TESTING
1. Give permissions to allow DB creation
* docker exec -it genesys_db_1 bash
* mysql -u root -p
* Use MYSQL_ROOT_PASSWORD from .env file
* GRANT ALL PRIVILEGES ON test_default.* TO 'root';
2. Run tests
* docker exec -it genesys_api_1 bash
* python manage.py test

## ERRORS
If you encounter this error;
'''ERROR: for db  Cannot start service db: driver failed programming external connectivity on endpoint genesys_db_1: Error starting userland proxy: listen tcp 0.0.0.0:3306: bind: address already in use'''
Then make sure system MySQL is down and retry:
'''sudo service mysql stop'''