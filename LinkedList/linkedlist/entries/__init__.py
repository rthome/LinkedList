from ..core import Service
from .models import Entry

class EntriesService(Service):
    __model__ = Entry
