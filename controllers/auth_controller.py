"""Controller untuk proses login dan manajemen user."""

from __future__ import annotations

from typing import Optional

from utils.validators import validate_required_fields


class AuthController:
    def __init__(self, user_model: "UserModel") -> None:
        self.user_model = user_model

    def login(self, username: str, password: str) -> tuple[bool, Optional[dict], str]:
        """Validasi login dan kembalikan status, data user, serta pesan."""

        valid, message = validate_required_fields({"Username": username, "Password": password})
        if not valid:
            return False, None, message

        user = self.user_model.authenticate(username, password)
        if user:
            return True, user, "Login berhasil"
        return False, None, "Username atau password salah"

