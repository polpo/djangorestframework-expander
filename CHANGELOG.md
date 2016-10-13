# Change Log

## [v0.2.3](https://github.com/silverlogic/djangorestframework-expander/tree/v0.2.2) (2016-10-05)

- Fix bug when intermediate expansion is missing. e.g. ?expand=section,section.first.second

## [v0.2.2](https://github.com/silverlogic/djangorestframework-expander/tree/v0.2.2) (2016-10-05)

- Allowed the expand request query param to be configurable.

## [v0.2.1](https://github.com/silverlogic/djangorestframework-expander/tree/v0.2.1) (2016-08-29)

- Fix a bug where the expandable fields' state was being altered between requests

## [v0.2.0](https://github.com/silverlogic/djangorestframework-expander/tree/v0.2.0) (2016-08-04)

- Add support for multiple nested expansions. i.e. `?expand=menu.restaurant,menu.chef`
