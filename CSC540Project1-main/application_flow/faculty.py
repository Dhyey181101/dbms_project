from application_flow.flow import Flow
from database.Users import *
from database.Textbooks import *
from database.Chapters import *
from database.Sections import *
from database.ContentBlocks import *
from database.Courses import *
from database.Enrollments import *
from database.CourseTAs import *
from utils.db_connector import DatabaseConnectionManager
from utils.utils import print_list_as_table

usercrud = UserCRUD(DatabaseConnectionManager.get_connection())
textbookcrud = TextbookCRUD(DatabaseConnectionManager.get_connection())
chaptercrud = ChapterCRUD(DatabaseConnectionManager.get_connection())
sectioncrud = SectionCRUD(DatabaseConnectionManager.get_connection())
contentblockcrud = ContentBlockCRUD(DatabaseConnectionManager.get_connection())
coursecrud = CourseCRUD(DatabaseConnectionManager.get_connection())
enrollmentcrud = EnrollmentCRUD(DatabaseConnectionManager.get_connection())
coursetacrud = CourseTACRUD(DatabaseConnectionManager.get_connection())

class FacultyFlow(Flow):
    def __init__(self, user_id,email) -> None:
        self.logout = False
        super().__init__(email=email,user_id=user_id)

    def print_menu(self):
        while True:
            print("Faculty Menu:")
            print("1. Go to active course")
            print("2. Go to evaluation course")
            print("3. View Courses")
            print("4. Change Password")
            print("6. Logout")
            choice = int(input(""))
            if choice==1:
                self.handle_go_to_active_course()
            elif choice==2:
                self.handle_go_to_eval_course()
            elif choice==3:
                self.handle_view_courses()
            elif choice==4:
                self.handle_change_password()
            elif choice==5:
                self.handle_logout()
                break
            else:
                print("Bad Choice")

    def handle_go_to_active_course(self):
        #display the active courses
        courses = coursecrud.get_all_courses()
        for i,course in enumerate(courses):
            print(course)
        course_id = input("Enter CourseID of course you want to view: ")
            
        while True:
            print("1. View Worklist")
            print("2. Approve enrollment")
            print("3. View Students")
            print("4. Add new chapters")
            print("5. Modify chapters")
            print("6. Add TA")
            print("7. Add Question")
            print("8. Go Back")
            choice = int(input("Enter the operation you want to do: "))
            if choice==1:
                self.handle_view_worklist(course_id)
            elif choice==2:
                self.handle_approve_enrollment(course_id)
            elif choice==3:
                self.handle_view_students(course_id)
            elif choice==4:
                self.handle_add_chapter(course_id)
            elif choice==5:
                self.handle_modify_chapter(course_id)
            elif choice==6:
                self.handle_add_ta(course_id)
            elif choice==7:
                self.handle_add_question()
            elif choice==8:
                break
        
    
    def handle_add_question(self):
        #print acitvities
        activity_id = input("")
        #take question input
        
    
    def handle_view_students(self, course_id):
        enrollment = enrollmentcrud.get_course_enrollment(course_id, "approved")

    def handle_view_worklist(self,course_id):
        enrollment = enrollmentcrud.get_course_enrollment(course_id, status="pending")

    def handle_approve_enrollment(self, course_id):
        user_id = input("Enter user ID of student to approve enrollment")
        res = enrollmentcrud.enroll_student(course_id, user_id)


    def handle_add_chapter(self):
        print("Creating a new chapter...")
        #get all textbooks
        textbook_id = input("Enter ID of textbook: ")
        chapter_title = input("Enter ChapterTitle: ")
        is_hidden = input("Is the chapter hidden (yes/no): ")
        is_hidden = "yes" ==is_hidden
        chaptercrud.add_chapter(textbook_id,chapter_title,is_hidden)


    def handle_modify_chapter(self):
        #get all textbooks
        textbook_id = input("Enter ID of textbook: ")
        while True:
            print("1. Hide Chapter")
            print("2. Delete Chapter")
            print("3. Add New Section")
            print("4. Modify Section")
            print("5. Go Back")
            choice = int(input("Enter the operation you want to do: "))
            if choice==1:
                self.handle_view_worklist(textbook_id)
            elif choice==2:
                self.handle_approve_enrollment(textbook_id)
            elif choice==3:
                self.handle_view_students(textbook_id)
            elif choice==4:
                self.handle_add_chapter(textbook_id)
            elif choice==5:
                break
        
    def handle_hide_chapter(self):
        print("Hiding a chapter...")
        # Retrieve all chapters first to display them
        textbooks = textbookcrud.get_all_textbooks()  # Get all textbooks
        if not textbooks:
            print("No textbooks found.")
            return

        print("Available E-textbooks:")
        for textbook in textbooks:
            print(f"ID: {textbook['TextbookID']}, Title: {textbook['Title']}")

        textbook_title = input("Enter the E-textbook Title containing the chapter: ")
        textbook_id = next((textbook['TextbookID'] for textbook in textbooks if textbook['Title'].lower() == textbook_title.lower()), None)
        
        if not textbook_id:
            print("Textbook not found. Please try again.")
            return

        # Fetch chapters for the selected textbook
        chapters = chaptercrud.get_all_chapters(textbook_id)
        if not chapters:
            print("No chapters found for this textbook.")
            return

        print("Available Chapters:")
        for chapter in chapters:
            print(f"ID: {chapter['ChapterID']}, Title: {chapter['Title']}")

        chapter_id = input("Enter the Chapter ID to hide: ")
        chaptercrud.hide_chapter(chapter_id)

    def handle_delete_chapter(self):
        print("Hiding a chapter...")
        chapter_id = input("Enter the Chapter ID to hide: ")
        chaptercrud.hide_chapter(chapter_id)
    
    def handle_add_new_section(self, textbook_id, chapter_id):
        print("Hiding a chapter...")
        chapter_id = input("Enter the Chapter ID to hide: ")
        chaptercrud.hide_chapter(chapter_id)

    def handle_modify_section(self,textbook_id):
        chapter_id = input("")
        while True:
            print("1. Hide Section")
            print("2. Delete Section")
            print("3. Add New Content Block")
            print("4. Modify Content Block")
            print("5. Go Back")
            choice = int(input("Enter the operation you want to do: "))
            if choice==1:
                self.handle_view_worklist(textbook_id)
            elif choice==2:
                self.handle_approve_enrollment(textbook_id)
            elif choice==3:
                self.handle_view_students(textbook_id)
            elif choice==4:
                self.handle_add_chapter(textbook_id)
            elif choice==5:
                break
    
    
    def handle_delete_section(self, textbook_id,chapter_id):
        pass
    
    def handle_add_new_content_block(self, textbook_id,chapter_id):
        section_id = input("")
        while True:
            print("1. Add Text")
            print("2. Add Picture")
            print("3. Add activity")
            print("4. Go Back")
            choice = int(input("Enter the operation you want to do: "))
            if choice==1:
                self.handle_add_text(section_id)
            elif choice==2:
                self.handle_add_picture(section_id)
            elif choice==3:
                self.handle_add_activity(section_id)
            elif choice==4:
                break
    
    def handle_add_text(self, section_id):
        pass
    
    def handle_add_picture(self, section_id):
        pass

    def handle_add_activity(self, section_id):
        pass


    
    def handle_modify_content_block(self, textbook_id,chapter_id, section_id):
        block_id = input("")
        while True:
            print("1. Hide Content Block")
            print("2. Delete Content Block")
            print("3. Add Text")
            print("4. Add Picture")
            print("5. Hide Activity")
            print("6. Delete Activity")
            print("7. Add Activity")
            print("8. Go Back")
            
            choice = int(input("Enter the operation you want to do: "))
            
            if choice == 1:
                self.handle_hide_content_block(block_id)
            elif choice == 2:
                self.handle_delete_content_block(block_id)
            elif choice == 3:
                self.handle_update_text(block_id)
            elif choice == 4:
                self.handle_update_picture()
            elif choice == 5:
                self.handle_hide_activity(block_id)
            elif choice == 6:
                self.handle_delete_activity(block_id)
            elif choice == 7:
                self.handle_add_activity(block_id)
            elif choice == 8:
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 8.")

    def handle_delete_content_block(self, block_id):
        # Add logic to delete content block
        pass

    def handle_update_text(self,block_id):
        pass

    def handle_update_picture(self,block_id):
        pass
    
    def handle_hide_activity(self, block_id):
        # Add logic to hide activity
        pass

    def handle_delete_activity(self, block_id):
        # Add logic to delete activity
        pass

    def handle_add_activity(self, block_id):
        
        pass

    




    def handle_add_ta(self, course_id):
        tas = usercrud.fetch_user_using_role(role="teaching_assistant")
        if not len(tas):
            print("No TAs in database")
            return

        ta_id = input("Enter ID of TA to add: ")
        coursetacrud.assign_ta_to_course(course_id, ta_id)



    def handle_go_to_eval_course(self):
        pass

    
    def handle_view_course(self):
        courses = coursecrud.get_all_courses()
        if not len(courses):
            print("No Courses Found.")
            return
        headings = ['']
        print_list_as_table(headings=headings, rows=courses)

        
    def handle_change_password(self):
        user = usercrud.fetch_user_using_email(email=self.email, role='faculty')
        if not user:
            print("User not found")
            return
        
        password = input("Enter new password: ")
        usercrud.update_password(self.email, password)
        return []
        
    def handle_show_chapter(self):
        print("Showing a chapter...")
        # Same as handle_hide_chapter
        textbooks = textbookcrud.get_all_textbooks()
        if not textbooks:
            print("No textbooks found.")
            return

        print("Available E-textbooks:")
        for textbook in textbooks:
            print(f"ID: {textbook['TextbookID']}, Title: {textbook['Title']}")

        textbook_title = input("Enter the E-textbook Title containing the chapter: ")
        textbook_id = next((textbook['TextbookID'] for textbook in textbooks if textbook['Title'].lower() == textbook_title.lower()), None)

        if not textbook_id:
            print("Textbook not found. Please try again.")
            return

        chapters = chaptercrud.get_all_chapters(textbook_id)
        if not chapters:
            print("No chapters found for this textbook.")
            return

        print("Available Chapters:")
        for chapter in chapters:
            print(f"ID: {chapter['ChapterID']}, Title: {chapter['Title']}")

        chapter_id = input("Enter the Chapter ID to show: ")
        chaptercrud.show_chapter(chapter_id)


    def handle_hide_content_block(self):
        print("Hiding a content block...")
        # Fetch all chapters first to find the corresponding content block
        textbooks = textbookcrud.get_all_textbooks()
        if not textbooks:
            print("No textbooks found.")
            return

        print("Available E-textbooks:")
        for textbook in textbooks:
            print(f"ID: {textbook['TextbookID']}, Title: {textbook['Title']}")

        textbook_title = input("Enter the E-textbook Title containing the content block: ")
        textbook_id = next((textbook['TextbookID'] for textbook in textbooks if textbook['Title'].lower() == textbook_title.lower()), None)

        if not textbook_id:
            print("Textbook not found. Please try again.")
            return

        # Fetch chapters for the selected textbook
        chapters = chaptercrud.get_all_chapters(textbook_id)
        if not chapters:
            print("No chapters found for this textbook.")
            return

        print("Available Chapters:")
        for chapter in chapters:
            print(f"ID: {chapter['ChapterID']}, Title: {chapter['Title']}")

        chapter_id = input("Enter the Chapter ID containing the content block: ")
        # Fetch sections for the selected chapter
        sections = sectioncrud.get_sections_by_chapter(chapter_id)
        if not sections:
            print("No sections found for this chapter.")
            return

        print("Available Sections:")
        for section in sections:
            print(f"ID: {section['SectionID']}, Title: {section['Title']}")

        section_id = input("Enter the Section ID containing the content block: ")
        content_blocks = contentblockcrud.get_content_blocks_by_section(section_id)
        if not content_blocks:
            print("No content blocks found for this section.")
            return

        print("Available Content Blocks:")
        for block in content_blocks:
            print(f"ID: {block['BlockID']}, Type: {block['BlockType']}")

        content_block_id = input("Enter the Content Block ID to hide: ")
        contentblockcrud.hide_content_block(content_block_id)


    def handle_show_content_block(self):
        print("Showing a content block...")
        # Similar to handle_hide_content_block
        textbooks = textbookcrud.get_all_textbooks()
        if not textbooks:
            print("No textbooks found.")
            return

        print("Available E-textbooks:")
        for textbook in textbooks:
            print(f"ID: {textbook['TextbookID']}, Title: {textbook['Title']}")

        textbook_title = input("Enter the E-textbook Title containing the content block: ")
        textbook_id = next((textbook['TextbookID'] for textbook in textbooks if textbook['Title'].lower() == textbook_title.lower()), None)

        if not textbook_id:
            print("Textbook not found. Please try again.")
            return

        chapters = chaptercrud.get_all_chapters(textbook_id)
        if not chapters:
            print("No chapters found for this textbook.")
            return

        print("Available Chapters:")
        for chapter in chapters:
            print(f"ID: {chapter['ChapterID']}, Title: {chapter['Title']}")

        chapter_id = input("Enter the Chapter ID containing the content block: ")
        sections = sectioncrud.get_sections_by_chapter(chapter_id)
        if not sections:
            print("No sections found for this chapter.")
            return

        print("Available Sections:")
        for section in sections:
            print(f"ID: {section['SectionID']}, Title: {section['Title']}")

        section_id = input("Enter the Section ID containing the content block: ")
        content_blocks = contentblockcrud.get_content_blocks_by_section(section_id)
        if not content_blocks:
            print("No content blocks found for this section.")
            return

        print("Available Content Blocks:")
        for block in content_blocks:
            print(f"ID: {block['BlockID']}, Type: {block['BlockType']}")

        content_block_id = input("Enter the Content Block ID to show: ")
        contentblockcrud.show_content_block(content_block_id)



    def handle_create_faculty_account(self):
        print("Creating a faculty account...")

    def handle_create_textbook(self):
        print("Creating a textbook...")

    def handle_modify_textbook(self):
        print("Modifying a textbook...")

    def handle_new_course(self):
        print("Creating a new course...")

    def handle_create_evaluation_course(self):
        print("Creating a new evaluation course...")
    
    def handle_logout(self):
        self.logout = True