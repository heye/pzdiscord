import sys
from rcon import Client
import discord
from config import Config

def run_rcon(cmd: str) -> str:
    with Client(Config.rcon_ip, int(Config.rcon_port), passwd=Config.rcon_passwd) as client:
        response = client.run(cmd)

    print("RCON RESPONSE: " + str(response))
    return str(response)


def main(argv) -> int:
    
    Config.load(argv)

    allowed_commands = [
        "save"]

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
                    await message.channel.send(reply)
                    return

            await message.channel.send("unknown command " + message.content)
            
    client.run(Config.discord_bot_token)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))  # next section explains the use of sys.exit