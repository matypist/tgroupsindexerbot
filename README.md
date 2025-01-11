# Telegram Groups Indexer Bot

## About the project

The "Telegram Groups Indexer Bot" ([TGroupsIndexerBot](https://github.com/matypist/tgroupsindexerbot)) project was born out of the need, in its time by the "Sapienza Students" organization, and today by the [Sapienza Students Network](https://github.com/sapienzastudentsnetwork/sapienzastudentsnetwork.github.io) organization, to promote and make the Telegram groups of students of different courses and their different subjects more easily discoverable from other prospective students.

### Demo

A live demo of the "Telegram Groups Indexer Bot" is available for you to try out. You can access it directly through this [link to @SapienzaStudentsBot](https://telegram.me/SapienzaStudentsBot), where you can explore the various features of the bot and see how it helps prospective students discover and join Telegram groups related to their courses and subjects at the university. The bot provides an easy-to-use interface, allowing users to quickly search for relevant groups based on their field of study, course, or subject, making the process of connecting with other students more efficient and streamlined.

### Current project status

This first version lays the foundations for indexing in particular with regard to the listing of indexed groups to bot users, but there is still a long way to go, since the main functionality, which consists of the bot's users being able to add the bot to a group and autonomously make the group indexed by choosing a category (e.g. a degree course) and a sub-category, is still to be implemented.

🔔 Keep up to date with updates to this GitHub repository by joining https://t.me/TGroupsIndexerBotGit

## Deploy your own instance

### Prerequisites

1. Create your bot instance on BotFather

    1. Start https://t.me/BotFather on Telegram

    2. Send `/newbot` to https://t.me/BotFather on Telegram

    3. Follow the prompts to choose a name and username for your bot instance

    4. Once you are done following the instructions, you should receive a token in the final confirmation message, that will be your TOKEN value

2. Create your PostgreSQL instance

   a. Get an instance hosted for free by ElephantSQL

      1. Go to https://customer.elephantsql.com/signup

      2. Enter your email address

      3. Check your inbox for a confirmation mail from ElephantSQL

      4. Open the link contained in the confirmation mail to open the account creation page

      5. Enter a password of your choosing and check the "Yes" checkbox to accept the Terms of Service

      6. Click the "Create Account" button

      7. Click the "Create New Instance" button and follow the instructions to name, set up and create your instance

      8. Once created, go to the Instance Panel (https://customer.elephantsql.com/instance/) and access the instance

      9. In the instance details page, copy the postgres:// URL with the copy icon, that will be your DATABASE_URL value
      
### Set up a local running environment

1. Install python3 and python3-pip on your operating system

   - Windows (not tested)

     - Download Python3 from the [official website](https://www.python.org/downloads/windows/)
     - Run the installer and follow the prompts to install Python3 on your system
     - Open the Command Prompt and type `python3 -m ensurepip --upgrade` to install python3-pip
   
   - Debian-based GNU/Linux distributions

     - Open the terminal and run the command `sudo apt update` to update the package lists
     - Run the command `sudo apt install python3 python3-pip` to install Python3 and python3-pip

   - Arch Linux

     - Open the terminal and run the command `sudo pacman -Syu` to update the package lists
     - Run the command `sudo pacman -S python python-pip` to install Python3 and python3-pip

2. Clone this repository on your filesystem

   a. Using `git`:
    ```
    git clone https://github.com/matypist/tgroupsindexerbot/
    ```
   
   b. Downloading it as ZIP [[Mirror]](https://github.com/matypist/tgroupsindexerbot/archive/refs/heads/main.zip) and extracting it in a directory

3. Verify that python3 and python3-pip are correctly installed and functioning by running the `python3 -V` and `pip3 -V` commands respectively

4. Open a terminal window or command prompt window and go to the local project root directory using the `cd` command followed by the directory path (e.g. `cd "C:\Users\matypist\Downloads\tgroupsindexerbot"`)

5. Run the `pip install pipenv` command to install pipenv, a tool required to create and manage a virtual environment containing this project's dependencies and environment variables 

6. Run the `pipenv install` command to install all the dependencies required for this project _(which, should you be interested, are specified in this project's Pipfile)_

7. Create a file named `.env` on the local project root directory, with the two following lines:
   ```
   TOKEN=(your TOKEN value without parentheses)
   DATABASE_URL=(your DATABASE_URL value without parentheses)
   ```
   
   To define the environment variable values required for the bot functioning

   _**N.B.:** replace the values with the ones you got in the ["Prerequisites" section](https://github.com/matypist/tgroupsindexerbot#prerequisites)_

### Run

1. Open a terminal window or command prompt window and go to the project root directory using the `cd` command followed by the directory path (e.g. `cd "C:\Users\matypist\Downloads\tgroupsindexerbot"`)

2. Run the `pipenv shell` command to activate this project's virtual environment (previously set up in the ["Set up a local running environment" section](https://github.com/matypist/tgroupsindexerbot/blob/main/README.md#set-up-a-local-running-environment)) and load the environment variables

3. Run the `python main.py` command to finally run your bot instance

4. Start a chat with your bot instance on Telegram finding it through the username that you had previously chosen, e.g. via https://telegram.me/(your_bot_instance_username)
