from entities.search_filter import SearchFilter


class GetFilters:
    def __init__(self, search_filter_service, logging_service):
        self.search_filter_service = search_filter_service
        self.logging_service = logging_service

    def execute(self):
        self.logging_service.log('Getting search filters')
        search_filters = self.search_filter_service.get_random_search_filters(2)
        for search_filter in search_filters:
            self.logging_service.log('Picked item: ' + search_filter.name)
        return search_filters
