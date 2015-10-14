from rest_framework import status

import pytest

import tests.factories as f


pytestmark = pytest.mark.django_db


def test_it_should_be_collapsed_when_no_expansion_is_specified(client):
    menu_item = f.MenuItemFactory()
    r = client.get('/menu-items/%s/' % menu_item.pk)
    assert r.data['menu'] == menu_item.menu.pk


def test_it_should_expand_when_expansion_is_specified(client):
    menu_item = f.MenuItemFactory()
    r = client.get('/menu-items/%s/?expand=menu' % menu_item.pk)
    assert r.data['menu'] == {
        'id': menu_item.menu.pk,
        'restaurant': menu_item.menu.restaurant.pk,
        'title': menu_item.menu.title
    }


def test_when_expand_is_not_in_expandable_fields(client):
    menu_item = f.MenuItemFactory()
    r = client.get('/menu-items/%s/?expand=blub' % menu_item.pk)
    assert r.status_code == status.HTTP_200_OK


def test_it_should_be_able_to_expand_multiple_fields(client):
    menu_item = f.MenuItemFactory()
    r = client.get('/menu-items/%s/?expand=menu,price_bracket' % menu_item.pk)
    assert r.data['menu'] == {
        'id': menu_item.menu.pk,
        'restaurant': menu_item.menu.restaurant.pk,
        'title': menu_item.menu.title
    }
    assert r.data['price_bracket'] == {
        'id': menu_item.price_bracket.pk,
        'title': menu_item.price_bracket.title
    }


def test_can_expand_nested(client):
    option = f.MenuItemOptionFactory()
    menu_item = option.menu_item
    r = client.get('/menu-item-options/%s/?expand=menu_item.menu.restaurant' % option.pk)
    assert r.data['menu_item']['menu'] == {
        'id': menu_item.menu.pk,
        'restaurant': {
            'id': menu_item.menu.restaurant.pk,
            'title': menu_item.menu.restaurant.title,
        },
        'title': menu_item.menu.title
    }


def test_can_expand_lists(client):
    option = f.MenuItemOptionFactory()
    choice1 = f.MenuItemOptionChoiceFactory(option=option)
    choice2 = f.MenuItemOptionChoiceFactory(option=option)
    r = client.get('/menu-item-options/%s/?expand=choices' % option.pk)
    assert r.data['choices'] == [
        {'id': choice1.pk, 'title': choice1.title},
        {'id': choice2.pk, 'title': choice2.title},

    ]
