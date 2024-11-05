from application_flow.flow import Flow
from database.Users import *
from database.Courses import *
from database.Enrollments import *
from database.ContentBlocks import *
from database.Sections import *
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
        headings = ['SectionID', 'Title']
        header_row = " | ".join(headings)
        print("-" * (len(header_row) + 4))
        print("| " + header_row + " |")
        print("-" * (len(header_row) + 4))

        # Print each section in a formatted row
        for section in sections:
            row = f"| {section['section_id']} | {section['title']} |"
            print(row)

        print("-" * (len(header_row) + 4))
        section_id = input("Enter Section ID: ")
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
        block_id = input("Enter block you want to select: ")
        #get block
        #if block is image or picture just display it else
        #else print question, option and take answer input


    def handle_enroll(self):
        print("Please enter the following details to enroll in a course:")

        # Step 1: Gather student information
        first_name = input("Enter your First Name: ").strip()
        last_name = input("Enter your Last Name: ").strip()
        email = input("Enter your Email: ").strip()
        course_token = input("Enter the Course Token: ").strip()

        # Step 2: Display menu with Enroll and Go Back options
        print("\nMenu:")
        print("1. Enroll")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ").strip()

        if choice == "1":
            # Step 3: Check if the user exists or create a new account if needed
            user = usercrud.get_user_by_email(email=email)
            
            if not user:
                print("User not found. Creating a new account...")
                password = input("Set your password: ").strip()
                usercrud.create_user(first_name=first_name, last_name=last_name, email=email, password=password, role="student")
                user = usercrud.get_user_by_email(email=email)
                if not user:
                    print("Error creating user account. Please try again.")
                    return

            # Step 4: Find the course by token
            course = coursecrud.find_course_using_token(course_token)
            if not course:
                print("Course not found. Please check the course token.")
                return
            
            # Access course_id based on the structure of `course`
            if isinstance(course, dict):
                course_id = course.get("course_id")
            elif isinstance(course, tuple) or isinstance(course, list):
                course_id = course[0]
            else:
                print("Unexpected course format. Unable to retrieve course_id.")
                return

            if not course_id:
                print("Invalid course data. Cannot retrieve course ID.")
                return

            student_user_id = user[0]  # Assuming user[0] is the user ID

            # Step 5: Enroll the student in the course with 'Pending' status
            enrollment_successful = enrollcrud.enroll_student(course_id=course_id, student_user_id=student_user_id, enrollment_status="Pending")

            if enrollment_successful:
                print("Enrollment request submitted. You have been added to the waiting list.")
            else:
                print("Enrollment request failed. You might already be enrolled in this course.")
        
        elif choice == "2":
            # Go back to the previous menu
            print("Returning to the previous menu...")
            return
        else:
            print("Invalid option. Please select 1 or 2.")



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