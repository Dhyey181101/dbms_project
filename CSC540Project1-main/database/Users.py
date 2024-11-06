from utils.db_connector import DatabaseConnectionManager
from datetime import datetime

class UserCRUD:
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def create_user_id(self, first_name, last_name):
        # Get the current date
        current_date = datetime.now()
        
        # Extract the month and year
        month = current_date.month
        year = current_date.year
        
        # Ensure the first two letters of the first name, pad if necessary
        first_part = first_name[:2] + 'X' * (2 - len(first_name[:2]))
        
        # Ensure the first two letters of the last name, pad if necessary
        last_part = last_name[:2] + 'X' * (2 - len(last_name[:2]))
        
        # Ensure the month is two digits
        month_part = str(month).zfill(2)
        
        # Take the last two digits of the year
        year_part = str(year)[-2:]
        
        # Combine all parts to form the user ID
        return f"{first_part}{last_part}{month_part}{year_part}"

    def create_user(self, first_name, last_name, email, password, role):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                user_id = self.create_user_id(first_name, last_name)
                query = """
                INSERT INTO Users (user_id, first_name, last_name, email, password_hash, role)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (user_id, first_name, last_name, email, password, role))
                self.connection.commit()
                print("User created successfully.")
            except Exception as e:
                print(f"Error creating user: {e}")
            finally:
                cursor.close()

    def read_user(self, user_id):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM Users WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                user = cursor.fetchone()
                if user:
                    print(user)
                else:
                    print("User not found.")
            except Exception as e:
                print(f"Error reading user: {e}")
            finally:
                cursor.close()

    def update_user(self, user_id, first_name=None, last_name=None, email=None, password=None, role=None):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                if first_name:
                    updates.append("first_name = %s")
                    values.append(first_name)
                if last_name:
                    updates.append("last_name = %s")
                    values.append(last_name)
                if email:
                    updates.append("email = %s")
                    values.append(email)
                if password:
                    updates.append("password_hash = %s")
                    values.append(password)
                if role:
                    updates.append("role = %s")
                    values.append(role)
                
                if updates:
                    query = f"UPDATE Users SET {', '.join(updates)} WHERE user_id = %s"
                    values.append(user_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("User updated successfully.")
                else:
                    print("No updates provided.")
            except Exception as e:
                print(f"Error updating user: {e}")
            finally:
                cursor.close()

    def delete_user(self, user_id):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM Users WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                self.connection.commit()
                print("User deleted successfully.")
            except Exception as e:
                print(f"Error deleting user: {e}")
            finally:
                cursor.close()

    def fetch_user_using_email(self, email, role):
        if self.connection:
            cursor = self.connection.cursor(dictionary=True)  # Return results as a dictionary
            try:
                query = "SELECT * FROM Users WHERE email = %s AND role = %s"
                cursor.execute(query, (email, role))
                user = cursor.fetchone()
                return user if user else None
            except Exception as e:
                print(f"Error reading user: {e}")
            finally:
                cursor.close()

    def fetch_user_using_role(self, role):
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT * FROM Users WHERE role = %s"
                cursor.execute(query, (role,))
                users = cursor.fetchall()
                return users
            except Exception as e:
                print(f"Error fetching users with role {role}: {e}")
                return []
            finally:
                cursor.close()
        return []

    def update_password(self, email, password):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE Users SET password_hash = %s WHERE email = %s"
                cursor.execute(query, (password, email))
                self.connection.commit()
                print("Password updated.")
            except Exception as e:
                print(f"Error updating password: {e}")
            finally:
                cursor.close()

    def get_user_by_email(self, email):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM Users WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                return user if user else None
            except Exception as e:
                print(f"Error fetching user by email: {e}")
                return None
            finally:
                cursor.close()

    def fetch_user_by_email(self, email):
        """Fetch a user by email."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT * FROM Users WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                return user if user else None
            except Exception as e:
                print(f"Error fetching user by email: {e}")
                return None
            finally:
                cursor.close()
        return None

    def create_user_id(self, first_name, last_name):
        current_date = datetime.now()
        month = current_date.month
        year = current_date.year
        first_part = first_name[:2] + 'X' * (2 - len(first_name[:2]))
        last_part = last_name[:2] + 'X' * (2 - len(last_name[:2]))
        month_part = str(month).zfill(2)
        year_part = str(year)[-2:]
        return f"{first_part}{last_part}{month_part}{year_part}"

    def create_ta_user(self, first_name, last_name, email, password):
        """
        Special function to create a Teaching Assistant user.
        """
        if self.connection:
            try:
                cursor = self.connection.cursor()
                user_id = self.create_user_id(first_name, last_name)
                role = "Teaching_Assistant"  # Set role specifically for TAs
                query = """
                INSERT INTO Users (user_id, first_name, last_name, email, password_hash, role)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (user_id, first_name, last_name, email, password, role))
                self.connection.commit()
                print("TA user created successfully.")
                return True
            except Exception as e:
                print(f"Error creating TA user: {e}")
                return False
            finally:
                cursor.close()