from discord import Embed
from discord.ext import commands
from data_models import Servers, AlbionGuilds
from helpers import get_guild, get_guild_players

## TODO Adicionar logging

class Admin(commands.Cog):
    def __init__(self, bot, Session):
        self.bot = bot
        self.Session = Session
        self.god_id = 329761865766928385

    @commands.command()
    async def init(self, ctx):
        """
            Saves server and guild informations in the database
        """
        async with ctx.typing():
            if ctx.author == ctx.guild.owner or ctx.author.id == self.god_id:
                
                try:
                    # test if server already exists in the database
                    with self.Session() as session:
                        server = session.query(Servers) \
                                .filter(Servers.server_id == ctx.guild.id) \
                                .one_or_none()

                        # if server not exists then create record in the database
                        if server is None:
                            new_server = Servers(server_id = ctx.guild.id, \
                                                server_name = ctx.guild.name, \
                                                owner_id = ctx.guild.owner.id, \
                                                owner_name = ctx.guild.owner.name) \

                            session.add(new_server)
                            session.commit()
                            await ctx.send(f"{ctx.guild.name} iniciado com sucesso.")

                        else:
                            await ctx.send(f"{ctx.guild.name} já foi iniciado.")
                    
                    # ask the guild name at albion online
                    await ctx.send("Qual o nome da sua guild no albion?")

                    # function to check message response
                    def check_message(message):
                        return message.author == ctx.guild.owner or message.author.id == self.god_id
                   
                    # wait for user to respond    
                    message = await self.bot.wait_for('message', check=check_message)

                    # fetch guild in tools4albion API based on user response
                    albion_guild = await get_guild(message.content)
                    if albion_guild is None:
                        await ctx.send("Guild não encontrada.")
                        return

                    # ask if guild name provide by the API is correct 
                    msg = await ctx.send(f"O nome da sua guild é exatamente: {albion_guild.Name} ?")
                    await msg.add_reaction("\U0001F44D")
                    await msg.add_reaction("\U0001F44E")

                    # function to check reaction response
                    def check_reaction(reaction, user):
                        return (user == ctx.guild.owner or user.id == self.god_id) and str(reaction.emoji) in ["\U0001F44D","\U0001F44E"]

                    # wait for user to react
                    reaction, user = await self.bot.wait_for('reaction_add', check=check_reaction)
                    
                    if str(reaction.emoji) == "\U0001F44D":
                        # check if guild already exists in the database
                        with self.Session() as session:
                            db_guild = session.query(AlbionGuilds) \
                                        .filter(AlbionGuilds.guild_id == albion_guild.Id) \
                                        .one_or_none()

                            # if not exists then create record in the database
                            if db_guild is None:
                                new_guild = AlbionGuilds(guild_id = albion_guild.Id, \
                                                            guild_name = albion_guild.Name, \
                                                            server_id = ctx.guild.id)
                                session.add(new_guild)
                                session.commit()

                                await ctx.send("Guild cadastrada com sucesso.")
                            else:
                                await ctx.send(f'A {db_guild.guild_name} já foi cadastrada por outro servidor')
                    else:
                        await ctx.send(f"Operação cancelada.")

                except Exception as e:
                    await ctx.send("Ocorreu um erro.")
                    print(e)
            else:
                await ctx.send("Você não tem permissões para executar esse comando")

    @commands.command()
    async def check_players(self, ctx):
        try:
        # fectch guild info in the database
            with self.Session() as session:
                guild = session.query(AlbionGuilds) \
                        .filter(AlbionGuilds.server_id == ctx.guild.id) \
                        .one_or_none()

            # create list with players name consulting tools4albion API and sort
            players = [player.Name for player in await get_guild_players(guild.guild_id)]
            players.sort()

            # create chunks to better display the information in discord embed
            chunk_size= int(len(players) / 3)
            chunk=[players[i:i + chunk_size] for i in range(0, len(players), chunk_size)]

            column1 = ''.join(f'{player}\n' for player in chunk[0])
            column2 = ''.join(f'{player}\n' for player in chunk[1])
            column3 = ''.join(f'{player}\n' for player in chunk[2])

            # crate embed
            embed = Embed(
                title=f'Jogadores da {guild.guild_name}',
                description=f'Atualmente temos {len(players)} ativos na guild.'
            )
            
            embed.add_field(name="Jogadores", value=column1, inline=True)
            embed.add_field(name="Jogadores", value=column2, inline=True)
            embed.add_field(name="Jogadores", value=column3, inline=True)
            embed.set_footer(text="""
    Esta lista é carregada do projeto tools4albion e pode
    ter um delay de 2 dias em relação ao Albion Online.
    Desenvolvido por Ac1dTrip""")
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send('Ocorreu um erro.')
            print(e)
    
    @commands.command()
    async def check_active_players(self, ctx):
        try:
        # fectch guild info in the database
            with self.Session() as session:
                guild = session.query(AlbionGuilds) \
                        .filter(AlbionGuilds.server_id == ctx.guild.id) \
                        .one_or_none()

            # create list with players name consulting tools4albion API and sort
            players = [player.Name for player in await get_guild_players(guild.guild_id)]
            players.sort()

            members = [member.nick for member in ctx.guild.members if not member.nick is None]
        
            members.sort()

            print(members)
        
        except Exception as e:
            await ctx.send('Ocorreu um erro.')
            print(e)
