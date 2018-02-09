from rest_framework import mixins, serializers
from rest_framework.viewsets import ModelViewSet

from expander import ExpanderSerializerMixin

from .models import Restaurant, Chef, Menu, PriceBracket, MenuItem, \
    MenuItemOption, MenuItemOptionChoice


class RestaurantSerializer(ExpanderSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'title')

    # Overriding init to avoid circular dependency (MenuSerializer not defined yet)
    # This could also be implemented by making expandable_fields lazily evaluated,
    # using a get_expandable_fields() function, etc.
    def __init__(self, *args, **kwargs):
        expandable_fields = getattr(self.Meta, 'expandable_fields', {})
        expandable_fields.update({
            'menus': (MenuSerializer, (), {'many': True}),
        })
        setattr(self.Meta, 'expandable_fields', expandable_fields)
        super(RestaurantSerializer, self).__init__(*args, **kwargs)


class ChefSerializer(ExpanderSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id', 'name', 'stars')


class MenuSerializer(ExpanderSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'title')
        expandable_fields = {
            'restaurant': RestaurantSerializer,
            'chef': ChefSerializer,
        }


class ChefMenuSerializer(ExpanderSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id', 'name', 'stars')
        expandable_fields = {
            'menus': (MenuSerializer, (), {'many': True})
        }


class PriceBracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceBracket
        fields = ('id', 'title')


class MenuItemSerializer(ExpanderSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'menu', 'title', 'description', 'price')
        expandable_fields = {
            'menu': MenuSerializer,
            'price_bracket': (PriceBracketSerializer, (), {}),
        }


class MenuItemOptionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemOptionChoice
        fields = ('id', 'title')

    def to_representation(self, obj):
        # test: make sure the context is passed through
        assert self.context['request']
        return super(MenuItemOptionChoiceSerializer, self).to_representation(obj)


class MenuItemOptionSerializer(ExpanderSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MenuItemOption
        fields = ('id', 'menu_item', 'title')
        expandable_fields = {
            'menu_item': MenuItemSerializer,
            'choices': (MenuItemOptionChoiceSerializer, (), {'many': True}),
        }


class ChefViewSet(ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefMenuSerializer


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemOptionViewSet(ModelViewSet):
    queryset = MenuItemOption.objects.all()
    serializer_class = MenuItemOptionSerializer
