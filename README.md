## ZioNet homework microservices application

### ;TL:DR

The application gets current stock and futures prices, and calculates how much dividends are in the future, given the futures expiration date and current discount rate. 

It uses microservices architecture and provides an API exposed to the outer world. There's also a sample telegram robot to see the service is functioning.

#### The robot

For demonstration purposes I've created a small telegram robot, which acts as a frontend for the backend in production. Feel free to add https://t.me/zionet_hw_bot to your telegram to see that the app is working. It does not store any details about the user. The robot accepts two types of commands: 
- */list* - lists tickers with at least one future available
- *TICKER* - send any exchange ticker from the previous list and the bot will poll the backend, and format the json to a something-like-table in telegram.
The robot is not a part of the docker-compose.yml, since it can be run anywhere. It's source code is included in the project. Right now the service and the robot are running 24/7 on a #Raspberry Pi 4 4GB#

![application scheme](https://github.com/holohup/div_bot_2.0/blob/main/img/scheme.png?raw=true)




### ToDo
- decouple business logic from management - create a financial engine underneath the manager
- increase test coverage, especially for data tossing and None values
