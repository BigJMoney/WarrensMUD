"""
Overworld

This module governs everything relating to the Overworld and its basic
navigation.

Usage:

    ???


Implementation details:

    An OverworldScript handles the creation of the world by creating a node map
    of sectors, and then fills in each sector with a map (courtesy of the
    evennia wilderness contrib from titeuf87).

    It also handles recruit and other object movement throughout the overworld.

    The SectorRoom class has some extended functionality beyond evennia Rooms

    Recruit maps are also managed by the RecruitMapperScript

"""
import random

from evennia import logger
from typeclasses.scripts import Script
from evennia import create_script
import wilderness

def create_overworld():
    """
    Just a test function to get the ball rolling

    """
    global overworld
    mapprovider = SectorMapProvider("[][][][]")
    overworld = create_script(OverworldScript, key="overworld")
    overworld.db.mapprovider = mapprovider

class OverworldScript(wilderness.WildernessScript):
    """
    Creates a world map (nodes of sectors) upon creation, but can also create
    a new one during a world storm.

    A TODO for me that I just realized is when I make my create_world function
    I need the OverworldScript to be able to handle working with more than one
    mapprovider

    These methods will also need fixing for this:
    is_valid_coordinates()
    _create_room()
    location_name()
    set_active_coordinates()

    A trick I want to try is to wrap these methods in my extended methods which
    simply figure out the correct mapprovider and set self.mapprovider to it

    ...OR...
    I should create multiple WildernessScript instances
    """
    def at_script_creation(self):
        """


        Associates each type of map glyph with properties (name, desc, etc)
        This data will likely be store elsewhere eventually to keep the code clean

        Also, I don't know if this is the correct way to set properties on
        tclasses; I'll need to research.

            Args:
                map_config: A dict pairing overworld levels with the size (in
                sectors) to make them
        """
        # The legend for loc names and descriptions, for each map glyph
        # TODO: Find a good way to soft-code text strings like this
        self.db.glyph_legend = {
            "f": {
                "name":"forest",
                "desc":"I'm too lazy to include a sample forest description that"
                       "will just be replaced with the real thing later"
            },
            "w": {
                "name":"wasteland",
                "desc":"Yep, same thing here except this ain't multi-line"
            }
        }
        # The number of sectors per world level
        # TODO: Implement retrieval from settings.py
        self.db.map_config = { 1:100 }
        logger.log_info("OverworldInit: PLACEHOLDER: Retrieved world makeup"
                        "from settings.py")
        # A map of world node coordinates to sector objects
        self.db.worldmap = {}
        for level in self.map_config:
            self.worldmap[level] = {}

        # Make a world!
        self.world_storm(self.map_config)

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

        for num in range(size):
            placeholder['ph_coord'] = 'ph_neighbor'
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
        secmap_str = '[][][][]'

        # TODO: Algorithm to create a sector
        logger.log_info("WorldStorm: PLACEHOLDER: Generated a sector")

        mapprovider = SectorMapProvider(secmap_str)
        # Create the wilderness script for this sector
        # TODO: I need to generate unique names for my wilderness scripts, or alter the module code to allow similar names
        wilderness.create_wilderness("placeholder", mapprovider)
        logger.log_info("WorldStorm: PLACEHOLDER: Sector wilderness created")
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
                logger.log_info("WorldStorm: PLACEHOLDER: Set neighbors for "
                                "sector {}".format(str(coord)))
                # 'Move' the sector to where it belongs on the node map
                sec.neighbors[side] = neighbor_coord
            # TODO: Code to 'decaveinate' this sctor
            logger.log_info("WorldStorm: PLACEHOLDER: Decaveinated sector")
            # TODO: Code to 'caveinate' this sector according to its new neighbors
            logger.log_info("WorldStorm: PLACEHOLDER: Caveinated sector")

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

        for level in list(self.mapconfig.keys()):
            # Used to combine any existing sectors with newly creted ones
            secs = []
            # Create node map of coords:neighbors
            neighbormap.update(self.create_mapnodes(self.map_config[level]))
            logger.log_info("WorldStorm: PLACEHOLDER: Node map finished")
            logger.log_info("WorldStorm: Map of neighbors created")
            if self.map_config[level] < 1:
                logger.log_error("WorldStorm: ERROR: OverWorldScript.map_config "
                                "is less than 1. This is not the proper way to "
                                "erase a level. Fix in settings.py. Aborting "
                                "world storm.")
                return False
            # Code if there is an existing overworld
            if len(self.worldmap[level]) > 0:
                if len(self.worldmap[level]) > len(neighbormap):
                    logger.log_error("WorldStorm: ERROR: OverWorldScript.map_config "
                                    "is less than the existing world size. Fix "
                                    "in settings.py. Aborting world storm.")
                    return False
                # TODO: Broadcast the storm and lock down inter-sector travel 5 mins
                logger.log_info("WorldStorm: PLACEHOLDER: Broadcast storm and locked "
                                "intersector travel for "
                                "{} minutes...".format(locktime))
                # Make a list of our existing sectors and shuffle them
                secs_old = list(self.worldmap[level].values())
                random.shuffle(secs_old)
                # And add them to the big list of sectors
                secs.append(secs_old)
            diff = len(neighbormap) - len(self.worldmap[level])
            # Code if the new scrambled will be larger than previous (or is new)
            if diff > 0:
                # Maybe one day I want to run a function here that picks biomes
                # for the new neighbormap and assigns them as a biomemap. Then I can
                # pass biome to create_sector() in the comprehension below.

                secs_new = [self.create_sector() for s in range(diff)]
                logger.log_info("WorldStorm: New sectors created")
                secs.append(secs_new)
            # Create final world map of sectors
            self.worldmap[level] = {coord:sec for coord,sec in \
                                    zip(neighbormap,secs)}
            logger.log_info("WorldStorm: World maps created")
            # caveinate this level
            self.caveinate_sectors(self.worldmap[level], neighbormap)

class SectorMapProvider(wilderness.WildernessMapProvider):
    """
    Documentation on mapproviders can be found in evennia/contrib/wilderness.py

    See the functions below for this class's extensions
    """

    # Associates this hex's sides (ints) with a ref to the neighbor sector
    neighbors = {}

    def __init__(self, map_str):
        """
        Args:
            map_str: This sector's map string
        """
        self.map_str = map_str

    def is_valid_coordinates(self, overworld, coordinates):
        """
        Uses the map string to check if the coordinates are valid to move to
        Needs to check for cave walls and movement into adjacent sectors

        Args:
            overworld: Ref to the OverworldScript (caller)
            coordinates: The coordinates to validate

        Returns:
            Not sure yet :) Possibly true, false or a ref to a neighbor
        """

        # TODO: Check for cave walls

        # TODO: Use neighbors to handle cross-sector travel
        # Remember to block cross-sector travel during a world-storm
        logger.log_info("WorldStorm: PLACEHOLDER: Neighbor found and cross "
                        "sector travel initiated")
        pass

    def get_location_name(self, coordinates):
        """
        Used if a builder attempts to run commands on this room, I believe

        Args:
            coordinates: coordinates of the loc
        """
        # I'm honestly not sure what this is supposed to return
        # TODO: Test and fix this
        return "biffle-diffle"

    def at_prepare_room(self, coords, caller, room):
        """
        Set loc attributes and minimap

        Args:
            coords: Loc coordinates
            caller: ???
            room: ???
        """
        # TODO: use self.map_str to determine room desc and minimap strings
        # Use EvTable for minimap
        logger.log_info("WorldStorm: PLACEHOLDER: Loc desc retrieved")
        logger.log_info("WorldStorm: PLACEHOLDER: Loc minimap retrieved")
        pass

class Loc(WildernessRoom):
    """
    Where any special loc code goes
    """
    pass

# Here is the recruit mapping code

class RecruitMapper(Script):
    """
    A recruit's personal mapper that records a map of each sector they
    visit and the world map of all the sectors

    Either a catalogue of a recruit's sectormaps, or an object for each map they contain; not sure yet

    I know that an actual sector map will be made of at least an id and a string
    It might also be made of a dict containing map features and their coords

    Plus each recruit's map of the world
    """
    pass