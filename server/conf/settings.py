"""
Evennia settings file.

The available options are found in the default settings file found
here:

e:\muddev\evennia\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "WarrensMUD"

# open to the internet: 4000, 8000, 8001
# closed to the internet (internal use): 5000, 5001
TELNET_PORTS = [4000]
WEBSOCKET_CLIENT_PORT = 8001
WEBSERVER_PORTS = [(8000, 5001)]
AMP_PORT = 5000

# Interface addresses to listen to. If 0.0.0.0, listen to all. Use :: for IPv6.
TELNET_INTERFACES = ['0.0.0.0']
# Interface addresses to listen to. If 0.0.0.0, listen to all. Use :: for IPv6.
WEBSOCKET_CLIENT_INTERFACE = '0.0.0.0'
# This is a security setting protecting against host poisoning
# attacks.  It defaults to allowing all. In production, make
# sure to change this to your actual host addresses/IPs.
ALLOWED_HOSTS = ["*"]

# uncomment to take server offline
# LOCKDOWN_MODE = True

# Register with game index (see games.evennia.com for first setup)
# GAME_DIRECTORY_LISTING = {
#     'game_status': 'pre-alpha',
#     'game_website': 'http://warrensmud.com:4002',
#     'listing_contact': 'pipplepopple@gmail.com',
#     'telnet_hostname': 'warrensmud.com',
#     'telnet_port': 4000,
#     'short_description': "WarrensMUD",
#     'long_description':'A multiplayer, roguelike text adventure set '
#     'in an ominous underground world.'
# }

######################################################################
# Django web features
######################################################################


# The secret key is randomly seeded upon creation. It is used to sign
# Django's cookies. Do not share this with anyone. Changing it will
# log out all active web browsing sessions. Game web client sessions
# may survive.
SECRET_KEY = 'a/7Oy8[>H-3BbA(c6&Tn_qVuh,5:@p?jkdJ.lXYv'

######################################################################
# WarrensMUD config
######################################################################

# This enables in-game debugging.  Should be disabled before beta.
IN_GAME_ERRORS = True