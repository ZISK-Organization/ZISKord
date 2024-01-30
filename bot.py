#!/usr/bin/python3
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import requests
import datetime

banTime = 300

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)


class Bot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.all()
        commands.Bot.__init__(self, command_prefix=command_prefix, setlf_bot=False, intents=intents)
        self.remove_command("help")
        self.load_commands()
        self.help_message = "Vítej na ZISKordu. Pokud chceš znát deadline, napiš do channelu !deadline. Pokud potřebuješ něco jiného, neboj se zeptat mě, nebo organizátorů.\n"
    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    def load_commands(self):
        @self.command(name="help")
        async def _help(ctx):
            message = self.help_message
            if 'Organizátor' in map(lambda x: x.name, ctx.message.author.roles):
                message += "Příkazem !forward mi můžeš napsat zprávu a channel, kde tvou zprávu za tebe vyřídím. (Navštiv channel bot-forward pro více info.)\n"
            await ctx.channel.send(content=help_message)

        @self.command(name="deadline")
        async def deadline(ctx):
            ENDPOINT = '/meta/'
            for year in range(23, 33):
                for series in range(1, 5):
                    for task in range(1, 5):
                        id = str(year) + '0' + str(series) + '0' + str(task)
                        resp = requests.get("https://api.zisk-go.com/tasks/meta?id=" + id).json()
                        if 'error' in resp:
                            await ctx.channel.send("Request on zisk server went wrong")
                            if 'Organizátor' in map(lambda x: x.name, ctx.message.author.roles):
                                await ctx.channel.send(resp['error'])
                            return
                        deadline = datetime.datetime.fromisoformat(resp['deadline'])
                        if datetime.datetime.now() < deadline:
                            await ctx.channel.send("Nejbližší deadline je: " + deadline.strftime("%d. %m. %Y v %H:%M") + ".")
                            return


        @self.command(name="forward")
        @commands.has_role('Organizátor')
        async def forward(ctx, channelName, msg):
            channel = discord.utils.get(ctx.guild.channels, name=channelName)
            if channel is None:
                await ctx.channel.send("Channel [" + channelName +"] was not found.")
            else:
                await channel.send(msg)

        @self.event
        async def on_message(message):
            await self.process_commands(message)
            ctx = await self.get_context(message)

            if message.content == "kakakah":
                # trollíme Kubu
                await ctx.channel.send("Co se to snažíš vytvořit, že to má reagovat na kakakah?")

            if ctx.channel.name.endswith('memes') or True:
                pic_ext = ['.jpg','.png','.jpeg']
                for file in message.attachments:
                    for ext in pic_ext:
                        if file.filename.endswith(ext):
                            url = 'https://api.zisk-go.com/files/uploadMeme'
                            f = await file.read()
                            resp = requests.post(url, files={file.filename: f})


bot = Bot("!")
bot.run(TOKEN)
