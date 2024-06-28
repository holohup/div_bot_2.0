## ZioNet homework microservices application

### ;TL:DR

The application gets current stock and futures prices, and calculates how much dividends are in the future, given the futures expiration date and current discount rate. Russian stock market is ineffective right now and gives opportunities for arbitrage quite often.

It uses microservices architecture and provides an API exposed to the outer world. There's also a sample telegram robot to see the service is functioning. 

![application scheme](https://github.com/holohup/div_bot_2.0/blob/main/img/scheme.png?raw=true)




### ToDo
- decouple business logic from management - create a financial engine underneath the manager
- increase test coverage, especially for data tossing and None values
