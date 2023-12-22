from os import path
from urllib.parse import urlparse
from typing import Literal

BASE_PATH = path.abspath(path.join(__file__, "../"))
DISCORD_TOKEN = ""
DEFAULT_DISCORD_WEBHOOK = ""
USER = "/home/reconbot"
ADMIN_ROLE ="♾️ MC"
RECON_PATH = "/home/reconbot"
DEBUG = True
ADMIN_CHANNEL = 123431512342145
ADMIN_CHANNEL = int(urlparse(str(ADMIN_CHANNEL)).path.split('/')[-1:][0])
DISABLE_NUCLEI_INFO = False
NUCLEI_WEBHOOK = ""
COMMANDS_PREFIX = "!"
AVAILABLE_NETWORKING = Literal[
    "nslookup",
    "whois",
    "dig",
    "ip",
    "statuscode", 
    "prips",
    "dig"
]
AVAILABLE_TOOLS = Literal[
    "dirsearch",
    "arjun",
    "gitgraber",
    "waybackurls",
    "subfinder", 
    "assetfinder",
    "findomain", 
    "paramspider", 
    "trufflehog", 
    "gitls", 
    "katana"
]

TOOLS = {
    "dirsearch": f"{BASE_PATH}/tools/dirsearch/",
    "gitgraber": f"{BASE_PATH}/tools/gitGraber/",
    "findomain": f"{BASE_PATH}/tools/findomain-linux",
    "nuclei-templates": f"{BASE_PATH}/tools/nuclei-templates/",
    "paramspider": f"{BASE_PATH}/tools/ParamSpider/",
    "smuggler": f"{BASE_PATH}/tools/smuggler/"
}

RCE = [';' , '`' , '$' , '(' , ')' , '|' , '&' , '%', '\n', '<', '>']
