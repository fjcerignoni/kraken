import os
from dotenv import load_dotenv
import re

import urllib.request
import json
import pandas as pd
import jellyfish as jf
import datetime
#TODO Adicionar logging

import discord
from discord.ext import commands

load_dotenv()
currentPath = os.path.dirname(os.path.realpath(__file__))

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.item_list = os.getenv("ITEMLIST")

    def _loadItems(self):
        # adicionar lib retry
        try:
            with urllib.request.urlopen(self.item_list) as url:
                data = json.loads(url.read().decode())
                df = pd.json_normalize(data)[['Index','UniqueName','LocalizedNames.PT-BR','LocalizedDescriptions.PT-BR']]
                df['LocalizedNames.PT-BR'] = df['LocalizedNames.PT-BR'].astype('str')
                return df

        except Exception as e:
            print(e)  

    async def _getItems(self, item):
        tier = None
        enchantment = None
        try:
            item_list = self._loadItems() 
            #TODO avaliar colocar pra carregar no inicio da aplicação;
            #     colocar um validador de timestamp para atualizar a lista depois de algum tempo

            # item = 'espada dupla t5.2' ; 'espada dupla', 'espada dupla t5'
            if re.search("[tT]+[4-8].[1-3]",item): #t5.2
                tier, enchantment = item[-5:].replace(' ','').split('.')
                tier = tier.upper()
                enchantment = '@'+ enchantment
                item = item[:-5]
            elif re.search("[tT]+[3-8]", item): #t5
                tier = item[-3:].replace(' ','').upper()
                item = item[:-3]
            else:
                pass

            item_list['score'] = [jf.jaro_distance(item.lower(), i.lower()) for i in item_list['LocalizedNames.PT-BR']]     
            unique = item_list[item_list['score'] == item_list['score'].max()]['UniqueName'].iloc[0]
            suggested =  item_list[(item_list['UniqueName'].str.contains(unique[3:])) & (item_list['score'] > 0.7)] # em construção

            for name in suggested['UniqueName'].tolist():
                if tier and enchantment:
                    if name.startswith(tier) and name.endswith(enchantment): # T5_SWORD@2
                        unique = name
                        break
                elif tier:
                    if name.startswith(tier): # T5_SWORD
                        unique = name
                        break
                else:
                    break
            return unique, suggested
        except Exception as e:
            print(e)
    

    def _fetchPrice(self, item):
        market_url = os.getenv("ITEMPRICE")
        market_locations = '?locations=' + os.getenv("LOCATIONS")
        market_url = market_url + item + market_locations

        try:
            with urllib.request.urlopen(market_url) as url:
                data = json.loads(url.read().decode())
                df = pd.json_normalize(data)
                return df[df['sell_price_min_date'] != '0001-01-01T00:00:00'][['item_id','city','quality','sell_price_min','sell_price_min_date']].to_dict(orient='records')
        except Exception as e:
            print(e)     

    def _getItemImage(self, item):
        url = os.getenv("ITEMIMG") + item + '.png?&quality=3'
        return url

    @commands.command()
    async def price(self, ctx, *, item):
        # Loading
        async with ctx.typing():

            # Load selected items info
            sel_item, sugg_item = await self._getItems(item)

            #Get item name and desciption
            item_name = sugg_item[sugg_item['UniqueName'] == sel_item]['LocalizedNames.PT-BR'].item()
            item_desc = sugg_item[sugg_item['UniqueName'] == sel_item]['LocalizedDescriptions.PT-BR'].item()

            # suggested = sugg_item['UniqueName'].tolist()
            # suggested_emojis = [ getItemImage(sugg) for sugg in suggested ]              

            # Grab prices
            prices = self._fetchPrice(sel_item)
            try:
                if prices == []:
                    raise Exception
                
                location_string_all = []
                sell_price_all = []
                time_string_all = []

                for (i, price) in enumerate(prices):
                    
                    # Skip if no data for entry
                    if price['sell_price_min'] == 0:
                        continue
                    
                    #  LOCATION
                    #  put item quality beside location
                    try:
                        if price['quality'] == 0 or price['quality'] == 1:
                            location_string = price['city'] + ' (Normal)'
                        elif price['quality'] == 2:
                            location_string = price['city'] + ' (Bom)'
                        elif price['quality'] == 3:
                            location_string = price['city'] + ' (Excepcional)'
                        elif price['quality'] == 4:
                            location_string = price['city'] + ' (Excelente)'
                        elif price['quality'] == 5:
                            location_string = price['city'] + ' (Obra-Prima)'
                    except:
                        location_string = price['city']

                    location_string_all.append(location_string)

                    # PRICE
                    sell_price_all.append(price['sell_price_min'])

                    # TIME
                    # convert time to find how long ago the date was updated
                    timestamp = datetime.datetime.strptime(prices[i]['sell_price_min_date'], "%Y-%m-%dT%H:%M:%S")
                    tdelta = datetime.datetime.utcnow() - timestamp
                    tdelta = datetime.timedelta.total_seconds(tdelta)

                    if tdelta >= 3600:
                        time_string = str(round(tdelta/3600, 1)) + ' horas'
                    elif tdelta >= 60:
                        time_string = str(round(tdelta/60)) + ' minutos'
                    else:
                        time_string = str(round(tdelta)) + ' segundos'

                    time_string_all.append(time_string)


            except Exception as e:
                print(e)


            finally:
            
                # EMBED 
                embed = discord.Embed(
                    title=f'Preços atuais para {item_name}',
                    description=f'{item_desc}'
                )
                embed.set_thumbnail(url= self._getItemImage(sel_item))
                # embed.add_field(name="confira os preços abaixo", value=20*"-", inline=False)

                try:
                # construct embed fields
                    em_sell_price = ''
                    em_time_string = ''
                    em_location_string = ''

                    for (i, location_string) in enumerate(location_string_all):
                        if sell_price_all[i] != 0:
                            em_location_string += location_string + "\n"
                            em_sell_price += format(sell_price_all[i], ',d') + "\n"
                            em_time_string += time_string_all[i] + "\n"

                    if em_sell_price:
                        embed.add_field(name="Local/Qualidade", value=em_location_string, inline=True)
                        embed.add_field(name="Valor Vendido", value=em_sell_price, inline=True)
                        embed.add_field(name="Atualização", value=em_time_string, inline=True)
                
                except Exception as e:
                    print(e)
                    embed.add_field(name="Sem Dados", value="Sem dados para o item requisitado.", inline=True)

                finally:
                    embed.set_footer(text="Desenvolvido por Ac1dTrip")
                    message = await ctx.send(embed=embed)

                    # for emoji in suggested_emojis:
                    #     await message.add_reaction(emoji)