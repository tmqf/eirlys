import nextcord, json, asyncpg, asyncio
from nextcord.ext import commands

#|----------Normal Commands----------|

from cogs.normalCommands.general import General, RunTimes
from cogs.normalCommands.anilist import Anilist, AnilistDB
from cogs.normalCommands.errorHandlers import ErrorHandlers
from classes.anilistClasses import AniClassDB

#|----------Slash Commands----------|

from cogs.slashCommands.SLAnilist import SLAnilist, SLAnilistDB
from cogs.slashCommands.SLGeneral import SLGeneral

#|----------Setting Client and Token----------|

client = commands.Bot(command_prefix=".", help_command=None, intents=nextcord.Intents.all(), case_insensitive=True)
privateFile = open('private.json'); token = json.loads(privateFile.read())

#|----------Cog and DB Dicts----------|

cogs = {General: True, Anilist: True, SLAnilist: True, SLGeneral: True, ErrorHandlers: True}
DBs = {AnilistDB: True, SLAnilistDB: True, AniClassDB: True}

#|----------Print when bot is online----------|

@client.event
async def on_ready():
    print(f"| -- {client.user.name}#{client.user.discriminator} -- ONLINE")
    await client.change_presence(status=nextcord.Status.online, activity = nextcord.Activity(name=f"Prefix is {client.command_prefix}", type=1, url="https://www.twitch.tv/aoi_asmr"))

    #|----------Adding Cogs----------|

    for cog in cogs:
        if cogs[cog] == True:
            print(f"| -- {cog.__name__} -- ONLINE")
            client.add_cog(cog(client))

    #|----------Adding Databases----------|
    sql = await asyncpg.connect(user=token['Database']['Username'], host=token['Database']['Host'], database=token['Database']['Database'], password=token['Database']['Password'])
    
    for DB in DBs:
        if DBs[DB] == True:
            print(f"| -- {DB.__name__} -- ONLINE")
            await DB(sql)

if __name__ == "__main__":
    client.loop.create_task(RunTimes(client))
    client.run(token['Miumi']['Miumi'])