import urllib.request
import json

import re
import jellyfish as jf

from data_models import Item, Price

async def get_items():
    url = "https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json"
    try:
        with urllib.request.urlopen(url) as src:
            data = json.loads(src.read().decode())
            items = [Item(**item_data) for item_data in data]
        return items
    except Exception as e:
        print(e)

async def find_item(typed, item_list):
    t_item_name = None
    item_name = None
    tier = None
    enchantment = None
    with_scores=[]

    try:
        if re.search("[tT]+[4-8].[1-3]", typed):
            t_tier, t_enchantment = typed[-5:].replace(' ','').split('.')
            tier = t_tier.upper()
            enchantment = '@'+t_enchantment
            t_item_name = typed[:-5]
        elif re.search("[tT]+[3-8]", typed):
            tier = typed[-3:].replace(' ','').upper()
            t_item_name = typed[:-3]
        else:
            t_item_name = typed

        print(t_item_name, tier, enchantment)

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

async def get_prices(item):
    main_url = 'https://www.albion-online-data.com/api/v2/stats/prices/'
    locations = '?locations=Caerleon,Lymhurst,Martlock,Bridgewatch,FortSterling,Thetford' 
    url = main_url + item + locations

    try:
        with urllib.request.urlopen(url) as src:
            data = json.loads(src.read().decode())
            return [Price(**item_price) for item_price in data]
    except Exception as e:
        print(e)
    
async def get_image_url(item, quality = 3):
    try:
        return f'https://render.albiononline.com/v1/item/{item}.png?&quality={quality}'
    except Exception as e:
        print(e)
    