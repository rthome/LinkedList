from ..core import Service
from .models import Entry, ArchivedEntry


class EntriesService(Service):
    __model__ = Entry


class ArchiveService(Service):
    __model__ = ArchivedEntry
