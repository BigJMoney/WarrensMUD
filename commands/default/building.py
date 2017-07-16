"""
Building and world design commands
"""
import types
import evennia
import world.strings
import world.wilderness
from evennia.commands.default import building
from evennia import logger, search_object
from server.conf import settings
from evennia.utils import create


#############################################
# Reserving this code for later
#
# class CmdLocOpen(building.ObjManipCommand):
#     """
#     ...
#
#     Usage:
#       @open ...
#
#     ...
#
#     """
#     key = "@open"
#     locks = "cmd:perm(open) or perm(Builders)"
#     help_category = "Building"
#
#     # a custom member method to chug out exits and do checks
#     def create_exit(self, exit_name, location, destination,
#                                     exit_aliases=None, typeclass=None):
#         """
#         Helper function to avoid code duplication.
#         At this point we know destination is a valid location
#
#         """
#         caller = self.caller
#         string = ""
#         # check if this exit object already exists at the location.
#         # we need to ignore errors (so no automatic feedback)since we
#         # have to know the result of the search to decide what to do.
#         exit_obj = caller.search(exit_name, location=location, quiet=True,
#                                  exact=True)
#         if len(exit_obj) > 1:
#             # give error message and return
#             caller.search(exit_name, location=location, exact=True)
#             return None
#         if exit_obj:
#             exit_obj = exit_obj[0]
#             if not exit_obj.destination:
#                 # we are trying to link a non-exit
#                 string = "'%s' already exists and is not an exit!\nIf you want " \
#                          "to convert it "
#                 string += "to an exit, you must assign an object to the " \
#                           "'destination' property first."
#                 caller.msg(string % exit_name)
#                 return None
#             # we are re-linking an old exit.
#             old_destination = exit_obj.destination
#             if old_destination:
#                 string = "Exit %s already exists." % exit_name
#                 if old_destination.id != destination.id:
#                     # reroute the old exit.
#                     exit_obj.destination = destination
#                     if exit_aliases:
#                         [exit_obj.aliases.add(alias) for alias in exit_aliases]
#                     string += " Rerouted its old destination '%s' to '%s' and " \
#                               "changed aliases." % \
#                         (old_destination.name, destination.name)
#                 else:
#                     string += " It already points to the correct place."
#
#         else:
#             # exit does not exist before. Create a new one.
#             if not typeclass:
#                 typeclass = settings.BASE_EXIT_TYPECLASS
#             exit_obj = create.create_object(typeclass,
#                                             key=exit_name,
#                                             location=location,
#                                             aliases=exit_aliases,
#                                             report_to=caller)
#             if exit_obj:
#                 # storing a destination is what makes it an exit!
#                 exit_obj.destination = destination
#                 string = "" if not exit_aliases else " (aliases: %s)" % (
#                     ", ".join([str(e) for e in exit_aliases]))
#                 string = "Created new Exit '%s' from %s to %s%s." % (
#                     exit_name, location.name, destination.name, string)
#             else:
#                 string = "Error: Exit '%s' not created." % (exit_name)
#         # emit results
#         caller.msg(string)
#         return exit_obj
#
#     def func(self):
#         """
#         This is where the processing starts.
#         Uses the ObjManipCommand.parser() for pre-processing
#         as well as the self.create_exit() method.
#         """
#         caller = self.caller
#
#         if not self.args or not self.rhs:
#             string = "Usage: @open <new exit>[;alias...][:typeclass]" \
#                      "[,<return exit>[;alias..][:typeclass]]] "
#             string += "= <destination>"
#             caller.msg(string)
#             return
#
#         # We must have a location to open an exit
#         location = caller.location
#         if not location:
#             caller.msg("You cannot create an exit from a None-location.")
#             return
#
#         # obtain needed info from cmdline
#
#         exit_name = self.lhs_objs[0]['name']
#         exit_aliases = self.lhs_objs[0]['aliases']
#         exit_typeclass = self.lhs_objs[0]['option']
#         dest_name = self.rhs
#
#         # first, check so the destination exists.
#         destination = caller.search(dest_name, global_search=True)
#         if not destination:
#             return
#
#         # Create exit
#         ok = self.create_exit(exit_name,
#                               location,
#                               destination,
#                               exit_aliases,
#                               exit_typeclass)
#         if not ok:
#             # an error; the exit was not created, so we quit.
#             return
#         # Create back exit, if any
#         if len(self.lhs_objs) > 1:
#             back_exit_name = self.lhs_objs[1]['name']
#             back_exit_aliases = self.lhs_objs[1]['aliases']
#             back_exit_typeclass = self.lhs_objs[1]['option']
#             self.create_exit(back_exit_name,
#                              destination,
#                              location,
#                              back_exit_aliases,
#                              back_exit_typeclass)


class CmdLocLink(building.ObjManipCommand):
    """
    Link a WildernessExit to a Loc. Should only be used on permanent exits
    outside of a Sector.

    Usage:
      @loclink <level>:<sector>, <loc_x>:<loc_y> = <exit>

    <sector> must be a name. This may change to a tuple (worldcoords) in the
    future.
    <loc_x> and <loc_y> must be integers that represent valid coordinates in a
    Sector.

    *HEY, LISTEN*! If an llinked exit leaves its current room, it will need to
    be llinked again.
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
            caller.msg("Usage: @loclink <level>:<sector>, <loc_x>:<loc_y> = <exit>")
            return

        VAL_ERR_MSG = "Arguments: <level>, <sec_x> and <sec_y> must " \
                      "be integers."

        try:
            level = int(self.lhs_objs[0]['name'])
            loc_x = int(self.lhs_objs[1]['name'])
            loc_y = int(self.lhs_objs[1]['option'])
        except ValueError:
            caller.msg(VAL_ERR_MSG); return
        sec_id = self.lhs_objs[0]['option']
        exit_name = self.rhs
        coords = loc_x, loc_y

        SEC_ERR_MSG = 'Sector must be a tuple in the form of two numbers like ' \
                      '"(1, 20)", must referece a level and sector that ' \
                      'exist in the world, and must not lead to impassable ' \
                      'terrain. Whew!'

        # All parameters are mandatory
        if not level or not sec_id or loc_x is None or loc_y is None\
                or not exit_name:
            string = "Usage: @loclink <level>:<sector>, <loc_x>:<loc_y> = <exit>"
            string += ""
            caller.msg(string); return
        # Level must be in the world
        worldmap = evennia.search_script('overworld')[0].db.worldmap
        if level not in worldmap:
            caller.msg(SEC_ERR_MSG)
            return
        # sec_id must refer to a sector that is on the specified level
        try:
            sec = world.overworld.Sector.objects.get(db_key=sec_id)
        except world.overworld.Sector.DoesNotExist:
            caller.msg(SEC_ERR_MSG); return
        if not sec or sec not in list(worldmap[level].values()):
            caller.msg(SEC_ERR_MSG); return
        # locate the exit
        # first, search locally
        exit = caller.search(exit_name)
        if not exit:
            # then, search globally
            try:
                exit = world.wilderness.WildernessExit.objects.get(db_key=exit_name)
            except world.wilderness.WildernessExit.MultipleObjectsReturned:
                string = "\nMultiple '{}' SectorExits. You may use a db_ref " \
                         "instead of a name." \
                         "".format(exit_name)
                string += ""
                caller.msg(string)
                return
            except:
                string = "SectorExit '{}' not found. Choose an existing " \
                         "SectorExit (one created with @lopen; not a SiteExit)." \
                         "".format(exit_name)
                string += ""
                caller.msg(string)
                return
        # exit_name must refer to one in the world
        if not exit or not exit.location:
            caller.msg(SEC_ERR_MSG)
            return
        # Check the coordinates are valid in this sector
        if not sec.is_valid_coordinates(coords):
            caller.msg(SEC_ERR_MSG)
            return
        # A Loc can't be linked to multiple WildernessExits
        if coords in sec.mapprovider.externalrooms:
            caller.msg('Loc {} already associated with exit {}. Destroy ' \
                       'that exit before proceeding'
                       ''.format(coords, sec.mapprovider.externalrooms[coords][4]))
            return
        # Case: 'Re-link"; we want to eliminate the old link
        relink = False
        oldcoords = exit.attributes.get("coords_destination")
        if oldcoords:
            exit.attributes.remove("coords_destination")
            try:
                mapprovider = sec.mapprovider
                del mapprovider.externalrooms[oldcoords]
                sec.db.mapprovider = mapprovider
            # This is here for safety but I don't believe it should occur
            except:
                logger.log_err("Cmd-Llink: ERROR: Failed to delete coords {}"
                               "from {}.externalrooms".format(oldcoords, sec.key))
            else:
                relink = True

        # Add the link info to the mapprovider externalrooms dict
        # ! Don't change the order of these !
        mapprovider = sec.mapprovider
        mapprovider.externalrooms[coords] = \
            [exit.location.dbref]
        mapprovider.externalrooms[coords].append(
            world.strings.DEF_SITEENTRANCE_NAME)
        mapprovider.externalrooms[coords].append(
            world.strings.DEF_SITEENTRANCE_DESC)
        mapprovider.externalrooms[coords].append(
            world.strings.DEF_SITEENTRANCE_GLYPH)
        mapprovider.externalrooms[coords].append(
            exit.dbref)
        sec.db.mapprovider = mapprovider
        exit.location.ndb.wildernessscript = sec
        # Add the Loc coords link to the exit
        exit.db.coords_destination = coords
        string = 'Exit {} linked with coordinates {} in Sector {} on level {}.' \
                 ''.format(exit, coords, sec, level)
        if relink:
            string +='\nRemember to delete the old return exit if there is one.'
        caller.msg(string)


class CmdLocDesc(building.ObjManipCommand):
    """
    Set the description of a Loc that has an external Site entrance. The Loc
    must already be linked from an exit in a Site (see help @llink).

    Usage:
      @ldesc <level>:<sector>, <loc_x>:<loc_y> = <description>

    Switches:
      edit - [ FUTURE RELEASE: edit mode ]

    <sector> must be a name. This may change to a tuple (worldcoords) in the
    future
    <loc_x> and <loc_y> must be integers that represent valid coordinates in a
    Sector.
    """
    key = "@locdesc"
    aliases = ["@locdescribe", "@ldescribe", "@ldesc"]
    locks = "cmd:perm(desc) or perm(Builders)"
    help_category = "Building"

    #########################
    # Reserved code
    #
    # def edit_handler(self):
    #     if self.rhs:
    #         self.msg("|rYou may specify a value, or use the edit switch, "
    #                  "but not both.|n")
    #         return
    #     if self.args:
    #         obj = self.caller.search(self.args)
    #     else:
    #         obj = self.caller.location or self.msg("|rYou can't describe oblivion.|n")
    #     if not obj:
    #         return
    #
    #     self.caller.db.evmenu_target = obj
    #     # launch the editor
    #     EvEditor(self.caller, loadfunc=_desc_load, savefunc=_desc_save,
    #              quitfunc=_desc_quit, key="desc", persistent=True)
    #     return

    def func(self):
        "Runs command"
        caller = self.caller
        if not self.args or not self.rhs:
            string = "Usage: @locdesc <level>:<sector>, <loc_x>:<loc_y> = " \
                     "<description>"
            string += ""
            caller.msg(string)
            return

        ############################
        # Reserved Code
        #
        #if 'edit' in self.switches:
        #    self.edit_handler()
        #    return

        VAL_ERR_MSG = "Arguments: <level>, <sec_x> and <sec_y> must " \
                      "be integers."

        try:
            level = int(self.lhs_objs[0]['name'])
            loc_x = int(self.lhs_objs[1]['name'])
            loc_y = int(self.lhs_objs[1]['option'])
        except ValueError:
            caller.msg(VAL_ERR_MSG);
            return
        sec_id = self.lhs_objs[0]['option']
        desc = self.rhs
        coords = loc_x, loc_y

        SEC_ERR_MSG = 'Sector must be a tuple in the form of two numbers like ' \
                      '"1:20" and must referece a level and sector that ' \
                      'exist in the world.'
        LOC_ERR_MSG = 'Coordinates must refer to a Loc that is linked to an ' \
                      'external Site via an exit (see help @llink).'

        # All parameters mandatory
        if not level or not sec_id or loc_x is None or loc_y is None \
                or not desc:
            string = "Usage: @locdesc <level>:<sector>, <loc_x>:<loc_y> = " \
                     "<description>"
            string += ""
            caller.msg(string)
            return
        worldmap = evennia.search_script('overworld')[0].db.worldmap
        # Level must be in the world
        if level not in worldmap:
            caller.msg(SEC_ERR_MSG)
            return
        # sec_id must refer to a sector that is on the specified level
        try:
            sec = world.overworld.Sector.objects.get(db_key=sec_id)
        except world.overworld.Sector.DoesNotExist:
            caller.msg(SEC_ERR_MSG);
            return
        if not sec or sec not in list(worldmap[level].values()):
            caller.msg(SEC_ERR_MSG);
            return
        # Check the coordinates are valid in this sector
        if not sec.is_valid_coordinates(coords):
            caller.msg(SEC_ERR_MSG)
            return
        # Coordinates must refer to a loc linked to externalrooms
        if coords not in sec.mapprovider.externalrooms:
            caller.msg(LOC_ERR_MSG)
            return
        # Find and edit the Loc
        props = sec.mapprovider.externalrooms[coords]
        # Only allow someone with Site edit access to do this, however
        room = search_object(props[0])[0]
        if room.access(caller, "edit"):
            mapprovider = sec.mapprovider
            mapprovider.externalrooms[coords][2] = desc
            sec.db.mapprovider = mapprovider
            caller.msg(
                "The entrance description was set on Loc {}.".format(coords))
        else:
            caller.msg("You don't have permission to edit the Site properties "
                       "of %s." % room.key)


class CmdLocName(building.ObjManipCommand):
    """
    Name a Loc that has an external Site entrance

    Usage:
      @lname <level>:<sector>, <loc_x>:<loc_y> = <name>

    Sets the "name" attribute on a Loc with the given coordinates. The Loc
    must already be linked from an exit in a Site (see help @llink).
    """
    key = "@locname"
    aliases = "@lname"
    locks = "cmd:perm(desc) or perm(Builders)"
    help_category = "Building"

    def func(self):
        "Define command"
        caller = self.caller
        if not self.args or not self.rhs:
            string = "Usage: @locname <level>:<sector>, <loc_x>:<loc_y> = " \
                     "<name>"
            string += ""
            caller.msg(string)
            return

        VAL_ERR_MSG = "Arguments: <level>, <sec_x> and <sec_y> must " \
                      "be integers."

        try:
            level = int(self.lhs_objs[0]['name'])
            loc_x = int(self.lhs_objs[1]['name'])
            loc_y = int(self.lhs_objs[1]['option'])
        except ValueError:
            caller.msg(VAL_ERR_MSG);
            return
        sec_id = self.lhs_objs[0]['option']
        name = self.rhs
        coords = loc_x, loc_y

        SEC_ERR_MSG = 'Sector must be a tuple in the form of two numbers like ' \
                      '"1:20" and must referece a level and sector that ' \
                      'exist in the world.'
        LOC_ERR_MSG = 'Coordinates must refer to a Loc that is linked to an ' \
                      'external Site via an exit (see help @llink).'

        # All parameters mandatory
        if not level or not sec_id or loc_x is None or loc_y is None \
                or not name:
            string = "Usage: @locname <level>:<sector>, <loc_x>:<loc_y> = " \
                     "<name>"
            string += ""
            caller.msg(string)
            return
        worldmap = evennia.search_script('overworld')[0].db.worldmap
        # Level must be in the world
        if level not in worldmap:
            caller.msg(SEC_ERR_MSG)
            return
        # sec_id must refer to a sector that is on the specified level
        try:
            sec = world.overworld.Sector.objects.get(db_key=sec_id)
        except world.overworld.Sector.DoesNotExist:
            caller.msg(SEC_ERR_MSG);
            return
        if not sec or sec not in list(worldmap[level].values()):
            caller.msg(SEC_ERR_MSG);
            return
        # Check the coordinates are valid in this sector
        if not sec.is_valid_coordinates(coords):
            caller.msg(SEC_ERR_MSG)
            return
        # Coordinates must refer to a loc linked to externalrooms
        if coords not in sec.mapprovider.externalrooms:
            caller.msg(LOC_ERR_MSG)
            return
        # Find and edit the Loc
        props = sec.mapprovider.externalrooms[coords]
        # Only allow someone with Site edit access to do this, however
        room = search_object(props[0])[0]
        if room.access(caller, "edit"):
            mapprovider = sec.mapprovider
            mapprovider.externalrooms[coords][1] = name
            sec.db.mapprovider = mapprovider
            caller.msg(
                "The entrance name was set on Loc {}.".format(coords))
        else:
           caller.msg("You don't have permission to edit the Site properties "
                      "of %s." % room.key)