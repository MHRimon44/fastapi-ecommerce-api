CUSTOMER = "Customer"
SELLER = "Seller"
ADMIN = "Admin"
SUPER_ADMIN = "SuperAdmin"

ADMIN_ROLES = [ADMIN, SUPER_ADMIN]


def normalize_role(role):
    if role is None:
        return None

    role_text = str(role).strip().lower()

    if role_text == "admin":
        return ADMIN

    if role_text in ["superadmin", "super_admin", "super admin"]:
        return SUPER_ADMIN

    if role_text == "seller":
        return SELLER

    if role_text == "customer":
        return CUSTOMER

    return str(role).strip()
