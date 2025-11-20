"""View utama setelah login."""

from __future__ import annotations

import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.formatters import format_currency

class MainView(tk.Frame):
    def __init__(
        self,
        master: tk.Tk,
        user: dict,
        item_controller: "ItemController",
        supplier_controller: "SupplierController",
        dashboard_controller: "DashboardController",
        report_controller: "ReportController",
        chart_builder: "ChartBuilder",
    ) -> None:
        super().__init__(master)
        self.master = master
        self.user = user
        self.item_controller = item_controller
        self.supplier_controller = supplier_controller
        self.dashboard_controller = dashboard_controller
        self.report_controller = report_controller
        self.chart_builder = chart_builder

        self.item_vars = {
            "item_id": tk.IntVar(value=0),
            "item_code": tk.StringVar(),
            "item_name": tk.StringVar(),
            "category": tk.StringVar(),
            "stock": tk.IntVar(value=0),
            "purchase_price": tk.DoubleVar(value=0.0),
            "selling_price": tk.DoubleVar(value=0.0),
            "supplier": tk.StringVar(),
            "search": tk.StringVar(),
        }

        self.supplier_vars = {
            "supplier_id": tk.IntVar(value=0),
            "supplier_name": tk.StringVar(),
            "address": tk.StringVar(),
            "search": tk.StringVar(),
        }

        self.transaction_vars = {
            "item": tk.StringVar(),
            "quantity": tk.IntVar(value=1),
            "type": tk.StringVar(value="IN"),
            "notes": tk.StringVar(),
        }

        self.categories_cache = []
        self.suppliers_cache = []
        self.items_cache = []

        self._build_ui()
        self.refresh_all()
        self._apply_role_permissions()

    def _build_ui(self) -> None:
        self.master.title("Sistem Informasi Inventori Barang")
        self.master.geometry("1024x640")
        self.master.minsize(900, 600)

        header = ttk.Frame(self)
        header.pack(fill="x", padx=16, pady=8)

        ttk.Label(
            header,
            text=f"Selamat datang, {self.user['username']} ({self.user['level']})",
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left")

        ttk.Button(header, text="Keluar", command=self._logout).pack(side="right")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.dashboard_tab = ttk.Frame(self.notebook)
        self.items_tab = ttk.Frame(self.notebook)
        self.suppliers_tab = ttk.Frame(self.notebook)
        self.transactions_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.items_tab, text="Barang")
        self.notebook.add(self.suppliers_tab, text="Pemasok")
        self.notebook.add(self.transactions_tab, text="Transaksi")

        self._build_dashboard_tab()
        self._build_items_tab()
        self._build_suppliers_tab()
        self._build_transactions_tab()

        self.pack(fill="both", expand=True)

    def _build_dashboard_tab(self) -> None:
        frame = self.dashboard_tab
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        summary_frame = ttk.LabelFrame(frame, text="Ringkasan")
        summary_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        summary_frame.columnconfigure(0, weight=1)

        self.total_items_var = tk.StringVar(value="0 Barang")
        self.total_stock_var = tk.StringVar(value="0 Stok")

        ttk.Label(summary_frame, textvariable=self.total_items_var, font=("Segoe UI", 14)).pack(pady=8)
        ttk.Label(summary_frame, textvariable=self.total_stock_var, font=("Segoe UI", 14)).pack(pady=8)

        low_stock_frame = ttk.LabelFrame(frame, text="Stok Rendah")
        low_stock_frame.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")

        columns = ("nama", "stok")
        self.low_stock_tree = ttk.Treeview(low_stock_frame, columns=columns, show="headings", height=6)
        self.low_stock_tree.heading("nama", text="Barang")
        self.low_stock_tree.heading("stok", text="Stok")
        self.low_stock_tree.column("nama", width=180)
        self.low_stock_tree.column("stok", width=80, anchor="center")
        self.low_stock_tree.pack(fill="both", expand=True, padx=6, pady=6)

        chart_frame = ttk.LabelFrame(frame, text="Grafik Stok")
        chart_frame.grid(row=1, column=0, columnspan=2, padx=12, pady=12, sticky="nsew")
        chart_frame.columnconfigure(0, weight=1)

        self.chart_canvas = None
        self.chart_container = ttk.Frame(chart_frame)
        self.chart_container.pack(fill="both", expand=True)

        recent_frame = ttk.LabelFrame(frame, text="Transaksi Terbaru")
        recent_frame.grid(row=2, column=0, columnspan=2, padx=12, pady=12, sticky="nsew")

        columns = ("tanggal", "barang", "jenis", "jumlah")
        self.recent_tree = ttk.Treeview(recent_frame, columns=columns, show="headings", height=6)
        self.recent_tree.heading("tanggal", text="Tanggal")
        self.recent_tree.heading("barang", text="Barang")
        self.recent_tree.heading("jenis", text="Jenis")
        self.recent_tree.heading("jumlah", text="Jumlah")
        for col in columns:
            self.recent_tree.column(col, anchor="center")
        self.recent_tree.pack(fill="both", expand=True, padx=6, pady=6)

    def _build_items_tab(self) -> None:
        frame = self.items_tab
        frame.columnconfigure(0, weight=2)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)

        # Search bar
        search_frame = ttk.Frame(frame)
        search_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ttk.Entry(search_frame, textvariable=self.item_vars["search"], width=30).pack(side="left", padx=(0, 8))
        ttk.Button(search_frame, text="Cari", command=self.search_items).pack(side="left")
        ttk.Button(search_frame, text="Reset", command=self.reset_item_search).pack(side="left", padx=(8, 0))

        # Treeview
        columns = ("kode", "nama", "kategori", "stok", "harga_beli", "harga_jual", "pemasok")
        self.items_tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.items_tree.heading(col, text=col.replace("_", " ").title())
        self.items_tree.column("kode", width=100)
        self.items_tree.column("nama", width=160)
        self.items_tree.column("kategori", width=100)
        self.items_tree.column("stok", width=80, anchor="center")
        self.items_tree.column("harga_beli", width=100, anchor="e")
        self.items_tree.column("harga_jual", width=100, anchor="e")
        self.items_tree.column("pemasok", width=120)
        self.items_tree.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        self.items_tree.bind("<<TreeviewSelect>>", self.on_item_select)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=0, sticky="nse")

        # Form
        form_frame = ttk.LabelFrame(frame, text="Form Barang")
        form_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=8, pady=8)
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Kode Barang").grid(row=0, column=0, sticky="w", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.item_vars["item_code"]).grid(row=0, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Nama Barang").grid(row=1, column=0, sticky="w", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.item_vars["item_name"]).grid(row=1, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Kategori").grid(row=2, column=0, sticky="w", pady=4, padx=4)
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.item_vars["category"], state="readonly")
        self.category_combo.grid(row=2, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Stok").grid(row=3, column=0, sticky="w", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.item_vars["stock"]).grid(row=3, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Harga Beli").grid(row=4, column=0, sticky="w", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.item_vars["purchase_price"]).grid(row=4, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Harga Jual").grid(row=5, column=0, sticky="w", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.item_vars["selling_price"]).grid(row=5, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Pemasok").grid(row=6, column=0, sticky="w", pady=4, padx=4)
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.item_vars["supplier"], state="readonly")
        self.supplier_combo.grid(row=6, column=1, sticky="ew", pady=4, padx=4)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        self.btn_item_save = ttk.Button(button_frame, text="Simpan", command=self.save_item)
        self.btn_item_save.grid(row=0, column=0, padx=4)
        self.btn_item_delete = ttk.Button(button_frame, text="Hapus", command=self.delete_item)
        self.btn_item_delete.grid(row=0, column=1, padx=4)
        self.btn_item_clear = ttk.Button(button_frame, text="Bersihkan", command=self.clear_item_form)
        self.btn_item_clear.grid(row=0, column=2, padx=4)

        report_frame = ttk.Frame(form_frame)
        report_frame.grid(row=8, column=0, columnspan=2, pady=10)
        self.btn_export_pdf = ttk.Button(report_frame, text="Export PDF", command=self.export_pdf)
        self.btn_export_pdf.grid(row=0, column=0, padx=4)
        self.btn_export_excel = ttk.Button(report_frame, text="Export Excel", command=self.export_excel)
        self.btn_export_excel.grid(row=0, column=1, padx=4)

    def _build_suppliers_tab(self) -> None:
        frame = self.suppliers_tab
        frame.columnconfigure(0, weight=2)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)

        search_frame = ttk.Frame(frame)
        search_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ttk.Entry(search_frame, textvariable=self.supplier_vars["search"], width=30).pack(side="left", padx=(0, 8))
        ttk.Button(search_frame, text="Cari", command=self.search_suppliers).pack(side="left")
        ttk.Button(search_frame, text="Reset", command=self.reset_supplier_search).pack(side="left", padx=(8, 0))

        columns = ("nama", "alamat")
        self.suppliers_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.suppliers_tree.heading("nama", text="Nama Pemasok")
        self.suppliers_tree.heading("alamat", text="Alamat")
        self.suppliers_tree.column("nama", width=180)
        self.suppliers_tree.column("alamat", width=180)
        self.suppliers_tree.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        self.suppliers_tree.bind("<<TreeviewSelect>>", self.on_supplier_select)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.suppliers_tree.yview)
        self.suppliers_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=0, sticky="nse")

        form_frame = ttk.LabelFrame(frame, text="Form Pemasok")
        form_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=8, pady=8)
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Nama Pemasok").grid(row=0, column=0, sticky="w", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.supplier_vars["supplier_name"]).grid(row=0, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Alamat").grid(row=1, column=0, sticky="w", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.supplier_vars["address"]).grid(row=1, column=1, sticky="ew", pady=4, padx=4)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.btn_supplier_save = ttk.Button(button_frame, text="Simpan", command=self.save_supplier)
        self.btn_supplier_save.grid(row=0, column=0, padx=4)
        self.btn_supplier_delete = ttk.Button(button_frame, text="Hapus", command=self.delete_supplier)
        self.btn_supplier_delete.grid(row=0, column=1, padx=4)
        self.btn_supplier_clear = ttk.Button(button_frame, text="Bersihkan", command=self.clear_supplier_form)
        self.btn_supplier_clear.grid(row=0, column=2, padx=4)

    def _build_transactions_tab(self) -> None:
        frame = self.transactions_tab
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        form_frame = ttk.LabelFrame(frame, text="Form Transaksi")
        form_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Barang").grid(row=0, column=0, sticky="w", pady=4, padx=4)
        self.transaction_item_combo = ttk.Combobox(form_frame, textvariable=self.transaction_vars["item"], state="readonly")
        self.transaction_item_combo.grid(row=0, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Jumlah").grid(row=1, column=0, sticky="w", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.transaction_vars["quantity"]).grid(row=1, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Jenis").grid(row=2, column=0, sticky="w", pady=4, padx=4)
        ttk.Combobox(
            form_frame,
            textvariable=self.transaction_vars["type"],
            values=("IN", "OUT"),
            state="readonly",
        ).grid(row=2, column=1, sticky="ew", pady=4, padx=4)

        ttk.Label(form_frame, text="Catatan").grid(row=3, column=0, sticky="nw", pady=4, padx=4)
        ttk.Entry(form_frame, textvariable=self.transaction_vars["notes"]).grid(row=3, column=1, sticky="ew", pady=4, padx=4)

        ttk.Button(form_frame, text="Simpan Transaksi", command=self.save_transaction).grid(row=4, column=0, columnspan=2, pady=10)

        history_frame = ttk.LabelFrame(frame, text="Riwayat Transaksi")
        history_frame.grid(row=1, column=0, padx=12, pady=12, sticky="nsew")

        columns = ("tanggal", "barang", "jenis", "jumlah")
        self.transaction_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.transaction_tree.heading(col, text=col.title())
            self.transaction_tree.column(col, anchor="center")
        self.transaction_tree.pack(fill="both", expand=True, padx=6, pady=6)

    # Event handlers
    def refresh_all(self) -> None:
        self.load_categories()
        self.load_suppliers()
        self.load_items()
        self.load_suppliers_list()
        self.load_transactions()
        self.load_dashboard()

    def load_dashboard(self) -> None:
        data = self.dashboard_controller.get_dashboard_data()
        summary = data["summary"]
        self.total_items_var.set(f"Total Barang: {summary['total_items']}")
        self.total_stock_var.set(f"Total Stok: {summary['total_stock']}")

        for row in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(row)
        for item in summary["low_stock_items"]:
            self.low_stock_tree.insert("", "end", values=(item["item_name"], item["stock"]))

        for row in self.recent_tree.get_children():
            self.recent_tree.delete(row)
        for trx in data["recent_transactions"]:
            self.recent_tree.insert(
                "",
                "end",
                values=(trx["transaction_date"], trx["item_name"], trx["transaction_type"], trx["quantity"]),
            )

        items = self.item_controller.list_items()
        figure = self.chart_builder.build_stock_chart(items[:8])
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
        self.chart_canvas = FigureCanvasTkAgg(figure, master=self.chart_container)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_items(self, keyword: str = "") -> None:
        records = self.item_controller.list_items(keyword)
        if not keyword:
            self.items_cache = records
        for row in self.items_tree.get_children():
            self.items_tree.delete(row)
        for item in records:
            self.items_tree.insert(
                "",
                "end",
                iid=item["id"],
                values=(
                    item["item_code"],
                    item["item_name"],
                    item.get("category", "-"),
                    item["stock"],
                    format_currency(item["purchase_price"]),
                    format_currency(item["selling_price"]),
                    item.get("supplier", "-"),
                ),
            )

    def load_suppliers_list(self, keyword: str = "") -> None:
        records = self.supplier_controller.list_suppliers(keyword)
        for row in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(row)
        for supplier in records:
            self.suppliers_tree.insert(
                "",
                "end",
                iid=supplier["id"],
                values=(supplier["supplier_name"], supplier.get("address", "-")),
            )

    def load_transactions(self) -> None:
        records = self.item_controller.get_all_transactions()
        for row in self.transaction_tree.get_children():
            self.transaction_tree.delete(row)
        for trx in records:
            self.transaction_tree.insert(
                "",
                "end",
                values=(trx["transaction_date"], trx["item_name"], trx["transaction_type"], trx["quantity"]),
            )

    def load_categories(self) -> None:
        categories = self.item_controller.get_categories()
        self.categories_cache = categories
        self.category_combo["values"] = [cat["name"] for cat in categories]

    def load_suppliers(self) -> None:
        suppliers = self.supplier_controller.list_suppliers()
        self.suppliers_cache = suppliers
        self.supplier_combo["values"] = [sup["supplier_name"] for sup in suppliers]
        display_items = self.items_cache or self.item_controller.list_items()
        self.transaction_item_combo["values"] = [
            "{} - {}".format(item["item_code"], item["item_name"])
            for item in display_items
        ]

    def search_items(self) -> None:
        keyword = self.item_vars["search"].get()
        self.load_items(keyword)

    def reset_item_search(self) -> None:
        self.item_vars["search"].set("")
        self.load_items()

    def search_suppliers(self) -> None:
        keyword = self.supplier_vars["search"].get()
        self.load_suppliers_list(keyword)

    def reset_supplier_search(self) -> None:
        self.supplier_vars["search"].set("")
        self.load_suppliers_list()

    def on_item_select(self, event) -> None:  # noqa: D401
        selection = self.items_tree.selection()
        if not selection:
            return
        item_id = int(selection[0])
        data = self.item_controller.item_model.get_by_id(item_id)
        if not data:
            return
        self.item_vars["item_id"].set(data["id"])
        self.item_vars["item_code"].set(data["item_code"])
        self.item_vars["item_name"].set(data["item_name"])
        self.item_vars["stock"].set(data["stock"])
        self.item_vars["purchase_price"].set(data["purchase_price"])
        self.item_vars["selling_price"].set(data["selling_price"])

        category = next((c for c in self.categories_cache if c["id"] == data.get("category_id")), None)
        supplier = next((s for s in self.suppliers_cache if s["id"] == data.get("supplier_id")), None)
        self.item_vars["category"].set(category["name"] if category else "")
        self.item_vars["supplier"].set(supplier["supplier_name"] if supplier else "")

    def on_supplier_select(self, event) -> None:  # noqa: D401
        selection = self.suppliers_tree.selection()
        if not selection:
            return
        supplier_id = int(selection[0])
        data = self.supplier_controller.supplier_model.get_by_id(supplier_id)
        if not data:
            return
        self.supplier_vars["supplier_id"].set(data["id"])
        self.supplier_vars["supplier_name"].set(data["supplier_name"])
        self.supplier_vars["address"].set(data.get("address", ""))

    def save_item(self) -> None:
        category_id = self._get_category_id(self.item_vars["category"].get())
        supplier_id = self._get_supplier_id(self.item_vars["supplier"].get())
        payload = {
            "item_code": self.item_vars["item_code"].get(),
            "item_name": self.item_vars["item_name"].get(),
            "category_id": category_id,
            "stock": self._safe_int(self.item_vars["stock"].get()),
            "purchase_price": self._safe_float(self.item_vars["purchase_price"].get()),
            "selling_price": self._safe_float(self.item_vars["selling_price"].get()),
            "supplier_id": supplier_id,
        }
        item_id = self.item_vars["item_id"].get()
        if item_id:
            success, message = self.item_controller.update_item(item_id, payload)
        else:
            success, message = self.item_controller.add_item(payload)

        if success:
            messagebox.showinfo("Informasi", message)
            self.clear_item_form()
            self.load_items()
            self.load_suppliers()
            self.load_dashboard()
        else:
            messagebox.showerror("Gagal", message)

    def delete_item(self) -> None:
        item_id = self.item_vars["item_id"].get()
        if not item_id:
            messagebox.showwarning("Perhatian", "Pilih data barang terlebih dahulu")
            return
        if not messagebox.askyesno("Konfirmasi", "Yakin akan menghapus data ini?"):
            return
        success, message = self.item_controller.delete_item(item_id)
        if success:
            messagebox.showinfo("Informasi", message)
            self.clear_item_form()
            self.load_items()
            self.load_suppliers()
            self.load_dashboard()
        else:
            messagebox.showerror("Gagal", message)

    def clear_item_form(self) -> None:
        for key in ["item_id", "stock"]:
            self.item_vars[key].set(0)
        for key in ["item_code", "item_name", "category", "supplier"]:
            self.item_vars[key].set("")
        self.item_vars["purchase_price"].set(0.0)
        self.item_vars["selling_price"].set(0.0)
        self.items_tree.selection_remove(self.items_tree.selection())

    def export_pdf(self) -> None:
        destination = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Simpan Laporan Lengkap PDF",
        )
        if not destination:
            return
        success, message = self.report_controller.export_pdf(
            self.item_controller.list_items(),
            self.item_controller.get_all_transactions(),
            destination
        )
        if success:
            messagebox.showinfo("Sukses", message)
        else:
            messagebox.showerror("Gagal", message)

    def export_excel(self) -> None:
        destination = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            title="Simpan Laporan Lengkap Excel",
        )
        if not destination:
            return
        success, message = self.report_controller.export_excel(
            self.item_controller.list_items(),
            self.item_controller.get_all_transactions(),
            destination
        )
        if success:
            messagebox.showinfo("Sukses", message)
        else:
            messagebox.showerror("Gagal", message)


    def save_supplier(self) -> None:
        payload = {
            "supplier_name": self.supplier_vars["supplier_name"].get(),
            "address": self.supplier_vars["address"].get(),
        }
        supplier_id = self.supplier_vars["supplier_id"].get()
        if supplier_id:
            success, message = self.supplier_controller.update_supplier(supplier_id, payload)
        else:
            success, message = self.supplier_controller.add_supplier(payload)
        if success:
            messagebox.showinfo("Informasi", message)
            self.clear_supplier_form()
            self.load_suppliers_list()
            self.load_suppliers()
        else:
            messagebox.showerror("Gagal", message)

    def delete_supplier(self) -> None:
        supplier_id = self.supplier_vars["supplier_id"].get()
        if not supplier_id:
            messagebox.showwarning("Perhatian", "Pilih data pemasok terlebih dahulu")
            return
        if not messagebox.askyesno("Konfirmasi", "Yakin akan menghapus data pemasok?"):
            return
        success, message = self.supplier_controller.delete_supplier(supplier_id)
        if success:
            messagebox.showinfo("Informasi", message)
            self.clear_supplier_form()
            self.load_suppliers_list()
            self.load_suppliers()
        else:
            messagebox.showerror("Gagal", message)

    def clear_supplier_form(self) -> None:
        self.supplier_vars["supplier_id"].set(0)
        self.supplier_vars["supplier_name"].set("")
        self.supplier_vars["address"].set("")
        self.suppliers_tree.selection_remove(self.suppliers_tree.selection())

    def save_transaction(self) -> None:
        raw_item = self.transaction_vars["item"].get()
        if not raw_item:
            messagebox.showwarning("Perhatian", "Pilih barang terlebih dahulu")
            return
        item_id = self._parse_item_from_combo(raw_item)
        payload = {
            "transaction_date": datetime.now().strftime("%Y-%m-%d"),
            "item_id": item_id,
            "quantity": self._safe_int(self.transaction_vars["quantity"].get()),
            "transaction_type": self.transaction_vars["type"].get(),
            "notes": self.transaction_vars["notes"].get(),
        }
        success, message = self.item_controller.record_transaction(payload)
        if success:
            messagebox.showinfo("Informasi", message)
            self.transaction_vars["quantity"].set(1)
            self.transaction_vars["notes"].set("")
            self.load_items()
            self.load_transactions()
            self.load_dashboard()
        else:
            messagebox.showerror("Gagal", message)

    def _get_category_id(self, category_name: str) -> int | None:
        match = next((c for c in self.categories_cache if c["name"] == category_name), None)
        return match["id"] if match else None

    def _get_supplier_id(self, supplier_name: str) -> int | None:
        match = next((s for s in self.suppliers_cache if s["supplier_name"] == supplier_name), None)
        return match["id"] if match else None

    def _parse_item_from_combo(self, value: str) -> int:
        code = value.split(" - ")[0]
        for item in self.items_cache or self.item_controller.list_items():
            if item["item_code"] == code:
                return item["id"]
        raise ValueError("Barang tidak ditemukan")

    def _safe_int(self, value) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def _safe_float(self, value) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _logout(self) -> None:
        self.master.destroy()

    def _apply_role_permissions(self) -> None:
        """Nonaktifkan/ sembunyikan fitur tertentu untuk non-admin."""
        if self.user.get("level") != "admin":
            # Nonaktifkan operasi admin di tab Barang
            self.btn_item_save.state(["disabled"])  # tambah/ubah barang
            self.btn_item_delete.state(["disabled"])  # hapus barang
            # Nonaktifkan ekspor
            self.btn_export_pdf.state(["disabled"])
            self.btn_export_excel.state(["disabled"])
            # Sembunyikan tab pemasok (hanya admin)
            try:
                index = self.notebook.index(self.suppliers_tab)
                self.notebook.hide(index)
            except Exception:
                pass
            # Nonaktifkan operasi admin di tab Pemasok (kalau tab tidak disembunyikan)
            self.btn_supplier_save.state(["disabled"])
            self.btn_supplier_delete.state(["disabled"]) 

