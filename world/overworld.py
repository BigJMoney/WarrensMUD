# -*- coding: UTF-8 -*-
"""
Overworld

This module governs everything relating to the Overworld and its basic
navigation.

Developer Usage:

    Easy batch: @batchcommands make_dev_world

    A la carte:
    @py from world import overworld; overworld.create_overworld()
    @py from world import overworld; overworld.enter_sector(me)
    @py from world import overworld; overworld.destroy_overworld()

Implementation details:

    The Overworld (Script) handles the creation of the world by randomly
    generating a node map of hexagonal sectors. Each Sector has a set of
    world coordinates on this hex map.

    It then runs a 'World Storm' which chooses a cartesian Sector map for each
    Sector, and then generates cave walls so that each Sector is logically
    connected to its 'neighbor', while preventing player travel outside of the
    Overworld map.

    A World Storm may also be run during active play to 'scramble' the world
    layout.

    A recruit's personal  maps are managed by the RecruitMapperScript

    Sector map and player movement functionalty are based on the Evennia
    Wilderness contrib, courtesy of titeuf87.

"""
import random
import world.strings
from evennia import logger, create_script, search_object
from evennia import EvTable
from typeclasses.scripts import Script
import wilderness

##################
# WORLD GENERATION
##################

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
        obj.execute_cmd('look')
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


class Overworld(Script):
    """
    Creates a world map (nodes of sectors) upon creation, but can also create
    a new one during a world storm.

    """


    def at_script_creation(self):
        """
        This function creates a new world but it doesn't delete the previous
        one which would still be present in the db with all its sectors.

        """
        self.persistent = True
        # The legend for loc names and descriptions, for each map glyph
        self.db.glyph_legend = world.strings.GLYPH_LEGEND
        # The number of sectors per world level {<level>: <num_sectors>}
        # TODO: Implement retrieval from settings.py
        map_config = {1: 2}
        # Sector counter to create unique keys from
        self.db.numsectors = 0
        logger.log_info("OverworldInit: PLACEHOLDER: Retrieved world makeup "
                        "from settings.py")
        # A map of world node coordinates to sector objects
        self.db.worldmap = {}
        for level in map_config:
            self.db.worldmap[level] = {}

        # Make a world!
        self.world_storm(map_config)

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
            placeholder['ph_coord' + str(num)] = (1, 2, 3)
        return placeholder

    def create_sector(self):
        """
        Randomly generates a Sector (WildernessScript) and its db.mapprovider

        Returns:
             Sector instance
        """
        # TODO: Algorithm to generate a sector, unless I decide to go hand-made
        # Maybe both? Currently I'm pulling from a hand-made file
        str_file = open('.\\world\\sector_proto.txt')
        # Our sector map
        secmap_str = str_file.read()
        logger.log_info("WorldStorm: PLACEHOLDER: Generated a sector")

        # Create a Sector with a unique key. In the future when they have unique
        # world coords, this will no longer be needed
        script = create_script(Sector, key=str(self.db.numsectors+1))
        # Increase our unique keyname counter
        self.db.numsectors = self.db.numsectors + 1
        mapprovider = SectorMapProvider(secmap_str)
        script.db.mapprovider = mapprovider
        logger.log_info("WorldStorm: PLACEHOLDER: Sector created")
        return script

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
        # TODO: world storm must disconnect all external exits
        # then reconnect them to the new appropriate coordinates after the storm

        # Map of coordinates:neighbor_sides
        neighbormap = {}
        # How many seconds a world storm lasts
        locktime = 300

        for level in list(map_config.keys()):
            # Combines existing sectors with newly created ones
            secs = []
            # Create node map of coords:neighbors
            neighbormap.update(self.create_mapnodes(map_config[level]))
            logger.log_info("WorldStorm: PLACEHOLDER: Node map finished")
            logger.log_info("WorldStorm: Map of neighbors created")
            if map_config[level] < 1:
                logger.log_error("WorldStorm: ERROR: Overworld.map_config "
                                 "is less than 1. This is not the proper way "
                                 "to erase a level. Fix in settings.py. "
                                 "Aborting world storm.")
                return False
            # Code if there is an existing overworld
            if len(self.db.worldmap[level]) > 0:
                if len(self.db.worldmap[level]) > len(neighbormap):
                    logger.log_error("WorldStorm: ERROR: Overworld.map_config "
                                     "is less than the existing world size. "
                                     "Fix in settings.py. Aborting world "
                                     "storm.")
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

###################
# WORLD EXPLORATION
###################

class Sector(wilderness.WildernessScript):
    """
    Mostly a name change wrapper.
    """
    def at_start(self):
        """
        Every Loc with an external Site entrance references the Room it connects
        to. Set the ndb.wildernessscript for all of these Rooms so their exits
        lead to their resepctive Locs
        """
        super(Sector, self).at_start()
        ## Reload the glyph legend every restart so designers can make changes
        #self.mapprovider.legend = world.strings.GLYPH_LEGEND
        try:
            for coordinates, props in self.mapprovider.externalrooms.items():
                room = search_object(props[0])[0]
                room.ndb.wildernessscript = self
                logger.log_info("SectorScriptStart: External room {} "
                                "found in Sector {}".format(room.key, self.key))
        except AttributeError:
            logger.log_info("SectorScriptStart: "
                            "Sector {} has no externalrooms".format(self.key))


class SectorMapProvider(wilderness.WildernessMapProvider):
    """
    Documentation on mapproviders can be found in evennia/contrib/wilderness.py

    See the functions below for this class's extensions
    """
    # Coordinates of landmarks associated with their properties
    # Eventually this will be created programmatically
    # Or, if mannually, I'l move this over to strings.py
    legend = world.strings.GLYPH_LEGEND
    landmarks = {
        (37, 26): {
            'name': 'High Hill',
            'desc': 'Deep in the hillside, you find yourself on a very high '
                    'hill that stands out from all the others'
        },
        (39, 21): {
            'name': 'Valley',
            'desc': 'Deep in the hillside, you find yourself passing through a '
                    'long and winding valley'
        },
        (43, 47): {
            'name': 'Scenic Overlook',
            'desc': 'Clambering down one of the slopes, you arrive on a scenic '
                    'overlook where the gray twilight of the Earthstar limns '
                    'the horizon as far as the eye can see'
        },
        (12, 31): {
            'name': 'Cliff\'s Edge',
            'desc': "Clambering down one of the slopes, you arrive at the edge "
                    "of a very sharp cliff, with a drop you'll not soon forget"
        }
    }

    def __init__(self, map_str):
        """
        Sets attributes.

        Args:
            map_str: This sector's map string
        """
        self.map_str = map_str
        # Associates this hex's sides (ints) with a ref to the neighbor sector
        # Shit, I think this is invalid in Evennia... non db objects cannot
        # store db objects and expect them to be saved
        # I might need to save this as an attribute on the Sector itself
        # Or I could have this associated with the Sector key instead of ref
        self.neighbors = {}
        # Keeps track of Site exits leading into this Sector
        self.externalrooms = {}
        # Copy comment from Sector

    @staticmethod
    def glyph_coordinates(coords):
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

    def find_glyph(self, coords, externalrooms=None, scan=False):
        """
        Find the character in self.map_str, given its coordinates

        Can optionally find the scan glyph, which is used for the minimap

        Args:
            coords (tuple): Coordinates (in-game)
            loc (Loc): The Loc being prepared
            scan (boolean): Whether to return a "scan" glyph
        Returns:
            The glyph string
        """
        gcoords = self.glyph_coordinates(coords)
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
        if glyph not in self.legend:
            glyph = '!'

        if scan:
            #First check if this Loc is a Site entrance
            if externalrooms:
                if coords in externalrooms:
                    # 4th item is the entrance glyph
                    return externalrooms[coords][3]
            return self.legend[glyph]["scan"]
        return glyph

    def is_valid_coordinates(self, overworld, coords):
        """
        Uses the map string to check if the coordinates are valid to move to.
        Cave wall, river and out of bounds are currently invalid.

        Args:
            overworld: Ref to the Overworld (caller)
            coords: The coordinates to validate

        Returns:
            Boolean depending on success

            Perhaps in the future it will return a neighbor if we're talking
            about coordinates which lead to a neighboring sector.
        """
        # TODO: Detect SiteRoom for external travel
        # TODO: Detect edge for cross-sector travel
        # Remember to block cross-sector travel during a world-storm

        # Translate WarrensMUD coords to map_str coords
        gcoords = self.glyph_coordinates(coords)
        # Ensure gcoords are on the map (negative index exploit)
        if gcoords < (0, 0) or tuple(reversed(gcoords)) < (0, 0):
            logger.log_err('Navigation: ERROR: invalid coordinates {} given to '
                           'SectorMapProvider'.format(coords))
            return False
        glyph = self.find_glyph(coords)
        # Ensure the glyph was on the map
        if glyph == 'invalid':
            logger.log_err('Navigation: ERROR: invalid coordinates {} given to '
                           'SectorMapProvider'.format(coords))
            return False

        # If the glyph is an external location, look it up
        # Return the location reference?

        # The characters that define impassable spaces (out of bounds)
        oob_glyphs = [gkey for gkey in self.legend if not self.legend[gkey]["pass"]]
        return glyph not in oob_glyphs

    def get_location_name(self, coords):
        """
        Used in many places where a room is called; hooked into Locs

        Args:
            coords: coordinates of the loc

        Returns:
            String: name of the Loc
        """
        legend = world.strings.GLYPH_LEGEND
        glyph = self.find_glyph(coords)
        locprops = legend[glyph]
        gcoords = self.glyph_coordinates(coords)
        # Loc with an external site entrance
        if coords in self.externalrooms:
            name = '{}{}{}'.format(locprops["color"],
                                   self.externalrooms[coords][1], '|n')
        # Loc with a Landmark name
        elif gcoords in self.landmarks:
            name = '{}{}{}'.format(locprops["color"],
                                   self.landmarks[gcoords]["name"], '|n')
        # Regular Loc name
        else:
            name = '{}{}{}'.format(locprops["color"],
                                   locprops["name"], '|n')
        return name

    def at_prepare_room(self, coords, caller, loc):
        """
        Create and display the Loc: name, description, minimap, hud, etc

        Args:
            coords: Loc coordinates
            caller: ???
            loc: Loc being moved into
        """
        # TODO: Major refactor of this and descendant functions
        # It's spaghetti code, but also there is quite a bit more functionality
        # that will end up here, like wanderers, special sites, encounters,
        # loot stashes, etc... So I need to do a high-level re-org of it, BUT
        # NOT until I have a very firm grasp on what features I'll have
        externalrooms = loc.ndb.wildernessscript.mapprovider.externalrooms
        # Set our legend for normal Locs
        legend = world.strings.GLYPH_LEGEND
        # Set our MAP glyph for normal Locs
        glyph = self.find_glyph(coords)
        # Set a normal Loc's properties
        locprops = legend[glyph]
        gcoords = self.glyph_coordinates(coords)
        logger.log_info("Navigation: Retrieving Loc name and desc")
        # Loc with a special entrance to external Site
        if coords in externalrooms:
            desc_string = '\n|555' + externalrooms[coords][2] + '|n'
        # Loc with a Landmark description
        elif gcoords in self.landmarks:
            # loc.db.name = self.landmarks[gcoords]["name"]
            desc_string = '\n|555' + self.landmarks[gcoords]["desc"] + '|n'
        # Regular Loc properties
        else:
            # Set Loc desc
            desc_string = '\n{}{}{}'.format('|045', locprops["desc"], '|n')
        guide_string1 = '|045\n  ╓\n  ║\n  ║\n  ║\n  ╙\n|n'
        loc.db.desc = EvTable.EvTable(guide_string1, desc_string,
                                      align="l", valign="t", height=6,
                                      border=None)
        loc.db.desc.reformat_column(0, width=5)
        loc.db.desc.reformat_column(1, width=75)
        logger.log_info("Navigation: Loc name and desc retrieved")

        # Build the hud
        # TODO: Account for adjacent sectors
        # Future Release: Account for different sized scans
        logger.log_info("Navigation: Building Loc HUD")

        # 1. Readout
        #
        logger.log_info("Navigation: Retrieving Loc readout")
        rstring = "ENVIRONMENT\n"
        rstring += "Loc: {}\n".format(self.get_location_name(coords))
        rstring += "Terrain: {}{}{}\n".format(legend[self.find_glyph(coords)]["color"],
                                              self.find_glyph(coords, scan=True),
                                              '|n')
        rstring += "Sector: {}".format(loc.ndb.wildernessscript.key)
        logger.log_info("Navigation: Loc readout retrieved")

        def scan_glyphs(slf, cds, sgrid):
            # Adds sgrid offsets to gcs (coordinates) and returns minimap glyphs
            # including colorcodes
            gc = self.glyph_coordinates(cds)
            elements = []
            # For each scanner x,y
            for offset in sgrid:
                ncds = tuple(x + y for x, y in zip(cds, offset))
                # Get the offset glyph's color
                e = legend[slf.find_glyph(ncds)]["color"]
                # Get its minimap glyph
                e += slf.find_glyph(ncds, externalrooms, scan=True)
                # Close the color code
                e += '|n'
                elements.append(e)
            return elements

        # 2. Scanner
        #
        logger.log_info("Navigation: Retrieving Loc scanner")
        x, y = coords
        xchar = str(x)
        xsymbol = ''
        if x < 0:
            xsymbol = '-'
            xchar = str(abs(x))
        xpad = '0'
        if x <= -10:
            xpad = ''
        if 0 <= x < 10:
            xpad = '00'
        ychar = str(y)
        ysymbol = ''
        if y < 0:
            ysymbol = '-'
            ychar = str(abs(y))
        ypad = '0'
        if y <= -10:
            ypad = ''
        if 0 <= y < 10:
            ypad = '00'
        xstring = ''.join(['|555', xsymbol, xpad, xchar, '|n'])
        ystring = ''.join(['|555', ysymbol, ypad, ychar, '|n'])
        print('x', xstring)
        print('y', ystring)
        scan_grid = ((-1, 1),  (0, 1),  (1, 1),
                     (-1, 0),  (0, 0),  (1, 0),
                     (-1, -1), (0, -1), (1, -1))
        recruit_glyph = '|555{|550@|555}|n'

        line1 = '╓──────║scanY║──────╖\n'
        line2 = '║                   ║\n'
        line3 = '─────  {} {} {}  ─────\n'
        line4 = 'scanX  {2} {0} {4}   {1} \n'
        line5 = '─────  {} {} {}  ─────\n'
        line6 = '║                   ║\n'
        line7 = '╙──────║ %s ║──────╜'

        scan_string = line1
        scan_string += line2
        scan_string += line3.format(*(scan_glyphs(self, coords, scan_grid[0:3])))
        scan_string += line4.format(recruit_glyph, xstring, *(scan_glyphs(self, coords, scan_grid[3:6])))
        scan_string += line5.format(*(scan_glyphs(self, coords, scan_grid[6:9])))
        scan_string += line6
        scan_string += line7 % ystring
        logger.log_info("Navigation: Loc scanner retrieved")

        # 3. Vitals
        # One day this will reference real health :)
        health_disp = 2
        bauble_disp = 0
        vstring = "VITALS\n"
        vstring += "|511{}▾|n\n".format('♥ ' * health_disp)
        vstring += "|550{} ⤈|n".format(str(bauble_disp))

        loc.db.hud = EvTable.EvTable(scan_string, rstring, vstring, valign='t',
                                     border=None)
        loc.db.hud.reformat_column(0, align='c', width=29)
        loc.db.hud.reformat_column(1, width=32)
        loc.db.hud.reformat_column(2, align='r', width=19)
        logger.log_info("Navigation: Loc HUD finished")
        # Use EvTable for minimap

#################
# RECRUIT MAPPING
#################

class RecruitMapper(Script):
    """
    A recruit's personal mapper that records a map of each sector they
    visit and the world map of all the sectors

    Either a catalogue of a recruit's sectormaps, or an object for each map they
    contain; not sure yet

    I know that an actual sector map will be made of at least an id and a string
    It might also be made of a dict containing map features and their coords

    Plus each recruit's node map of the world
    """
    pass
