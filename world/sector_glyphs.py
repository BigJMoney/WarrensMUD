# -*- coding: UTF-8 -*-
"""
Sector Glyphs

The legend of map string glyphs and their Loc properties. Edit this file to
change those of any map location.

Properties:
    name: The Loc name
    color: Color shown in the minimap (xterm256 string)
    desc: The Loc description
    pass: Whether this character is passable or impassable by objects

"""
glyph_legend = {
    "f": {
        "name":"Forest",
        "color":"|020",
        "desc":"Can't see very far in the forest",
        "scan":"FFF",
        "pass":True
    },
    "w": {
        "name":"Wasteland",
        "color":"|111",
        "desc":"A wasteland of rubble and debris",
        "scan":"w.w",
        "pass":True
    },
    "g": {
        "name":"Grassland",
        "color":"|230", #or 240
        "desc":"Grass sways in the breeze for miles",
        "scan":'"""',
        "pass":True
    },
    "h": {
        "name":"Hills",
        "color":"|321", #or 221
        "desc":"Hiking through the hills is a tiring effort",
        "scan":"hhh",
        "pass":True
    },
    "p": {
        "name":"Plains",
        "color":"|531",
        "desc":"Plains stretch as far as...well you get the point",
        "scan":"_._",
        "pass":True
    },
    "I": {
        "name":"Road",
        "color":"|555",
        "desc":"A crumbling road snakes through the wilderness",
        "scan":".I.",
        "pass":True
    },
    "M": {
        "name":"Mountain",
        "color":"|333",
        "desc":"Upon a mountain range, surveying the land around you",
        "scan":"/M\\",
        "pass":True
    },
    "m": {
        "name":"Marsh",
        "color":"|415|[011",
        "desc":"You slog through some stinking marshland",
        "scan":'"""',
        "pass":True
    },
    "C": {
        "name":"Cavewall",
        "color":"|211",
        "desc":"Uncrossable cave wall",
        "scan":"[C]",
        "pass":False
    },
    "r": {
        "name":"River",
        "color":"|115",
        "desc":"How did you get here, are you Jesus?",
        "scan":"~~~",
        "pass":False
    },
    "s": {
        "name": "Shallows",
        "color": "|235",
        "desc": "A place where water is shallow enough to ford",
        "scan": "~s~",
        "pass": True
    },
    ".": {
        "name":"out_of_bounds",
        "color":"|000",
        "desc":"sectorbounds_error!",
        "scan":"...",
        "pass":False
    },
    # A catch-all replacement for unexpected glyph errors in the map
    "!": {
        "name":"unknown_glyph",
        "color":"|500",
        "desc":"glyphlegend_error!",
        "scan":"!!!",
        "pass":True
    }
}