import json
from pathlib import Path
from turtle import title
from discord import Embed
from discord.ext import commands
from data_models import Permited

current_path = current_path = Path(__file__).parent.absolute()

class Raids(commands.Cog):
    def __init__(self, bot:commands.Bot, god_id:int, Session: object, reaction_list: list[str]) -> None:
        self.bot = bot
        self.god_id = god_id
        self.Session = Session
        self.reaction_list = reaction_list

    @commands.command()
    async def organize_raid_help(self, ctx: commands.Context) -> None:
        with open(current_path / 'raids_template.json', 'r') as file:
            templates = json.load(file)
        
        description = """
$organize_raid <content> <date> <description>

O comando $organize_raid serve para auxiliar a guild montar uma party para algum conteúdo
        """
        template = ''.join(f"{template}\n" for template in templates.keys())
        params = """
<content> : define a composição das vagas de acordo com os templates disponíveis.
<date> : data no formato DD/MM/AAAA.
<description> : descrição extra para o conteúdo, como horario, IP, montaria, etc. Utilize ';' para quebrar linha.        
        """
        
        embed = Embed(title="ORGANIZE RAID HELP", description=description)
        embed.add_field(name="Parametros", value=params, inline=False)
        embed.add_field(name="Templates", value=template, inline=False)
        embed.set_footer(text="Raid Organizer desenvolvido por Ac1dTrip.")

        await ctx.send(embed=embed)


    @commands.command()
    async def organize_raid(self, ctx: commands.Context, r_type: str, r_date: str, r_details: str) -> None:
        
        # Check if author is in the database:
        with self.Session() as session:
            perms = session.query(Permited).filter(Permited.role_id >= 2).all()
            permited = [perm.member_id for perm in perms]

        if ctx.author == ctx.guild.owner or ctx.author.id == self.god_id or ctx.author.id in permited:
            
            with open(current_path / 'raids_template.json', 'r') as file:
                templates = json.load(file)

            if r_type in templates.keys():

                reaction_list = self.reaction_list[:len(templates[r_type])]

                embed_body = ''.join(f"{reaction} - {role} ;\n" for reaction,role in zip(reaction_list, templates[r_type]))

                embed = Embed(title=r_type.upper(), description=r_date)
                embed.add_field(name='Informações', value=r_details.replace(';','\n'), inline=False)
                embed.add_field(name='Vagas', value=embed_body, inline=False)              
                embed.set_footer(text="Raid Organizer desenvolvido por Ac1dTrip.")
                msg = await ctx.send(embed=embed)
                for reaction in reaction_list:
                    await msg.add_reaction(reaction)
                print(msg.id)

            else:
                embed_body = ''.join(f"{template}\n" for template in templates.keys())
                embed = Embed(title='Erro', description='Template Inválido')
                embed.add_field(name='Templates disponíveis', value=embed_body)
                embed.set_footer(text="Raid Organizer desenvolvido por Ac1dTrip.")
                await ctx.send(embed=embed)    
        else:
            await ctx.send("Você não tem permissões para executar esse comando")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:object ) -> None:
        while True:
            try:
                payload = await self.bot.wait_for('raw_reaction_add', check=lambda payload: payload.emoji.name in self.reaction_list)
                channel = await self.bot.fetch_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)

                if payload.member == self.bot.user:
                    return

                content = msg.embeds[0].fields[1].value.split('\n')
                content[self.reaction_list.index(payload.emoji.name)] = content[self.reaction_list.index(payload.emoji.name)] \
                                                                    .replace(';', f': <@!{payload.user_id}>')
                
                new_value = ''.join(f"{el}\n" for el in content)
                update = msg.embeds[0].set_field_at(index=1, name='Vagas', value=new_value, inline=False)

                await msg.edit(embed=update)
            
            except Exception as e:
                print(e)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload:object) -> None:

        while True:
            try:
                payload = await self.bot.wait_for('raw_reaction_remove', check=lambda payload: payload.emoji.name in self.reaction_list)
                channel = await self.bot.fetch_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)

                if payload.member == self.bot.user:
                    return

                content = msg.embeds[0].fields[1].value.split('\n')
                content[self.reaction_list.index(payload.emoji.name)] = content[self.reaction_list.index(payload.emoji.name)] \
                                                                    .replace(f': <@!{payload.user_id}>', ';')
                
                new_value = ''.join(f"{el}\n" for el in content)
                update = msg.embeds[0].set_field_at(index=1, name='Vagas', value=new_value, inline=False)
                await msg.edit(embed=update)
            except Exception as e:
                print(e)