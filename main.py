import sys
from typing import List
from rcon import Client
import discord
from config import Config

def run_rcon(cmd: str) -> str:
    try:
        with Client(Config.rcon_ip, int(Config.rcon_port), passwd=Config.rcon_passwd) as client:
            response = client.run(cmd)

        print("RCON RESPONSE: " + str(response))
        return str(response)
    except:
        return "error"


def split_lines2000(input: str) -> List[str]:
    blocks = []
    one_line = ""
    for line in input.splitlines():
        if len(one_line + line) < 2000:
            one_line += line + "\n"
        else:
            blocks.append(one_line)
            one_line = ""

    if one_line:
        blocks.append(one_line)

    return blocks


def main(argv) -> int:
    
    Config.load(argv)

    allowed_commands = [
        "addalltowhitelist",
        "additem",
        "adduser",
        "addusertowhitelist",
        "addvehicle",
        "addxp",
        "alarm",
        "banid",
        "banuser",
        "changeoption",
        "chopper",
        "createhorde",
        "godmod",
        "gunshot",
        "help",
        "invisible",
        "kickuser",
        "noclip",
        "players",
        "quit",
        "releasesafehouse",
        "reloadlua",
        "reloadoptions",
        "removeuserfromwhitelist",
        "removezombies",
        "replay",
        "save",
        "sendpulse",
        "servermsg",
        "setaccesslevel",
        "showoptions",
        "startrain",
        "stoprain",
        "teleport",
        "teleportto",
        "unbanid",
        "unbanuser",
        "voiceban"]

    client = discord.Client()

    @client.event
    async def on_ready():
        print('Discord logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        #print("ON MESSAGE")
        #print(message)
        if message.author == client.user:
            return
                    
        if str(message.channel.id) == Config.discord_channel_id:
            for one_cmd in allowed_commands:
                if message.content.startswith(one_cmd):
                    print("COMMAND: " + message.content)
                    reply = run_rcon(message.content)
                    if len(reply) < 2000:
                        await message.channel.send(reply)
                    else:
                        for line in split_lines2000(reply):
                            await message.channel.send(line)
                    return

            await message.channel.send("unknown command " + message.content)
            
    client.run(Config.discord_bot_token)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))  # next section explains the use of sys.exit