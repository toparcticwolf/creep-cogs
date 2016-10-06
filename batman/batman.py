import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
import os
import aiohttp

# if this seem hard to read/understand, remove the comments. Might make it easier

class batman:
    """bat"""

    def __init__(self,bot):
        self.bot = bot
        self.url = "https://pixabay.com/static/uploads/photo/2014/04/03/11/51/batman-312342_960_720.png"
        self.batLoaded = os.path.exists('data/batman/batman.png')
        self.image = "data/batman/batman.png"
        self.servers = fileIO("data/batman/servers.json", "load")

    # doesn't make sense to use this command in a pm, because pms aren't in servers
    # mod_or_permissions needs something in it otherwise it's mod or True which is always True
    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_roles=True)
    async def batman(self, ctx):
        """Enables/Disables batman for this server"""
        #default off.
        server = ctx.message.server
        if server.id not in self.servers:
            self.servers[server.id] = False
        else:
            self.servers[server.id] = not self.servers[server.id]
        #for a toggle, settings should save here in case bot fails to send message
        fileIO("data/batman/servers.json", "save", self.servers)
        if self.servers[server.id]:
            await self.bot.say("batman on. Please turn this off in the Red - DiscordBot server. This is only an example cog.")
        else:
            await self.bot.say("batman off.")

    async def check_bat(self, message):
        # check if setting is on in this server
        #let batmans happen in PMs always
        server = message.server
        if server != None:
            if server.id not in self.servers:
                #default off
                self.servers[server.id] = False
            # batman is off, so ignore
            if not self.servers[server.id]:
                return

        # comments explaining next section. seemed easier to read this way
        # check for a phrase in message
        #   if batman isn't downloaded yet, dl it
        #       try
        #           get image from url
        #           write image to file
        #           it worked \o/
        #           send it
        #       except
        #           there was a problem, print an error then try to send the url instead
        #   else batman image already downloaded, send it

        if "nana" in message.content.lower():
            if not self.batLoaded:
                try:
                    async with aiohttp.get(self.url) as r:
                        image = await r.content.read()
                    with open('data/batman/batman.png','wb') as f:
                        f.write(image)
                    self.batLoaded = os.path.exists('data/batman/batman.png')
                    await self.bot.send_message(message.channel,"BATMAN!!!!!")
                    await self.bot.send_file(message.channel,self.image)
                except Exception as e:
                    print(e)
                    print("batman error D: I couldn't download the file, so we're gonna use the url instead")
                    await self.bot.send_message(message.channel,"BATMAN!!!!!")
                    await self.bot.send_message(message.channel,self.url)
            else:
                await self.bot.send_message(message.channel,"BATMAN!!!!!")
                await self.bot.send_file(message.channel,self.image)

def check_folders():
    # create data/batman if not there
    if not os.path.exists("data/batman"):
        print("Creating data/batman folder...")
        os.makedirs("data/batman")

def check_files():
    # create server.json if not there
    # put in default values
    default = {}
    if not os.path.isfile("data/batman/servers.json"):
        print("Creating default batman servers.json...")
        fileIO("data/batman/servers.json", "save", default)


def setup(bot):
    check_folders()
    check_files()
    n = batman(bot)
    # add an on_message listener
    bot.add_listener(n.check_bat, "on_message")
    bot.add_cog(n)
