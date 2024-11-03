from utils.db_connector import DatabaseConnectionManager
from datetime import datetime

class UserCRUD:

    def __init__(self,connection) -> None:
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
                user_id = self.create_user_id(first_name,last_name,)
                query = """
                INSERT INTO User (UserID,FirstName, LastName, Email, Password, Role)
                VALUES (%s,%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (user_id,first_name, last_name, email, password, role))
                self.connection.commit()
                print("User created successfully.")
            except Exception as e:
                print(f"Error creating user: {e}")
            finally:
                cursor.close()

    def read_user(self,user_id):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM User WHERE UserID = %s"
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

    def update_user(self,user_id, first_name=None, last_name=None, email=None, password=None, role=None):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                if first_name:
                    updates.append("FirstName = %s")
                    values.append(first_name)
                if last_name:
                    updates.append("LastName = %s")
                    values.append(last_name)
                if email:
                    updates.append("Email = %s")
                    values.append(email)
                if password:
                    updates.append("Password = %s")
                    values.append(password)
                if role:
                    updates.append("Role = %s")
                    values.append(role)
                
                if updates:
                    query = f"UPDATE User SET {', '.join(updates)} WHERE UserID = %s"
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

    def delete_user(self,user_id):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM User WHERE UserID = %s"
                cursor.execute(query, (user_id,))
                self.connection.commit()
                print("User deleted successfully.")
            except Exception as e:
                print(f"Error deleting user: {e}")
            finally:
                cursor.close()
    
    def fetch_user_using_email(self,email,role):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM User WHERE Email = %s AND Role=%s"
                cursor.execute(query, (email,role,))
                user = cursor.fetchone()
                if user:
                    return user
                else:
                    return None
            except Exception as e:
                print(f"Error reading user: {e}")
            finally:
                cursor.close()

    
    def fetch_user_using_role(self, role):
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT * FROM User WHERE Role=%s"
                cursor.execute(query, (role,))
                users = cursor.fetchall()
                return users
            except Exception as e:
                print(f"Error fetching Users with role {role}: {e}")
                return []
            finally:
                cursor.close()
        return []

    def update_password(self,email,password):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = f"UPDATE User SET Password=%s WHERE email = %s"
                cursor.execute(query, tuple(password,email))
                self.connection.commit()
                print("password updated.")
            except Exception as e:
                print(f"Error updating user: {e}")
            finally:
                cursor.close()

    def get_user_by_email(self, email):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM User WHERE Email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                return user if user else None
            except Exception as e:
                print(f"Error fetching user by email: {e}")
                return None
            finally:
                cursor.close()
    