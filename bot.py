#!/usr/bin/python3
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time

banTime = 300

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)



class Bot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.all()
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=False, intents=intents)
        self.remove_command("help")
        self.load_commands()
        self.help_message = "TODO"

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    def load_commands(self):
        @self.command(name="help")
        async def _help(ctx):
            await ctx.channel.send(content=self.help_message)

        @self.command(name="forward")
        @commands.has_role('Organizátor')
        async def forward(ctx, channelName, msg):
            channel = discord.utils.get(ctx.guild.channels, name=channelName)
            if channel is None:
                await ctx.channel.send("Channel [" + channelName +"] was not found.")
            else:
                await channel.send(msg)


bot = Bot("!")
bot.run(TOKEN)
