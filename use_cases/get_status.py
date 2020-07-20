class GetStatus:
    def __init__(self, status_service):
        self._status_service = status_service

    def execute(self):
        club_name = self._status_service.get_club_name()
        coins = self._status_service.get_coins()

        return {"club_name": club_name, "coins": coins}
