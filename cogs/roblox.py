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

class Gear(object):
    def __init__(self):
        self.MELEE = 0
        self.RANGED = 1
        self.EXPLOSIVE = 2
        self.POWERUP = 3
        self.NAVIGATION = 4
        self.MUSICAL = 5
        self.SOCIAL = 6
class Subcategory(object):
    def __init__(self):
        self.FEATURED = 0
        self.ALL = 1
        self.COLLECTIBLES = 2
        self.CLOTHING = 3
        self.BODYPARTS = 4
        self.GEAR = 5
        self.MODELS = 6
        self.PLUGINS = 7
        self.DECALS = 8
        self.HATS = 9
        self.FACES = 10
        self.PACKAGES = 11
        self.SHIRTS = 12
        self.TSHIRTS = 13
        self.PANTS = 14
        self.HEADS = 15
        self.AUDIO = 16
        self.ROBLOXCREATED = 17
        self.MESHES = 18
class Genre(object):
    def __init__(self):
        self.ALL = 0
        self.TOWNANDCITY = 1
        self.MEDIEVAL = 2
        self.SCIFI = 3
        self.FIGHTING = 4
        self.HORROR = 5
        self.NAVAL = 6
        self.ADVENTURE = 7
        self.SPORTS = 8
        self.COMEDY = 9
        self.WESTERN = 10
        self.MILITARY = 11
        self.SKATING = 12
        self.BUILDING = 13
        self.FPS = 14
        self.RPG = 15
class Category(object):
    def __init__(self):
        self.FEATURED = 0
        self.ALL = 1
        self.COLLECTIBLES = 2
        self.CLOTHING = 3
        self.BODYPARTS = 4
        self.GEAR = 5
        self.MODELS = 6
        self.PLUGINS = 7
        self.DECALS = 8
        self.AUDIO = 9
        self.MESHES = 10
class Currency(object):
    def __init__(self):
        self.ALL = 0
        self.ROBUX = 1
        self.FREE = 2
class Sort(object):
    def __init__(self):
        self.RELEVANCE = 0
        self.MOSTFAVORITED = 1
        self.BESTSELLING = 2
        self.RECENTLYUPDATED = 3
        self.PRICELOWTOHIGH = 4
        self.PRICEHIGHTOLOW = 5
class Time(object):
    def __init__(self):
        self.PASTDAY = 0
        self.PASTWEEK = 1
        self.PASTMONTH = 2
        self.ALLTIME = 3

class RobloxApiClient(object):
    
    def __init__(self):
        self.s = requests.session()
        self.token = None
    def friends(self,id1,id2):
        t = self.s.get('https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=IsFriendsWith&playerId='+id1+'&userId='+id2).text
        t=t.replace('<Value Type="boolean">','')
        t=t.replace('</Value>','')
        if t == 'true':
            return True
        else:
            return False
    def name(self,iyd):
        r = self.s.get('https://api.roblox.com/Users/'+iyd)
        jdict = json.loads(r.text)
        return jdict["Username"]

    def assetComments(self,id1):
        r = self.s.get('https://www.roblox.com/API/Comments.ashx?rqtype=getComments&assetID='+id1+'&startIndex=0')
        js = json.loads(r.text)
        return js
            
    def catalogSearch(self,geartype = -1, genre = -1, subcategory = -1, category = -1, currency = -1, sort = -1, freq = -1, keyword = None, creatorID = None, minim = 0, maxim = None, notforsale = True, pagenumber = -1, resultsperpage = -1, url = False):
        req = 'http://roblox.com/catalog/json?'
        if geartype != -1:
            req += '&Gears={}'.format(geartype)
        if genre != -1:
            req += '&Genres={}'.format(genre)
        if subcategory != -1:
            req += '&Subcategory={}'.format(subcategory)
        if category != -1:
            req += '&Category={}'.format(category)
        if currency != -1:
            req += '&CurrencyType={}'.format(currency)
        if sort != -1:
            req += '&SortType={}'.format(sort)
        if freq != -1:
            req += '&AggregationFrequency={}'.format(freq)
        if keyword != None:
            req += '&Keyword={}'.format(keyword)
        if creatorID != None:
            req += '&CreatorID={}'.format(creatorID)
        req += '&PxMin={}'.format(minim)
        if maxim != None:
            req += '&PxMax={}'.format(maxim)
        if notforsale:
            req += '&IncludeNotForSale=true'
        else:
            req += '&IncludeNotForSale=false'
        if pagenumber != -1:
            req +=  '&PageNumber={}'.format(pagenumber)
        if resultsperpage != -1:
            req += '&ResultsPerPage={}'.format(resultsperpage)
        r = self.s.get(req)
        if url:
            print(r.url)
        return json.loads(r.text)
    def getFriends(self,userid):
        return self.s.get('https://api.roblox.com/users/'+str(userid)+'/friends').json()

    def friendCrawl(self,userid, maxfr = 100):
        usercount = 0
        users = []
        friendlist1 = getFriends(userid)       
        for friend in friendlist1:
            if len(users) < maxfr:
                if self.s.get('https://www.roblox.com/users/'+str(friend['Id'])+'/profile').status_code != 404:
                    users.append({'Id':friend['Id'],'Username':friend['Username']})
                    usercount += 1
                    print("Users: "+ str(usercount))
            else:
                return users
        for user in users:
            req = self.s.get("https://api.roblox.com/users/"+str(user['Id'])+"/friends")
            if req.status_code != 404:
                friendlist1 = json.loads(req.text)
            else:
                pass
            for friend in friendlist1:
                if len(users) < maxfr:
                    if self.s.get('https://www.roblox.com/users/'+str(friend['Id'])+'/profile').status_code != 404:
                        d = {'Id':friend['Id'],'Username':friend['Username']}
                        if d not in users:
                            users.append(d)
                            usercount += 1
                            print("Users: "+ str(usercount))
                else:
                    return users

    def getCurrentStatus(self):
        return self.s.get('https://www.roblox.com/client-status').text

    def getUserPresence(self,userid):
        return self.s.get('https://www.roblox.com/presence/user?userId={}'.format(userid)).json()
    
    def createAccount(self,username,password,bd,gender = 2): #birthday is a datetime object
        params = {
            "isEligibleForHideAdsAbTest":False,
            "username":username,
            "password":password,
            "birthday": bd.strftime("%d %b %Y").lstrip("0").replace(" 0", " "),
            "gender": gender, #3 for female, 2 for male
            "context":"RollerCoasterSignupForm"
        }
        print(params)
        r = self.s.post("https://api.roblox.com/signup/v1",data = params, headers = {'Content-Type':'application/json'})
        return r

    def getItemInfo(self,itemid):
        return self.s.get("https://api.roblox.com/marketplace/productinfo?assetId="+str(itemid)).json()

    def buyItem(self,itemid):
        info = self.getItemInfo(itemid)
        url="https://web.roblox.com/api/item.ashx?rqtype=purchase&productID={}&expectedCurrency=1&expectedPrice={}&expectedSellerID={}&userAssetID=".format(info["ProductId"], 0 if info["PriceInRobux"] == None else info["PriceInRobux"],info["Creator"]["Id"])
        self.token = self.s.post(url).headers['X-CSRF-TOKEN']
        r = self.s.post(url, headers = {"X-CSRF-TOKEN":self.token})
        return r

    def logIn(self,username,password,returnurl = ""):
        r = self.s.post("https://www.roblox.com/newlogin",data={"username":username,"password":password,"submitLogin":"Log In","ReturnUrl":returnurl})
        return r

    def giveBadge(self,userid,badgeid,placeid):
        return self.s.post("https://api.roblox.com/assets/award-badge", data = {'userId':userid,'badgeId':badgeid,'placeId':placeid}).json()
    
    def getVersions(self,itemid):
        return self.s.get("https://api.roblox.com/assets/{}/versions".format(itemid)).json()

    def getCurrency(self):
        return self.s.get("https://api.roblox.com/currency/balance").json()

    def setXsrfToken(self):
        r = self.s.get("https://roblox.com/home")
        tok = r.text[r.text.find("Roblox.XsrfToken.setToken('") + 27::]
        tok = tok[:tok.find("');"):]
        self.token = tok
        return tok

    def sendMessage(self,subject,body,recipientid):
        if not self.token:
            self.setXsrfToken()
        r = self.s.post('https://www.roblox.com/messages/send',headers = {'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8","X-CSRF-TOKEN":self.token}, data = {"subject":subject,"body":body,"recipientid":recipientid,"cacheBuster":round(time.time(),3)})
        return r

    def forumPost(self,forumid,subject,body,disablereplies = False): #currently nonfunctional
        earl = "https://forum.roblox.com/Forum/AddPost.aspx?ForumID={}".format(forumid)
        view = self.s.get(earl)
        soup = BeautifulSoup(view.text,'html.parser')
        params = {
            "__EVENTTARGET" : '',
            "__EVENTARGUMENT": '',
            '__VIEWSTATE':soup.find(id="__VIEWSTATE")['value'],
            "__VIEWSTATEGENERATOR":soup.find(id="__VIEWSTATEGENERATOR")['value'],
            "__EVENTVALIDATION" : soup.find(id="__EVENTVALIDATION")['value'],
            "ctl00$cphRoblox$Createeditpost1$PostForm$NewPostSubject":subject,
            "ctl00$cphRoblox$Createeditpost1$PostForm$PostBody":body,
            "ctl00$cphRoblox$Createeditpost1$PostForm$PostButton":" Post "
        }
        if disablereplies:
            params["ctl00$cphRoblox$Createeditpost1$PostForm$AllowReplies"] = 'on'
        r = self.s.post(earl, data = params, headers = {"Content-Type":"application/x-www-form-urlencoded"})
        return r

    def replyToForumPost(self, postid, text, disablereplies = False):
        earl = "https://forum.roblox.com/Forum/AddPost.aspx?PostID={}".format(postid)
        view = self.s.get(earl)
        soup = BeautifulSoup(view.text,'html.parser')
        params = {
            "__EVENTTARGET" : '',
            "__EVENTARGUMENT": '',
            '__VIEWSTATE':soup.find(id="__VIEWSTATE")['value'],
            "__VIEWSTATEGENERATOR":soup.find(id="__VIEWSTATEGENERATOR")['value'],
            "__EVENTVALIDATION" : soup.find(id="__EVENTVALIDATION")['value'],
            "ctl00$cphRoblox$Createeditpost1$PostForm$PostBody":text,
            "ctl00$cphRoblox$Createeditpost1$PostForm$PostButton":" Post "
        }
        if disablereplies:
            params["ctl00$cphRoblox$Createeditpost1$PostForm$AllowReplies"] = 'on'
        r = self.s.post(earl, data = params, headers = {"Content-Type":"application/x-www-form-urlencoded"})
        return r

    
    def getRobloSecurityCookie(self):
        return self.s.cookies.get_dict()['.ROBLOSECURITY']

    def commentOnAsset(self,assetid,text):
        if not self.token:
            self.setXsrfToken()
        r = self.s.post("https://www.roblox.com/comments/post",data = {'assetId':assetid,'text':text}, headers = {"X-CSRF-TOKEN":self.token})
        return r
    
    def joinGroup(self,groupid):
        viewpage = self.s.get("https://www.roblox.com/groups/group.aspx?gid={}".format(groupid))
        soup = BeautifulSoup(viewpage.text,'html.parser')
        params = {
        '__EVENTTARGET':"JoinGroupDiv",
        '__EVENTARGUMENT':"Click",
        '__LASTFOCUS':'',
        '__VIEWSTATE':soup.find(id="__VIEWSTATE")['value'],
        '__VIEWSTATEGENERATOR':soup.find(id="__VIEWSTATEGENERATOR")['value'],
        '__EVENTVALIDATION':soup.find(id="__EVENTVALIDATION")['value'],
        'ctl00$cphRoblox$GroupSearchBar$SearchKeyword':"Search all groups",
        'ctl00$cphRoblox$rbxGroupRoleSetMembersPane$dlRolesetList':soup.find(id="ctl00_cphRoblox_rbxGroupRoleSetMembersPane_dlRolesetList").find(selected="selected")['value'],
        'ctl00$cphRoblox$rbxGroupRoleSetMembersPane$RolesetCountHidden':soup.find(id="ctl00_cphRoblox_rbxGroupRoleSetMembersPane_RolesetCountHidden")['value'],
        'ctl00$cphRoblox$rbxGroupRoleSetMembersPane$dlUsers_Footer$ctl01$PageTextBox':soup.find(id="ctl00_cphRoblox_rbxGroupRoleSetMembersPane_dlUsers_Footer_ctl01_PageTextBox")['value'],
        'ctl00$cphRoblox$rbxGroupRoleSetMembersPane$currentRoleSetID':soup.find(id="ctl00_cphRoblox_rbxGroupRoleSetMembersPane_currentRoleSetID")['value']
        }
        r = self.s.post("https://www.roblox.com/groups/group.aspx?gid={}".format(groupid), data = params, headers = {'Content-Type':'application/x-www-form-urlencoded'})
        return r

    def reportAbuse(self,userid,category,comment):
        view = self.s.get("https://www.roblox.com/abusereport/UserProfile?id={}".format(userid))
        params = {
        '__RequestVerificationToken':re.search('name="__RequestVerificationToken" type="hidden" value="(.+)"',view.text).group(1),
        'ReportCategory':category,
        'Comment':comment,
        'Id':userid,
        'RedirectUrl':'/Login',
        'PartyGuid':'',
        'ConversationId':''
        }
        r = self.s.post("https://www.roblox.com/abusereport/UserProfile?id={}",data=params)
        return r

    def getRAP(self,aid, returnv = None):
        txt = requests.get("https://www.roblox.com/asset/{}/sales-data".format(aid)).json()
        value = txt['data']['AveragePrice']
        if returnv:
            returnv[0] += value
        else:
            return value
    
    def getUserRAP(self,uid):
        hats = self.s.get("https://www.roblox.com/users/inventory/list-json?assetTypeId=8&cursor=&itemsPerPage=999999&pageNumber=1&userId={}".format(uid)).json()
        gear = self.s.get("https://www.roblox.com/users/inventory/list-json?assetTypeId=19&cursor=&itemsPerPage=999999&pageNumber=1&userId={}".format(uid)).json()
        faces = self.s.get("https://www.roblox.com/users/inventory/list-json?assetTypeId=18&cursor=&itemsPerPage=999999&pageNumber=1&userId={}".format(uid)).json()
        hatlist = []
        gearlist = []
        facelist = []
        if hats['IsValid'] == False:
            return None
        for hat in hats['Data']['Items']:
            try:
                if hat['Product'] and hat['Product']['IsLimited'] or hat['Product']['IsLimitedUnique']:
                    hatlist.append(hat['Item']['AssetId'])
            except TypeError as e:
                pass
        for hat in gear['Data']['Items']:
            try:
                if hat['Product'] and hat['Product']['IsLimited'] or hat['Product']['IsLimitedUnique']:
                    gearlist.append(hat['Item']['AssetId'])
            except TypeError as e:
                pass
        for hat in faces['Data']['Items']:
            try:
                if hat['Product'] and hat['Product']['IsLimited'] or hat['Product']['IsLimitedUnique']:
                    facelist.append(hat['Item']['AssetId'])
            except TypeError as e:
                pass
        threadarr = []
        returnval = [0]
        for item in hatlist+gearlist+facelist:
            threadarr.append(Thread(target=self.getRAP,args=(item,returnval)))
        for thread in threadarr:
            thread.start()
        for thread in threadarr:
            thread.join()
        return returnval[0]

    def getSellers(self,aid):
        return requests.get("https://www.roblox.com/asset/resellers?productId={}&startIndex=0&maxRows=9999999".format(self.getItemInfo(aid)['ProductId'])).json()

    def getSalesData(self,aid):
        return requests.get("https://www.roblox.com/asset/{}/sales-data".format(aid)).json()

    def snipeLimited(self,aid,desiredprice):
        self.token = requests.post("https://web.roblox.com/api/item.ashx?rqtype=purchase&productID={}&expectedCurrency=1&expectedPrice={}&expectedSellerID={}&userAssetID={}").headers['X-CSRF-TOKEN']
        sellers = self.getSellers(aid)
        for seller in sellers['data']['Resellers']:
            if seller['Price'] <= desiredprice:
                return requests.post("https://web.roblox.com/api/item.ashx?rqtype=purchase&productID={}&expectedCurrency=1&expectedPrice={}&expectedSellerID={}&userAssetID={}".format(self.getItemInfo(aid)['ProductId'],seller['Price'],seller['SellerId'],seller['UserAssetId']),headers = {"X-CSRF-TOKEN":self.token})
        return False

    def logOut(self):
        if not self.token:
            self.setXsrfToken()
        r = self.s.post("https://api.roblox.com/sign-out/v1",headers={'X-CSRF-TOKEN':self.token})
        return r

    def favItem(self,itemid) : # made by Vibe
        if not self.token:
            self.setXsrfToken()
        r = self.s.post('https://www.roblox.com/favorite/toggle', data = {'assetid': itemid,'isguest' : 'false'}, headers = {"X-CSRF-TOKEN":self.token})
        return r
    def updateStatus(self, message) : # also made by Vibe
        if not self.token:
            self.setXsrfToken()
        r = self.s.post('https://www.roblox.com/home/updatestatus', data = {'status': message}, headers = {"X-CSRF-TOKEN":self.token})
        return r
    
    def sendVerEmail(self):
        r=self.s.post('https://www.roblox.com/my/account/sendverifyemail')
        return r

    def getLeaderBoard(self,gid):
        git = self.s.get('https://www.roblox.com/--item?id={}'.format(gid))
        text=git.text
        reg = re.search("data-distributor-target-id=\"(.+)\"\s*data-max=\"(.+)\"\s*data-rank-max=\"(.+)\"\s*data-target-type=\"(.+)\"\s*data-time-filter=\"(.+)\"\s*data-player-id=\"(.+)\"\s*data-clan-id=\"(.+).></div>",text)
        if reg:
            data={
            'targetType': reg.group(4),
            'distributorTargetId': reg.group(1),
            'timeFilter': reg.group(5),
            'startIndex': 0,
            'currentRank': 1,
            'previousPoints': - 1,
            'max': reg.group(2),
            'imgWidth': 48,
            'imgHeight': 48,
            'imgFormat': 'PNG'
          }
            r= requests.get('https://roblox.com/leaderboards/rank/json',params=data)
            return r
        else:
            return None

class roblox:
    """Cogs for ROBLOX"""
    def __init__(self, bot):
        self.bot = bot
        self.s = requests.session()
        self.token = None

    @commands.command()
    async def rbxrap(self, username : str, encoding='utf-8', errors='strict'):
         """Gets the Rap from A ROBLOX User"""
         user = str.format(username)
         url = "https://api.roblox.com/users/get-by-username?username=" + user
         await self.bot.say("Searching ROBLOX For " + user + "'s ID")
         async with aiohttp.get(url) as r:
             result = await r.json()
             id = format(result['Id'])
             await self.bot.say("Found " + user + "'s ID: " + id)
             url2 = "https://piczy.pro/t.php?userId=" + id
             async with aiohttp.get(url2) as r2:
                 self.decoder = codecs.getincrementaldecoder(encoding)(errors=errors)
                 data = await r2.read()
                 result2 = self.decoder.decode(data)
                 user = str.format(username)
                 await self.bot.say(user + "'s Rap Is " + format(result2))
                 
    @commands.command()
    async def rbxuserinfo(self, username : str):
        """Gets the ROBLOX User Info"""
        user = str.format(username)
        url = "https://www.roblox.com/Groups/GetPrimaryGroupInfo.ashx?users=" + user
        async with aiohttp.get(url) as r:
            result = await r.json()
            url2 = "https://api.roblox.com/users/get-by-username?username=" + user
            await self.bot.say("Primary Group Will be added in the future")
            async with aiohttp.get(url2) as r2:
                result2 = await r2.json()
                id = format(result2['Id'])
                avat = "https://www.roblox.com/bust-thumbnail/json?userId=" + id + "&height=140&width=140"
                async with aiohttp.get(avat) as av:
                    do = await av.json()
                    if do['Final'] == True:
                        pic = format(do['Url'])
                        data = discord.Embed(description="Username: " + user)
                        data.add_field(name="Items", value="Soon")
                        data.add_field(name="Info", value="ROBLOX is a Free MMO Which allows you to be creative and play other players games!")
                        data.set_thumbnail(url=pic)
                        data.set_footer(text="Info of the user: " + user + "! Thanks to ROBLOX for their APIs!")
                        await self.bot.say(embed=data)
                    if do['Final'] == False:
                        await self.bot.say("Avatar Pic Of " + user + " Was not rendered yet! Please Try Again!")
    @commands.command()
    async def rbxpm(self, subject, body, recipientid):
         """PM Someone with the bot"""
         client = RobloxApiClient()
         client.logIn("Investive","")
         client.sendMessage(subject,body,recipientid)
         await self.bot.say("Sent PM to " + recipientid + " With Investive!")
    @commands.command()
    async def rbxcreate(self,username,password,birthday,gender = 2):
        client = RobloxApiClient()
        bd = datetime.strptime(birthday, '%Y-%m-%d')
        client.createAccount(username,password,bd,gender)
        await self.bot.say("User " + username + " was created succesfully!")
    
def setup(bot):
    n = roblox(bot)
    bot.add_cog(n)
