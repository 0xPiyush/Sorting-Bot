from functools import update_wrapper
from discord import player
from discord.ext import commands
from discord import Embed
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from mojang_api import Player


class mh(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

        self.scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                      "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            'cogs/GoogleSheetsCreds.json', self.scope)

        self.client = gspread.authorize(self.creds)

        self.sheet = self.client.open_by_key(
            '13bnby_zhIR22KvMzfDtOBt9e-goD8-ORZ0FMIynbriY').sheet1

    @commands.group(aliases=['manhunt'])
    async def mh(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=Embed(title=':x: Error, incomplete Command, plesase provide a subcommand'))

    @mh.command(aliases=['reg', 'r'])
    async def register(self, ctx: commands.Context, ign: str):
        if ctx.author.discriminator in self.sheet.col_values(2):
            await ctx.send(embed=Embed(
                title=f':x: {ctx.author.name} is already registered for the Minecraft Manhunt.'))
            return None

        reg_ign = ign
        if reg_ign[0] == '\\':
            reg_ign = reg_ign[1:]

        if not self.ignValid(reg_ign):
            await ctx.send(embed=Embed(title=f':x: Could not register the IGN: "{ign}", no such Minecraft Account found.'))
            return None

        row = [ctx.author.name, ctx.author.discriminator, reg_ign]

        self.sheet.append_row(row)
        await ctx.send(embed=Embed(
            title=f':rocket: {ctx.author.name} registered for the Minecraft Manhunt with IGN: "{ign}"'))

    @mh.command(aliases=['upd', 'u'])
    async def update(self, ctx: commands.Context, ign: str):
        if ctx.author.discriminator not in self.sheet.col_values(2):
            await ctx.send(embed=Embed(
                title=f':x: {ctx.author.name} is not registered for the Minecraft Manhunt. Cannot update IGN without registering.'))
            return None

        reg_ign = ign
        if reg_ign[0] == '\\':
            reg_ign = reg_ign[1:]

        if not self.ignValid(reg_ign):
            await ctx.send(embed=Embed(title=f':x: Could not register the IGN: "{ign}", no such Minecraft Account found.'))
            return None

        row_num = self.sheet.col_values(2).index(ctx.author.discriminator) + 1

        self.sheet.update_cell(row_num, 3, reg_ign)
        await ctx.send(embed=Embed(
            title=f':rocket: {ctx.author.name}\'s registered IGN updated to "{ign}"'))

    @mh.command(aliases=['ur', 'ureg'])
    async def unregister(self, ctx: commands.Context):
        if ctx.author.discriminator not in self.sheet.col_values(2):
            await ctx.send(embed=Embed(
                title=f':x: {ctx.author.name} is not registered for the Minecraft Manhunt. Cannot Unregister without registering.'))
            return None

        row_num = self.sheet.col_values(2).index(ctx.author.discriminator) + 1

        self.sheet.delete_row(row_num)
        await ctx.send(embed=Embed(
            title=f':rocket: {ctx.author.name} Unregisterd from the Minecraft Manhunt.'))

    def ignValid(self, ign: str):
        try:
            player = Player(ign)
            return True
        except Exception:
            return False


def setup(Bot):
    Bot.add_cog(mh(Bot))
