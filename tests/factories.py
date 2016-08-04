from decimal import Decimal

import factory

from .project.models import Restaurant, Chef, Menu, PriceBracket, MenuItem, \
    MenuItemOption, MenuItemOptionChoice


class RestaurantFactory(factory.DjangoModelFactory):
    title = "Bob's Burgers"

    class Meta:
        model = Restaurant


class ChefFactory(factory.DjangoModelFactory):
    name = "DeGarnier"
    stars = 4

    class Meta:
        model = Chef


class MenuFactory(factory.DjangoModelFactory):
    restaurant = factory.SubFactory(RestaurantFactory)
    chef = factory.SubFactory(ChefFactory)
    title = 'Breakfast'

    class Meta:
        model = Menu


class PriceBracketFactory(factory.DjangoModelFactory):
    title = 'Super Expensive'

    class Meta:
        model = PriceBracket


class MenuItemFactory(factory.DjangoModelFactory):
    menu = factory.SubFactory(MenuFactory)
    price_bracket = factory.SubFactory(PriceBracketFactory)
    title = 'Scrambled Eggs'
    description = 'Deliciously Scrambled'
    price = Decimal('3.50')

    class Meta:
        model = MenuItem


class MenuItemOptionFactory(factory.DjangoModelFactory):
    menu_item = factory.SubFactory(MenuItemFactory)
    title = 'Extra Eggs'

    class Meta:
        model = MenuItemOption


class MenuItemOptionChoiceFactory(factory.DjangoModelFactory):
    option = factory.SubFactory(MenuItemOptionFactory)
    title = 'Da Doo'

    class Meta:
        model = MenuItemOptionChoice
