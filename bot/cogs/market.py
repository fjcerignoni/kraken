from discord import Embed
from discord.ext import commands
from datetime import datetime, timedelta
from helpers import find_item, get_prices, get_image_url
## TODO Adicionar logging

class Market(commands.Cog):
    def __init__(self, bot, item_list):
        self.bot = bot
        self.item_list = item_list

    @commands.command()
    async def price(self, ctx, *, typed):
        # Loading
        async with ctx.typing():
            try:
                # Load selected items info
                selected_item = await find_item(typed, self.item_list)

                # Get item name and desciption
                item_info = next((item for item in self.item_list if item.UniqueName == selected_item))

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
                
                    # EMBED 
                    embed = Embed(
                        title=f'Preços atuais para {item_name}',
                        description=f'{item_desc}'
                    )
                    embed.set_thumbnail(url= await get_image_url(selected_item))
                    embed.add_field(name="confira os preços abaixo", value=20*"-", inline=False)

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
                        await ctx.send(embed=embed)

                        # for emoji in suggested_emojis:
                        #     await message.add_reaction(emoji)
            except Exception as e:
                print(e)
                embed = Embed(
                    title=f'Item não encontrado',
                    description=f'Não encontramos informação para o item requisitado.'
                )
                embed.set_footer(text="Desenvolvido por Ac1dTrip")
                await ctx.send(embed=embed)
