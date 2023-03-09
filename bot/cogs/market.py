from locale import setlocale, format_string, LC_ALL
from discord import Embed
from discord.ext import commands
from datetime import datetime, timedelta

from helpers import find_item, get_prices, get_image_url, get_items
from data_models import Item
## TODO Adicionar logging

setlocale(LC_ALL, 'pt_BR.UTF-8')

class Market(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def price_help(self, ctx: commands.Context) -> None:
        a=0

    @commands.command()
    async def price(self, ctx: commands.Context, *, typed:str) -> None:
        # Loading
        async with ctx.typing():
            try:
                # Load selected items info
                selected_item = await find_item(typed)

                # Get item name and desciption
                item_info = next(
                    (
                        item for item in await get_items()
                            if item.UniqueName == selected_item
                    )
                )

                item_name = item_info.LocalizedNames.PTBR
                item_desc = item_info.LocalizedDescriptions.PTBR

                # Get prices
                prices = await get_prices(selected_item)
                try:
                    if prices == []:
                        raise Exception
                    
                    location_string_all = []
                    sell_price_all = []
                    time_string_all = []

                    for price in prices:
                        # Skip if no data for entry
                        if price.sell_price_min == 0:
                            continue
                        
                        #  LOCATION
                        #  put item quality beside location
                        try:
                            if price.quality == 0 or price.quality == 1:
                                location_string = price.city + ' (Normal)'
                            elif price.quality == 2:
                                location_string = price.city + ' (Bom)'
                            elif price.quality == 3:
                                location_string = price.city + ' (Excepcional)'
                            elif price.quality == 4:
                                location_string = price.city + ' (Excelente)'
                            elif price.quality == 5:
                                location_string = price.city + ' (Obra-Prima)'
                        except:
                            location_string = price.city

                        location_string_all.append(location_string)

                        # PRICE
                        sell_price_all.append(price.sell_price_min)

                        # TIME
                        # calculate time delta to find how long ago the date was updated
                        tdelta = datetime.utcnow() - price.sell_price_min_date
                        tdelta = timedelta.total_seconds(tdelta)

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
                
                    try:
                        # EMBED 
                        embed = Embed(
                            title=f'Preços atuais para {item_name}',
                            description=f'{item_desc}'
                        )
                        embed.set_thumbnail(url= await get_image_url(selected_item))
                        embed.add_field(name="confira os preços abaixo", value=20*"-", inline=False)

                    
                        # construct embed fields
                        em_location_string = ''.join(f"{location_string}\n" for location_string in location_string_all)
                        em_sell_price = ''.join(f"{format_string('%d', sell_price, 1)}\n" for sell_price in sell_price_all)
                        em_time_string = ''.join(f"{time_string}\n" for time_string in time_string_all)

                        if em_sell_price:
                            embed.add_field(name="Local/Qualidade", value=em_location_string, inline=True)
                            embed.add_field(name="Valor Vendido", value=em_sell_price, inline=True)
                            embed.add_field(name="Atualização", value=em_time_string, inline=True)
                        else:
                            raise Exception
                    
                    except Exception as e:
                        print(e)
                        embed.add_field(name="Sem Dados", value="Sem dados para o item requisitado.", inline=True)

            except Exception as e:
                print(e)
                embed = Embed(
                    title=f'Item não encontrado',
                    description=f'Não encontramos informação para o item requisitado.'
                )
            finally:
                embed.set_footer(text="Desenvolvido por Ac1dTrip & Caionagyy")
                await ctx.send(embed=embed)
