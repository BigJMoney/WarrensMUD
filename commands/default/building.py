"""
Building and world design commands
"""

from evennia.commands.default import building
from server.conf import settings
from evennia.utils import create


class CmdOpen(building.ObjManipCommand):
    """
    open a new exit from the current room

    Usage:
      @open <new exit>[;alias;alias..][:typeclass] [,<return exit>[;alias;..][:typeclass]]] = <destination>

    Switches:
      sector - create an exit that leads to a sector

    Handles the creation of exits. If a destination is given, the exit
    will point there. The <return exit> argument sets up an exit at the
    destination leading back to the current room. Destination name
    can be given both as a #dbref and a name, if that name is globally
    unique.

    """
    key = "@open"
    locks = "cmd:perm(open) or perm(Builders)"
    help_category = "Building"

    # a custom member method to chug out exits and do checks
    def create_exit(self, exit_name, location, destination, coords_destination,
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


class CmdSlink(building.ObjManipCommand):
    """
    link an exit to a sector loc

    Usage:
      @slink <sector>:<loc> = <exit>

    <sector> must be a tuple of the form (level #, sector #)
    <loc> must be a coordinates tuple in the form (x, y). Be warned that it's
    possible to provide invalid coordinates which will cause the exit to
    not function.

    Note that if a slinked exit leaves its current room, it will need to be
    slinked again to operate.

    """
    key = "@slink"
    locks = "cmd:perm(open) or perm(Builders)"
    help_category = "Building"

    def func(self):
        """
        ???
        """
        caller = self.caller

        if not self.args or not self.rhs:
            string = "???"
            string += ""
            caller.msg(string)
            return

        sector_in = self.lhs_objs[0]['name']
        coords_in = self.lhs_objs[0]['option']
        exit_name = self.rhs

        if not coords_in:
            string = "???"
            string += ""
            caller.msg(string)
            return

        # Check that sector and loc values are correct format

        # Check that this key refers to a Sector object

        # Check that exit_name is a valid exit with a location

        # Add 'here' to the Sector's db.externalrooms dict, associated to a list
        #  of exits (of which this new exit is added)

        # Set current SiteRoom's ndb.wildernessscript attribute to the sector

        # Set the WildernessExit's db.coords_destination to the coordinates