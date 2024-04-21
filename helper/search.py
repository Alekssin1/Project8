import operator
from functools import reduce


from django.db.models.constants import LOOKUP_SEP


from django.db import models


class SearchFilter:
    # The URL query parameter used for the search.
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
    }

    def __init__(self, search_fields, search_terms):
        self.search_fields = search_fields
        self.search_terms = search_terms

    def get_search_fields(self):
        """
        Search fields are obtained from the view, but the request is always
        passed to this method. Sub-classes can override this method to
        dynamically change the search fields based on request content.
        """
        return self.search_fields

    def get_search_terms(self):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """

        return self.search_terms.split()

    def construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = 'icontains'
        return LOOKUP_SEP.join([field_name, lookup])

    def filter_queryset(self, queryset, is_admin=False):
        search_fields = self.get_search_fields()
        search_terms = self.get_search_terms()

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]

        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))

        conditions_queryset = queryset.filter(
            reduce(operator.and_, conditions))

        return conditions_queryset