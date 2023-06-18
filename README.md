# TeleAssist - Telegram Bot

```
Frontend interface for the TeleAssist project!
```


## Features
[*TeleAssist - Web Server* Features](https://github.com/lihaan/TeleAssist-Web#features)


## Limitations

[*TeleAssist - Web Server* Limitations](https://github.com/lihaan/TeleAssist-Web#limitations)


## Requirements

Note that the functionality of this *TeleAssist - Telegram Bot* is meant to be paired with the [*TeleAssist - Web Server*](https://github.com/lihaan/TeleAssist-Web). It acts as the back-end containing all the core functionalities.

- Python 3
  - Recommended: >= 3.10.4
- Host Machine
  - RAM: >= 75MB to ensure optimal performance
  - Internet connectivity
    - To ping Telegram for any new messages (these are termed by Telegram as "updates")
- Docker (optional)
  - Dockerfile provided if you wish to containerize it


## Setup

1. Create Telegram bot via BotFather
    - [Link to instructions on Telegram docs](https://core.telegram.org/bots/tutorial)
    - Obtain your bot token

2. Clone repository
    > \> git clone https://github.com/lihaan/TeleAssist-Bot.git

3. Create message_templates.py in */src* directory
    - This python file will contain the messages that the app sends
    - Refer to samples_messages_templates.txt for a quickstart!

4. Create a .env file with the following parameters
    - BOT_TOKEN (Telegram bot_token)
    - MY_USER_ID (Your Telegram user_id, can be easily found by using @userinfobot on Telegram)

5. Install dependencies
    - Recommended to create a virtual environment (eg. venv) before installing
        > \> pip install -r requirements.txt


## Run
1. Run locally
   > \> python src/main.py


## Build and Deploy (with Docker)

- Dockerfile is provided for reference at */src/Dockerfile*
- Take note to amend the URL of the web server in */src/rest.py* from localhost to \[name\_assigned\_to\_web\_server\_container\]. By default, you should change the URL to *http://web:5000*
- If you are using *TeleAssist - Web Server*, you should consider placing all docker containers in the same network
- Final list of commands to build and run:
  > \> docker network create tele-assist-network

  > \> docker build -t tele-assist-bot .

  > \> docker run --name bot --net tele-assist-network -d tele-assist-bot


## Contributing

Although *TeleAssist* is simply a pet project of mine, I am super keen on improving it and expanding its capabilities. Feel free to raise issues to provide feedback if you have any. If this project has helped you in any way, do give it a star or [buy this struggling university student a coffee](https://www.buymeacoffee.com/lihanong)! Thank you!

~ Li Han