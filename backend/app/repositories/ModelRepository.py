from typing import List, Optional, TypeVar, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, lazyload, selectinload

#from configs.Database import (
#    get_db_connection,
#)
from configs.Database import get_async_session

# Type definition for Model
M = TypeVar("M")

# Type definition for Unique Id
K = TypeVar("K")

class ModelRepository:
    db: AsyncSession
    model: Type[M]

    def __init__(
        self, model: Type[M], db: AsyncSession = Depends(get_async_session) #Depends(get_db_connection)
    ) -> None:
        self.db = db
        self.model = model

    async def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[M]:
        query = self.db.query(self.model)

        if name:
            query = query.filter_by(name=name)

        return await query.offset(start).limit(limit).all()

    async def get(self, id: K, relationships: Optional[List[str]] = None) -> Optional[M]:
        """Get an instance by id and optionally eager/lazy-load relationships.

        `relationships` should be a list of attribute names on the model (e.g. `['books', 'author']`).
        The method will build `lazyload` options for each name. Invalid names are ignored.
        """
        options = None
        if relationships:
            opts = []
            for rel in relationships:
                try:
                    attr = getattr(self.model, rel)
                except Exception:
                    # ignore invalid relationship names
                    continue
                opts.append(lazyload(attr))
            if opts:
                options = opts
        """
        options = []
        if relationships:
            for rel in relationships:
                try:
                    attr = getattr(self.model, rel)
                except Exception:
                    continue
                options.append(selectinload(attr))
        """
        return await self.db.get(self.model, id, options=options)

    async def create(self, instance: M) -> M:
        await self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, id: K, instance: M) -> M:
        instance.id = id
        await self.db.merge(instance)
        await self.db.commit()
        return instance

    async def delete(self, instance: M) -> None:
        await self.db.delete(instance)
        await self.db.commit()
        await self.db.flush()
