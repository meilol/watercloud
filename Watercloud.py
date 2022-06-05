import os, discord, mysql.connector
from discord.ext import commands
import pkg_resources
import pkg_resources

VERSION = "0.6.4"

print("Checking dependencies...")

dependencies = [
    "mysql-connector",
    "discord.py",
    "buttons",
    "requests"
]

try: pkg_resources.require(dependencies)
except pkg_resources.DistributionNotFound:
    print("Dependencies not found")
    print("Please install the following dependencies:")
    print(dependencies)
    exit()

print("No conflicts detected, all dependencies installed")

#! DATABASE CONFIGURATION: DO NOT EDIT

config = {
    "host":  "",
    "user": "",
    "password": "",
    "database": "",
    "raise_on_warnings": True,
}

try: #Everything
    cnx = mysql.connector.connect(**config)
    mycursor = cnx.cursor()
    print(f"Connected to {config['user']}")
except mysql.connector.Error as err: #This is fine
    print("You fucked up lmao" + err)
print("Loaded setup database successfully")

#! DATABASE CONFIGURATION: DO NOT EDIT

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', description="Watercloud | a closed-source multipurpose logging bot ", intents=intents, help_command=None)

for extension in os.listdir("./ext"):
    if extension.endswith('.py'):
        try:
            bot.load_extension(f'ext.{extension[:-3]}')
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

print('Initialized')            
bot.run("")