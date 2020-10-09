import random
import json
import os
from re import error
import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get

au_config_model = {
    'blacklist': [],
    'public_commands_access_roles': [],
    'public_commands_channels': [],
    'management_commands_channels': [],
    'management_commands_access_roles': [],
}

AU_CONFIG_PATH = './au_config.json'


def role_exists(ctx: commands.Context, role):
    if get(ctx.guild.roles, name=role):
        return True
    return False


def has_any_role(ctx: commands.Context, roles: list):
    if len(roles) == 0:
        return True
    author_roles = ctx.message.author.roles
    for role in author_roles:
        if role.name in roles:
            return True
    return False


class au(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot
        self.session_running = False
        self.que = []
        self.running_que = []
        self.session_blacklist = []

        self.code = ''
        self.region = ''

        global AU_CONFIG_PATH
        self.config = self.load_au_config(AU_CONFIG_PATH)

    def load_au_config(self, config_path):
        if os.path.isfile(config_path):
            with open(config_path, 'r') as config:
                return json.load(config)
        else:
            with open(config_path, 'w+') as config:
                json.dump(au_config_model, config)
                return au_config_model

    def save_config(self, config_data, config_file, auto_reload: bool = True):
        with open(config_file, 'w') as config:
            json.dump(config_data, config)
        if auto_reload:
            self.reload_config(config_file)

    def reload_config(self, config_file):
        with open(config_file, 'r') as config_file:
            self.config = json.load(config_file)

    @commands.group(aliases=['amongus', 'among_us'])
    async def au(self, ctx: commands.Context):
        """Command to manage and create Among Us Games."""
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=Embed(title=':x: Error, incomplete Command, plesase provide a subcommand'))

    @au.command(aliases=['start'])
    async def start_session(self, ctx: commands.Context):
        if has_any_role(ctx, self.config['management_commands_access_roles']):
            if not self.session_running:
                self.session_running = True
                await ctx.send(embed=Embed(title=f':rocket: Among Us Session started successfully.'))
            else:
                await ctx.send(embed=Embed(title=f':x: Error Among Us Session is already running.'))
        else:
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))

    @au.command(aliases=['stop'])
    async def stop_session(self, ctx: commands.Context):
        if has_any_role(ctx, self.config['management_commands_access_roles']):
            if self.session_running:
                self.session_running = False
                self.session_blacklist.clear()
                self.que.clear()
                self.running_que.clear()
                self.code = ''
                self.region = ''
                await ctx.send(embed=Embed(title=':rocket: Among Us session stopped, Que and Session blacklists reset.'))
            else:
                await ctx.send(embed=Embed(title=':x: No Among Us sessions are currently running.'))
        else:
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))

    @au.command(aliases=['reg'])
    async def register(self, ctx: commands.Context):
        if has_any_role(ctx, self.config['public_commands_access_roles']):
            if self.session_running:
                member = ctx.author
                if member in self.session_blacklist:
                    await ctx.send(embed=Embed(title=f':x: {member.name} is banned for registering for the session.'))
                    return None
                if member not in self.config['blacklist']:
                    if member not in self.que:
                        self.que.append(member)
                        self.running_que.append(member)
                        await ctx.send(embed=Embed(title=f':rocket: {member.name} registered for the session.'))
                    else:
                        await ctx.send(embed=Embed(title=f':x: {member.name} is already registered for the session.'))
                else:
                    await ctx.send(embed=Embed(title=f':x: {member.name} is banned from registering for Among Us games.'))
            else:
                await ctx.send(embed=Embed(title=':x: No Among Us sessions are running now.'))
        else:
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['public_commands_access_roles'])))

    @au.command(aliases=['sbl'])
    async def session_blacklist(self, ctx: commands.Context, member: discord.Member):
        if has_any_role(ctx, self.config['management_commands_access_roles']):
            if not self.session_running:
                await ctx.send(embed=Embed(title=':x: No Among Us sessions are currently running.'))
            if member in self.config['blacklist']:
                await ctx.send(embed=Embed(title=f':x: Error {member} is already permanently blacklisted.'))
                return None
            if member not in self.session_blacklist:
                self.session_blacklist.append(member)
                await ctx.send(embed=Embed(title=f':rocket: {member} blacklisted for the session.'))
            else:
                await ctx.send(embed=Embed(title=f':x: Error {member} is already blacklisted for the session.'))
        else:
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))

    @au.command(aliases=['subl'])
    async def session_unblacklist(self, ctx: commands.Context, member: discord.Member):
        if has_any_role(ctx, self.config['management_commands_access_roles']):
            if not self.session_running:
                await ctx.send(embed=Embed(title=':x: No Among Us sessions are currently running.'))
            if member not in self.session_blacklist:
                await ctx.send(embed=Embed(title=f':x: Error {member} is not session blacklisted.'))
            else:
                self.session_blacklist.remove(member)
                await ctx.send(embed=Embed(title=f':rocket: {member} removed from session blacklist.'))
        else:
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))

    @au.command(aliases=['bl'])
    async def blacklist(self, ctx: commands.Context, member: discord.Member):
        if has_any_role(ctx, self.config['management_commands_access_roles']):
            if not self.session_running:
                await ctx.send(embed=Embed(title=':x: No Among Us sessions are currently running.'))
            if member in self.session_blacklist:
                await ctx.send(embed=Embed(title=f':x: Error {member} is already blacklisted for the session.'))
                return None
            if member not in self.config['blacklist']:
                self.config['blacklist'].append(member)
                self.save_config(self.config, AU_CONFIG_PATH)
                await ctx.send(embed=Embed(title=f':rocket: {member} added to permanent blacklist.'))
            else:
                await ctx.send(embed=Embed(title=f':x: Error {member} is already permanently blacklisted.'))
        else:
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))

    @au.command(aliases=['ubl'])
    async def unblacklist(self, ctx: commands.Context, member: discord.Member):
        if has_any_role(ctx, self.config['management_commands_access_roles']):
            if not self.session_running:
                await ctx.send(embed=Embed(title=':x: No Among Us sessions are currently running.'))
            if member not in self.config['blacklist']:
                await ctx.send(embed=Embed(title=f':x: {member} is not permanently blacklisted.'))
            else:
                self.config['blacklist'].remove(member)
                self.save_config(self.config, AU_CONFIG_PATH)
                await ctx.send(embed=Embed(title=f':rocket: {member} is removed from permanent blacklist.'))
        else:
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))

    @au.command(aliases=['p'])
    async def pick(self, ctx: commands.Context, code: str, server: str, number=9):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        if not self.session_running:
            await ctx.send(embed=Embed(title=':x: No Among Us sessions are currently running.'))

        if len(self.running_que) < number:
            await ctx.send(embed=Embed(title=f':x: Error cannot pick {number} players out of the {len(self.running_que)} registered players.'))
            return None
        picked_members = random.sample(self.running_que, number)
        self.running_que = [
            member for member in self.running_que if member not in picked_members]

        embed = Embed(
            title=f':tada: Congratulations, You have been selected you play Among Us in this round :tada:')
        embed.add_field(
            name='Click below to reveal the Code', value=f'||{code}||')
        embed.add_field(
            name='Click below to reveal the Server', value=f'||{server}||')

        for _member in picked_members:
            await _member.send(embed=embed)

        await ctx.send(embed=Embed(title=f':rocket: {number} player(s) picked:', description='\n'.join([member.name for member in picked_members])))

    @au.command(aliases=['pm'])
    async def pick_member(self, ctx: commands.Context, code: str, server: str, member: discord.Member):
        if member not in self.que:
            await ctx.send(embed=Embed(title=f':x: Could not pick {member}, didn\'t registered.'))
            return None
        if member not in self.running_que:
            await ctx.send(embed=Embed(title=f':x: {member} is already picked for the game.'))
            return None
        if member in self.running_que:
            embed = Embed(
                title=f':tada: Congratulations, You have been selected you play Among Us in this round :tada:')
            embed.add_field(
                name='Click below to reveal the Code', value=f'||{code}||')
            embed.add_field(
                name='Click below to reveal the Region', value=f'||{server}||')
            await member.send(embed=embed)
            await ctx.send(embed=Embed(title=f':rocket: code and region sent to {member}'))
            self.running_que.remove(member)

    @pick_member.error
    async def pick_member_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title=f':x: Could not find that member.'))

    @au.command(aliases=['lr'])
    async def list_registered(self, ctx: commands.Context):
        if not self.session_running:
            await ctx.send(embed=Embed(title=':x: No Among Us sessions are running now.'))
            return None
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        await ctx.send(embed=Embed(title='The list of players who have registered for the session:', description='\n'.join([member.name for member in self.que])))

    @au.command(aliases=['lp'])
    async def list_played(self, ctx: commands.Context):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        played = [
            member for member in self.que if member not in self.running_que]

        await ctx.send(embed=Embed(title='The list of players who have already played in a round:', description='\n'.join([player.name for player in played])))

    @au.group(aliases=['pcc'])
    async def public_commands_channels(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=Embed(title=':x: Error, incomplete Command, plesase provide a subcommand'))

    @public_commands_channels.command(aliases=['add', 'a'])
    async def add_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        try:
            if channel in self.config['public_commands_channels']:
                await ctx.send(embed=Embed(title=f':x: Error adding "{channel.name}", the channel is already present in the list of channels that the bod is listening for public commands.'))
                return None
            self.config['public_commands_channels'].append(channel)
            self.save_config(self.config, AU_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: {channel.name} added to the list of channels that the bot is listening for public commands.'))
        except commands.ChannelNotFound:
            await ctx.send(embed=Embed(title=f':x: Error adding "{channel.name}", no such channel exists in the guild.'))

    @public_commands_channels.command(aliases=['remove', 'r'])
    async def remove_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        try:
            if channel not in self.config['public_commands_channels']:
                await ctx.send(embed=Embed(title=f':x: Error removing "{channel.name}", the channel is not present in the list of channels that the bod is listening for public commands.'))
                return None
            self.config['public_commands_channels'].remove(channel)
            self.save_config(self.config, AU_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: {channel.name} removed to the list of channels that the bot is listening for public commands.'))
        except commands.ChannelNotFound:
            await ctx.send(embed=Embed(title=f':x: Error removing "{channel.name}", no such channel exists in the guild.'))

    @au.group(aliases=['mcc'])
    async def management_commands_channel(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=Embed(title=':x: Error, incomplete Command, plesase provide a subcommand'))

    @management_commands_channel.command(aliases=['add', 'a'])
    async def add_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        try:
            self.config['management_commands_channels'].append(channel)
            self.save_config(self.config, AU_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: {channel.name} added to the list of channels that the bot is listening for management commands.'))
        except commands.ChannelNotFound:
            await ctx.send(embed=Embed(title=f':x: Error adding "{channel.name}", no such channel exists in the guild.'))

    @management_commands_channel.command(aliases=['remove', 'r'])
    async def remove_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        try:
            if channel not in self.config['management_commands_channels']:
                await ctx.send(embed=Embed(title=f':x: Error removing "{channel.name}", the channel is not present in the list of channels that the bod is listening for management commands.'))
                return None
            self.config['management_commands_channels'].remove(channel)
            self.save_config(self.config, AU_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: {channel.name} removed to the list of channels that the bot is listening for management commands.'))
        except commands.ChannelNotFound:
            await ctx.send(embed=Embed(title=f':x: Error removing "{channel.name}", no such channel exists in the guild.'))

    @au.group(aliases=['mr'])
    async def management_roles(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=Embed(title=':x: Error, incomplete Command, plesase provide a subcommand'))

    @management_roles.command(aliases=['a'])
    async def add(self, ctx: commands.Context, role: discord.Role):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        if role.name not in self.config['management_commands_access_roles']:
            self.config['management_commands_access_roles'].append(role.name)
            self.save_config(self.config, AU_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: "{role.name}" role added to AU management roles.'))
        else:
            await ctx.send(embed=Embed(title=f':x: Error, "{role.name}" role is already in AU management roles.'))

    @management_roles.command(aliases=['r'])
    async def remove(self, ctx: commands.Context, role: discord.Role):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        if role.name in self.config['management_commands_access_roles']:
            self.config['management_commands_access_roles'].remove(role.name)
            self.save_config(self.config, AU_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: "{role.name}" role removed from AU management roles.'))
        else:
            await ctx.send(embed=Embed(title=f':x: Error, "{role.name}" role is not in AU management roles.'))

    @au.group(aliases=['pr'])
    async def public_roles(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=Embed(title=':x: Error, incomplete Command, plesase provide a subcommand'))

    @public_roles.command(aliases=['a'])
    async def add(self, ctx: commands.Context, role: discord.Role):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        if role.name not in self.config['public_commands_access_roles']:
            self.config['public_commands_access_roles'].append(role.name)
            self.save_config(self.config, AU_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: "{role.name}" role added to public commands access roles.'))
        else:
            await ctx.send(embed=Embed(title=f':x: Error, "{role.name}" role is already in public commands access roles.'))

    @public_roles.command(aliases=['r'])
    async def remove(self, ctx: commands.Context, role: discord.Role):
        if not has_any_role(ctx, self.config['management_commands_access_roles']):
            await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(self.config['management_commands_access_roles'])))
            return None
        if role.name in self.config['public_commands_access_roles']:
            self.config['public_commands_access_roles'].remove(role.name)
            self.save_config(self.config, AU_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: "{role.name}" role removed from public commands access roles.'))
        else:
            await ctx.send(embed=Embed(title=f':x: Error, "{role.name}" role is not in public commands access roles.'))


def setup(Bot):
    Bot.add_cog(au(Bot))
