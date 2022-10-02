# Kraken
Discord Bot to fetch Albion Online information for the Shadow Spirits Guild

<img src="https://user-images.githubusercontent.com/21298220/193434889-c774aaaa-1b97-431c-a528-c655ad33c0f0.PNG" alt="kraken" style="height: 70px; width: 80px; align: right"/>

# Commands
### $price "item name tier"

Fetch item price from the [Albion Online Data Project](https://www.albion-online-data.com/)

### Usage:

Type the name of the item in Brazilian Portuguese (PT-BT) and the tier you want in front of it in 'tX.X' format </br>
If no tier information is supplied the bot will return the lowest tier for the item.

```
    $price brumário t6.2
```
![shadow-bot1](https://user-images.githubusercontent.com/21298220/191596762-d332d892-4990-412a-9082-e607303362fb.PNG)

# Dev Environment

- Requirements:
  - Python 3.8 or higher
  - Create Discord Bot at [Discord Developers Applications](https://discord.com/developers/applications) to get a valid token and use [Discord Permissions](https://discordapi.com/permissions.html) to add the bot in your server
  - Clone this repository
  - Add token to a .env file in the project root, use .env-sample as exemple.


1) Create python environment
   ```
    $ python -m venv --clear --copies .venv
   ```
2) Enter environment 
   ```
   Windows
    $ .venv\Scripts\activate.bat

   Linux
    $ source .venv\bin\activate
   ```
3) Upgrade pip and wheel
   ```
    (.venv) $ python -m pip install --upgrade pip wheel
   ```

4) Install dependencies

   ```
    (.venv) $ python -m pip install -r requirements.txt
   ```

5) Start bot
   ```
    (.venv) $python bot\main.py
   ```

