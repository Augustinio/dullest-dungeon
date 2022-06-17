class Weapon:
    """Define Weapon class."""

    def __init__(self, name, dmg, backlash):
        """Initialize Weapon instance.

        A weapon as a name.
        A weapon has dmg that it deals to other characters.
        A weapon has backlash that it deals to its holder.
        """
        self.name = name
        self.dmg = dmg
        self.backlash = backlash
