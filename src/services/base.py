import abc

from adapters.repository import BaseRepository


class BaseService(abc.ABC):
    def __init__(self, repo: BaseRepository) -> None:
        self.repo = repo
