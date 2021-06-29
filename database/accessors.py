"""Обёртки на случай трансформации БД в JSON'ку или смены ORM"""

from typing import Iterable

from sqlalchemy.orm import Session

from database.connect import make_session
from database.models import Product, Component


class ProductsDataAccess:
    def add_single(self, data: dict):
        with make_session() as session:
            session: Session
            record = Product()
            record.name = data.get('name')
            record.code = data.get('code')
            session.add(record)
            session.commit()

    def replace_single_by_id(self, data: dict, id_: int):
        with make_session() as session:
            session: Session
            record = session.query(Product).filter_by(id=id_).first()
            if record is not None:
                record.name = data.get('name')
                record.code = data.get('code')
                session.commit()

    def del_single_by_id(self, id_: int):
        with make_session() as session:
            session: Session
            record = session.query(Product).filter_by(id=id_).first()
            if record is not None:
                session.delete(record)
                session.commit()

    def get_all(self) -> Iterable[dict]:
        with make_session() as session:
            session: Session
            return map(Product.asdict, session.query(Product).all())

    def count(self) -> int:
        with make_session() as session:
            session: Session
            return session.query(Product).count_by_product_id()


class ComponentsDataAccess:
    def add_single(self, data: dict):
        with make_session() as session:
            session: Session
            record = Component()
            record.name = data.get('name')
            record.code = data.get('code')
            record.product_id = data.get('product_id')
            session.add(record)
            session.commit()

    def replace_single_by_id(self, data: dict, id_: int):
        with make_session() as session:
            session: Session
            record: Component = session.query(Component).filter_by(id=id_).first()
            if record is not None:
                record.name = data.get('name')
                record.code = data.get('code')
                record.product_id = data.get('product_id')
                session.commit()

    def del_single_by_id(self, id_: int):
        with make_session() as session:
            session: Session
            record = session.query(Component).filter_by(id=id_).first()
            if record is not None:
                session.delete(record)
                session.commit()

    def get_all_by_product_id(self, product_id: int) -> Iterable[dict]:
        with make_session() as session:
            session: Session
            records = session.query(Component).filter_by(product_id=product_id).all()
            return map(Component.asdict, records)

    def count_by_product_id(self, product_id: int) -> int:
        with make_session() as session:
            session: Session
            return session.query(Component).filter_by(product_id=product_id).count()
