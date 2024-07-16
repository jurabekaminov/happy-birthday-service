from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    async def create_one(self, *args, **kwargs):
        ...

    @abstractmethod
    async def read_one(self, *args, **kwargs):
        ...

    @abstractmethod
    async def read_many(self, *args, **kwargs):
        ...

    @abstractmethod
    async def delete(self, *args, **kwargs):
        ...
