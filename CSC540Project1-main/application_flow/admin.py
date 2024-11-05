from application_flow.flow import Flow
from database.Users import UserCRUD
from database.Textbooks import TextbookCRUD
from database.Chapters import ChapterCRUD
from database.Sections import SectionCRUD
from database.ContentBlocks import ContentBlockCRUD
from database.Courses import CourseCRUD
from database.CourseTAs import CourseTACRUD
from database.Enrollments import EnrollmentCRUD
from utils.db_connector import DatabaseConnectionManager

# Database CRUD operations
usercrud = UserCRUD(DatabaseConnectionManager.get_connection())
textbookcrud = TextbookCRUD(DatabaseConnectionManager.get_connection())
chaptercrud = ChapterCRUD(DatabaseConnectionManager.get_connection())
sectioncrud = SectionCRUD(DatabaseConnectionManager.get_connection())
contentblockcrud = ContentBlockCRUD(DatabaseConnectionManager.get_connection())
coursecrud = CourseCRUD(DatabaseConnectionManager.get_connection())
coursetacrud = CourseTACRUD(DatabaseConnectionManager.get_connection())
enrollmentcrud = EnrollmentCRUD(DatabaseConnectionManager.get_connection())

class AdminFlow(Flow):
    def __init__(self, user_id, email):
        self.operation = -1
        self.logout = False
        super().__init__(user_id, email)

    def print_menu(self):
        while True:
            print("Admin Menu:")
            print("1. Create a Faculty Account")
            print("2. Create E-textbook")
            print("3. Modify E-textbooks")
            print("4. Create New Active Course")
            print("5. Create New Evaluation Course")
            print("6. Logout")
            choice = int(input("Enter choice: "))
            
            if choice == 1:
                self.handle_create_faculty_account()
            elif choice == 2:
                self.handle_create_textbook()
            elif choice == 3:
                self.handle_modify_textbook()
            elif choice == 4:
                self.handle_new_course(active=True)
            elif choice == 5:
                self.handle_new_course(active=False)
            elif choice == 6:
                self.handle_logout()
                break
            else:
                print("Invalid choice. Please try again.")

    def handle_create_faculty_account(self):
        print("Creating a faculty account...")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        role = "faculty"
        usercrud.create_user(first_name, last_name, email, password, role)

    def handle_create_textbook(self):
        print("Creating an E-textbook...")
        title = input("Enter E-textbook title: ")
        admin_id = self.user_id
        is_hidden = input("Is the textbook hidden? (yes/no): ").strip().lower() == 'yes'
        textbookcrud.create_etextbook(title, admin_id, is_hidden)
        textbook_id = textbookcrud.get_textbook_id_by_title(title)
        
        if textbook_id:
            self.textbook_menu(textbook_id)
        else:
            print("Failed to retrieve textbook ID.")

    def textbook_menu(self, textbook_id):
        print("\nE-textbook Menu:")
        print("1. Add New Chapter")
        print("2. Modify Chapter")
        print("3. Go Back")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            self.handle_add_new_chapter(textbook_id)
        elif choice == 2:
            self.handle_modify_new_chapter(textbook_id)
        elif choice == 3:
            return
        else:
            print("Invalid choice.")

    def handle_modify_textbook(self):
        print("Modifying an E-textbook...")
        textbooks = textbookcrud.get_all_textbooks()
        
        if not textbooks:
            print("No textbooks available.")
            return

        title = input("Enter E-textbook title to modify: ")
        textbook_id = textbookcrud.get_textbook_id_by_title(title)
        
        if textbook_id:
            self.textbook_menu(textbook_id)
        else:
            print("Textbook not found.")

    def handle_add_new_chapter(self, textbook_id):
        print("Adding a new chapter...")
        chapter_title = input("Enter Chapter Title: ")
        chapter_name = input("Enter Chapter Name: ")
        chaptercrud.add_chapter(textbook_id, chapter_title, chapter_name)

    def handle_modify_new_chapter(self, textbook_id):
        print("Modifying a chapter...")
        chapters = chaptercrud.get_all_chapters(textbook_id)
        
        if not chapters:
            print("No chapters available.")
            return

        chapter_id = input("Enter Chapter ID to modify: ")
        selected_chapter = next((chapter for chapter in chapters if str(chapter['ChapterID']) == chapter_id), None)
        
        if selected_chapter:
            new_title = input("Enter new Chapter Title: ") or selected_chapter['Title']
            new_chapter_name = input("Enter new Chapter Name: ") or selected_chapter['Chaptername']
            chaptercrud.modify_chapter(chapter_id, new_title, new_chapter_name)
        else:
            print("Chapter ID not found.")

    def handle_add_section(self, chapter_id):
        print("Adding a new section...")
        section_number = input("Enter Section Number: ")
        section_title = input("Enter Section Title: ")
        sectioncrud.add_section(chapter_id, section_number, section_title)
        sections = sectioncrud.get_sections_by_chapter(chapter_id)
        
        if sections:
            self.section_menu(sections[-1]["SectionID"])
        else:
            print("Failed to retrieve section ID.")

    def handle_modify_section(self):
        print("Modifying a section...")
        textbook_id = input("Enter E-textbook ID: ")
        chapter_id = input("Enter Chapter ID: ")
        section_number = input("Enter Section Number to modify: ")
        sections = sectioncrud.get_sections_by_chapter(chapter_id)
        selected_section = next((section for section in sections if str(section['SectionNumber']) == section_number), None)

        if not selected_section:
            print("Section not found. Returning to menu.")
            return

        section_id = selected_section['SectionID']
        new_section_number = input("Enter new Section Number (leave blank if no change): ")
        new_section_title = input("Enter new Section Title (leave blank if no change): ")
        sectioncrud.modify_section(section_id, new_section_number or None, new_section_title or None)

    def handle_add_content_block(self, section_id):
        print("Adding a new content block...")
        block_type = input("Enter Content Block Type: ")
        content = input("Enter Content: ")
        contentblockcrud.add_content_block(section_id, block_type, content)
        print("Content block added successfully.")

    def handle_modify_content_block(self, section_id):
        print("Modifying a content block...")
        content_blocks = contentblockcrud.get_content_blocks_by_section(section_id)
        
        if not content_blocks:
            print("No content blocks found for this section.")
            return

        block_id = input("Enter Content Block ID to modify: ")
        selected_block = next((block for block in content_blocks if str(block['BlockID']) == block_id), None)
        
        if selected_block:
            new_block_type = input("Enter new Content Block Type (leave blank if no change): ") or selected_block['BlockType']
            new_content = input("Enter new Content (leave blank if no change): ") or selected_block['Content']
            contentblockcrud.modify_content_block(block_id, new_block_type, new_content)
            print("Content block modified successfully.")
        else:
            print("Content Block ID not found.")

    def handle_new_course(self, active=True):
        print("Creating a new course...")
        course_id = input("Enter Course ID: ")
        course_name = input("Enter Course Name: ")
        textbook_id = int(input("Enter Textbook ID: "))
        faculty_id = input("Enter Faculty User ID: ")
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        end_date = input("Enter End Date (YYYY-MM-DD): ")
        access_token = input("Enter Access Token: ")
        max_enrollment = int(input("Enter Max Enrollment: "))
        course_category = "Active" if active else "Evaluation"
        
        coursecrud.create_course(course_id, course_name, textbook_id, faculty_id, start_date, end_date, course_category, access_token, max_enrollment)

    def handle_logout(self):
        self.logout = True
