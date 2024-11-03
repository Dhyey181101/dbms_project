from application_flow.flow import Flow
from database.user import *
from database.course import *
from database.enrollment import *
from database.contentblock import *
from database.section import *
from utils.db_connector import *
from utils.utils import print_list_as_table

usercrud = UserCRUD(DatabaseConnectionManager.get_connection())
coursecrud = CourseCRUD(DatabaseConnectionManager.get_connection())
enrollcrud = EnrollmentCRUD(DatabaseConnectionManager.get_connection())
contentblockcrud = ContentBlockCRUD(DatabaseConnectionManager.get_connection())
sectioncrud = SectionCRUD(DatabaseConnectionManager.get_connection())

class StudentFlow(Flow):
    def __init__(self,user_id,email) -> None:
        self.logout = False
        super().__init__(email=email,user_id=user_id)


    def print_menu(self):
            while True:
                print(self.email,self.user_id)
                if not self.email or not self.user_id:
        
                    print("Student Menu:")
                    print("1. Enroll in a Course")
                    print("2. Sign In")
                    print("3. Go Back")
                    choice = int(input(""))
                    if choice==1:
                        self.handle_enroll()
                    elif choice==2:
                        self.handle_sign_in()
                    elif choice==3:
                        self.handle_logout()
                        break
                else:
                    print("Student Menu:")
                    print("1. View Section")
                    print("2. View Participation activity point")
                    print("3. Logout")
                    choice = int(input(""))
                    if choice==1:
                        self.handle_view_section()
                    elif choice==2:
                        self.handle_sign_in()
                    elif choice==3:
                        self.handle_logout()
                        break
                
                    
    def handle_view_section(self):
        sections = sectioncrud.get_all_sections_associated_with_user(self.user_id)
        print_list_as_table(headings=['SectionID',"Title"],rows=sections)
        section_id = int(input("Enter Section ID: "))
        while True:
            print("\nBlock Menu:")
            print("1. View Block")
            print("2. Go Back")
            choice = int(input("Enter your choice (1-2): "))
        
            if choice == 1:
                self.handle_view_block(section_id)
            elif choice==2:
                break
            else:
                continue
                
    
    def handle_view_block(self,section_id):
        #display blocks
        content_blocks = contentblockcrud.get_content_blocks_by_section(section_id=section_id)
        headings = ['BlockID', 'ContentType', 'Content', 'SequenceNumber', 'IsHidden']
        print_list_as_table(headings=headings,rows=content_blocks)
        block_id = int(input("Enter block you want to select: "))
        #get block
        #if block is image or picture just display it else
        #else print question, option and take answer input


    def handle_enroll(self):
        email = input("Enter your email: ")
        user= usercrud.get_user_by_email(email=email)
        if not user:
            print("User not found creating new account.")
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            password = input("Enter your password: ")
            usercrud.create_user(first_name=first_name,last_name=last_name,
                                 email=email,password=password,role='student')
            user = usercrud.get_user_by_email(email=email)
        course_token = input("")
        course = coursecrud.find_course_using_token(token=course_token)
        if not course:
            print("Course Not Found")
            return
        course_id = course[0]
        user_id = user[0]
        enrollcrud.enroll_student(course_id=course_id, user_id=user_id)


    def handle_sign_in(self):
        # Input email and password
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        #fetch password from database
        user = usercrud.fetch_user_using_email(email=email, role='student')
        if not user:
            print("User not found")
            self.role=""
            return None
        
        if password!=user[4]:
            print("Incorrect Password")
            self.role=""
            return None
        self.user_id = user[0]
        self.email = user[3]


    

        

    
    def handle_logout(self):
        self.logout = True