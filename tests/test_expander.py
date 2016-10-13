from rest_framework import status

import pytest

import tests.factories as f
import tests.project.views as test_views
from expander.parse_qs import qs_from_dict
from expander.parse_qs import dict_from_qs


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


def test_it_should_be_able_to_expand_multiple_nested_fields(client):
    menu_item = f.MenuItemFactory()
    r = client.get('/menu-items/%s/?expand=menu.restaurant,menu.chef' % (
        menu_item.pk,))
    assert r.data['menu'] == {
        'id': menu_item.menu.pk,
        'restaurant': {
            'id': menu_item.menu.restaurant.pk,
            'title': menu_item.menu.restaurant.title,
        },
        'chef': {
            'id': menu_item.menu.chef.pk,
            'name': menu_item.menu.chef.name,
            'stars': menu_item.menu.chef.stars,
        },
        'title': menu_item.menu.title
    }

def test_kwargs_reused_across_requests(client):
    meta = test_views.MenuItemSerializer.Meta
    price_bracket_spec = meta.expandable_fields['price_bracket']

    assert (test_views.PriceBracketSerializer, (), {}) == price_bracket_spec

    menu_item = f.MenuItemFactory()
    r = client.get('/menu-items/%s/?expand=menu.restaurant,menu.chef' % (
        menu_item.pk,))

    # Spec has not been altered
    assert (test_views.PriceBracketSerializer, (), {}) == price_bracket_spec


def test_can_parse_expand_querystring(client):
    assert {"latestPeriod": {}} == dict_from_qs("latestPeriod")
    assert {"latestPeriod": {"fhr": {}}} == dict_from_qs("latestPeriod.fhr")
    assert {"latestPeriod": {"fhr": {}, "di": {}}} == (
        dict_from_qs("latestPeriod.fhr,latestPeriod.di"))
    assert {"latestPeriod": {"fhr": {"asd": {}}}} == dict_from_qs("latestPeriod,latestPeriod.fhr.asd")

    expected = {"latestPeriod": {
                "fhr": {}, "di": {}, "creditModel": {
                    "creditModel": {}}}}
    actual = dict_from_qs(
                    "latestPeriod.fhr,latestPeriod.di,"
                    "latestPeriod.creditModel.creditModel")
    assert expected == actual


def test_can_reverse_parse_dict_to_querystring(client):
    assert "fhr" == qs_from_dict({"fhr": {}})
    assert "di,fhr" == qs_from_dict({"fhr": {}, "di": {}})

    assert "di,fhr.inner1" == qs_from_dict({"fhr": {"inner1": {}}, "di": {}})

    assert ("di,fhr.inner1.inner2,fhr.inner1.inner3" ==
            qs_from_dict({"fhr": {"inner1": {
                         "inner2": {}, "inner3": {}}},
                         "di": {}}))
