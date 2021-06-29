from enum import Enum
from functools import partial

from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout,
                             QGridLayout, QLabel, QLineEdit, QMessageBox, QDialog)
from sqlalchemy.exc import IntegrityError

from database.accessors import ProductsDataAccess, ComponentsDataAccess


class ProductsForm(QDialog):
    def __init__(self, products_accessor: ProductsDataAccess,
                 components_accessor: ComponentsDataAccess):
        super().__init__()
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(70, 150, 663, 482)
        self.setWindowTitle("Товары")

        self.products_accessor = products_accessor
        self.components_accessor = components_accessor

        layout = QVBoxLayout(self)

        self.add_button = QPushButton("Добавить")
        # noinspection PyUnresolvedReferences
        self.add_button.clicked.connect(self.show_add_form)
        layout.addWidget(self.add_button)

        self.products_table = QTableWidget()
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.update_table()
        layout.addWidget(self.products_table)

        self.setLayout(layout)

    def clear_table(self):
        curr_cols_count = self.products_table.columnCount()
        for icol in range(curr_cols_count):
            self.products_table.removeColumn(0)
        curr_rows_count = self.products_table.rowCount()
        for irow in range(curr_rows_count):
            self.products_table.removeRow(0)

    def update_table(self):
        self.clear_table()

        class Column(Enum):
            code = 0
            name = 1
            components = 2
            edit = 3
            delete = 4

        headers = ['Артикул', 'Наименование', 'Детали', 'Редактировать', 'Удалить']
        records = self.products_accessor.get_all()

        for icol, _ in enumerate(headers):
            self.products_table.insertColumn(0)

        for irow, record in enumerate(records):
            self.products_table.insertRow(irow)

            code_cell = QTableWidgetItem(record.get('code'))
            self.products_table.setItem(irow, Column.code.value, code_cell)

            name_cell = QTableWidgetItem(record.get('name'))
            self.products_table.setItem(irow, Column.name.value, name_cell)

            components_button = QPushButton('Детали')
            # noinspection PyUnresolvedReferences
            components_button.clicked.connect(partial(self.show_components_form, record))
            self.products_table.setCellWidget(irow, Column.components.value, components_button)

            add_button = QPushButton('Редактировать')
            # noinspection PyUnresolvedReferences
            add_button.clicked.connect(partial(self.show_edit_form, record))
            self.products_table.setCellWidget(irow, Column.edit.value, add_button)

            del_button = QPushButton('Удалить')
            # noinspection PyUnresolvedReferences
            del_button.clicked.connect(partial(self.delete_record, record))
            self.products_table.setCellWidget(irow, Column.delete.value, del_button)

        self.products_table.setHorizontalHeaderLabels(headers)

    def show_edit_form(self, record: dict):
        print(f"Edit form for {record = }")
        form = AddEditProductForm(self.products_accessor, replace_id=record.get('id'))
        form.show()
        form.exec_()
        self.update_table()

    def delete_record(self, record: dict):
        print(f"Delete row for {record = }")
        self.products_accessor.del_single_by_id(record.get('id'))
        self.update_table()

    def show_add_form(self):
        print("Add form")
        form = AddEditProductForm(self.products_accessor)
        form.show()
        form.exec_()
        self.update_table()

    def show_components_form(self, record: dict):
        print(f"Components form for {record = }")

        form = ComponentsForm(components_accessor=self.components_accessor,
                              product_id=record['id'])

        form.show()
        form.exec_()

        self.update_table()


class ComponentsForm(QDialog):
    def __init__(self, components_accessor: ComponentsDataAccess, product_id: int):
        super().__init__()
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(70, 150, 663, 482)
        self.setWindowTitle("Товары")

        self.components_accessor = components_accessor
        self.product_id = product_id

        layout = QVBoxLayout(self)

        self.add_button = QPushButton("Добавить")
        # noinspection PyUnresolvedReferences
        self.add_button.clicked.connect(self.show_add_form)
        layout.addWidget(self.add_button)

        self.components_table = QTableWidget()
        self.components_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.update_table()
        layout.addWidget(self.components_table)

        self.setLayout(layout)

    def clear_table(self):
        curr_cols_count = self.components_table.columnCount()
        for icol in range(curr_cols_count):
            self.components_table.removeColumn(0)
        curr_rows_count = self.components_table.rowCount()
        for irow in range(curr_rows_count):
            self.components_table.removeRow(0)

    def update_table(self):
        self.clear_table()

        class Column(Enum):
            code = 0
            name = 1
            edit = 2
            delete = 3

        headers = ['Артикул', 'Наименование', 'Редактировать', 'Удалить']
        records = self.components_accessor.get_all_by_product_id(product_id=self.product_id)

        for icol, _ in enumerate(headers):
            self.components_table.insertColumn(0)

        for irow, record in enumerate(records):
            self.components_table.insertRow(irow)

            code_cell = QTableWidgetItem(record.get('code'))
            self.components_table.setItem(irow, Column.code.value, code_cell)

            name_cell = QTableWidgetItem(record.get('name'))
            self.components_table.setItem(irow, Column.name.value, name_cell)

            add_button = QPushButton('Редактировать')
            # noinspection PyUnresolvedReferences
            add_button.clicked.connect(partial(self.show_edit_form, record))
            self.components_table.setCellWidget(irow, Column.edit.value, add_button)

            del_button = QPushButton('Удалить')
            # noinspection PyUnresolvedReferences
            del_button.clicked.connect(partial(self.delete_record, record))
            self.components_table.setCellWidget(irow, Column.delete.value, del_button)

        self.components_table.setHorizontalHeaderLabels(headers)

    def show_edit_form(self, record: dict):
        print(f"Edit form for {record = }")
        form = AddEditComponentForm(self.components_accessor,
                                    self.product_id,
                                    replace_id=record.get('id'))
        form.show()
        form.exec_()
        self.update_table()

    def delete_record(self, record: dict):
        print(f"Delete row for {record = }")
        self.components_accessor.del_single_by_id(record.get('id'))
        self.update_table()

    def show_add_form(self):
        print("Add form")
        form = AddEditComponentForm(self.components_accessor, self.product_id)
        form.show()
        form.exec_()
        self.update_table()

    def show_components_form(self, record: dict):
        print(f"Components form for {record = }")
        self.update_table()


class AddEditProductForm(QDialog):
    def __init__(self, products_accessor: ProductsDataAccess, replace_id: int = None):
        super().__init__()
        if replace_id is None:
            self.setWindowTitle('Добавить новый товар')
        else:
            self.setWindowTitle('Изменить существующий товар')
        self.resize(500, 120)

        self.products_accessor = products_accessor
        self.replace_id = replace_id

        layout = QGridLayout()

        label_name = QLabel('Наименование:')
        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText('Название товара')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.edit_name, 0, 1)

        label_code = QLabel('Артикул:')
        self.edit_code = QLineEdit()
        self.edit_code.setPlaceholderText('Артикул товара')
        layout.addWidget(label_code, 1, 0)
        layout.addWidget(self.edit_code, 1, 1)

        button_login = QPushButton('Сохранить')
        # noinspection PyUnresolvedReferences
        button_login.clicked.connect(self.save_and_close)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

    def save_and_close(self):
        try:
            name = self.edit_name.text()
            code = self.edit_code.text()
            data = {
                'name': name,
                'code': code,
            }
            if self.replace_id is None:
                self.products_accessor.add_single(data)
            else:
                self.products_accessor.replace_single_by_id(data, id_=self.replace_id)
            self.close()
        except IntegrityError as e:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText('Произошла ошибка при добавлении записи в БД')
            msg.exec_()


class AddEditComponentForm(QDialog):
    def __init__(self, accessor: ComponentsDataAccess,
                 product_id: int, replace_id: int = None):
        super().__init__()
        if replace_id is None:
            self.setWindowTitle('Добавить новую деталь')
        else:
            self.setWindowTitle('Изменить существующую деталь')
        self.resize(500, 120)

        self.components_accessor = accessor
        self.product_id = product_id
        self.replace_id = replace_id

        layout = QGridLayout()

        label_name = QLabel('Наименование:')
        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText('Название детали')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.edit_name, 0, 1)

        label_code = QLabel('Артикул:')
        self.edit_code = QLineEdit()
        self.edit_code.setPlaceholderText('Артикул детали')
        layout.addWidget(label_code, 1, 0)
        layout.addWidget(self.edit_code, 1, 1)

        button_login = QPushButton('Сохранить')
        # noinspection PyUnresolvedReferences
        button_login.clicked.connect(self.save_and_close)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

    def save_and_close(self):
        try:
            name = self.edit_name.text()
            code = self.edit_code.text()
            product_id = self.product_id
            data = {
                'name': name,
                'code': code,
                'product_id': product_id,
            }
            if self.replace_id is None:
                self.components_accessor.add_single(data)
            else:
                self.components_accessor.replace_single_by_id(data, id_=self.replace_id)
            self.close()
        except IntegrityError as e:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Произошла ошибка при добавлении записи в БД")
            msg.exec_()
