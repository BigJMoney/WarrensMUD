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
        "desc":"This is a forest",
        "scan":"ff",
        "pass":True
    },
    "w": {
        "name":"Wasteland",
        "color":"|111",
        "desc":"This is a wasteland",
        "scan":"ww",
        "pass":True
    },
    "g": {
        "name":"Grassland",
        "color":"|230", #or 240
        "desc":"This is some grassland",
        "scan":"gg",
        "pass":True
    },
    "h": {
        "name":"Hills",
        "color":"|321", #or 221
        "desc":"Here are yon hills",
        "scan":"hh",
        "pass":True
    },
    "p": {
        "name":"Plains",
        "color":"|531",
        "desc":"Plains stretch as far as...well you get the point",
        "scan":"pp",
        "pass":True
    },
    "I": {
        "name":"Road",
        "color":"|555",
        "desc":"A crumbling road snakes through the wilderness",
        "scan":"II",
        "pass":True
    },
    "M": {
        "name":"Mountain",
        "color":"|333",
        "desc":"Upon a mountain range",
        "scan":"MM",
        "pass":True
    },
    "m": {
        "name":"Marsh",
        "color":"|415|[011",
        "desc":"You slog through some marshland",
        "scan":"mm",
        "pass":True
    },
    "C": {
        "name":"Cavewall",
        "color":"|211",
        "desc":"Uncrossable cave wall",
        "scan":"CC",
        "pass":False
    },
    "r": {
        "name":"Water",
        "color":"|115",
        "desc":"How did you get here, are you Jesus?",
        "scan":"rr",
        "pass":True
    },
    ".": {
        "name":"out_of_bounds",
        "color":"|000",
        "desc":"sectorbounds_error!",
        "scan":"..",
        "pass":False
    },
# A catch-all replacement for unexpected glyph errors in the map
    "!": {
        "name":"unknown_glyph",
        "color":"|500",
        "desc":"glyphlegend_error!",
        "scan":"!!",
        "pass":True
    }
}