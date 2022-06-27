"""Contains the JSON interface."""


class JSONInterface():
    """
    Parent class.
    A class that has `to_json` and `from_json` methods to convert to and from JSON.
    """

    def to_json(self) -> list | dict:
        """Function that returns a list or dictionary version of the object."""
        return self.__dict__

    @classmethod
    def from_json(cls, data: list | dict) -> None:
        """Function that takes in a list or dictionary then returns the class instantiated version."""
        raise TypeError(f"\"{cls.__name__}\" does not implement dictionary conversion.")
