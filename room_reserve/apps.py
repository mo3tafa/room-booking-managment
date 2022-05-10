from django.apps import AppConfig


class RoomReserveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'room_reserve'

    def ready(self):
        import room_reserve.signals