## ZioNet homework microservices application

### ;TL:DR

The application gets current stock and futures prices, and calculates how much dividends are in the future, given the futures expiration date and current discount rate. 

It uses microservices architecture and provides an API exposed to the outer world. There's also a sample telegram robot to see the service is functioning.

#### The robot

For demonstration purposes I've created a small telegram robot, which acts as a frontend for the backend in production. Feel free to add [@zionnet_hw_bot](https://t.me/zionnet_hw_bot) to your telegram to see that the app is working. It does not store any details about the user. The robot accepts two types of commands: 
- */list* - lists tickers with at least one future available
- *TICKER* - send any exchange ticker from the previous list in any combination of upper/lowercase, like 'sber', 'TATNP' or any other, and the bot will poll the backend, and format the json to a something-like-table in telegram.
The robot is not a part of the docker-compose.yml, since it can be run anywhere. It's source code is included in the project. Right now the service and the robot are running 24/7 on a **Raspberry Pi 4 4GB**

### Installation

Clone the repository and do a

```
docker compose up [-d]
```

After some *rustring* the app with all its microservices should be running.
##### Fair word of warning

I've tested it only on two devices so far, sometimes it doesn't run from the first time on a ##Raspberry Pi##, since the containers are launching slowly and by the time the needed container is ready, the container that needs it has already exited(1). This problem is solved by relaunching, since for some reason when it is not building the images, the python containers start faster.

I am thinking about adding healthcheck endpoints to each container for docker to know when exactly is the right time for the launch. On a PC the process works flawlessly.

#### Another external API

The application uses an external API - Tinkoff Broker. If you happen to have it's API key, you can add it to the TCSApiAccessor/.env.example and the application will work correctly. Without it, it provides data from fixtures - everything including tests is running, but you cannot trust the data it provides. The Telegram bot is connected to a backend that utilizes the real key, therefore the robot responses are legit.


### How to test

#### API

The two endpoints are available as a Swagger interface at http://127.0.0.1:8005/docs/

#### Integration tests

##!NB## Make sure you have docker compose up running.
In the app root folder, create a virtual environment on a machine with Python installed, activate it, install the dependencies, and launch pytest - all of them should bass
```
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pytest
```

### Structure

![application scheme](https://github.com/holohup/div_bot_2.0/blob/main/img/scheme.png?raw=true)

The structure above is pretty self-explanitory, I'll write more details after I get some feedback from real people who wish to know more about the structure.


### ToDo
- decouple business logic from management - create a financial engine underneath the manager
- increase test coverage, especially for data tossing and None values
- if the project is to be developed, more Docstrings to the God of Docstrings and more type annotations
- health check endpoints for docker compose
