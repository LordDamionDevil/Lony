import discord
from discord.ext import commands
from .utils.chat_formatting import escape_mass_mentions, italics, pagify
from random import randint
from random import choice
from enum import Enum
from urllib.parse import quote_plus
import datetime
import time
import aiohttp
import asyncio
import codecs
import json
from threading import Thread
from bs4 import BeautifulSoup
import requests
from datetime import datetime

class roblox:
    """Cogs for ROBLOX"""
    def __init__(self, bot):
        self.bot = bot
        self.s = requests.session()
        self.token = None

    """@commands.command()
    async def rbxrap(self, username : str, encoding='utf-8', errors='strict'):
         Gets the Rap from A ROBLOX User
         user = str.format(username)
         url = "https://api.roblox.com/users/get-by-username?username=" + user
         await self.bot.say("Searching ROBLOX For " + user + "'s ID")
         async with aiohttp.get(url) as r:
             result = await r.json()
             id = format(result['Id'])
             await self.bot.say("Found " + user + "'s ID: " + id)
             url2 = "http://138.197.45.3/apis/api.php?userid=" + id
             async with aiohttp.get(url2) as r2:
                 self.decoder = codecs.getincrementaldecoder(encoding)(errors=errors)
                 data = await r2.read()
                 result2 = self.decoder.decode(data)
                 user = str.format(username)
                 await self.bot.say(user + "'s Rap Is " + format(result2))"""
                 
    @commands.command()
    async def rbxuserinfo(self, username : str):
        """Gets the ROBLOX User Info"""
        user = str.format(username)
        url = "https://www.roblox.com/Groups/GetPrimaryGroupInfo.ashx?users=" + user
        async with aiohttp.get(url) as r:
            result = await r.json()
            url3 = "https://api.roblox.com/groups/" + result['HQ_Trivia']['GroupId']
            async with aiohttp.get(url3) as r3:
            result3 = await r3.json()
            url2 = "https://api.roblox.com/users/get-by-username?username=" + user
            async with aiohttp.get(url2) as r2:
                result2 = await r2.json()
                id = format(result2['Id'])
                avat = "https://www.roblox.com/bust-thumbnail/json?userId=" + id + "&height=140&width=140"
                async with aiohttp.get(avat) as av:
                    do = await av.json()
                    if do['Final'] == True:
                        pic = format(do['Url'])
                        pic2 = format(result3['EmblemUrl'])
                        data = discord.Embed(description="Username: " + user)
                        data.add_field(name="Items", value="Soon")
                        data.add_field(name="Info", value="ROBLOX is a Free MMO Which allows you to be creative and play other players games!")
                        data.set_thumbnail(url=pic)
                        data.set_footer(text="Info of the user: " + user + "! Thanks to ROBLOX for their APIs!")
                        data2 = discord.Embed(description="Primary Group from: " + user)
                        data2.add_field(name="Description", value=result3['Description'])
                        data2.set_thumbnail(url=pic2)
                        data2.set_footer(text="Info of group: " + result3['Name'] + "! Thanks to ROBLOX for their APIs!")
                        await self.bot.say(embed=data) self.bot.say(embed=data2)
                    if do['Final'] == False:
                        await self.bot.say("Avatar Pic Of " + user + " Was not rendered yet! Please Try Again!")
    
def setup(bot):
    n = roblox(bot)
    bot.add_cog(n)
