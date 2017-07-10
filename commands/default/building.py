"""
Building and world design commands
"""
import types
import evennia
import world.strings
import world.wilderness
from evennia.commands.default import building
from evennia import logger
from server.conf import settings
from evennia.utils import create


class CmdLocOpen(building.ObjManipCommand):
    """
    ...

    Usage:
      @open ...

    ...

    """
    key = "@open"
    locks = "cmd:perm(open) or perm(Builders)"
    help_category = "Building"

    # a custom member method to chug out exits and do checks
    def create_exit(self, exit_name, location, destination,
                                    exit_aliases=None, typeclass=None):
        """
        Helper function to avoid code duplication.
        At this point we know destination is a valid location

        """
        caller = self.caller
        string = ""
        # check if this exit object already exists at the location.
        # we need to ignore errors (so no automatic feedback)since we
        # have to know the result of the search to decide what to do.
        exit_obj = caller.search(exit_name, location=location, quiet=True, exact=True)
        if len(exit_obj) > 1:
            # give error message and return
            caller.search(exit_name, location=location, exact=True)
            return None
        if exit_obj:
            exit_obj = exit_obj[0]
            if not exit_obj.destination:
                # we are trying to link a non-exit
                string = "'%s' already exists and is not an exit!\nIf you want to convert it "
                string += "to an exit, you must assign an object to the 'destination' property first."
                caller.msg(string % exit_name)
                return None
            # we are re-linking an old exit.
            old_destination = exit_obj.destination
            if old_destination:
                string = "Exit %s already exists." % exit_name
                if old_destination.id != destination.id:
                    # reroute the old exit.
                    exit_obj.destination = destination
                    if exit_aliases:
                        [exit_obj.aliases.add(alias) for alias in exit_aliases]
                    string += " Rerouted its old destination '%s' to '%s' and changed aliases." % \
                        (old_destination.name, destination.name)
                else:
                    string += " It already points to the correct place."

        else:
            # exit does not exist before. Create a new one.
            if not typeclass:
                typeclass = settings.BASE_EXIT_TYPECLASS
            exit_obj = create.create_object(typeclass,
                                            key=exit_name,
                                            location=location,
                                            aliases=exit_aliases,
                                            report_to=caller)
            if exit_obj:
                # storing a destination is what makes it an exit!
                exit_obj.destination = destination
                string = "" if not exit_aliases else " (aliases: %s)" % (
                    ", ".join([str(e) for e in exit_aliases]))
                string = "Created new Exit '%s' from %s to %s%s." % (
                    exit_name, location.name, destination.name, string)
            else:
                string = "Error: Exit '%s' not created." % (exit_name)
        # emit results
        caller.msg(string)
        return exit_obj

    def func(self):
        """
        This is where the processing starts.
        Uses the ObjManipCommand.parser() for pre-processing
        as well as the self.create_exit() method.
        """
        caller = self.caller

        if not self.args or not self.rhs:
            string = "Usage: @open <new exit>[;alias...][:typeclass][,<return exit>[;alias..][:typeclass]]] "
            string += "= <destination>"
            caller.msg(string)
            return

        # We must have a location to open an exit
        location = caller.location
        if not location:
            caller.msg("You cannot create an exit from a None-location.")
            return

        # obtain needed info from cmdline

        exit_name = self.lhs_objs[0]['name']
        exit_aliases = self.lhs_objs[0]['aliases']
        exit_typeclass = self.lhs_objs[0]['option']
        dest_name = self.rhs

        # first, check so the destination exists.
        destination = caller.search(dest_name, global_search=True)
        if not destination:
            return

        # Create exit
        ok = self.create_exit(exit_name,
                              location,
                              destination,
                              exit_aliases,
                              exit_typeclass)
        if not ok:
            # an error; the exit was not created, so we quit.
            return
        # Create back exit, if any
        if len(self.lhs_objs) > 1:
            back_exit_name = self.lhs_objs[1]['name']
            back_exit_aliases = self.lhs_objs[1]['aliases']
            back_exit_typeclass = self.lhs_objs[1]['option']
            self.create_exit(back_exit_name,
                             destination,
                             location,
                             back_exit_aliases,
                             back_exit_typeclass)


class CmdLoclink(building.ObjManipCommand):
    """
    link an exit to a sector loc

    Usage:
      @loclink <level>:<sector>, <loc_x>:<loc_y> = <exit>

    <sector> must be a name. this may chance to a tuple (worldcoords) in the
    future
    <loc> must be a coordinates tuple in the form (x, y). Be warned that it's
    possible to provide invalid coordinates which will cause the exit to
    not function.

    Note that if an llinked exit leaves its current room, it will need to be
    llinked again to operate.
    """
    key = "@loclink"
    aliases = ["@llink"]
    locks = "cmd:perm(open) or perm(Builders)"
    help_category = "Building"

    def func(self):
        """
        Runs the command
        """

        caller = self.caller
        if not self.args or not self.rhs:
            string = "Usage: @loclink <level>:<sector>, <loc_x>:<loc_y> = <exit>"
            string += ""
            caller.msg(string)
            return

        level = int(self.lhs_objs[0]['name'])
        secnum = self.lhs_objs[0]['option']
        loc_x = int(self.lhs_objs[1]['name'])
        loc_y = int(self.lhs_objs[1]['option'])
        exit_name = self.rhs
        coords = loc_x, loc_y

        SEC_ERR_MSG = 'Sector must be a tuple in the form of two numbers like ' \
                      '"(1, 20)" and must referece a level and sector that ' \
                      'exist in the world.'
        DUP_ERR_MSG = 'Loc {} already associated with another exit. Destroy ' \
                      'that exit before proceeding'.format(coords)

        # All parameters mandatory
        if not level or not secnum or loc_x is None or loc_y is None\
                or not exit_name:
            string = "Usage: @loclink <level>:<sector>, <loc_x>:<loc_y> = <exit>"
            string += ""
            caller.msg(string)
            return

        worldmap = evennia.search_script('overworld')[0].db.worldmap
        # Level must be in the world
        if level not in worldmap:
            caller.msg(SEC_ERR_MSG)
            return
        # secnum must refer to a sector that is on this particular level
        # sec = evennia.search_script(secnum)[0]
        sec = world.overworld.Sector.objects.get(db_key=secnum)
        if not sec or sec not in list(worldmap[level].values()):
            caller.msg(SEC_ERR_MSG)
            return
        try:
            exit = world.wilderness.WildernessExit.objects.get(db_key=exit_name)
        except:
            string = "WildernessExit '{}' not found. Choose an existing exit "\
                     "(which must be a WildernessExit.".format(exit_name)
            string += ""
            caller.msg(string)
            return
        # exit_name must refer to one in the world
        # TODO: Test ambiguity and handle it, maybe by being in same room?
        if not exit or not exit.location:
            caller.msg(SEC_ERR_MSG)
            return
        # Check the coordinates are valid in this sector
        if not sec.is_valid_coordinates(coords):
            caller.msg(SEC_ERR_MSG)
            return

        # Final check to see if this is a 're-link', so we erase the old link
        oldcoords = exit.attributes.get("coords_destination")
        if oldcoords:
            exit.attributes.remove("coords_destination")
            try:
                del sec.db.externalrooms[oldcoords]
            except AttributeError:
                logger.log_err("Cmd-Llink: ERROR: No externalrooms att found on "
                               "Sector {}".format(sec.key))
            except:
                logger.log_err("Cmd-Llink: ERROR: Failed to delete coords {}"
                               "from {}.externalrooms".format(oldcoords, sec.key))

        # Set up the site entrance in the sector dict
        # If the Sector finds a room already associated with this Loc
        # if coords in sec.db.externalrooms:
        #     caller.msg(DUP_ERR_MSG)
        #     return
        # ! Don't change the order of these !
        sec.db.externalrooms[coords] = [exit.location]
        sec.db.externalrooms[coords].append(world.strings.DEF_SITEENTRANCE_NAME)
        sec.db.externalrooms[coords].append(world.strings.DEF_SITEENTRANCE_DESC)
        sec.db.externalrooms[coords].append(world.strings.DEF_SITEENTRANCE_GLYPH)
        sec.db.externalrooms[coords].append(
            world.strings.DEF_SITEENTRANCE_GLYPHCOLOR)
        # sec.db.externalrooms[coords].append(exit)
        # Set SiteRoom's ndb.wildernessscript attribute to the sector
        exit.location.ndb.wildernessscript = sec
        # This black magic gives the special WildernessRoom property to our SiteRoom
        # this might not be persistent tho...
        # exit.location.wilderness = types.MethodType(
        #     world.wilderness.WildernessRoom.wilderness.im_func, exit.location)
        # Set the WildernessExit's db.coords_destination to the coordinates
        exit.db.coords_destination = coords
        caller.msg('Exit {} linked with coordinates {} in Sector {} on level {}.'.format(exit, coords, sec, level))

        # TODO: Add the remove switch that searches for this room/exit in the previous coords sector in order to remove it

        # TODO: change the at_start code for sectors to iterate through db.externalrooms and set ndb.wilderness for each one
        # TODO: remove room and coords reference from sec.db.externalrooms when the linked exit is deleted