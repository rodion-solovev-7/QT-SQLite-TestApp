from PyQt5.QtWidgets import QApplication
from sqlalchemy.orm import Session

from database.connect import make_session
from database.accessors import ProductsDataAccess, ComponentsDataAccess
from database.models import Product, Component
from forms import ProductsForm


def suppress_qt_warnings():
    from os import environ
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def fill_db_if_empty():
    with make_session() as session:
        session: Session

        if session.query(Product).first() is None:
            # noinspection PyArgumentList
            products = [Product(name=str(i), code=str(i))
                        for i in range(1, 10 + 1)]
            session.add_all(products)
            session.commit()

            # noinspection PyArgumentList
            components = [Component(name=str(i), code=str(i), product_id=(i % 10) + 1)
                          for i in range(1, 100 + 1)]
            session.add_all(components)
            session.commit()


def main():
    suppress_qt_warnings()
    fill_db_if_empty()

    from sys import argv
    app = QApplication(argv)

    form = ProductsForm(products_accessor=ProductsDataAccess(),
                        components_accessor=ComponentsDataAccess())
    form.show()
    exit(app.exec_())


if __name__ == "__main__":
    main()
