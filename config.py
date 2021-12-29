from typing import Dict
import os
import argparse

class Config:

    discord_bot_token = ""
    discord_channel_id = ""
    rcon_ip = ""
    rcon_passwd = ""
    rcon_port = 0

    @classmethod
    def load(cls, arg: Dict[str, str] = None, path = None):
        
        configFilePath = path

        # process command line args
        parser = argparse.ArgumentParser()
        parser.add_argument("--config", help="force a config path", default="")
        args = parser.parse_args()
            
        if args.config: 
            configFilePath = args.config

        #get the configuration file path
        if not configFilePath:
            try:
                configFilePath = open("config_path", 'r').read().rstrip("\n\r")
            except FileNotFoundError:
                print("WARN: using fallback config path /home/ubuntu/config")
                configFilePath = "/home/ubuntu/config"
                
        print("load config from: " + configFilePath)
                   
        config_values = {}
        with open(configFilePath, 'r') as confFile:
            confFileLines = confFile.readlines()
            for line in confFileLines:

                split_idx = line.find("=")
                key = line[0:split_idx].rstrip("\n\r")
                value = line[split_idx+1:].rstrip("\n\r")
                #print("CONF " + key + "=" + value)
                config_values.update({key:value})
            
        #process config file values
        #testing
        cls.discord_bot_token = config_values.get("discord_bot_token",cls.discord_bot_token)
        cls.discord_channel_id = config_values.get("discord_channel_id",cls.discord_channel_id)
        cls.rcon_ip = config_values.get("rcon_ip",cls.rcon_ip)
        cls.rcon_passwd = config_values.get("rcon_passwd",cls.rcon_passwd)
        cls.rcon_port = config_values.get("rcon_port",cls.rcon_port)
        #cls.graylog_enable = config_values.get("graylog_enable","false") in ["yes", "y", "true", "1"]
        print("CONFIG LOADING DONE")