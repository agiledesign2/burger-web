from typing import List, Optional, Generic, TypeVar, Type

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload

from configs.Database import (
    get_db_connection,
)

# Type definition for Model
M = TypeVar("M")

# Type definition for Unique Id
K = TypeVar("K")

class ModelRepository:
    db: Session
    model: Type[M]

    def __init__(
        self, model: Type[M], db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db
        self.model = model

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[M]:
        query = self.db.query(self.model)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()

    def get(self, id: K, relationships: Optional[List[str]] = None) -> Optional[M]:
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

        return self.db.get(self.model, id, options=options)

    def create(self, instance: M) -> M:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: K, instance: M) -> M:
        instance.id = id
        self.db.merge(instance)
        self.db.commit()
        return instance

    def delete(self, instance: M) -> None:
        self.db.delete(instance)
        self.db.commit()
        self.db.flush()
