from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship


class __ModelExtensions:
    """Class with functions for useful work with models"""

    def __repr__(self):
        represent = ", ".join((f"{k}={repr(v)}" for k, v in self.asdict().items()))
        return f"<{type(self).__name__} ({represent})>"

    def asdict(self) -> dict:
        """Get model as dict"""
        return dict((k, v) for k, v in self.__dict__.items() if not k.startswith('_'))


base = declarative_base()


class Product(base, __ModelExtensions):
    __tablename__ = "products"
    __table_args__ = tuple()

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)


class Component(base, __ModelExtensions):
    __tablename__ = "components"
    __table_args__ = tuple()

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)


# <= you can insert new models here

metadata: MetaData = base.metadata
