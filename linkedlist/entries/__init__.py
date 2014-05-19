from ..core import Service
from .models import Entry


class EntriesService(Service):
    __model__ = Entry

    def get_for_user(self, user):
        return self.find(user_id = user.id)
