from pathlib import Path
from discord.ext import commands
from discord import Embed
from helpers import get_player

current_path = current_path = Path(__file__).parent.absolute()


class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def profile(self, ctx: commands.Context, *args) -> None:
        # join all arguments provided by the user to get the nickname
        nickname = ' '.join(args)
        player_data = await get_player(nickname)
        ally = player_data['AllianceName']
        guild = player_data['GuildName']
        pve_stats = player_data['LifetimeStatistics']['PvE']
        # Criando um objeto Embed com título, descrição, imagem e cor
        embed = Embed(title="> Perfil do jogador", description=f"{player_data['Name']}", color=0xFF5733)
        embed.set_thumbnail(
            url="https://render.albiononline.com/v1/spell/HASTE.png")
        # Adicionando campos com informações
        embed.add_field(name="Guild", value=f"({ally}) {guild}\n", inline=False)
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

        # Enviando o embed para o canal


        embed.set_footer(text="Desenvolvido por Ac1dTrip")

        # Enviando o embed para o canal
        await ctx.send(embed=embed)