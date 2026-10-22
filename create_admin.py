from getpass import getpass
from app import create_database, get_db_connection
from werkzeug.security import generate_password_hash


def create_admin():
    create_database()

    print("\n===== HelpDesk Admin Setup =====")

    name = input("Enter admin name: ").strip()
    email = input("Enter admin email: ").strip().lower()
    password = getpass("Create admin password: ")

    if not name or not email or not password:
        print("All fields are required.")
        return

    if "@" not in email or len(email) > 254:
        print("Please enter a valid email address.")
        return

    if len(name) > 100:
        print("Name must be 100 characters or fewer.")
        return

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    hashed_password = generate_password_hash(password)

    with get_db_connection() as connection:
        existing_user = connection.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_user:
            connection.execute(
                """
                UPDATE users
                SET name = ?, password = ?, role = 'admin'
                WHERE email = ?
                """,
                (name, hashed_password, email)
            )
        else:
            connection.execute(
                """
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, 'admin')
                """,
                (name, email, hashed_password)
            )

    print("\nAdmin account created successfully!")


if __name__ == "__main__":
    create_admin()