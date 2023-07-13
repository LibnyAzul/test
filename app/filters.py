"""
Filtra el queryset según los datos proporcionados en el diccionario 'data'.
Args:
    data (dict): Diccionario con los datos de filtrado.
    queryset (QuerySet): QuerySet inicial a filtrar.

Returns:
    QuerySet: QuerySet filtrado.
"""
class CustomFilter():
    def custom_filter(self, data, queryset):
        OPERATORS = {
            'exact': '__exact',
            'iexact': '__iexact',
            'contains': '__contains',
            'lt': '__lt',
            'lte': '__lte',
            'gt': '__gt',
            'gte': '__gte',
            'distinct': '__distinct',
            'isEmpty': '__isnull',
            'isNotEmpty': '__isnull',
            'startswith': '__startswith',
            'startsWith': '__startswith',
            'endswith': '__endswith',
            'endsWith': '__endswith',
            'isAnyOf': '__in',
            'orderBy': ''
        }

        if 'filters' in data:
            filters = data['filters']
            if len(filters) > 0:
                for filter in filters:
                    for operation in OPERATORS:
                        if operation in filter['filter']:
                            if operation == 'orderBy':
                                if filter['value'] == 'asc':
                                    queryset = queryset.order_by(filter['column'])
                                elif filter['value'] == 'desc':
                                    queryset = queryset.order_by('-' + filter['column'])
                            else:
                                column_filter = f"{filter['column']}{OPERATORS[operation]}"
                                value = not filter['value'] if 'Not' in operation else filter['value']
                                queryset = queryset.filter(**{column_filter: value})

        return queryset
