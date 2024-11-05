from application_flow.flow import Flow
from database.Users import UserCRUD
from database.Textbooks import TextbookCRUD
from database.Chapters import ChapterCRUD
from database.Sections import SectionCRUD
from database.ContentBlocks import ContentBlockCRUD
from database.Courses import CourseCRUD
from database.CourseTAs import CourseTACRUD
from database.Enrollments import EnrollmentCRUD
from database.Questions import QuestionsCRUD 
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
questions_crud = QuestionsCRUD(DatabaseConnectionManager.get_connection()) 

class AdminFlow(Flow):
    def __init__(self, user_id, email):
        super().__init__(user_id, email)  
        self.operation = -1
        self.logout = False
        self.user_id = user_id  

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
        while True:
            # Display menu options first
            print("\nCreate a Faculty Account Menu:")
            print("1. Add a Faculty User")
            print("2. Go Back")
            
            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            
            if choice == 1:
                # Ask for faculty details and save to the database
                print("Enter Faculty Account Details:")
                first_name = input("Enter First Name: ")
                last_name = input("Enter Last Name: ")
                email = input("Enter Email: ")
                password = input("Enter Password: ")
                role = "faculty"
                
                usercrud.create_user(first_name, last_name, email, password, role)
                print("Faculty account created successfully.")
                break  # Go back to the previous menu after adding the user
            elif choice == 2:
                # Go back to the previous menu
                print("Going back to the previous menu.")
                break
            else:
                print("Invalid choice. Please select 1 or 2.")

    def handle_create_textbook(self):
        print("Creating an E-textbook...")
        # Prompt for textbook ID and title
        title = input("Enter E-textbook title: ")
        textbook_id = input("Enter E-textbook ID: ")
        admin_id = self.user_id
        is_hidden = input("Is the textbook hidden? (yes/no): ").strip().lower() == 'yes'
                
        # Pass the textbook_id as an argument in the create_etextbook method
        textbookcrud.create_etextbook(textbook_id, title, admin_id, is_hidden)        
        while True:
            # Display menu options first
            print("\nCreate E-Textbook Menu:")
            print("1. Add New Chapter")
            print("2. Go Back")

            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if choice == 1:
                # # Check if the textbook was created successfully
                # created_textbook_id = textbookcrud.get_textbook_id_by_title(title)
                # if created_textbook_id:
                self.textbook_menu(textbook_id)
                # else:
                #     print("Failed to retrieve textbook ID.")
            elif choice == 2:
                # Go back to the previous menu
                print("Going back to the previous menu.")
                break
            else:
                print("Invalid choice. Please select 1 or 2.")                

    def textbook_menu(self, textbook_id):
        print("Creating New Chapter")
        # Correctly pass `textbook_id` to `handle_add_new_chapter`
        chapter_id = self.handle_add_new_chapter(textbook_id)
        
        if not chapter_id:
            print("Failed to create a chapter. Returning to Admin Home page.")
            return

        while True:        
            print("\nChapter Menu:")
            print("1. Add New Section")
            print("2. Go Back")
            print("3. Admin Home page")
            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == 1:
                # Correctly pass `textbook_id` and `chapter_id` to `handle_add_section`
                self.handle_add_section(textbook_id, chapter_id)
            elif choice == 2:
                # Go back to the previous menu
                print("Going back to the previous menu.")
                break
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

        # title = input("Enter E-textbook title to modify: ")
        textbook_id = input("Enter Unique E-textbook ID to modify: ")
        while True:        
            print("\nChapter Menu:")
            print("1. Add New Chapter")
            print("2. Modify Chapter")
            print("3. Go Back")
            print("4. Admin Home page")
            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue                    
            if choice == 1:
                self.textbook_menu(textbook_id)
            elif choice == 2:
                self.handle_modify_new_chapter(textbook_id)
            elif choice == 3:
                # Go back to the previous menu
                print("Going back to the previous menu.")
                break                
            elif choice == 4:
                return
            else:
                print("Invalid choice.")

    def handle_add_new_chapter(self, textbook_id):
        print("Adding a new chapter...")
        chapter_id = input("Enter Chapter ID: ")        
        chapter_title = input("Enter Chapter Title: ")
        # Pass parameters in correct order to `add_chapter`
        chaptercrud.add_chapter(textbook_id, chapter_id, chapter_title)
        print("Chapter created successfully.")
        return chapter_id

    def handle_modify_new_chapter(self, textbook_id):
        print("Modifying a chapter...")
        chapters = chaptercrud.get_all_chapters(textbook_id)

        if not chapters:
            print("No chapters available.")
            return

        chapter_id = input("Enter Chapter ID to modify: ")
        selected_chapter = next((chapter for chapter in chapters if str(chapter['chapter_id']) == chapter_id), None)

        if selected_chapter:
            while True:
                print("\nModify Chapter Menu:")
                print("1. Add New Section")
                print("2. Modify Section")
                print("3. Go Back")
                print("4. Landing Page")
                
                try:
                    choice = int(input("Choose an option: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == 1:
                    self.handle_add_section(textbook_id, chapter_id)
                elif choice == 2:
                    self.handle_modify_section(textbook_id, chapter_id)
                elif choice == 3:
                    # Go back to the previous menu
                    print("Going back to the previous menu.")
                    break
                elif choice == 4:
                    # Return to main landing page
                    return
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Chapter ID not found.")

    def handle_add_section(self, textbook_id, chapter_id):
        print("Adding a new section...")
        section_number = input("Enter Section Number: ")
        section_title = input("Enter Section Title: ")
        sectioncrud.add_section(textbook_id, chapter_id, section_number, section_title)
        print("Section created successfully.")

        while True:
            print("\nSection Menu:")
            print("1. Add New Content Block")
            print("2. Go Back")
            print("3. Landing Page")
            
            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == 1:
                # Redirect to Add New Content Block function
                self.handle_add_content_block(section_number, chapter_id, textbook_id)
            elif choice == 2:
                # Go back to the previous menu
                print("Going back to the previous menu.")
                break
            elif choice == 3:
                # Go back to the main landing page
                print("Returning to User Landing Page.")
                return
            else:
                print("Invalid choice. Please try again.")

    def handle_modify_section(self, textbook_id, chapter_id):
        print("Modifying a section...")
        section_number = input("Enter Section Number to modify: ")
        sections = sectioncrud.get_sections_by_chapter_and_textbook(chapter_id, textbook_id)  # Updated function
        selected_section = next((section for section in sections if str(section['section_id']) == section_number), None)

        if selected_section:
            while True:
                print("\nModify Section Menu:")
                print("1. Add New Content Block")
                print("2. Modify Content Block")
                print("3. Go Back")
                print("4. Landing Page")

                try:
                    choice = int(input("Choose an option: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == 1:
                    self.handle_add_content_block(textbook_id, chapter_id, section_number)
                elif choice == 2:
                    self.handle_modify_content_block(textbook_id, chapter_id, section_number)
                elif choice == 3:
                    print("Going back to the previous menu.")
                    break
                elif choice == 4:
                    return
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Section Number not found.")

    def handle_add_content_block(self, section_id, chapter_id, textbook_id):
        while True:
            print("Adding a new content block...")
            content_block_id = input("Enter Content Block ID: ")

            print("\nContent Block Menu:")
            print("1. Add Text")
            print("2. Add Picture")
            print("3. Add Activity")
            print("4. Go Back")
            print("5. Landing Page")

            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == 1:
                self.handle_add_text(content_block_id, section_id, chapter_id, textbook_id)
                return
            elif choice == 2:
                self.handle_add_picture(content_block_id, section_id, chapter_id, textbook_id)
                return
            elif choice == 3:
                self.handle_add_activity(content_block_id, section_id, chapter_id, textbook_id)
                return
            elif choice == 4:
                print("Going back to the previous menu.")
                break
            elif choice == 5:
                print("Returning to User Landing Page.")
                return
            else:
                print("Invalid choice. Please try again.")

    ### Function to Add Text
    def handle_add_text(self, content_block_id, section_id, chapter_id, textbook_id):
        while True:
            print("Adding Text Content Block...")
            text_content = input("Enter Text: ")

            print("\nText Menu:")
            print("1. Add")
            print("2. Go Back")
            print("3. Landing Page")

            choice = int(input("Choose an option: "))
            
            if choice == 1:
                # Insert text content block into the database
                contentblockcrud.add_content_block(textbook_id, chapter_id, section_id, content_block_id, "text", text_content)
                print("Text content block added successfully.")
                return
            elif choice == 2:
                print("Going back to the previous menu.")
                break
            elif choice == 3:
                print("Returning to User Landing Page.")
                return
            else:
                print("Invalid choice. Please try again.")

    def handle_add_picture(self, content_block_id, section_id, chapter_id, textbook_id):
        while True:
            print("Adding Picture Content Block...")
            picture_content = input("Enter Picture URL or Path: ")

            print("\nPicture Menu:")
            print("1. Add")
            print("2. Go Back")
            print("3. Landing Page")

            choice = int(input("Choose an option: "))
            
            if choice == 1:
                # Insert picture content block into the database
                contentblockcrud.add_content_block(textbook_id, chapter_id, section_id, content_block_id, "picture", picture_content)
                print("Picture content block added successfully.")
                return
            elif choice == 2:
                print("Going back to the previous menu.")
                break
            elif choice == 3:
                print("Returning to User Landing Page.")
                return
            else:
                print("Invalid choice. Please try again.")

    def handle_add_activity(self, content_block_id, section_id, chapter_id, textbook_id):
        while True:
            print("Adding Activity Content Block...")
            activity_id = input("Enter Unique Activity ID: ")

            print("\nActivity Menu:")
            print("1. Add Question")
            print("2. Go Back")
            print("3. Landing Page")

            choice = int(input("Choose an option: "))
            
            if choice == 1:
                # Insert activity content block and then redirect to question addition
                contentblockcrud.add_content_block(textbook_id, chapter_id, section_id, content_block_id, "activity", activity_id)
                print("Activity content block added successfully.")
                self.handle_add_question(activity_id, content_block_id, section_id, chapter_id, textbook_id)
                return
            elif choice == 2:
                print("Going back to the previous menu.")
                break
            elif choice == 3:
                print("Returning to User Landing Page.")
                return
            else:
                print("Invalid choice. Please try again.")

    def handle_add_question(self, activity_id, content_block_id, section_id, chapter_id, textbook_id):
        print("Adding a new question...")

        # Collect question details
        question_id = input("Enter Question ID: ")
        question_text = input("Enter Question Text: ")

        # Collect options and explanations
        options = []
        for i in range(1, 5):
            option_text = input(f"Enter Option {i} Text: ")
            option_explanation = input(f"Enter Option {i} Explanation: ")
            option_label = input(f"Enter Option {i} Label (Correct or Incorrect): ")
            options.append((option_text, option_explanation, option_label == "Correct"))

        answer = next((i + 1 for i, opt in enumerate(options) if opt[2]), None)  # Find the correct option index

        while True:
            print("\nQuestion Menu:")
            print("1. Save")
            print("2. Cancel")
            print("3. Landing Page")

            choice = int(input("Choose an option: "))

            if choice == 1:
                # Save question to database
                questions_crud.add_question(
                    question_id, textbook_id, chapter_id, section_id, content_block_id, activity_id,
                    question_text, options, answer
                )
                print("Question saved successfully.")
                return
            elif choice == 2:
                print("Canceling and going back to Add Activity page.")
                break
            elif choice == 3:
                print("Returning to User Landing Page.")
                return
            else:
                print("Invalid choice. Please try again.")


    def handle_modify_content_block(self, textbook_id, chapter_id, section_number):
        print("Modifying a content block...")
        content_blocks = contentblockcrud.get_content_blocks_by_section(textbook_id, chapter_id, section_number)

        if not content_blocks:
            print("No content blocks found for this section.")
            return

        content_block_id = input("Enter Content Block ID to modify: ")
        selected_block = next((block for block in content_blocks if str(block['content_block_id']) == content_block_id), None)

        if selected_block:
            while True:
                print("\nModify Content Block Menu:")
                print("1. Add Text")
                print("2. Add Picture")
                print("3. Add New Activity")
                print("4. Go Back")
                print("5. Landing Page")

                try:
                    choice = int(input("Choose an option: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == 1:
                    # Use the existing function to handle adding text content
                    self.handle_add_text(content_block_id, section_number, chapter_id, textbook_id)
                    return
                elif choice == 2:
                    # Use the existing function to handle adding picture content
                    self.handle_add_picture(content_block_id, section_number, chapter_id, textbook_id)
                    return
                elif choice == 3:
                    # Use the existing function to handle adding activity content
                    self.handle_add_activity(content_block_id, section_number, chapter_id, textbook_id)
                    return
                elif choice == 4:
                    print("Going back to the previous menu.")
                    break
                elif choice == 5:
                    print("Returning to User Landing Page.")
                    return
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Content Block ID not found.")


    def handle_new_course(self, active=True):
        print("Creating a new {} course...".format("Active" if active else "Evaluation"))
        
        # Prompt for common course details
        course_id = input("Enter Course ID: ")
        course_name = input("Enter Course Name: ")
        textbook_id = int(input("Enter E-textbook ID: "))
        faculty_id = input("Enter Faculty Member ID: ")
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        end_date = input("Enter End Date (YYYY-MM-DD): ")
        
        # Prompt for additional fields based on course type
        if active:
            access_token = input("Enter Unique Token: ")
            max_enrollment = int(input("Enter Course Capacity: "))
            course_category = "Active"
        else:
            access_token = None  # Evaluation courses don't require a token
            max_enrollment = None  # Evaluation courses don't have a capacity limit
            course_category = "Evaluation"

        # Menu for saving or discarding the entry
        while True:
            print("\nCourse Creation Menu:")
            print("1. Save")
            print("2. Cancel")
            print("3. Landing Page")
            
            choice = int(input("Choose an option: "))
            
            if choice == 1:
                # Call the CRUD method to save course details to the database
                coursecrud.create_course(course_id, course_name, textbook_id, faculty_id, start_date, end_date, course_category, access_token, max_enrollment)
                print("Course created successfully.")
                return  # Return to the previous menu after saving
            elif choice == 2:
                print("Cancelling course creation and going back.")
                break
            elif choice == 3:
                print("Returning to User Landing Page.")
                return
            else:
                print("Invalid choice. Please try again.")


    def handle_logout(self):
        self.logout = True
