import discord , subprocess, sys
from discord.ext import commands
# from discord import app_commands
from discord import app_commands
from discord import Interaction
from settings import *
from datetime import datetime
from urllib.parse import urlparse
from os import path, getcwd, chdir, execl
from typing import List,Literal
from assets import CommandInjection
from assets import getIp
from assets import randomStrings
from assets import removeColors
from assets import Duplicates
from assets import removeString
from assets import logsParser
from assets import resolvedParser
from assets import fileSize
from assets import filesUploader
from assets import subdomainsFilter
from assets import pyExecute
from assets import commandsLogger
from assets import statusCode

# Define globals
logsItems = logsParser.logsParser()
if not logsItems or len(logsItems) == 0:
    logsItems = {}

resolvedItems = resolvedParser.resolvedParser()
if not resolvedItems or len(resolvedItems) == 0:
    resolvedItems = {}


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())
    
    async def on_ready(self):
        await self.tree.sync()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="skid trying use bot", details="just a automation penetration bot, Please use wisely"))
        print("Successfully synced commands")
        print(f"Logged onto {self.user}")\


bot = Bot()

# Util Bot commands 
@bot.tree.command(name="exec", description="executing a system shell directly into a server ( Admin Only )")
@commands.has_role(ADMIN_ROLE)
@app_commands.describe(argument='The payload that will execute')
async def exec(interaction: discord.Interaction, argument:str):
    try:
        Process = subprocess.Popen(argument, shell=True, executable="/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Results = Process.communicate()[0].decode('UTF-8')
        if len(Results) > 2000:
            RandomStr = randomStrings.Genrate()

            with open(f'messages/{RandomStr}' , 'w') as Message:
                Message.write(Results); Message.close()
                await interaction.response.send_message("Results: ", file=discord.File(f"messages/{RandomStr}"))
        else:
            if Results != '': await interaction.response.send_message(f'> **{argument}**\n```{Results}```')
            else: await interaction.response.send_message(f"**The Command You Performed Didn't Return an Output.**")
    except Exception as e:
        await interaction.response.send_message(f"**Your Command Returned an Error: {e}**")
        
@bot.tree.command(name="sudo", description="make a user to be sudo/admin")
@commands.has_role(ADMIN_ROLE)
async def sudo(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f"> Successfully added **{role.name}** to **{member.name}**")
    except Exception as e:
        await interaction.response.send_message(f"**Your Command Returned an Error: {e}**")
        
@bot.tree.command(name="unsudo", description="make a user to be unsudo/unadmin")
@commands.has_role(ADMIN_ROLE)
async def unsudo(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await interaction.response.send_message(f"> Successfully removed **{role.name}** from **{member.name}**")


@bot.tree.command(name="restart", description="restart a server")
@commands.has_role(ADMIN_ROLE)
async def restart(interaction: discord.Interaction):
    await interaction.response.send_message(f"**Restarting hackerman, It might take up to one minute**")
    python = sys.executable
    execl(python, python, * sys.argv)

@bot.tree.command(name="compile", description="compiled a python code")
@commands.has_role(ADMIN_ROLE)
async def compile(interaction: discord.Interaction, *, argument:str):
    Message = pyExecute.detectContent(argument)
    if Message != '':
        await interaction.response.send_message("**Compiled Python Code Output:**")
        await interaction.response.send_message(Message)
    else:
        await interaction.response.send_message("**The Python Code You Compiled Didn't Return an Output**")

# Error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if DEBUG:
        await interaction.followup.send(f"**got an error :**\n ```{error}```")
    else:
        await interaction.followup.send(f"**something wrong**")

# Sending Result to the user
async def sendResultTo(interaction: discord.Interaction, results: any):
    if not len(results) > 2000:
        await interaction.followup.send(f"**Results**\n{results}") 
    else: 
        RandomStr = randomStrings.Genrate()
        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(results)
            Message.close()
            await interaction.followup.send("**Results**\n", file=discord.File(f"messages/{RandomStr}"))
    await interaction.followup.send(f"\n- Done running requested by : **{interaction.user}**")    
     
# Networking tools
@bot.tree.command(name="networking", description="various networking tools such as nslookup, whois and more")
async def networking(interaction: discord.Interaction, tools: AVAILABLE_NETWORKING, argument:str):
    if tools == "nslookup":
        Results = subprocess.check_output(['nslookup', f'{argument}'] , shell=False).decode('UTF-8')
        await interaction.response.send_message(f'{Results}')
    elif tools == "whois":
        await interaction.response.send_message(f"starting WHOIS on {argument}")
        Output = subprocess.check_output(['whois', f'{argument}'], shell=False).decode('UTF-8')
        await sendResultTo(interaction,results=Output)
    elif tools == "dig":
        await interaction.response.send_message(f"starting DIG on {argument}")
        Output = subprocess.check_output(['dig', f'{argument}'] , shell=False).decode('UTF-8')
        await sendResultTo(interaction,results=Output)          
    elif tools == "ip":
        Message = getIp.getIp(Domain=argument)
        await interaction.response.send_message(Message)
    elif tools == "statuscode":
        await interaction.response.send_message(f"**Starting statuscode on {argument}**")
        URLparts = urlparse(argument)
        URLscheme = URLparts.scheme

        if URLscheme == '':
            argument = f"http://{argument}"
        elif URLscheme not in ["http", "https"]:
            await interaction.followup.send("**The URL scheme you're using isn't allowed**")
            return
        else:
            pass

        statusCodeDict = statusCode.getStatusCodes(argument)
        Message = ""

        for method,code in statusCodeDict.items():
            Message += f"{method}: {str(code)}\n"

        await interaction.followup.send(Message)
    elif tools == "prips":
            await interaction.response.send_message(f"**Prips start on :{argument}**")
            Output = subprocess.check_output(['prips', f'{argument}'] , shell=False)
            Output = Output.decode('UTF-8')
            await sendResultTo(interaction,results=Output)   
   
# Tools commands
@bot.tree.command(name="tools", description="various tools for recon")
async def tools(interaction: discord.Interaction, tools:AVAILABLE_TOOLS, argument:str):
    argument = CommandInjection.sanitizeInput(argument)
    if tools == "dirsearch":
        fileName = randomStrings.Genrate()
        dirsearchPath = TOOLS['dirsearch']
        chdir(dirsearchPath)
        await interaction.response.send_message(f"**Running Your Dirsearch Scan, We Will Send The Results When It's Done .This dirsearch maybe take a long time**")
        p = subprocess.Popen(f'python3 dirsearch.py -u {argument} -e "*" -o {BASE_PATH}/messages/{fileName} && python3 {BASE_PATH}/notify.py --mode 2 -m "Dirsearch results:" -f "- {interaction.user}" --file {fileName}', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        chdir(BASE_PATH)
        p.terminate()
    elif tools == 'arjun':
        await interaction.response.send_message(f"**Running Your Arjun Scan, We Will Send The Results When It's Done**")
        Process = subprocess.Popen(f'arjun -u {argument}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        Output = Process.communicate()[0].decode('UTF-8')
        Output = removeColors.Remove(Output)
        Output = removeString.removeString('Processing' , Output=Output)
        await sendResultTo(interaction,results=Output)
    elif tools == 'gitgraber':
        Path = TOOLS['gitgraber']; chdir(Path)
        await interaction.response.send_message(f"**Running Your GitGraber Scan, See gitGraber Channel For Possible Leaks**")
        p = subprocess.Popen(f'python3 gitGraber.py -k wordlists/keywords.txt -q {argument} -d' , shell=True , stdin=None, stdout=None, stderr=None, close_fds=True)
        chdir(Path)
        p.terminate()
    elif tools == 'waybackurls':
        await interaction.response.send_message(f"**Collecting Waybackurls, We Will Send The Results When It's Done**")
        Process = subprocess.Popen(f"echo {argument} | ~/go/bin/waybackurls",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Output =  Process.communicate()[0].decode('UTF-8')
        await sendResultTo(interaction,results=Output)
        Process.terminate()
    elif tools == 'subfinder':
        await interaction.response.send_message(f"**Collecting Subdomains Using Subdinder, We Will Send The Results When It's Done**")
        Process = subprocess.Popen(f"subfinder -d {argument} -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Output = Process.communicate()[0].decode('UTF-8')
        await sendResultTo(interaction,results=Output)
    elif tools == 'assetfinder':
        await interaction.response.send_message("**Collecting Subdomains Using Assetfinder, We Will Send The Results When It's Done**")
        Process = subprocess.Popen(f"assetfinder --subs-only {argument}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Output = Process.communicate()[0].decode('UTF-8')
        await sendResultTo(interaction,results=Output)
    elif tools == 'findomain':
        print(f'[{interaction.user}] running findomain for args {argument}')
        findomainPath = TOOLS['findomain']
        await interaction.response.send_message("**Collecting Subdomains Using Findomain, We Will Send The Results When It's Done**")
        Process = subprocess.Popen(f"{findomainPath} --target {argument} --quiet",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Output = Process.communicate()[0].decode('UTF-8')
        await sendResultTo(interaction,results=Output)
    elif tools == 'paramspider':
        paramPath = TOOLS['paramspider']
        await interaction.response.send_message("**Collecting Parameters Using ParamSpider, We Will Send The Results When It's Done**")
        Process = subprocess.Popen(f"python3 {paramPath}/paramspider.py -d {argument}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Output = Process.communicate()[0].decode('UTF-8')

        Output = removeColors.Remove(Text=Output)
        Output = Output.split('\n')
        urlsList = []
        for singleLine in Output:
            if singleLine.startswith('http'):
                urlsList.append(singleLine)
            else:
                pass

        Output = '\n'.join(urlsList)

        await sendResultTo(interaction,results=Output)
    elif tools == 'trufflehog':
        await interaction.response.send_message("**Starting trufflehog please wait**")
        urlParsed = urlparse(argument)
        urlHost = urlParsed.netloc
        if urlHost != "github.com" and urlHost != "gitlab.com":
            await interaction.followup.send("**You're trying to scan unallowed URL, please use a github/gitlab URL.**")
            return
        
        urlScheme = urlParsed.scheme
        if urlScheme not in ["http", "https"]:
            await interaction.followup.send("**You're trying to scan unallowed URL, please use a github/gitlab URL.**")
            return

        # status code validation
        statusCodeInteger = statusCode.getCode(argument)
        if statusCodeInteger == 404:
            await interaction.followup.send("**The project you're trying to scan doesn't exists, double check the URL**")
            return

        await interaction.followup.send(f"**Scanning {argument} for possible data leaks using truffleHog**")
        argument = CommandInjection.sanitizeInput(argument)
        _ = subprocess.Popen(f"trufflehog --regex --entropy=False {argument} | python3 notify.py --mode 1 -m 'truffleHog Results:' -f '- {interaction.user}'", shell=True , stdin=None, stdout=None, stderr=None, close_fds=True)
        await interaction.followup.send(f"**pyNotify gonna send the results when it's done**")
    elif tools == 'gitls':
            await interaction.response.send_message("**Collecting github projects using gitls**")
            Process = subprocess.Popen(f"echo https://github.com/{argument} | gitls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            Output = Process.communicate()[0].decode('UTF-8')
            await sendResultTo(interaction,results=Output)
    elif tools == 'katana':
        await interaction.response.send_message(f"**Scrap Using Katana, We Will Send The Results When It's Done**")
        Process = subprocess.Popen(f"katana -u {argument} -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Output = Process.communicate()[0].decode('UTF-8')
        await sendResultTo(interaction,results=Output)
        
bot.run(token=DISCORD_TOKEN)



# # # My Own Recon Data. It Isn't About You.
# # @Client.command()
# # async def recon(interaction , *, argument):
# #     if path.exists(f'/{USER}/{RECON_PATH}/{argument}'):
# #         try:
# #             Path = f'/{USER}/{RECON_PATH}/{argument}'.replace('//' , '/').replace('..', '')
# #             Data = open(Path).read().rstrip()
# #             Data = removeColors.Remove(Text=Data)
# #             Message = f"""```{Data}```"""
# #         except Exception:
# #             Message = f"**Couldn't Find The Recon Data With This Path: {argument}**"
# #     else:
# #         Message = "**Sorry The Path You Added Doesn't Exists On Our Records**"

# #     if len(Message) > 2000:
# #         RandomStr = randomStrings.Genrate()

# #         with open(f'messages/{RandomStr}' , 'w') as writerHere:
# #             writerHere.write(Message)
# #             writerHere.close()

# #             messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
# #             if not messageSize:
# #                 await interaction.response.send_message("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
# #                 return
# #             elif messageSize > 8:
# #                 URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
# #                 if not URL_:
# #                     await interaction.response.send_message("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
# #                     return
# #                 else:
# #                     await interaction.response.send_message(f"Recon Results: {URL_}")
# #             else:
# #                 await interaction.response.send_message("**Recon Results:**", file=discord.File(f"messages/{RandomStr}"))
# #                 await interaction.response.send_message(f"\n**- {interaction.user}**")
# #     else:
# #         await interaction.response.send_message(f'{Message}')



# # # Recon Collections


# # @Client.command()
# # async def info(interaction , *, argument):
# #     global logsItems

# #     try:
# #         subdomainsFile = logsItems[argument]
# #     except Exception:
# #         await interaction.response.send_message("**There's no subdomains has been collected for this target. please use** `/subdomains [TARGET]` **Then try again.**")
# #         retpri

# #     await interaction.response.send_message(f"**Getting Subdomains Information (titles , status-codes, web-servers) for {argument} using httpx.**")
# #     Process = subprocess.Popen(f"cat data/subdomains/{subdomainsFile} | httpx -title -web-server -status-code -follow-redirects -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
# #     httpxResults = Process.communicate()[0].decode('UTF-8')
# #     httpxResults = removeColors.Remove(Text=httpxResults)

# #     if len(httpxResults) > 2000:
# #         RandomStr = randomStrings.Genrate()

# #         with open(f'messages/{RandomStr}' , 'w') as Message:
# #             Message.write(httpxResults)
# #             Message.close()

# #             messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
# #             if not messageSize:
# #                 await interaction.response.send_message("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
# #                 return
# #             elif messageSize > 8:
# #                 URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
# #                 if not URL_:
# #                     await interaction.response.send_message("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
# #                     return
# #                 else:
# #                     await interaction.response.send_message(f"Httpx Results: {URL_}")
# #             else:
# #                 await interaction.response.send_message("**Httpx Results:**", file=discord.File(f"messages/{RandomStr}"))
# #                 await interaction.response.send_message(f"\n**- {interaction.user}**")
# #     else:
# #         await interaction.response.send_message(f"**Httpx Results For {argument}:**")
# #         await interaction.response.send_message(f'```{httpxResults}```')
# #         await interaction.response.send_message(f"\n**- {interaction.user}**")

# # # Tools collection
# # @Client.command()
# # async def nuclei(interaction, *, argument):
# #     global logsItems
# #     nucleiTemplates = TOOLS['nuclei-templates']

# #     try:
# #         subdomainsFile = logsItems[argument]
# #     except Exception:
# #         await interaction.response.send_message("**There's no subdomains has been collected for this target. please use** `/subdomains [TARGET]` **Then try again.**")
# #         return

# #     await interaction.response.send_message(f"**Scanning {argument} For Possible Issues Using Nuclei.**")
# #     try:
# #         if DISABLE_NUCLEI_INFO:
# #             _ = subprocess.Popen(f"./nuclei -l data/subdomains/{subdomainsFile} -t {nucleiTemplates} -silent | grep -v 'info.*\]' | python3 notify.py --mode 0 --discord-webhook {NUCLEI_WEBHOOK}",shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
# #         else:
# #             _ = subprocess.Popen(f"./nuclei -l data/subdomains/{subdomainsFile} -t {nucleiTemplates} -silent | python3 notify.py --mode 0 --discord-webhook {NUCLEI_WEBHOOK}", shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
# #         await interaction.response.send_message("**Results gonna be sent to nuclei webhook channel**")
# #     except Exception as e:
# #         await interaction.response.send_message("**Err : " + str(e))

# # @Client.command()
# # async def subjack(interaction , *, argument):
# #     global resolvedItems
# #     argument = CommandInjection.sanitizeInput(argument)

# #     try:
# #         resolvedFile = resolvedItems[argument]
# #         fileStr = randomStrings.Genrate()
# #     except Exception:
# #         await interaction.response.send_message("**There's no subdomains has been collected for this target. please use** `/subdomains [TARGET]` **Then try again.**")
# #         return

# #     await interaction.response.send_message(f"**Scanning {argument} For Possible Subdomains Takeover Issues Using Subjack**")
# #     _ = subprocess.Popen(f"subjack -w data/hosts/{resolvedFile} -t 100 -timeout 30 -o data/subjack/{argument}-{fileStr}.subjack -ssl | python3 notify.py --mode 1 -m 'Subjack results:' -f '- {interaction.user}'", shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)

# #     await interaction.response.send_message(f"**Results gonna be sent to the results channel soon**")

# # @Client.command()
# # async def subjs(interaction , *, argument):
# #     global logsItems
# #     argument = CommandInjection.sanitizeInput(argument)

# #     try:
# #         subdomainsFile = logsItems[argument]
# #     except Exception:
# #         await interaction.response.send_message("**There's no subdomains has been collected for this target. please use** `/subdomains [TARGET]` **Then try again.**")
# #         return

# #     await interaction.response.send_message(f"**Extracting JS Files From {argument} Using Subjs**")
# #     _ = subprocess.Popen(f"cat data/subdomains/{subdomainsFile} | subjs | python3 notify.py --mode 1 -m 'Subjs results:' -f '- {interaction.user}'", shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
# #     await interaction.response.send_message(f"**Results gonna be sent soon on the results channel**")

# # @Client.command()
# # async def smuggler(interaction, *, argument):
# #     global logsItems
# #     argument = CommandInjection.sanitizeInput(argument)

# #     try:
# #         subdomainsFile = logsItems[argument]
# #     except Exception:
# #         await interaction.response.send_message("**There's no subdomains has been collected for this target. please use** `/subdomains [TARGET]` **Then try again.**")
# #         return

# #     smugglerPath = TOOLS['smuggler']
# #     await interaction.response.send_message(f"**Scanning {argument} For HTTP Request Smuggling Issues Using Smuggler**")

# #     if "http:" in argument or "https:" in argument:
# #         Process = subprocess.Popen(f"echo {argument} | python3 {smugglerPath}/smuggler.py",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
# #         smugglerResults = Process.communicate()[0].decode('UTF-8')
# #     else:
# #         Process = subprocess.Popen(f"cat data/subdomains/{subdomainsFile} | python3 {smugglerPath}/smuggler.py",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
# #         smugglerResults = Process.communicate()[0].decode('UTF-8')

# #     smugglerResults = removeColors.Remove(Text=smugglerResults)
# #     if len(smugglerResults) > 2000:
# #         RandomStr = randomStrings.Genrate()

# #         with open(f'messages/{RandomStr}' , 'w') as Message:
# #             Message.write(smugglerResults)
# #             Message.close()

# #             messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')

# #             if not messageSize:
# #                 await interaction.response.send_message("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
# #                 return
# #             elif messageSize > 8:
# #                 URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
# #                 if not URL_:
# #                     await interaction.response.send_message("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
# #                     return
# #                 else:
# #                     await interaction.response.send_message(f"Smuggler Results: {URL_}")
# #             else:
# #                 await interaction.response.send_message("**Smuggler Results:**", file=discord.File(f"messages/{RandomStr}"))
# #                 await interaction.response.send_message(f"\n**- {interaction.user}**")
# #     else:
# #         await interaction.response.send_message(f"**Smuggler Results For {argument}:**")
# #         await interaction.response.send_message(f'```{smugglerResults}```')
# #         await interaction.response.send_message(f"\n**- {interaction.user}**")

# # # Showing Current Recon Data
# # @Client.command()
# # @commands.has_role(ADMIN_ROLE)
# # async def show(interaction):
# #     global logsItems

# #     targetsList = []
# #     for site,_ in logsItems.items():
# #         targetsList.append(site)

# #     targetsMessage = '\n'.join(targetsList)
# #     targetsMessage = f"""```
# #     {targetsMessage}
# #     ```
# #     """
# #     await interaction.response.send_message(f"**Available records: \n\n{targetsMessage}**")

# # @Client.command()
# # @commands.has_role(ADMIN_ROLE)
# # async def count(interaction , *, argument):
# #     global logsItems , resolvedItems

# #     try:
# #         resolvedFile = resolvedItems[argument]
# #         resolvedContent = open(f'data/hosts/{resolvedFile}' , 'r').readlines()
# #         resolvedLength = len(resolvedContent)
# #     except Exception:
# #         await interaction.response.send_message("**There's no subdomains has been collected for this target. please use ** `/subdomains [TARGET]` ** Then try again.**")
# #         return

# #     try:
# #         subdomainsFile = logsItems[argument]
# #         subdomainsContent = open(f'data/subdomains/{subdomainsFile}' , 'r').readlines()
# #         subdomainsLength = len(subdomainsContent)
# #     except Exception:
# #         await interaction.response.send_message("**There's no subdomains has been collected for this target. please use** `/subdomains [TARGET]` **Then try again.**")
# #         return

# #     await interaction.response.send_message(f"**{argument}:\n\t\tResolved hosts: {str(resolvedLength)}\n\t\tLive subdomains: {str(subdomainsLength)}**")

# # @Client.command()
# # @commands.has_role(ADMIN_ROLE)
# # async def history(interaction):
# #     commandsContent = open('data/logs/commands.easy', 'r').read()
# #     await interaction.response.send_message(f"**DiscordRecon gonna send you the results in your DM**")

# #     if len(commandsContent) < 2000:
# #         await interaction.user.send('**Users Commands:**')
# #         await interaction.user.send(f'```{commandsContent}```')
# #     else:
# #         RandomStr = randomStrings.Genrate()
# #         with open(f'messages/{RandomStr}' , 'w') as Message:
# #             Message.write(commandsContent)
# #             Message.close()

# #         await interaction.user.send("**Users Commands:**", file=discord.File(f"messages/{RandomStr}"))

# # Main Event With Admin Channel Logger.
# @Client.event
# async def on_command_error(interaction, error):
#     if isinstance(error, commands.CommandNotFound):
#         await interaction.response.send_message("**Invalid command, please type `.help` to see the list of commands and tools.**")
#     elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
#         await interaction.response.send_message("**You don't have permession to use this command, role is required**")
#     else:
#         await interaction.response.send_message(f"**Unknown error: {error}**")

# @Client.event
# async def on_command(interaction):
#     Author = interaction.author
#     Command = interaction.command
#     Message = interaction.message.content

#     Date = datetime.now()
#     Date = f"{Date.year}:{Date.month}:{Date.day}"

#     commandsLogger.logCommand(Command, Author, Date, Message)

# @Client.event
# async def on_member_join(member):
#     welcomeMessage = f"""```
#     Welcome to Discord-Recon, a discord bot created to help bug bounty hunters with thier reconnaissance process from discord using simple commands
#     You can use the bot on the server, or if you wanna keep your recon data private you can always use the bot commands on the chat here 

#     In case you wanna host your own discord-recon server you can always use the source code at https://github.com/DEMON1A/Discord-Recon
#     And you can always support us at https://www.patreon.com/MohammedDief or https://paypal.me/MohammedDieff 
#     All of the donations goes for upgrading the server, and paying some of the VPS monthly payment
#     ```"""
#     await member.send(welcomeMessage)

# @Client.event
# async def on_member_remove(member):
#     adminChannel = Client.get_channel(ADMIN_CHANNEL)
#     await adminChannel.send(f"**{member}** has left the server.")

# @Client.event
# async def on_ready():
#     await Client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="skid trying use bot"))
#     adminChannel = Client.get_channel(ADMIN_CHANNEL)
#     if adminChannel:
#         try:
#             synced = await Tree.sync()
#             Dates = datetime.now()
#             Message = f"ReconServer started to work at {Dates.year}-{Dates.month}-{Dates.day}** \n**Synced ```{synced}``` "
#             await adminChannel.send(Message)
#         except Exception as e:
#             print('some failed : {e}')
#     else:
#         print("cant get admin channel")
        
# @Tree.command(name="subdomains", description = "subfinder, findomain, assetfinder")
# async def subdomains(interaction: Interaction,item: str):
#     global logsItems, resolvedItems
#     argument = CommandInjection.sanitizeInput(item)

#     '''
#     Subdomains collections gonna use three tools
#     subfinder, findomain, assetfinder

#     it won't use amass until we upgrade the server. if you're a developer
#     and you want to add amass. i guess you know what todo.
#     '''

#     await interaction.response.send(f"**Collecting Subdomains For {argument}, Gonna Send You It When It's Done**")

#     # global paths
#     findomainPath = TOOLS['findomain']

#     # findomain Subdomains
#     Process = subprocess.Popen(f"{findomainPath} --target {argument} --quiet",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     findomainResults = Process.communicate()[0].decode('UTF-8')

#     # assetfinder Subdomains
#     Process = subprocess.Popen(f"assetfinder --subs-only {argument}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     assetfinderResults = Process.communicate()[0].decode('UTF-8')

#     # subfinder Subdomains
#     Process = subprocess.Popen(f"subfinder -d {argument} -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     subfinderResults = Process.communicate()[0].decode('UTF-8')

#     # filter duplicates
#     allSubdomains = findomainResults + assetfinderResults + subfinderResults
#     allSubdomains = Duplicates.Duplicates(Subdomains=allSubdomains)
#     allSubdomains = subdomainsFilter.vSubdomains(sList=allSubdomains, huntingTarget=argument)

#     # saving subdomains
#     fileName = randomStrings.Genrate()
#     resolvedName = randomStrings.Genrate()

#     currentPath = getcwd()
#     allSubdomains = '\n'.join(allSubdomains)

#     with open(f'data/hosts/{resolvedName}' , 'w') as subdomainsFile:
#         subdomainsFile.write(allSubdomains); subdomainsFile.close()

#     # add resolved into logs
#     resolvedParser.resolvedWriter(Target=argument , fileName=f"{resolvedName}\n")
#     resolvedItems[argument] = resolvedName

#     # validate subdomains
#     Process = subprocess.Popen(f"cat data/hosts/{resolvedName} | httpx -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     httpxResults = Process.communicate()[0].decode('UTF-8')

#     # saving httpx results
#     with open(f'data/subdomains/{fileName}' , 'w') as subdomainsFile:
#         subdomainsFile.write(httpxResults); subdomainsFile.close()

#     # add results into logs
#     logsParser.logsWriter(Target=argument , fileName=fileName)
#     logsItems[argument] = fileName

#     # send httpx results
#     if len(httpxResults) > 2000:
#         RandomStr = randomStrings.Genrate()

#         with open(f'messages/{RandomStr}' , 'w') as Message:
#             Message.write(httpxResults)
#             Message.close()

#             messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
#             if not messageSize:
#                 await interaction.response.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
#                 return
#             elif messageSize > 8:
#                 URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
#                 if not URL_:
#                     await interaction.response.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
#                     return
#                 else:
#                     await interaction.response.send(f"Httpx Results: {URL_}")
#             else:
#                 await interaction.response.send("**Httpx Results:**", file=discord.File(f"messages/{RandomStr}"))
#                 await interaction.response.send(f"\n**- {interaction.response.message.author}**")
#     else:
#         await interaction.response.send(f"**Subdomains For {argument}:**")
#         await interaction.response.send(f'```{httpxResults}```')
#         await interaction.response.send(f"\n**- {interaction.response.message.author}**")
# if __name__ == "__main__":
#     Client.run(DISCORD_TOKEN)
