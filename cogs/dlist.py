import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.chat_formatting import escape_mass_mentions, italics, pagify
from enum import Enum
import aiohttp
import json
import logging

DISCORDLIST_API = 'https://bots.discordlist.net/api'

class dlist:
    """Cogs for discordlist.net"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def __unload(self):
        # pray it closes
        self.bot.loop.create_task(self.session.close())
        
    @commands.command(pass_context=True)
    async def update(self):
        payload = {
            "token": 'uGABnaqGt8',
            "servers": len(self.bot.servers)
        }
        url = "https://bots.discordlist.net/api.php"
        resp = await aiohttp.post(url, data=payload)
        resp.close()
        async with self.session.post(url, data=payload) as resp:
            await self.bot.say('DiscordList statistics'.format(resp,payload))

def setup(bot):
    n = dlist(bot)
    bot.add_cog(n)
