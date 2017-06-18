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
    "F": {
        "name":"Superfungi Forest",
        "color":"|302",
        "desc":"Be it rainfall, faint filtered light, decaying matter, quantum "
               "irregularities or something else you'd rather not speculate "
               "upon, the fungi of this region have grown unchecked, perhaps "
               "for generations",
        "scan":"♣Ω♠",
        "pass":True
    },
    "w": {
        "name":"Ruined Wasteland",
        "color":"|111",
        "desc":"Countless generations ago, these dry, decaying and crumbling "
               "remains were part of other civilizations; perhaps those of "
               "great people?",
        "scan":"π▄▌",
        "pass":True
    },
    "_": {
        "name":"Rock Flats",
        "color":"|443", #or 240
        "desc":"Miles of featureless earth and rock cause the mind to wander "
               "wildly by the light of the dim star, but at least the footing "
               "is easy",
        "scan":'_._',
        "pass":True
    },
    "h": {
        "name":"Rock Hills",
        "color":"|221", #or 221
        "desc":"This is a stony and rocky land, and it tires the legs and ruins "
               "the shoes of those who travel it",
        "scan":"⌂^∩",
        "pass":True
    },
    "p": {
        "name":"Rock Fungi Plains",
        "color":"|415",
        "desc":"The wide world teems with life, home to at least hundreds of "
               "varieties of fungi, judging from what you've seen",
        "scan":"°σ•",
        "pass":True
    },
    "I": {
        "name":"Road",
        "color":"|555",
        "desc":"Crumbling roads and highways that certainly lead nowhere, but "
               "are your companions and guides, nonetheless",
        "scan":"I█I",
        "pass":True
    },
    "M": {
        "name":"Mountains",
        "color":"|222",
        "desc":"What madness lives in the mountains? The sooner you can depart "
               "from them and their starshadow, the better",
        "scan":"▲▲▲",
        "pass":True
    },
    "T": {
        "name":"Stalagmite Forest",
        "color":"|211",
        "desc":"Moving warily through the claustrophobic spines, spurs and "
               "columns is nerve-wracking, as they seem to have no end",
        "scan":'↑↑↑',
        "pass":True
    },
    "C": {
        "name":"Cavewall",
        "color":"|211",
        "desc":"Uncrossable cave wall",
        "scan":"▒▒▒",
        "pass":False
    },
    "~": {
        "name":'Deep "Water"',
        "color":"|040|[002",
        "desc":"You carefully cross the sinister water, hoping such long "
               "exposure to the fumes alone aren't enough to kill or mutate",
        "scan":"≈≈≈",
        "pass":False
    },
    "s": {
        "name": "Shallows",
        "color": "|240|[012",
        "desc": "You slosh for miles through irradiated wetland, trying  your "
                "best to ignore the stench, or at least not pass out from it",
        "scan": "~~~",
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