# from pathlib import Path
from locale import setlocale, format_string, LC_ALL
from discord.ext import commands
from discord import Embed
from helpers import get_player, get_guild, get_guild_players, get_alliance

# current_path = current_path = Path(__file__).parent.absolute()
setlocale(LC_ALL, 'pt_BR.UTF-8')

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def profile(self, ctx: commands.Context, *args) -> None:
        """
            <player_name>

            The command shows the stats of a given player (IGN).
        """
        async with ctx.typing():
            try:
                  # join all arguments provided by the user to get the nickname
                  nickname = ' '.join(args)
                  player_data = await get_player(nickname)
                  
                  if player_data == None:
                        raise Exception("Player not found.")
                  
                  ally = player_data['AllianceName']
                  guild = player_data['GuildName']
                  pve_stats = player_data['LifetimeStatistics']['PvE']
                  # Criando um objeto Embed com título, imagem e cor

                  embed = Embed(title=f"> {player_data['Name']}", color=0xFF5733)
                  embed.set_thumbnail(
                        url="https://render.albiononline.com/v1/spell/HASTE.png")

                  # Adicionando campos com informações
                  embed.add_field(name="Guild", value=f"[{ally}] {guild}\n", inline=False)
                  embed.add_field(name="", value=f"```PvP```", inline=False)
                  embed.add_field(name="Kill Fame", value=f'{player_data["KillFame"]:,}', inline=True)
                  embed.add_field(name="Death Fame", value=f'{player_data["DeathFame"]:,}', inline=True)
                  embed.add_field(name="Fame Ratio", value=f'{player_data["FameRatio"]:.2f}', inline=False)

                  # Informações sobre as estatísticas de vida do jogador
                  embed.add_field(name="", value=f"```PvE```", inline=False)
                  embed.add_field(name=f"Total de PvE:", value=f"{pve_stats['Total']:,}", inline=False)
                  embed.add_field(name="Royal", value=f"{pve_stats['Royal']:,}", inline=True)
                  embed.add_field(name="Black", value=f"{pve_stats['Outlands']:,}", inline=True)
                  embed.add_field(name="Avalon", value=f"{pve_stats['Avalon']:,}\n", inline=True)
                  embed.add_field(name="Hellgate", value=f"{pve_stats['Hellgate']:,}", inline=True)
                  embed.add_field(name="Corrupted Dungeon", value=f"{pve_stats['CorruptedDungeon']:,}", inline=True)

                  # Informações sobre as estatísticas de coletas do jogador
                  embed.add_field(name="", value=f"```Coletas```", inline=False)
                  gather_stats = player_data['LifetimeStatistics']['Gathering']
                  embed.add_field(name="Linhos",
                                    value=f"Total: {gather_stats['Fiber']['Total']:,}\n"
                                          f"Royal: {gather_stats['Fiber']['Royal']:,}\n"
                                          f"Black: {gather_stats['Fiber']['Outlands']:,}\n"
                                          f"Avalon: {gather_stats['Fiber']['Avalon']:,}",
                                    inline=True)
                  embed.add_field(name="Pelegos",
                                    value=f"Total: {gather_stats['Hide']['Total']:,}\n"
                                          f"Royal: {gather_stats['Hide']['Royal']:,}\n"
                                          f"Black: {gather_stats['Hide']['Outlands']:,}\n"
                                          f"Avalon: {gather_stats['Hide']['Avalon']:,}",
                                    inline=True)
                  embed.add_field(name="Minérioss",
                                    value=f"Total: {gather_stats['Ore']['Total']:,}\n"
                                          f"Royal: {gather_stats['Ore']['Royal']:,}\n"
                                          f"Black: {gather_stats['Ore']['Outlands']:,}\n"
                                          f"Avalon: {gather_stats['Ore']['Avalon']:,}",
                                    inline=True)
                  embed.add_field(name="Pedras",
                                    value=f"Total: {gather_stats['Rock']['Total']:,}\n"
                                          f"Royal: {gather_stats['Rock']['Royal']:,}\n"
                                          f"Black: {gather_stats['Rock']['Outlands']:,}\n"
                                          f"Avalon: {gather_stats['Rock']['Avalon']:,}",
                                    inline=True)
                  embed.add_field(name="Madeiras",
                                    value=f"Total: {gather_stats['Wood']['Total']:,}\n"
                                          f"Royal: {gather_stats['Wood']['Royal']:,}\n"
                                          f"Black: {gather_stats['Wood']['Outlands']:,}\n"
                                          f"Avalon: {gather_stats['Wood']['Avalon']:,}",
                                    inline=True)
                  embed.add_field(name="Todos",
                                    value=f"Total: {gather_stats['All']['Total']:,}\n"
                                          f"Royal: {gather_stats['All']['Royal']:,}\n"
                                          f"Black: {gather_stats['All']['Outlands']:,}\n"
                                          f"Avalon: {gather_stats['All']['Avalon']:,}",
                                    inline=True)
            except Exception as e:
                  print(e)
                  embed = Embed(
                        title=f'Jogador não encontrado',
                        description=f'Não encontramos informações para o jogador requisitado.'
                  )
            finally:
                  embed.set_footer(text="""
Estas informações são carregadas do projeto tools4albion e podem
ter um delay alguns dias em relação ao Albion Online.

Desenvolvido por Ac1dTrip & Caionagyy""")
                  # Enviando o embed para o canal
                  await ctx.send(embed=embed)

    @commands.command()
    async def profile_guild(self, ctx:commands.Context, *, typed:str) -> None:
        """
            <guild_name>

            The command shows the stats of a given guild (IGN).
        """
        async with ctx.typing():
            try:
                guild = await get_guild(typed)
                if guild == None:
                  raise Exception('Guild not found.')
            
                alliance = await get_alliance(guild.AllianceId)

                # create list with players name consulting tools4albion API and sort
                players = [player.Name for player in await get_guild_players(guild.Id)]
                players.sort()

                # create chunks to better display the information in discord embed
                chunk_size= int(len(players) / 3)
                chunk=[players[i:i + chunk_size] for i in range(0, len(players), chunk_size)]

                column1 = ''.join(f'{player}\n' for player in chunk[0])
                column2 = ''.join(f'{player}\n' for player in chunk[1])
                column3 = ''.join(f'{player}\n' for player in chunk[2])

                # crate embed
                embed = Embed(
                    title=f'> [{guild.AllianceTag}] {guild.Name}',
                    color=0xFF5733
                )

                embed.add_field(name="Criada em", value=guild.Founded.strftime("%d/%m/%y"), inline=True)
                embed.add_field(name="Kill Fame", value=format_string('%d', guild.killFame, 1), inline=True)
                embed.add_field(name="Death Fame", value=format_string('%d', guild.DeathFame, 1), inline=True)
               
                embed.add_field(name="", value="```Jogadores```", inline=False)
                embed.add_field(name="Nº Players", value=len(players), inline=False)
                embed.add_field(name="", value=column1, inline=True)
                embed.add_field(name="", value=column2, inline=True)
                embed.add_field(name="", value=column3, inline=True)

                if alliance != None:
                  embed.add_field(name="", value="```Aliança```", inline=False)
                  embed.add_field(name="Nome", value=alliance.AllianceName, inline=True)
                  embed.add_field(name="Tag", value=alliance.AllianceTag, inline=True)
                  embed.add_field(name="Nº Players", value=alliance.NumPlayers, inline=True)

                embed.set_footer(text="""
Estas informações são carregadas do projeto tools4albion e podem
ter um delay alguns dias em relação ao Albion Online.

Desenvolvido por Ac1dTrip & Caionagyy""")
                
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send('Ocorreu um erro.')
                print(e)