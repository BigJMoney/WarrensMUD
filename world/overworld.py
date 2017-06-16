"""
Overworld

This module governs everything relating to the Overworld and its basic
navigation.

Usage:

    @py from world import overworld; overworld.create_overworld()
    @py from world import overworld; overworld.enter_sector(me)
    @py from world import overworld; overworld.destroy_overworld()

Implementation details:

    An Overworld handles the creation of the world by creating a node map
    of sectors, and then fills in each sector with a map (courtesy of the
    evennia wilderness contrib from titeuf87).

    It also handles recruit and other object movement throughout the overworld.

    The SectorRoom class has some extended functionality beyond evennia Rooms

    Recruit maps are also managed by the RecruitMapperScript

"""
import random

import world.sector_glyphs
from evennia import logger
from typeclasses.scripts import Script
from evennia import create_script
import wilderness

def create_overworld():
    """
    Test function to get the ball rolling
    """
    create_script(Overworld, key="overworld")

def enter_sector(obj, coords=(0, 0), name='1'):
    """
    Test function to get the player into a sector
    """
    sec = Sector.objects.get(db_key=name)
    if sec.is_valid_coordinates(coords):
        sec.move_obj(obj, coords)
        return True
    else:
        return False

def destroy_overworld():
    for i in range(1, 101):
        print(i)
        try:
            script = Sector.objects.get(db_key=str(i))
            script.stop()
        except Sector.DoesNotExist:
            pass

        # Sector.objects.get(db_key='2').stop()

class Overworld(wilderness.WildernessScript):
    """
    Creates a world map (nodes of sectors) upon creation, but can also create
    a new one during a world storm.

    """
    def at_script_creation(self):
        """
        Associates each type of map glyph with properties (name, desc, etc)
        This data will likely be store elsewhere eventually to keep the code
        clean

        This function creates a new world but it doesn't delete the previous
        one which would still be present in the db with all its sectors.

            Args:
                map_config: A dict pairing overworld levels with the size (in
                sectors) to make them
        """
        # The legend for loc names and descriptions, for each map glyph
        self.db.glyph_legend = world.sector_glyphs.glyph_legend
        # The number of sectors per world level
        # TODO: Implement retrieval from settings.py
        self.db.map_config = { 1:100 }
        # Sector counter to create unique keys from
        self.db.numsectors = 0
        logger.log_info("OverworldInit: PLACEHOLDER: Retrieved world makeup "
                        "from settings.py")
        # A map of world node coordinates to sector objects
        self.db.worldmap = {}
        for level in self.db.map_config:
            self.db.worldmap[level] = {}

        # Make a world!
        self.world_storm(dict(self.db.map_config))

    # @property
    # def numsectors(self):
    #     """
    #     Shortcut property to the map provider.
    #
    #     Returns:
    #         MapProvider: the mapprovider used with this wilderness
    #     """
    #     return self.db.numsectors

    def create_mapnodes(self, size):
        """
        Creates a map of hexagonal nodes and all their neighbors

        Starting with (0,0) randomly generate a map of hexagonally linked world
        coords, adding each set of coords to a list. Then pass this list into
        create_neighbors

        Args:
            size: number of desired sector nodes to create

        Returns:
            A dict of world coordinates to neighbors
        """

        # TODO: Algorithm for creating a list of connected sector nodes
        logger.log_info("WorldStorm: PLACEHOLDER: Generated world node map")

        # TODO: Take the list, figure out the neighbors and what hex side they're on and associate all neighbor-sides (tuple) for each coordinate on the list
        logger.log_info("WorldStorm: PLACEHOLDER: Determined node neighbors")

        placeholder = {}
        for num in range(size):
            placeholder['ph_coord' + str(num)] = (1,2,3)
        return placeholder
        pass

    def create_sector(self):
        """
        Creates a sector and its script

        Maybe one day I want this to accept a biome/region/terrain type?

        Returns:
             a SectorMapProvider instance
        """
        # Our sector map
        secmap_str = ''

        # TODO: Algorithm to create a sector
        # Currently I'm pulling from a hand-made file
        str_file = open('.\\world\\sector_proto.txt')
        secmap_str = str_file.read()
        logger.log_info("WorldStorm: PLACEHOLDER: Generated a sector")

        # Create a Sector with a unique key; not sure if needed though
        script = create_script(Sector, key=str(self.db.numsectors+1))
        # Increase our unique keyname counter
        self.db.numsectors = self.db.numsectors + 1
        mapprovider = SectorMapProvider(secmap_str)
        script.db.mapprovider = mapprovider
        logger.log_info("WorldStorm: PLACEHOLDER: Sector created")
        return mapprovider

    def caveinate_sectors(self, secmap, neighbormap):
        """
        Identifies sector connections and creates the world's cave walls
        accordingly.

        Args:
            secmap: Dict of coord:sector pairs
            neighbormap: Dict of coord:neighbors (tuples) pairs
        """
        for coord in secmap:
            sec = secmap[coord]
            for side in neighbormap[coord]:
                # TODO: Use the coord and the side to determine neighbor_coord
                neighbor_coord = 'placeholder'
                # 'Move' the sector to where it belongs on the node map
                sec.neighbors = {}
                sec.neighbors[side] = neighbor_coord
            logger.log_info("WorldStorm: PLACEHOLDER: Set neighbors for "
                            "sector {}".format(str(coord)))
            # TODO: Code to 'decaveinate' this sctor
            logger.log_info("WorldStorm: PLACEHOLDER: Decaveinated sector "
                            "sector {}".format(str(coord)))
            # TODO: Code to 'caveinate' this sector according to its new neighbors
            logger.log_info("WorldStorm: PLACEHOLDER: Caveinated sector "
                            "sector {}".format(str(coord)))

    def world_storm(self, map_config):
        """
        Scrambles the current world map, randomizing all the sector nodes.
        This will be run automatically by the MUD on some cadence or at some
        trigger which is still TBD.

        Args:
            map_config: A dict pairing overworld levels with the size
            (in sectors) to make them
        """
        # TODO: Function to broadcast the storm and bar cross-sector travel
        # I think I want it to last 5 minutes

        # Map of coordinates:neighbor_sides
        neighbormap = {}
        # How many seconds a world storm lasts
        locktime = 300

        for level in list(self.db.map_config.keys()):
            # Combines existing sectors with newly created ones
            secs = []
            # Create node map of coords:neighbors
            neighbormap.update(self.create_mapnodes(self.db.map_config[level]))
            logger.log_info("WorldStorm: PLACEHOLDER: Node map finished")
            logger.log_info("WorldStorm: Map of neighbors created")
            if self.db.map_config[level] < 1:
                logger.log_error("WorldStorm: ERROR: Overworld.map_config "
                                "is less than 1. This is not the proper way to "
                                "erase a level. Fix in settings.py. Aborting "
                                "world storm.")
                return False
            # Code if there is an existing overworld
            if len(self.db.worldmap[level]) > 0:
                if len(self.db.worldmap[level]) > len(neighbormap):
                    logger.log_error("WorldStorm: ERROR: Overworld.map_config "
                                    "is less than the existing world size. Fix "
                                    "in settings.py. Aborting world storm.")
                    return False
                # TODO: Broadcast the storm and lock down inter-sector travel 5 mins
                logger.log_info("WorldStorm: PLACEHOLDER: Broadcast storm and "
                                "locked intersector travel for "
                                "{} minutes...".format(locktime))
                # Make a list of our existing sectors and shuffle them
                secs_old = list(self.db.worldmap[level].values())
                random.shuffle(secs_old)
                # And add them to the big list of sectors
                secs = secs + secs_old
            diff = len(neighbormap) - len(self.db.worldmap[level])
            # Code if the new scrambled will be larger than previous (or is new)
            if diff > 0:
                # Maybe one day I want to run a function here that picks biomes
                # for the new neighbormap and assigns them as a biomemap. Then I
                # can pass biome to create_sector() in the comprehension below.

                secs_new = [self.create_sector() for s in range(diff)]
                logger.log_info("WorldStorm: New sectors created")
                secs = secs + secs_new
            # Create final world map of sectors
            # self.db.worldmap[level] = {coord:sec for coord,sec in \
            #                        zip(neighbormap,secs)}
            combined_map = list(zip(list(neighbormap.keys()), secs))
            for coord, sec in combined_map:
                self.db.worldmap[level][coord] = sec

            logger.log_info("WorldStorm: World maps created")
            # caveinate this level
            self.caveinate_sectors(dict(self.db.worldmap[level]), neighbormap)

class Sector(wilderness.WildernessScript):
    """
    Just a name change wrapper for now, but may be used in the future.
    """
    pass

class SectorMapProvider(wilderness.WildernessMapProvider):
    """
    Documentation on mapproviders can be found in evennia/contrib/wilderness.py

    See the functions below for this class's extensions
    """

    # Associates this hex's sides (ints) with a ref to the neighbor sector
    # Shit, I think this is invalid in Evennia... non db objects cannot
    # store db objects and expect them to be saved
    # I might need to save this as an attribute on the Sector itself
    # Or I could have this associated with the Sector key instead of ref
    neighbors = {}

    def __init__(self, map_str):
        """
        Args:
            map_str: This sector's map string
        """
        self.map_str = map_str
        # Legend of glyphs (dict)

    def glyph_coordinates(self, coords):
        """
        Translates sector (game) coordinates into glyph (map_str) coordinates

        This is needed because the string places 0,0 in the bottom left, while
        the game places 0,0 in the center of the sector hex

            Args:
                coords: The game coordinates to translate

            Returns:
                Tuple of coordinates that self.map_str can use
        """
        # The translation
        coords_offset = (36, 32)

        # Translate map coords into glyph coords
        gcoords = tuple(a + b for a, b in zip(coords, coords_offset))
        return gcoords

    def find_glyph(self, gcoords):
        """
        Find the character in self.map_str, given its coordinates

        Args:
            gcoords: Coordinates (in map_str/glyph translation)
        Returns:
            The glyph string
        """
        # Not saved on the SectorMapProvider because it needs to be loaded fresh
        legend = world.sector_glyphs.glyph_legend
        gx, gy = gcoords
        rows = self.map_str.split("\n")

        # Coordinates begin at the bottom row, not the top
        rows.reverse()
        # Y coordinate must exist on the map
        try:
            row = rows[gy]
        except IndexError:
            glyph = 'invalid'
            return glyph
        # X coordinate must exist on the map
        try:
            glyph = row[gx]
        except IndexError:
            glyph = 'invalid'
            return glyph
        # If the player runs into a glyph not in the legend, make it an error
        if glyph not in legend:
            glyph = '!'
        return glyph

    def is_valid_coordinates(self, overworld, coords):
        """
        Uses the map string to check if the coordinates are valid to move to
        Needs to check for cave walls and movement into adjacent sectors

        Args:
            overworld: Ref to the Overworld (caller)
            coords: The coordinates to validate

        Returns:
            Not sure yet :) Possibly true, false or a ref to a neighbor
        """
        legend = world.sector_glyphs.glyph_legend
        # The characters that define impassable spaces (out of bounds)
        oob_glyphs = [gkey for gkey in legend if legend[gkey]["pass"] == False]
        # oob_glyphs = []
        # # Find and set our impassable glyphs
        # legend = world.sector_glyphs.glyph_legend
        # for gkey in legend:
        #     if legend[gkey]["pass"] == False:
        #         oob_glyphs.append(gkey)
        # Convert sector coords to glyph coords
        gcoords = self.glyph_coordinates(coords)
        # Ensure gcoords are on the map (negative index exploit)
        if gcoords < (0, 0) or tuple(reversed(gcoords)) < (0, 0):
            logger.log_err('Navigation: ERROR: invalid coordinates {} given to '
                           'SectorMapProvider'.format(coords))
            return False
        glyph = self.find_glyph(gcoords)
        # Check if the glyph was on the map
        if glyph == 'invalid':
            logger.log_err('Navigation: ERROR: invalid coordinates {} given to '
                           'SectorMapProvider'.format(coords))
            return False
        return glyph not in oob_glyphs
        # TODO: Detect edge for cross-sector travel
        # Remember to block cross-sector travel during a world-storm
        pass

    def get_location_name(self, coords):
        """
        Used if a builder attempts to run commands on this room, I believe

        Args:
            coordss: coordinates of the loc
        """
        legend = world.sector_glyphs.glyph_legend
        gcoords = self.glyph_coordinates(coords)
        glyph = self.find_glyph(gcoords)
        locprops = legend[glyph]
        return '{} [{}{}{}]'.format(locprops["name"], locprops["color"],
                                           locprops["scan"], '|n')

    def at_prepare_room(self, coords, caller, loc):
        """
        Set loc attributes and minimap

        Args:
            coords: Loc coordinates
            caller: ???
            loc: Loc being moved into
        """
        legend = world.sector_glyphs.glyph_legend
        gcoords = self.glyph_coordinates(coords)
        glyph = self.find_glyph(gcoords)
        locprops = legend[glyph]
        loc.db.name = locprops["name"]
        loc.db.desc = '{}{}{}'.format(locprops["color"], locprops["desc"], '|n')
        logger.log_info("Navigation: Loc desc retrieved")
        # TODO: use self.map_str to determine minimap string
        # Use EvTable for minimap
        logger.log_info("Navigation: PLACEHOLDER: Loc minimap retrieved")
        pass

class Loc(wilderness.WildernessRoom):
    """
    Where any special loc code goes
    """
    pass

# Here is the recruit mapping code

class RecruitMapper(Script):
    """
    A recruit's personal mapper that records a map of each sector they
    visit and the world map of all the sectors

    Either a catalogue of a recruit's sectormaps, or an object for each map they
    contain; not sure yet

    I know that an actual sector map will be made of at least an id and a string
    It might also be made of a dict containing map features and their coords

    Plus each recruit's map of the world
    """
    pass