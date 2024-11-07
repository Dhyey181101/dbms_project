from application_flow.flow import Flow
from database.Users import UserCRUD
from database.Courses import CourseCRUD
from database.Enrollments import EnrollmentCRUD
from database.Chapters import ChapterCRUD
from database.Textbooks import TextbookCRUD
from database.Sections import SectionCRUD
from database.ContentBlocks import ContentBlockCRUD
from database.Questions import QuestionsCRUD
from database.Activities import ActivitiesCRUD
from utils.db_connector import DatabaseConnectionManager


usercrud = UserCRUD(DatabaseConnectionManager.get_connection())
coursecrud = CourseCRUD(DatabaseConnectionManager.get_connection())
enrollmentcrud = EnrollmentCRUD(DatabaseConnectionManager.get_connection())
chaptercrud= ChapterCRUD(DatabaseConnectionManager.get_connection())
textbookcrud= TextbookCRUD(DatabaseConnectionManager.get_connection())
sectioncrud = SectionCRUD(DatabaseConnectionManager.get_connection())
contentblockcrud= ContentBlockCRUD(DatabaseConnectionManager.get_connection())
questions_crud=QuestionsCRUD(DatabaseConnectionManager.get_connection())
activities_crud = ActivitiesCRUD(DatabaseConnectionManager.get_connection())



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
            choice = int(input("Select your option:"))    
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
        courses = coursecrud.get_all_active_courses()
        
        # Print the header
        print("+-------------------+-----------------------------------------+-----------------+------------+------------+--------------------------+")
        print("| Course ID         | Course Name                             | Faculty ID      | Start Date | End Date   | Category                |")
        print("+-------------------+-----------------------------------------+-----------------+------------+------------+--------------------------+")
    
        # Print each course in a formatted way
        for course in courses:
            print(f"| {course['course_id']:<17} | {course['course_name']:<40} | {course['faculty_user_id']:<15} | {course['start_date']} | {course['end_date']} | {course['course_category']:<22} |")
    
        print("+-------------------+-----------------------------------------+-----------------+------------+------------+--------------------------+")
    
        course_id = input("Enter CourseID of course you want to view: ")
        
        while True:
            print("1. View Students")
            print("2. Add new chapters")
            print("3. Modify chapters")
            print("4. Go Back")
            choice = int(input("Enter the operation you want to do: "))
            if choice == 1:
                self.handle_view_students(course_id)
            elif choice == 2:
                self.handle_add_chapter(course_id)
            elif choice == 3:
                self.handle_modify_new_chapter(course_id)
            elif choice == 4:
                break

    
    def handle_add_chapter(self, course_id):
        textbook_id = coursecrud.get_textbook_id_for_course(course_id)
        print(f"Adding Chapter to {textbook_id}")
        if textbook_id is None:
            print("No textbook found for this course.")
            return

        print("Adding a new chapter...")
        chapter_id = input("Enter Unique Chapter ID: ")
        chapter_title = input("Enter Chapter Title: ")
        chaptercrud.add_chapter(textbook_id,chapter_id,chapter_title)
        print("Chapter created successfully.")
        while True:
            print("1. Add New Section")
            print("2. Go Back")
            choice = int(input("Enter the operation you want to do: "))

            if choice == 1:
                self.handle_add_section(textbook_id,chapter_id)
            elif choice == 2:
                print("Going back...")
                break  # Exit the loop and return to the previous menu
            else:
                print("Invalid option, please choose 1 or 2.")


    
    def handle_modify_new_chapter(self, course_id):
        textbook_id=coursecrud.get_textbook_id_for_course(course_id)
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
                print("3. Delete Content Block")
                print("4. Hide Content Block")
                print("5. Go Back")
                print("6. Landing Page")

                try:
                    choice = int(input("Choose an option: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == 1:
                    self.handle_add_content_block(section_number, chapter_id, textbook_id)
                elif choice == 2:
                    self.handle_modify_content_block(textbook_id, chapter_id, section_number)
                elif choice == 3:
                        content_block_id = input("Enter Content Block ID to delete: ")
                        contentblockcrud.delete_content_block(content_block_id)
                elif choice == 4:
                        content_block_id = input("Enter Content Block ID to hide: ")
                        contentblockcrud.hide_content_block(content_block_id)##textbook_id, chapter_id, section_number, 
                elif choice == 5:
                    print("Going back to the previous menu.")
                    break
                elif choice == 6:
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
            query = """
                    INSERT INTO activities (activity_id, content_block_id, section_id, chapter_id, textbook_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """            
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
                activities_crud.add_activity(activity_id, content_block_id, section_id, chapter_id, textbook_id)
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

        content_block_id = input("Enter Content Block ID to modify: ")


        if content_block_id:
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
    
    def handle_view_students(self, course_id):
        students = enrollmentcrud.get_students_in_course(course_id)

        if not students:
            print(f"No students found for this {course_id}.")
            return

        # Print the header
        print("+----------+------------+-----------+---------------------+")
        print("| user_id  | first_name | last_name | email               |")
        print("+----------+------------+-----------+---------------------+")

        # Print each student's information with proper alignment
        for student in students:
            print(f"| {student['user_id']:<10} | {student['first_name']:<10} | {student['last_name']:<9} | {student['email']:<19} |")

        # Print the footer
        print("+----------+------------+-----------+---------------------+")

    def handle_view_courses(self):
        """Display all courses in a formatted table with dynamic widths."""
        courses = coursecrud.get_all_courses()  

        if not courses:
            print("No courses found.")
            return

        # Calculate maximum width for each column
        headers = ['Course ID', 'Course Name', 'Faculty ID', 'Start Date', 'End Date', 'Category']
        max_widths = [len(header) for header in headers]

        for course in courses:
            max_widths[0] = max(max_widths[0], len(course['course_id']))
            max_widths[1] = max(max_widths[1], len(course['course_name']))
            max_widths[2] = max(max_widths[2], len(course['faculty_user_id']))
            max_widths[3] = max(max_widths[3], len(str(course['start_date'])))
            max_widths[4] = max(max_widths[4], len(str(course['end_date'])))
            max_widths[5] = max(max_widths[5], len(course['course_category']))

        # Print the header
        header_line = '+' + '+'.join('-' * (width + 2) for width in max_widths) + '+'
        print(header_line)
        header_format = '| ' + ' | '.join(f'{{:<{width}}}' for width in max_widths) + ' |'
        print(header_format.format(*headers))
        print(header_line)

        for course in courses:
            print(header_format.format(
                course['course_id'],
                course['course_name'],
                course['faculty_user_id'],
                str(course['start_date']),
                str(course['end_date']),
                course['course_category']
            ))

        print(header_line)




    def handle_change_password(self):
        # Step A: Prompt for the current password
        current_password = input("Enter current password: ")

        # Step B: Prompt for the new password
        new_password = input("Enter new password: ")

        # Step C: Prompt for the confirmation of the new password
        confirm_password = input("Confirm new password: ")

        while True:
            # Display the options as per the image
            print("\nChange Password Menu")
            print("1. Update")
            print("2. Go Back")
            
            # Get the user's choice
            choice = input("Choose an option (1-2): ")

            if choice == "1":
                # Fetch the user based on email and role
                user = usercrud.fetch_user_using_email(email=self.email, role='faculty')
                if not user:
                    print("User not found.")
                    return

                # Check if the current password matches
                if current_password != user['password_hash']:
                    print("Incorrect current password.")
                    return  # Exit if current password is incorrect

                # Check if the new password matches the confirmation
                if new_password != confirm_password:
                    print("New password and confirmation do not match.")
                    return  # Exit if confirmation doesn't match

                # Update password if everything is correct
                usercrud.update_password(self.email, new_password)
                print("Password updated successfully.")
                return  # Exit after successful update

            elif choice == "2":
                # Go back to the previous menu without updating
                print("Returning to TA Landing Page without updating password.")
                return  # Exit the function to go back

            else:
                print("Invalid choice. Please try again.")
    

    def handle_logout(self):
        self.logout = True