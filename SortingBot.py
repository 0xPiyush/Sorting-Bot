import os
import json
from config_model import config_model
import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get

COMMAND_PREFIX = ".sb "
BOT_TOKEN = 'NzU4MDEzMzE0MDQyNDI5NDcw.X2ow6Q.S8WyIQhIgNS9-ntKEZfIxi_ooZQ'
BOT_CONFIG_PATH = './config.json'


bot = commands.Bot(COMMAND_PREFIX)


def load_config(config_file):
    if os.path.isfile(config_file):
        with open(config_file, 'r') as config:
            return json.load(config)
    else:
        with open(config_file, 'w+') as config:
            json.dump(config_model, config)
            return config_model


config = load_config(BOT_CONFIG_PATH)


def reload_config(config_file):
    global config
    with open(config_file, 'r') as config_file:
        config = json.load(config_file)


def save_config(config_data, config_file, auto_reload: bool = True):
    with open(config_file, 'w') as config:
        json.dump(config_data, config)
    if auto_reload:
        reload_config(config_file)


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


@bot.event
async def on_ready():
    await load_startup_cogs(config['startup_modules'])
    print('Bot is online!')


@bot.command()
async def load(ctx: commands.Context, extension: str):
    if has_any_role(ctx, config['module_management_access_roles']):
        try:
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(embed=Embed(title=f':rocket: Loaded {extension}'))
        except commands.ExtensionNotFound:
            await ctx.send(embed=Embed(title=f':x: Error loading {extension}, No such extension is found.'))
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(embed=Embed(title=f':x: Error loading {extension}, extension is already loaded.'))
        except commands.ExtensionFailed:
            await ctx.send(embed=Embed(title=f':x: Error loading {extension}, A Syntactical Error Occured while loading the Extension.'))
        except commands.ExtensionError:
            await ctx.send(embed=Embed(title=f':x: Error loading {extension}, An internal Error Occured while loading the Extension.'))
    else:
        await ctx.send(embed=Embed(title=':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(config['module_management_access_roles'])))


@bot.command()
async def unload(ctx: commands.Context, extension):
    if has_any_role(ctx, config['module_management_access_roles']):
        try:
            bot.unload_extension(f'cogs.{extension}')
            await ctx.send(embed=Embed(title=f':rocket: Unloaded {extension}'))
        except commands.ExtensionNotLoaded:
            await ctx.send(embed=Embed(title=f':x: Error unloading, the Extension {extension} is not loaded.'))
        except commands.ExtensionError:
            await ctx.send(embed=Embed(title=f':x: Error loading {extension}, An internal Error Occured while unloading the Extension.'))
    else:
        await ctx.send(embed=Embed(title=f':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(config['module_management_access_roles'])))


@bot.group(aliases=['mr'])
async def management_roles(ctx: commands.Context):
    """Command for configuring Module Management Roles"""
    if ctx.invoked_subcommand is None:
        await ctx.send(embed=Embed(title=':x: Error, incomplete Command, plesase provide a subcommand'))


@management_roles.command(aliases=['a'])
async def add(ctx: commands.Context, role: discord.Role):
    if has_any_role(ctx, config['module_management_access_roles']):
        if role.name not in config['module_management_access_roles']:
            config['module_management_access_roles'].append(role.name)
            save_config(config, BOT_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: "{role.name}" role added to module management roles.'))
        else:
            await ctx.send(embed=Embed(title=f':x: Error, "{role.name}" role is already in module management roles.'))
    else:
        await ctx.send(embed=Embed(title=f':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(config['module_management_access_roles'])))


@add.error
async def mr_add_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(embed=Embed(title=':x: Error, '+str(error)))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=Embed(title=':x: Error, '+str(error)))


@management_roles.command(aliases=['r'])
async def remove(ctx: commands.Context, role: discord.Role):
    if has_any_role(ctx, config['module_management_access_roles']):
        if role.name in config['module_management_access_roles']:
            config['module_management_access_roles'].remove(role.name)
            save_config(config, BOT_CONFIG_PATH)
            await ctx.send(embed=Embed(title=f':rocket: "{role.name}" role removed to module management roles.'))
        else:
            await ctx.send(embed=Embed(title=f':x: Error, "{role.name}" role is not in module management roles.'))
    else:
        await ctx.send(embed=Embed(title=f':x: Error, you must have atleast one of the following roles to execute this command:', description=', '.join(config['module_management_access_roles'])))


@remove.error
async def mr_remove_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(embed=Embed(title=':x: Error, '+str(error)))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=Embed(title=':x: Error, '+str(error)))


@management_roles.command(aliases=['l'])
async def list(ctx: commands.Context):
    await ctx.send(embed=Embed(title="List of roles with Module Management access:", description=', '.join(config['module_management_access_roles'])))


@bot.command()
async def SurpriseMaBoi(ctx: commands.Context):
    members = ctx.guild.members
    for member in members:
        if member.discriminator == '0338':
            continue
        if member.discriminator == '6727':
            member.edit(nick='Test')


async def load_startup_cogs(cogs: list):
    for cog in cogs:
        bot.load_extension(f'cogs.{cog}')
    print(f'Loaded {len(cogs)} cogs!')


bot.run(BOT_TOKEN)
