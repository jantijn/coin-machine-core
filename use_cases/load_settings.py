class LoadSettings:
    def __init__(self, user_service, filter_service):
        self._user_service = user_service
        self._filter_service = filter_service

    def execute(self):
        user = self._load_user()
        filters = self._load_filters()
        return user, filters

    def _load_user(self):
        return self._user_service.list()

    def _load_filters(self):
        return self._filter_service.list()
