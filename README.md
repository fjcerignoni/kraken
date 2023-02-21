# Shadow Bot
Discord Bot to fetch Albion Online information for the Shadow Spirits Guild 

# Commands

## ADM

### $init

Initiate the discord server for a given Guild. 
It asks and save the IGN of the Guild.

### $check_players

List all the players in the subscribed Guild.

### $give_permition "user_name"

Give moderation permition to a given user.
The users with permition should be able to execute Raid commands.

## MARKET

### $price "item name tier"

Fetch item price from the [Albion Online Data Project](https://www.albion-online-data.com/)

### Usage:

Type the name of the item in Brazilian Portuguese (PT-BT) and the tier you want in front of it in 'tX.X' format </br>
If no tier information is supplied the bot will return the lowest tier for the item.

```
    $price brumário t6.2
```
![shadow-bot1](https://user-images.githubusercontent.com/21298220/191596762-d332d892-4990-412a-9082-e607303362fb.PNG)


## RAID

### $organize_raid "content date 'description'"

Organize a list of roles to a certain content.
The content list templates are located in ``cogs\raids_template.json``

To consult the list of templates execute the command ``$organize_raid_help``

### Usage:

Type the template name of the raid, followed by the date in DD/MM/YYYY and the description of the raid. Use ``;`` to break lines in the description.

The list will be shown as a discord message and each role will have his own emoji. The players then should select the emoji they want to fill the specific role.

```
$organize_raid avalon 21/02/2023 "Saída as 18:00;Levar montaria rápida; Comida .2"
```
![image](https://user-images.githubusercontent.com/21298220/220457109-71013ce8-3657-4a80-b6c6-a9f5b78fc5b2.png)

### $organize_raid_help

Show help to organize a raid in Discord.

# Dev Environment

- Requirements:
  - Python 3.8 or higher
  - Create Discord Bot at [Discord Developers Applications](https://discord.com/developers/applications) to get a valid token and use [Discord Permissions](https://discordapi.com/permissions.html) to add the bot in your server
  - Add token to a .env file in the project root, use .env-sample as exemple.
  - Clone this repository

1) Create python environment
   ```
    $ python -m venv --clear --copies .venv
   ```
2) Enter environment 
   ```
   Windows
    $ .venv\Scripts\activate.bat

   Linux
    $ source .venv/bin/activate
   ```
3) Upgrade pip and wheel
   ```
    (.venv) $ python -m pip install --upgrade pip wheel
   ```

4) Install dependencies

   ```
    (.venv) $ python -m pip install -r requirements.txt
   ```

5) Create database
   ```
    (.venv) $python bot\db\init_db.py
   ```

6) Start bot
   ```
    (.venv) $python bot\main.py
   ```

# Scheduler
Inside the ``scheduler`` folder there are 2 scripts: ``scheduler.py`` and ``jobs.py``
- ``jobs.py``: ETL processes that can be executed manually or scheduled by applications/libraries like *python-crontab*;
- ``scheduler.py``: *python-crontab* implementation to run jobs defined on ``jobs.py``;

The shell script ``build.sh`` was created in order to provide a dockerized version of scheduled jobs (*Linux* environment with *docker.io* installed is required).
