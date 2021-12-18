"""A library for dataclasses."""

# pylint: disable=line-too-long
# pylint: disable=unused-argument
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods

from __future__ import annotations
import abc

import functions.other_functions as o_f


class Dataclass():
    """Base class for dataclasses."""

    def get_dict(self):
        """Gets the dictionary object of the function."""
        return o_f.get_dict_attr(self)

    def from_dict(self, data: dict):
        """Returns an object with data given by a dictionary."""
        for key, value in data.items():
            try:
                getattr(self, key)
            except AttributeError as exc:
                raise AttributeError(f"Attribute '{key}' not found for object of type '{self.__class__.__name__}'") from exc
            if isinstance(value, dict):
                obj: Dataclass = getattr(self, key)
                setattr(self, key, obj.from_dict(value))
            else:
                setattr(self, key, value)
        return self

    def __repr__(self) -> str:
        return str(self.get_dict())


class DataclassSub(Dataclass):
    """Base class for dataclasses inside dataclasses."""


def init_wrapper(init, end_init):
    """Wraps the init function of DataclassConvention classes."""
    def wrapper(*args, **kwargs):
        init(*args, **kwargs)
        end_init(*args, **kwargs)
    return wrapper

class DataclassConvention(Dataclass):
    """Base class for standard and non-standard dataclasses."""

    @abc.abstractmethod
    def end_init(self, data=None):
        """Called at the end of the __init__ function to implement the data."""

    def __init_subclass__(cls) -> None:
        cls.__init__ = init_wrapper(cls.__init__, cls.end_init)


class StandardDataclass(abc.ABC, DataclassConvention):
    """Base class for standard dataclasses.
    These are classes used as a base for other non-standard dataclasses."""

    def default_data(self):
        """Returns the default data."""
        return self.get_dict()

    def end_init(self, data=None):
        if data is None:
            self.from_dict(self.default_data())
            return
        self.from_dict(self.dict_from_nonstandard(data))

    @abc.abstractmethod
    def dict_from_nonstandard(self, data):
        """Creates a dictionary based off of the nonstandard dataclass."""

class NonStandardDataclass(abc.ABC, DataclassConvention):
    """Base class for non-standard dataclasses.
    These are classes that are slight derivations from a standard dataclass."""

    @abc.abstractproperty
    def default_class(self):
        """Default class to bind to."""

    def get_default_dict(self):
        """Gets the default dictionary for this dataclass."""
        return self.__class__(self.default_class()).get_dict()

    def end_init(self, data=None):
        """Added to the end of the __init__ function to put the data into the dataclass's fields."""
        if isinstance(data, self.default_class):
            converted_data = self.dict_from_default(data)
        elif isinstance(data, dict):
            converted_data = data
        else:
            converted_data = self.dict_from_default(self.default_class())

        self.from_dict(converted_data)

    @abc.abstractmethod
    def dict_from_default(self, data: StandardDataclass):
        """Returns a dictionary with default values of the default dataclass converted into this dataclass."""
        return {}
