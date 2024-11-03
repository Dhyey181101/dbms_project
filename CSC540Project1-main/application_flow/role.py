from database.user import *
from utils.db_connector import DatabaseConnectionManager

usercrud = UserCRUD(DatabaseConnectionManager.get_connection())

class RoleFlow():
    def __init__(self) -> None:
        self.role=""
        self.exit=False
        
    def set_role(self,role):
        self.role = role
    
    def print_role_menu(self):
        print("")
        print("1. Admin Login")
        print("2. Faculty Login")
        print("3. TA Login")
        print("4. Student Login")
        print("5. Exit")
    
    def get_role_input(self):
        """
        Return true if valid choice else false
        """
        role=input("Enter what you want to login as: ")
        role_map ={"1":"admin","2":"faculty","3":"teaching_assistant","4":"student"}
        try:
            if 0<int(role)<6:
                if int(role)==5:
                    self.exit=True
                else:
                    self.role=role_map[role]
                return True
            else:
                return False
        except Exception as E:
            print("Please enter valid choice")
            print(enumerate)
            return False

    def login(self):
        """
        Log in by verifying email and password for the selected role.
        """
        if not self.role:
            print("No role selected.")
            return None

        # Input email and password
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        #fetch password from database
        user = usercrud.fetch_user_using_email(email=email, role=self.role)
        if not user:
            print("User not found")
            self.role=""
            return None
        
        if not self._verify_password(password,user[4]):
            print("Incorrect Password")
            self.role=""
            return None
        user_id = user[0]
        
        return [user_id,email]
        
        

    def _verify_password(self, input_password, stored_password):
        """
        Verifies the password. Assumes the stored password is hashed.
        """
        return input_password == stored_password    
        
    

if __name__=="__main__":
    role = RoleFlow()
    role.print_role_menu()