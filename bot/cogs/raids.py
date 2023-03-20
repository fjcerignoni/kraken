from discord import Embed
from discord.ext import commands
from data_models import Servers, Permited
from helpers import get_raid_templates, save_raid_templates

import json

class Raids(commands.Cog):
    def __init__(self, bot:commands.Bot, god_id:int, Session: dict) -> None:
        self.bot = bot
        self.god_id = int(god_id)
        self.Session = Session

        self.reaction_list = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9", 
                              "\U0001F1EA", "\U0001F1EB", "\U0001F1EC", "\U0001F1ED", 
                              "\U0001F1EE",  "\U0001F1F0","\U0001F1F1", "\U0001F1F2", 
                              "\U0001F1F3", "\U0001F1F4", "\U0001F1F5", "\U0001F1F6", 
                              "\U0001F1F7", "\U0001F1F8", "\U0001F1F9", "\U0001F1FA" ] # J: "\U0001F1EF"

    async def get_permitions(self, server:str) -> list:
        with self.Session() as session:
            perms = session.query(Permited) \
                    .join(Servers) \
                    .filter(Servers.server_id == server) \
                    .filter(Permited.role_id >= 2) \
                    .all()
        return [perm.member_id for perm in perms]

    @commands.command()
    async def organize_raid(self, ctx: commands.Context, template: str, date: str, description: str) -> None:
        """
            <template> <date> "<description[;]>"

            This command helps to organize a raid. 
            
            The list of roles will appear based on the templates,
            The users should apply to the roles using the emoticon list.

            The command showd have a date in DD/MM/YYYY format and some description inside double quotes.
            You can use ';' to beak lines in the description.
            
            The available templates are availabe in $raid_templates

            The user need moderation permition to run this command.
        """
        # Check if author is in the database:
        permited = await self.get_permitions(ctx.guild.id)

        if ctx.author == ctx.guild.owner or ctx.author.id == self.god_id or ctx.author.id in permited:

            templates = await get_raid_templates(ctx.guild.id)

            if templates and template in templates.keys():

                reaction_list = self.reaction_list[:len(templates[template])]

                embed_body = ''.join(f"{reaction} - {role}: \n" for reaction,role in zip(reaction_list, templates[template]))
                embed = Embed(title=f'> {template.upper()}', description=date)
                embed.add_field(name='> Informações', value=description.replace(';','\n'), inline=False)
                embed.add_field(name='> Vagas', value=embed_body, inline=False)              
                embed.set_footer(text="Raid Organizer desenvolvido por Ac1dTrip")
                
                msg = await ctx.send(embed=embed)
                for reaction in reaction_list:
                    await msg.add_reaction(reaction)

            else:
                embed = Embed(title='Erro', description='Template Inválido')
                embed.add_field(name='Templates disponíveis', value=embed_body)
                embed.set_footer(text="Raid Organizer desenvolvido por Ac1dTrip")
                await ctx.send(embed=embed)    
        else:
            await ctx.send("Você não tem permissões para executar esse comando")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:object ) -> None:
        # while True:
            try:
                payload = await self.bot.wait_for('raw_reaction_add', check=lambda payload: payload.emoji.name in self.reaction_list)
                channel = await self.bot.fetch_channel(payload.channel_id)
                
                msg = await channel.fetch_message(payload.message_id)

                if payload.member == self.bot.user:
                    return

                content = msg.embeds[0].fields[1].value.split('\n')
                content[self.reaction_list.index(payload.emoji.name)] += f'<@!{payload.user_id}>  '

                new_value = ''.join(f"{el}\n" for el in content)
                update = msg.embeds[0].set_field_at(index=1, name='Vagas', value=new_value, inline=False)
                
                await msg.edit(embed=update)
                # break

            except Exception as e:
                print(e)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload:object) -> None:

        # while True:
            try:
                payload = await self.bot.wait_for('raw_reaction_remove', check=lambda payload: payload.emoji.name in self.reaction_list)
                channel = await self.bot.fetch_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)

                if payload.member == self.bot.user:
                    return

                content = msg.embeds[0].fields[1].value.split('\n')
                content[self.reaction_list.index(payload.emoji.name)] = content[self.reaction_list.index(payload.emoji.name)] \
                                                                    .replace(f' <@!{payload.user_id}>' , '')
                
                new_value = ''.join(f"{el}\n" for el in content)
                update = msg.embeds[0].set_field_at(index=1, name='Vagas', value=new_value, inline=False)
                await msg.edit(embed=update)
                
                # break
            except Exception as e:
                print(e)

    @commands.command()
    async def raid_templates(self, ctx:commands.Context) -> None:
        templates = await get_raid_templates(ctx.guild.id)
        if templates:

            embed = Embed(title='> Templates', description='Templates disponíveis para o comando $organize_raid')
            for key in templates:
                embed.add_field(name=f'> {key}', value=f'```{json.dumps(templates[key], sort_keys=True, indent=2)}```', inline=False)
            embed.set_footer(text="Raid Organizer desenvolvido por Ac1dTrip")
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Erro', description='Não foi possível realizar o comando.\n\nTente executar o comando:\n$create_raid_template <template>')
            embed.set_footer(text="Raid Organizer desenvolvido por Ac1dTrip")
            await ctx.send(embed=embed)

    @commands.command()
    async def create_raid_template(self, ctx:commands.Context, new_template:str) -> None:
        permited = await self.get_permitions(ctx.guild.id)

        async with ctx.typing():
            if ctx.author == ctx.guild.owner or ctx.author.id == self.god_id or ctx.author.id in permited:
                templates = await get_raid_templates(ctx.guild.id)

                if templates and new_template in templates:
                    await ctx.send("Template já existe")
                else:
                    
                    msg = await ctx.send(f'Atenção!\nTem certeza que você quer criar o template {new_template}?')

                    await msg.add_reaction("\U0001F44D")
                    await msg.add_reaction("\U0001F44E")

                    reaction, user = await self.bot.wait_for('reaction_add', check= lambda reaction, user: \
                                                                user == ctx.guild.owner or
                                                                user.id == self.god_id or
                                                                user.id in permited and 
                                                                str(reaction.emoji) in ["\U0001F44D","\U0001F44E"] \
                                                            )

                    if str(reaction.emoji) == "\U0001F44D":
                        await ctx.send("Qual a composição do novo template?")

                        message = await self.bot.wait_for('message', check= lambda message: \
                                                            message.author == ctx.guild.owner or
                                                            message.author.id == self.god_id or
                                                            message.author.id in permited
                                                        )
                        
                        try:
                            if templates is None:
                                await save_raid_templates(ctx.guild.id, json.loads(f'{{"{new_template}":{message.content}}}'))

                            else:
                                templates[new_template] = json.loads(message.content)
                                await save_raid_templates(ctx.guild.id, templates)
                           
                            await ctx.send("Operação concluida com sucesso.")

                        except Exception as e:
                            print(e)
                            await ctx.send("O template deve ser uma lista (array)")
                    else:
                        await ctx.send("Operação Cancelada")     
            else:
                await ctx.send("Você não tem permissões para executar esse comando")


    @commands.command()
    async def update_raid_template(self, ctx:commands.Context, template_name:str) -> None:
        permited = await self.get_permitions(ctx.guild.id)

        async with ctx.typing():
            if ctx.author == ctx.guild.owner or ctx.author.id == self.god_id or ctx.author.id in permited:
                
                templates = await get_raid_templates(ctx.guild.id)

                if templates and template_name in templates:
                    
                    template = templates[template_name]
                    embed = Embed(title=f'> {template_name}', description='')
                    embed.add_field(name='', value=f'```{json.dumps(template, sort_keys=True, indent=2)}```', inline=False)
                    embed.add_field(name='Atenção!', value=f'Tem certeza que você quer atualizar o template {template_name}?')
                    
                    msg = await ctx.send(embed=embed)

                    await msg.add_reaction("\U0001F44D")
                    await msg.add_reaction("\U0001F44E")

                    reaction, user = await self.bot.wait_for('reaction_add', check= lambda reaction, user: \
                                                                user == ctx.guild.owner or
                                                                user.id == self.god_id or
                                                                user.id in permited and 
                                                                str(reaction.emoji) in ["\U0001F44D","\U0001F44E"] \
                                                            )

                    if str(reaction.emoji) == "\U0001F44D":
                        await ctx.send("Qual o novo template?")

                        message = await self.bot.wait_for('message', check= lambda message: \
                                                            message.author == ctx.guild.owner or
                                                            message.author.id == self.god_id or
                                                            message.author.id in permited
                                                        )
                        
                        try:
                            input_template = json.loads(message.content)
                            templates[template_name] = input_template

                            await save_raid_templates(ctx.guild.id, templates)
                            
                            await ctx.send("Operação concluida com sucesso.")

                        except Exception as e:
                            print(e)
                            await ctx.send("O template deve ser uma lista (array)")
                    else:
                        await ctx.send("Operação Cancelada")     
                else:
                    await ctx.send("Erro ao carregar o template")
            else:
                await ctx.send("Você não tem permissões para executar esse comando")

    @commands.command()
    async def delete_raid_template(self, ctx:commands.Context, del_template:str) -> None:
        permited = await self.get_permitions(ctx.guild.id)

        async with ctx.typing():
            if ctx.author == ctx.guild.owner or ctx.author.id == self.god_id or ctx.author.id in permited:
                templates = await get_raid_templates(ctx.guild.id)
                if templates and not del_template in templates:
                    await ctx.send("Template não existe")
                else:
                    
                    template = templates[del_template]
                    embed = Embed(title=f'> {del_template}', description='')
                    embed.add_field(name='', value=f'```{json.dumps(template, sort_keys=True, indent=2)}```', inline=False)
                    embed.add_field(name='Atenção!', value=f'Tem certeza que você quer deletar o template {del_template}?')

                    msg = await ctx.send(embed=embed)

                    await msg.add_reaction("\U0001F44D")
                    await msg.add_reaction("\U0001F44E")

                    reaction, user = await self.bot.wait_for('reaction_add', check= lambda reaction, user: \
                                                                user == ctx.guild.owner or
                                                                user.id == self.god_id or
                                                                user.id in permited and 
                                                                str(reaction.emoji) in ["\U0001F44D","\U0001F44E"] \
                                                            )

                    if str(reaction.emoji) == "\U0001F44D":                        
                        try:
                            del templates[del_template]

                            await save_raid_templates(ctx.guild.id,templates)
                            
                            await ctx.send("Operação concluida com sucesso.")

                        except Exception as e:
                            print(e)
                    else:
                        await ctx.send("Operação Cancelada")     
            else:
                await ctx.send("Você não tem permissões para executar esse comando")