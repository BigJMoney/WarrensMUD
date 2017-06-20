"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def return_appearance(self, looker):
        """
        Appareance override

        Pieces of the appearance are broken into functions to allow overriding
        more specific pieces

        Space for self.db.hud added

        Args:
            looker (Object): Object doing the looking.
        """
        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and
                   con.access(looker, "view"))
        exits, users, things = [], [], []
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
            elif con.has_player:
                users.append("|c%s|n" % key)
            else:
                things.append(key)
        # get description, build string
        string = self.ra_name(looker)
        hud = self.db.hud
        if hud:
            string += self.ra_hud(hud)
        desc = self.db.desc
        if desc:
            string += self.ra_desc(desc)
        if exits:
            string += self.ra_exits(exits)
        if users or things:
            string += self.ra_users_things(users, things)
        string += self.ra_spacer()
        return string

    # return_appearance sub-methods

    def ra_name(self, looker):
        """
        Displays the room name

        Override for custom functionality

        Args:
            looker (Object): Object doing the looking.
        """
        return "\n|c%s|n\n" % self.get_display_name(looker)

    def ra_hud(self, hud):
        """
        Displays the room hud

        Override for custom functionality

        Args:
            hud (variable): Often an EvTable for the hud
        """
        return "%s\n" % hud

    def ra_desc(self, desc):
        """
        Displays the room desc

        Override for custom functionality

        Args:
            desc (String): The text description
        """
        return "%s" % desc

    def ra_exits(self, exits):
        """
        Displays the room exits

        Override for custom functionality

        Args:
            exits (list): Exit objects in the room (I believe)
        """
        return "\n|wExits:|n " + ", ".join(exits)

    def ra_users_things(self, users, things):
        """
        Displays the remaining room contents

        Override for custom functionality

        Args:
            users (list): Players in the room
            things (list): Other objects in the room
        """
        return "\n|wYou see:|n " + ", ".join(users + things)

    def ra_spacer(self):
        """
        Optional extra space after every room appearance
        """

        return '\n\n'
