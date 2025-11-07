"""Entry point aplikasi Inventori."""

import tkinter as tk

from controllers import (
    AuthController,
    DashboardController,
    ItemController,
    ReportController,
    SupplierController,
)
from models import Database, ItemModel, SupplierModel, TransactionModel, UserModel
from reports import ReportService
from utils import ChartBuilder
from views import LoginView, MainView


def main() -> None:
    database = Database()
    database.initialize()

    user_model = UserModel(database)
    item_model = ItemModel(database)
    supplier_model = SupplierModel(database)
    transaction_model = TransactionModel(database)

    auth_controller = AuthController(user_model)
    item_controller = ItemController(item_model, transaction_model)
    supplier_controller = SupplierController(supplier_model)
    dashboard_controller = DashboardController(item_model, transaction_model)
    report_controller = ReportController(ReportService())
    chart_builder = ChartBuilder()

    root = tk.Tk()

    def handle_login_success(user_data: dict) -> None:
        login_frame.destroy()
        for widget in root.winfo_children():
            widget.destroy()
        MainView(
            master=root,
            user=user_data,
            item_controller=item_controller,
            supplier_controller=supplier_controller,
            dashboard_controller=dashboard_controller,
            report_controller=report_controller,
            chart_builder=chart_builder,
        )

    login_frame = LoginView(root, auth_controller, handle_login_success)
    root.mainloop()


if __name__ == "__main__":
    main()

