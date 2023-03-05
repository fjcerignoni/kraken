import json
import logging
import os
import re
import urllib.request

import jellyfish as jf

from data_models import Guild, Item, Player, Price

BASE_DIR = os.path.dirname(os.path.abspath(__name__))


def _similarity_score(a:str, b:str) -> float:
    score =  jf.jaro_distance(a.lower(), b.lower())
    return score

# ITEMS APIs

async def get_items() -> list:

    item_list_filepath = os.path.join(BASE_DIR, 'bot', 'db', 'items.json')
    try:
        if os.path.exists(item_list_filepath):
            with open(item_list_filepath, 'r', encoding='utf8') as file:
                data = json.loads(file.read())

            return [Item(**item_data) for item_data in data]
        else:
            raise Exception('Arquivo db/items.json não encontrado.')

    except Exception as e:
        print(e)
    

async def find_item(usr_input:str) -> str:

    item_list = await get_items()
    tier = None
    enchantment = None

    resource_list = list(set(
            item.UniqueName.split('_')[1] for item in item_list
            if re.search("LEVEL+[1,4]+@",item.UniqueName)
        ))

    try:
        if re.search("[tT]+[4-8].[1-4]", usr_input):
            tier, enchantment = usr_input[-5:].replace(' ','').split('.')
            usr_input = usr_input[:-5]
        elif re.search("[tT]+[3-8]", usr_input):
            tier = usr_input[-3:].replace(' ','')
            usr_input = usr_input[:-3]
        else:
            pass

        for item in item_list:
            if item.LocalizedNames: 
                item.score = _similarity_score(usr_input, item.LocalizedNames.PTBR)
        item_list.sort(reverse = True, key=lambda item: item.score)

        if tier and enchantment:
            if any(resource in item_list[0].UniqueName for resource in resource_list):
                unique_name = f'{tier.upper()}_{item_list[0].UniqueName[3:]}_LEVEL{enchantment}@{enchantment}'
            else:
                unique_name = f'{tier.upper()}_{item_list[0].UniqueName[3:]}@{enchantment}'
        elif tier:
            unique_name = f'{tier.upper()}_{item_list[0].UniqueName[3:]}'
        else:
            unique_name = item_list[0].UniqueName

        return next((item for item in item_list if item.UniqueName == unique_name), None).UniqueName

    except Exception as e:
        print(e)

## MARKET API

async def get_prices(unique_name:str) -> list:
    main_url = 'https://www.albion-online-data.com/api/v2/stats/prices/'
    locations = '?locations=Caerleon,Lymhurst,Martlock,Bridgewatch,FortSterling,Thetford' 
    url = main_url + unique_name + locations

    try:
        with urllib.request.urlopen(url) as src:
            data = json.loads(src.read().decode())
            return [Price(**obj) for obj in data]
    except Exception as e:
        print(e)


async def get_image_url(unique_name:str, quality:int = 3) -> str:
    try:
        return f'https://render.albiononline.com/v1/item/{unique_name}.png?&quality={quality}'
    except Exception as e:
        print(e)


## GUILD AND PLAYERS API

def _url(endpoint:str) -> str:
    return f'https://gameinfo.albiononline.com/api/gameinfo/{endpoint}'


def _search(input:str) -> str:
    return f'{_url("search")}?q={input}'
    
def _player_info_url(player_id:str) -> str:
    return f'{_url("players")}/{player_id}'

async def get_guild(guild_name:str) -> dict:
    try:
        with urllib.request.urlopen(_search(urllib.parse.quote(guild_name))) as src:            
            data = json.loads(src.read().decode())
            return Guild(Id=data['guilds'][0]["Id"], Name=data['guilds'][0]["Name"])
            
    except Exception as e:
        print(e)


async def get_guild_players(guild_id:str) -> list:
    try:
        with urllib.request.urlopen(f'{_url("guilds")}/{guild_id}/members') as src:
            data = json.loads(src.read().decode())
            return [Player(Id=obj["Id"], Name=obj["Name"]) for obj in data]
            
    except Exception as e:
        print(e)

async def get_player(player_name:str) -> dict:
    try:
        # Search for player by name
        with urllib.request.urlopen(_search(urllib.parse.quote(player_name))) as src:
            data = json.loads(src.read().decode())
            player_id = data['players'][0]['Id']

        # Get player info by ID
        with urllib.request.urlopen(_player_info_url(player_id)) as src:
            data = json.loads(src.read().decode())

            return data

    except Exception as e:
        print(e)