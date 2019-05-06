import discord
from discord.ext import commands

#help command cog. 
class HelpCommand:

    def __init__(self, client):
        self.client = client
        
    #custom help command. Reads from a .txt file.
    @commands.command(pass_context = True)
    async def help(self, context):
        _file = open("help.txt", "r")
        if _file.mode == "r":
            print("Reading file. . .")
            help_text = _file.read()
            await self.client.send_message(context.message.author, help_text)
            _file.close()
        

def setup(client):
    client.add_cog(HelpCommand(client))