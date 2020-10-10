# SPAM App
Submitted for Programming in Security 2019 CA2 Assignment

## Built With
- Kivy Cross Platform Python framework
- SQlite Database


## Setup
- run `python /server/server.py` to start the server
- run `python /client/main.py` to start the client GUI

### Maintenance of Database
- run `python /server/admin.py` to modify/view db data like logs, food, promos etc.


## Extra Features not included in Assignment
| __Features__  | __Description__  |
|---|---|
| Full GUI for Client-side  | Built using the kivy module and kivy language together with python, clients have a full GUI interface to interact with when placing orders through spam <br><br>Run “main.py” to start the application  |
| Server runs asynchronously  | Server code is programmed to run asynchronously using the asyncio module to increase efficiency when dealing with client requests as the server is able to use multiple threads|

## App Images
![](/images/spam01.png)
![](/images/spam02.png)
