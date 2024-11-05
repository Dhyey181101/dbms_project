from application_flow.flow import Flow
from database.Users import UserCRUD
from database.Courses import CourseCRUD
from database.Enrollments import EnrollmentCRUD
from utils.db_connector import DatabaseConnectionManager


usercrud = UserCRUD(DatabaseConnectionManager.get_connection())
coursecrud = CourseCRUD(DatabaseConnectionManager.get_connection())
enrollmentcrud = EnrollmentCRUD(DatabaseConnectionManager.get_connection())


class TAFlow(Flow):
    def __init__(self,user_id,email) -> None:
        self.logout = False
        super().__init__(email=email,user_id=user_id)

    def print_menu(self):
        while True:
            print("TA Menu:")
            print("1. Go to Active Courses")
            print("2. View Courses")
            print("3. Change Password")
            print("4. Logout")
            choice = int(input(""))    
            if choice==1:
                self.handle_go_to_active_course()
            elif choice==2:
                self.handle_view_courses()
            elif choice==3:
                self.handle_change_password()
            elif choice==4:
                self.handle_logout()
                break
            else:
                print("Bad Choice")
            
    def handle_go_to_active_course(self):
        courses = coursecrud.get_all_courses()
        for i,course in enumerate(courses):
            print(course)
        course_id = input("Enter CourseID of course you want to view: ")
            
        while True:
            print("1. View Students")
            print("2. Add new chapters")
            print("3. Modify chapters")
            print("4. Go Back")
            choice = int(input("Enter the operation you want to do: "))
            if choice==1:
                self.handle_view_students(course_id)
            elif choice==2:
                self.handle_add_chapter(course_id)
            elif choice==3:
                self.handle_modify_chapter(course_id)
            elif choice==4:
                break
        
    def handle_view_students(self, course_id):
        enrollment = enrollmentcrud.get_course_enrollment(course_id, "approved")
    
    def handle_add_chapter(self, course_id):
        pass
    
    def handle_modify_chapter(self, course_id):
        chapter_id = input("")
        while True:
            print("1. Add New Section")
            print("2. Modify Section")
            print("3. Go Back")
            
            choice = int(input("Enter the operation you want to do: "))
            
            if choice == 1:
                self.handle_add_new_section(chapter_id)
            elif choice == 2:
                self.handle_modify_section(chapter_id)
            elif choice == 3:
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 3.")

    # Function stubs
    def handle_add_new_section(self,chapter_id):
        # Add logic to add a new section
        #create section
        #get id of section
        while True:
            print("1. Add New Content Block")
            print("2. Go Back")
            
            choice = int(input("Enter the operation you want to do: "))
            
            if choice == 1:
                self.handle_add_new_content_block(section_id)
            elif choice == 2:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    # Function stub
    def handle_add_new_content_block(self, section_id):
        # Add logic to add a new content block
        #print blocks
        block_id = input("")
        while True:
            print("1. Add Text")
            print("2. Add Picture")
            print("3. Add Activity")
            print("4. Hide Activity")
            print("5. Go Back")
            
            choice = int(input("Enter the operation you want to do: "))
            
            if choice == 1:
                self.handle_add_text()
            elif choice == 2:
                self.handle_add_picture()
            elif choice == 3:
                self.handle_add_activity()
            elif choice == 4:
                self.handle_hide_activity()
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")

    # Function stubs
    def handle_add_text(self, block_id):
        # Add logic to add text
        pass

    def handle_add_picture(self, block_id):
        # Add logic to add a picture
        pass

    def handle_add_activity(self,block_id):
        # create new activity
        while True:
            print("1. Add New Question")
            print("2. Go Back")

            choice = int(input("Enter the operation you want to do: "))

            if choice == 1:
                self.handle_add_new_question()
            elif choice == 2:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def handle_new_question(self,activity_id):
        pass


    def handle_hide_activity(self):
        # Add logic to hide an activity
        pass

    def handle_modify_section(self, chapter_id):
        # Add logic to modify an existing section
        section_id = input("")
        while True:
            print("1. Add New Content Block")
            print("2. Modify Content Block")
            print("3. Delete Content Block")
            print("4. Hide Content Block")
            print("5. Go Back")
            
            choice = int(input("Enter the operation you want to do: "))
            
            if choice == 1:
                self.handle_add_new_content_block(section_id)
            elif choice == 2:
                self.handle_modify_content_block(section_id)
            elif choice == 3:
                self.handle_delete_content_block(section_id)
            elif choice == 4:
                self.handle_hide_content_block(section_id)
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")


    def handle_modify_content_block(self,section_id):
        # Add logic to modify an existing content block
        print("Blocks")
        block_id = input("")
        while True:
            print("1. Add Text")
            print("2. Add Picture")
            print("3. Add Activity")
            print("4. Go Back")
            
            choice = int(input("Enter the operation you want to do: "))
            
            if choice == 1:
                self.handle_add_text(block_id)
            elif choice == 2:
                self.handle_add_picture(block_id)
            elif choice == 3:
                self.handle_add_activity(block_id)
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")


    def handle_delete_content_block(self, section_id):
        # Add logic to delete a content block
        pass

    def handle_hide_content_block(self, section_id):
        # Add logic to hide a content block
        pass


        

    def handle_view_courses(self):
        pass

    def handle_change_password(self):
        user = usercrud.fetch_user_using_email(email=self.email, role='teaching_assistant')
        if not user:
            print("User not found")
            return
        
        password = input("Enter new password: ")
        usercrud.update_password(self.email, password)
        return []
    

    def handle_logout(self):
        self.logout = True