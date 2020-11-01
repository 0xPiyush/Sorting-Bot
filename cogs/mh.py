from discord.ext import commands
from discord import Embed
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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

    @mh.command(aliases=['reg'])
    async def register(self, ctx: commands.Context, ign: str):
        if ctx.author.discriminator in self.sheet.col_values(2)[1:]:
            ctx.send(embed=Embed(
                title=f':x: {ctx.author.name} is already registered for the Minecraft Manhunt.'))
            return None

        row = [ctx.author.name, ctx.author.discriminator, ign]

        self.sheet.append_row(row)


def setup(Bot):
    Bot.add_cog(au(Bot))
