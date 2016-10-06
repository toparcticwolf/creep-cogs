import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
import os
import aiohttp
import random

# if this seem hard to read/understand,
# remove the comments. Might make it easier


class thunder:
    """thunder"""

    def __init__(self, bot):
        self.bot = bot
        self.thunderLoaded = os.path.exists('data/thunder/thunder.jpg')

        self.servers = fileIO("data/thunder/servers.json", "load")

    # doesn't make sense to use this command in a pm,
    # because pms aren't in servers
    # mod_or_permissions needs something in it otherwise
    # it's mod or True which is always True
    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_roles=True)
    async def thunder(self, ctx):
        """Enables/Disables thunder for this server"""
        # default off.
        server = ctx.message.server
        if server.id not in self.servers:
            self.servers[server.id] = False
        else:
            self.servers[server.id] = not self.servers[server.id]
        # for a toggle, settings should save here in
        # case bot fails to send message
        fileIO("data/thunder/servers.json", "save", self.servers)
        if self.servers[server.id]:
            await self.bot.say("thunder on. Please turn this off in the " +
                               "Red - DiscordBot server. This is only " +
                               "an example cog.")
        else:
            await self.bot.say("thunder off.")

    async def check_thunder(self, message):
        rand = (random.randint(1, 7))
        self.image = "data/thunder/thunder_%s.jpg" % (rand)
        # check if setting is on in this server
        # let thunders happen in PMs always
        server = message.server
        if server is not None:
            if server.id not in self.servers:
                # default off
                self.servers[server.id] = False
            # thunder is off, so ignore
            if not self.servers[server.id]:
                return

        # comments explaining next section. seemed easier to read this way
        # check for a phrase in message
        #   if thunder isn't downloaded yet, dl it
        #       try
        #           get image from url
        #           write image to file
        #           it worked \o/
        #           send it
        #       except
        # there was a problem, print an error then try to send the url instead
        #   else thunder image already downloaded, send it
        if not (message.author.id == self.bot.user.id):
            if "thunderfury" in message.content.lower():
                await self.bot.send_file(message.channel, self.image)


def check_folders():
    # create data/thunder if not there
    if not os.path.exists("data/thunder"):
        print("Creating data/thunder folder...")
        os.makedirs("data/thunder")


def check_files():
    # create server.json if not there
    # put in default values
    default = {}
    if not os.path.isfile("data/thunder/servers.json"):
        print("Creating default thunder servers.json...")
        fileIO("data/thunder/servers.json", "save", default)


def setup(bot):
    check_folders()
    check_files()
    n = thunder(bot)
    # add an on_message listener
    bot.add_listener(n.check_thunder, "on_message")
    bot.add_cog(n)
