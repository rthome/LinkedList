"""
LinkedList data services
"""

from .users import UsersService
from .entries import EntriesService, ArchiveService

users = UsersService()
entries = EntriesService()
archive = ArchiveService()
