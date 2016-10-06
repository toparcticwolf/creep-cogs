import discord
from discord.ext import commands
from .utils.dataIO import fileIO, dataIO
from .utils import checks
import os
import logging
import asyncio

# if this seem hard to read/understand, remove the comments. Might make it easier

class Cleandiscord:
    """cleandiscord"""

    def __init__(self,bot):
        self.bot = bot
        self.servers = fileIO("data/cleandiscord/servers.json", "load")
        self.cleandiscord_list = dataIO.load_json("data/cleandiscord/cleandiscord.json")


    # doesn't make sense to use this command in a pm, because pms aren't in servers
    # mod_or_permissions needs something in it otherwise it's mod or True which is always True
    @commands.command(pass_context=True)
    @checks.mod_or_permissions(manage_roles=True)
    async def cleandiscord(self, ctx):
        """Enables/Disables cleandiscord for this server"""
        #default off.
        server = ctx.message.server
        if server.id not in self.servers:
            self.servers[server.id] = False
        else:
            self.servers[server.id] = not self.servers[server.id]
        #for a toggle, settings should save here in case bot fails to send message
        fileIO("data/cleandiscord/servers.json", "save", self.servers)
        if self.servers[server.id]:
            await self.bot.say("cleandiscord on.")
        else:
            await self.bot.say("cleandiscord off.")


#    @cleandiscord.command(name="time")
#    async def _cleandiscord_time(self, time: int):
#        """Changes cleandiscord's deletion time"""
#        self.cleandiscord_list = []
#        dataIO.save_json("data/cleandiscord/cleandiscord.json", self.cleandiscord_list)
#        self.cleandiscord_list.append(time)
#        dataIO.save_json("data/cleandiscord/cleandiscord.json", self.cleandiscord_list)
#        await self.bot.say("Deletion time has been changed.")


    async def check_cleandiscord(self, command, ctx):
        # check if setting is on in this server
        #let cleandiscords happen in PMs always
        message = ctx.message
        server = ctx.message.server
        channel = ctx.message.channel
        message_id = ctx.message.id
        if server != None:
            if server.id not in self.servers:
                #default off
                self.servers[server.id] = False
            # cleandiscord is off, so ignore
            if not self.servers[server.id]:
                return
            try:
            # to increase or decrease the delay between deletions change this
            # number right here     ↓
                await asyncio.sleep(5)
                await self.bot.delete_message(message)
            except discord.errors.Forbidden:
                await self.bot.say("I need permissions to manage messages "
                                   "in this channel.")

        logger.info("deleted {} in channel {}"
                "".format(ctx.message, channel.name))


def check_folders():
    # create data/cleandiscord if not there
    if not os.path.exists("data/cleandiscord"):
        print("Creating data/cleandiscord folder...")
        os.makedirs("data/cleandiscord")


def check_files():
    # create server.json if not there
    # put in default values
    default = {}
    if not os.path.isfile("data/cleandiscord/servers.json"):
        print("Creating default cleandiscord servers.json...")
        fileIO("data/cleandiscord/servers.json", "save", default)
    if not os.path.isfile("data/mod/whitelist.json"):
        print("Creating empty whitelist.json...")
        fileIO("data/mod/whitelist.json", "save", [])


def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("cleandiscord")
    # Prevents the logger from being loaded again in case of module reload
    if logger.level == 0:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename='data/cleandiscord/cleandiscord.log', encoding='utf-8', mode='a')
        handler.setFormatter(
            logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    n = Cleandiscord(bot)
    # add an on_message listener
    bot.add_listener(n.check_cleandiscord, "on_command")
    bot.add_cog(n)
