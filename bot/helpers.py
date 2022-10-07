import urllib.request
import json

import re
import jellyfish as jf

from data_models import Item, Price, Guild, Player

# ITEMS API

async def get_items():
    url = "https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json"
    try:
        with urllib.request.urlopen(url) as src:
            data = json.loads(src.read().decode())
            items = [Item(**item_data) for item_data in data]
        return items
    except Exception as e:
        print(e)

async def find_item(text, item_list):
    t_item_name = None
    item_name = None
    tier = None
    enchantment = None
    with_scores=[]

    try:
        if re.search("[tT]+[4-8].[1-3]", text):
            t_tier, t_enchantment = text[-5:].replace(' ','').split('.')
            tier = t_tier.upper()
            enchantment = '@'+t_enchantment
            t_item_name = text[:-5]
        elif re.search("[tT]+[3-8]", text):
            tier = text[-3:].replace(' ','').upper()
            t_item_name = text[:-3]
        else:
            t_item_name = text

        # print(t_item_name, tier, enchantment)

        ## TODO tentar atribuir valor à uma classe pydantic
        for item in item_list:
            if item.LocalizedNames:
                score = jf.jaro_distance(t_item_name.lower(), item.LocalizedNames.PTBR.lower())
                temp = item.dict()
                temp['score'] = score
                with_scores.append(temp)
        with_scores.sort(reverse = True, key=lambda obj: obj['score'])

        if tier and enchantment:
            item_name = f'{tier}_{with_scores[0]["UniqueName"][3:]}{enchantment}'
        elif tier:
            item_name = f'{tier}_{with_scores[0]["UniqueName"][3:]}'
        else:
            item_name = with_scores[0]["UniqueName"]

        return next((item for item in item_list if item.UniqueName == item_name), None).UniqueName
    except Exception as e:
        print(e)


## MARKET API

async def get_prices(item):
    main_url = 'https://www.albion-online-data.com/api/v2/stats/prices/'
    locations = '?locations=Caerleon,Lymhurst,Martlock,Bridgewatch,FortSterling,Thetford' 
    url = main_url + item + locations

    try:
        with urllib.request.urlopen(url) as src:
            data = json.loads(src.read().decode())
            return [Price(**obj) for obj in data]
    except Exception as e:
        print(e)
    
async def get_image_url(item, quality = 3):
    try:
        return f'https://render.albiononline.com/v1/item/{item}.png?&quality={quality}'
    except Exception as e:
        print(e)


## GUILD AND PALYERS API

def _url(endpoint):
    return f'https://gameinfo.albiononline.com/api/gameinfo/{endpoint}'

def _search(text):
    return f'{_url("search")}?q={text}'

async def get_guild(text):
    try:
        with urllib.request.urlopen(_search(text).replace(' ', '%20')) as src:
            data = json.loads(src.read().decode())
            return Guild(Id=data['guilds'][0]["Id"], Name=data['guilds'][0]["Name"])
            
    except Exception as e:
        print(e)

async def get_guild_players(guild_id):
    try:
        with urllib.request.urlopen(f'{_url("guilds")}/{guild_id}/members') as src:
            data = json.loads(src.read().decode())
            return [Player(Id=obj["Id"], Name=obj["Name"]) for obj in data]
            
    except Exception as e:
        print(e)