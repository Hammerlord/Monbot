from src.elemental.attribute.attribute_factory import AttributeFactory
from src.elemental.elemental import Elemental


class ElementalFactory:
    """
    Factory methods for creating specific Elementals.
    """

    @staticmethod
    def rainatu():
        return Elemental(Rainatu(),
                         AttributeFactory.create_manager())

    @staticmethod
    def roaus():
        return Elemental(Roaus(),
                         AttributeFactory.create_manager())

    @staticmethod
    def mithus():
        return Elemental(Mithus(),
                         AttributeFactory.create_manager())

    @staticmethod
    def sithel():
        return Elemental(Sithel(),
                         AttributeFactory.create_manager())