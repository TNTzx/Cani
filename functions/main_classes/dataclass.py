"""Stores dataclasses."""

# pylint: disable=line-too-long
# pylint: disable=unused-argument
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods

import dataclasses as dtc
import functions.other_functions as o_f

class Dataclass():
    """Contains functions for dataclasses."""
    def get_dict(self):
        """Gets the dictionary object of the function."""
        return o_f.get_dict_attr(self)

    def from_dict(self, data: dict):
        """Returns an object with data given by a dictionary."""
        for key, value in data.items():
            if isinstance(value, dict):
                obj: Dataclass = getattr(self, key)
                setattr(self, key, obj.from_dict(value))
            else:
                setattr(self, key, value)
        return self

    def __repr__(self) -> str:
        return str(self.get_dict())


@dtc.dataclass()
class NewClass(Dataclass):
    """test class"""
    class NoBeans(Dataclass):
        """test class"""
        more_beans: int = 0

    beans: int = 0
    no_beans: NoBeans = NoBeans()

newestest = NewClass().from_dict({
    "beans": 1892361278931,
    "no_beans": {
        "more_beans": 10
    }
})

print(newestest)
