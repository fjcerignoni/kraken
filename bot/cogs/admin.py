from discord import Embed, Member
from discord.ext import commands
from data_models import Servers, Permited, Roles, AlbionGuilds
from helpers import get_guild, get_guild_players

## TODO Adicionar logging

class Admin(commands.Cog):
    def __init__(self, bot:commands.Bot, god_id:str, Session) -> None:
        self.bot = bot
        self.god_id = int(god_id)
        self.Session = Session

    @commands.command()
    async def init(self, ctx:commands.Context) -> None:
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
                        
                        guild = session.query(AlbionGuilds) \
                                .filter(AlbionGuilds.server_id == ctx.guild.id) \
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

                    if guild is None:
                    
                        # ask the guild name at albion online
                        await ctx.send("Qual o nome da sua guild no albion?")
                    
                        # wait for user to respond    
                        message = await self.bot.wait_for('message', check= lambda message: 
                                                            message.author == ctx.guild.owner or \
                                                            message.author.id == self.god_id \
                                                        )

                        # fetch guild in tools4albion API based on user response
                        albion_guild = await get_guild(message.content)
                        if albion_guild is None:
                            await ctx.send("Guild não encontrada.")
                            return

                        # ask if guild name provide by the API is correct 
                        msg = await ctx.send(f"O nome da sua guild é exatamente: {albion_guild.Name} ?")
                        
                        await msg.add_reaction("\U0001F44D")
                        await msg.add_reaction("\U0001F44E")

                        # wait for user to react
                        
                        reaction, user = await self.bot.wait_for('reaction_add', check= lambda reaction, user:
                                                                    user == ctx.guild.owner or user.id == self.god_id and \
                                                                    str(reaction.emoji) in ["\U0001F44D","\U0001F44E"] \
                                                                )
                        
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
    async def give_permition(self, ctx: commands.Context, member: Member, role:str = 'moderator') -> None:
        if ctx.author == ctx.guild.owner or ctx.author.id == self.god_id: 
            async with ctx.typing():
                try:
                    with self.Session() as session:
                        db_role = session.query(Roles) \
                                   .filter(Roles.role_name == role) \
                                   .one_or_none()
                        if db_role is None:
                            await ctx.send(f'{role} não cadastrada.')
                        else:
                            permited = session.query(Servers, Permited) \
                                        .join(Permited) \
                                        .filter(Permited.member_id == member.id) \
                                        .filter(Servers.server_id == ctx.guild.id) \
                                        .one_or_none()

                            if permited is None:
                                new_permited = Permited( \
                                                member_id = member.id, \
                                                member_name = member.name, \
                                                server_id = ctx.guild.id, \
                                                role_id = db_role.role_id)
                                session.add(new_permited)
                                session.commit()
                                await ctx.send(f'Permissão concedida para {member}')
                            else:
                                await ctx.send(f'{member} ja cadastrado.')

                except Exception as e:
                    await ctx.send('Ocorreu um erro.')
                    print(e)
        else:
            await ctx.send("Você não tem permissões para executar esse comando")


    @commands.command()
    async def revoke_permition(self, ctx: commands.Context, member: Member) -> None:
        if ctx.author == ctx.guild.owner or ctx.author.id == self.god_id: 
            async with ctx.typing():
                try:
                    with self.Session() as session:
                        
                        permited = session.query(Servers, Permited) \
                                    .join(Permited) \
                                    .filter(Permited.member_id == member.id) \
                                    .filter(Servers.server_id == ctx.guild.id) \
                                    .one_or_none()

                        if permited is not None:
                            session.delete(permited.Permited)
                            session.commit()
                            await ctx.send(f'Permissão removida para {member}')
                        else:
                            await ctx.send(f'{member} não tem permissões.')

                except Exception as e:
                    await ctx.send('Ocorreu um erro.')
                    print(e)
        else:
            await ctx.send("Você não tem permissões para executar esse comando")