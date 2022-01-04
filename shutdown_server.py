import sys
import multiprocessing
from typing import List, Dict
from rcon import Client
import discord
from config import Config
import traceback
import time 
import subprocess


def force_quit_process(pid: str):
    #Note: script must run as root for this to work?
    cmd = ["kill", "-9", pid]
    print(cmd)
    out, err = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE
    ).communicate()
    #print("KILL RESULT: " + out.decode("utf-8"))
    return out.decode("utf-8")


def run_rcon(cmd: str, return_dict: Dict[str, any]) -> str:
    try:
        with Client(Config.rcon_ip, int(Config.rcon_port), passwd=Config.rcon_passwd) as client:
            response = client.run(cmd)

        #print("RCON RESPONSE: " + str(response))
        return_dict.update({"reply": response})
    except:
        traceback.print_exc()
        return_dict.update({"reply": "rcon exception"})

def run_rcon_safe(cmd: str) -> str:
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    p = multiprocessing.Process(target=run_rcon, args=(cmd, return_dict))
    p.start()
    p.join(10) # wait max 10 seconds for rcon - after that assume it crashed and must be force quit
    if p.is_alive():
        force_quit_process(str(p.pid))
        p.join(1)
        return "rcon timeout (you should try again in a minute or so)"

    return return_dict.get("reply", "no reply from rcon")


def main(argv) -> int:
    Config.load(argv)

    for i in range(0, 10):
        result = run_rcon_safe("quit")
        print("RCON RESULT " + result)
        if result == "Quit":      
            return 0
    
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))  # next section explains the use of sys.exit