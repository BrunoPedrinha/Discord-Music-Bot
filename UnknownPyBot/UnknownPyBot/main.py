import discord
from discord.ext import commands

TOKEN = "put your bot token here"
#Prefix to use in discord. ? before command. Change it to whatever you want.
client = commands.Bot(command_prefix = "?")
#removes the default help command so we can custom make our own.
client.remove_command('help')

#add the cogs to an array.
extensions = ["HelpCommand","MusicCommands", ]

@client.event
async def on_ready():
    print("Bot online and loaded!")
    #Set the "game playing" of the bot to let people know they can type ?help for commands.
    await client.change_presence(game=discord.Game(name="Type ?help for a list of commands", type=1))

#error writing to discord. If people request a song without the url they need to put it between ""
#if they do "song title and don't close the quotes this will let them know they need to close the quote.
@client.event
async def on_command_error(error, context):
    if isinstance(error, commands.BadArgument):
        await client.send_message(context.message.channel, error)

#Make this the main file and load the extensions of they can be loaded and run the bot with the bot token provided by discord.
if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    client.run(TOKEN)
