## ZioNet Homework Microservices Application

### TL;DR

The application retrieves current stock and futures prices and calculates future dividends based on the futures expiration date and the current discount rate.

It uses a microservices architecture and provides an API exposed to the outside world. There is also a sample Telegram bot to demonstrate the service's functionality.

#### The Bot

For demonstration purposes, I have created a small Telegram bot that acts as a frontend for the backend in production. Feel free to add [@zionnet_hw_bot](https://t.me/zionet_hw_bot) to your Telegram to see that the app is working. It does not store any user details. The bot accepts two types of commands:
- */list* - lists tickers with at least one available future
- *TICKER* - send any exchange ticker from the previous list in any combination of upper/lowercase, like 'sber', 'TATNP,' or any other. The bot will poll the backend and format the JSON to something resembling a table in Telegram.
The bot is not part of the `docker-compose.yml` since it can be run anywhere. Its source code is included in the project. Currently, the service and the bot are running 24/7 on a **Raspberry Pi 4 4GB**.

### Installation

- Clone the repository:

```
git clone https://github.com/holohup/div_bot_2.0.git && cd div_bot_2.0
```

- Launch Docker Compose:

```
docker compose up [-d]
```

After some *rustling*, the app with all its microservices should be running.

#### Another External API

The application uses an external API - Tinkoff Broker. If you happen to have its API key, you can add it to the `TCSApiAccessor/.env.example`, and the application will work correctly. Without it, it provides data from fixtures - everything, including tests, runs smoothly, but you cannot trust the data it provides. The Telegram bot is connected to a backend that uses the real key, so the bot responses are legitimate.

### How to Test

#### API

The two endpoints are available via a Swagger interface at [http://127.0.0.1:8005/docs/](http://127.0.0.1:8005/docs/).

#### Integration Tests

**!NB** Make sure you have Docker Compose running.

In the app root folder, create a virtual environment on a machine with Python installed, activate it, install the dependencies, and launch pytest - all of them should pass:

```
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pytest
```

### Structure

![application scheme](https://github.com/holohup/div_bot_2.0/blob/main/img/scheme.png?raw=true)

The structure above is self-explanatory. I'll write more details after I get some feedback from real users who wish to know more about the structure. However, there's one important point:

##### log.txt

Since the logging server relies on Queue, it works asynchronously and adds the results of dividend estimation to the `log.txt` file in the root folder of the project. It's mapped from the LogAccessor, so you should see the changes in the log. 

### To-Do
- Decouple business logic from management - create a financial engine underneath the manager
- Increase test coverage, especially for data handling and `None` values
- If the project is to be developed further, add more docstrings and type annotations
- Add health check endpoints for Docker Compose
- ~Try to use MarkdownV2 and with mono-width font in a telegram bot for a neater table~
- Implement CI/CD using Github Actions: flake8, isort, unit and integration tests, images creation and push to Dockerhub, optionally SSH for deployment.
- ~DAPRize it.~
