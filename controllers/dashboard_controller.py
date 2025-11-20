"""Controller untuk data dashboard."""

from __future__ import annotations

from typing import Dict

class DashboardController:
    def __init__(self, item_model: "ItemModel", transaction_model: "TransactionModel") -> None:
        self.item_model = item_model
        self.transaction_model = transaction_model

    def get_dashboard_data(self) -> Dict[str, object]:
        summary = self.item_model.get_stock_summary()
        recent = self.transaction_model.get_recent()
        return {
            "summary": summary,
            "recent_transactions": recent,
        }

