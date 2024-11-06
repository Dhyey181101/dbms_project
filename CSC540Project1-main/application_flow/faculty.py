from application_flow.flow import Flow
from database.Users import *
from database.Textbooks import *
from database.Chapters import *
from database.Sections import *
from database.ContentBlocks import *
from database.Courses import *
from database.Enrollments import *
from database.CourseTAs import *
from database.Questions import QuestionsCRUD 
from database.Activities import ActivitiesCRUD
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
questions_crud = QuestionsCRUD(DatabaseConnectionManager.get_connection())
activities_crud = ActivitiesCRUD(DatabaseConnectionManager.get_connection())

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
            print("5. Logout")
            choice = int(input("Choose option: "))
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
        # Display active courses for the faculty to choose from
        courses = coursecrud.get_all_active_courses()
        for course in courses:
            print(f"Course ID: {course['course_id']}, Name: {course['course_name']}")
        
        course_id = input("Enter Course ID of the active course you want to view: ")
        
        # Verify if the selected course is active and valid
        course = coursecrud.get_course_by_id(course_id)
        if not course or course['course_category'] != "Active":
            print("The provided Course ID is not an Active Course.")
            return
        # Fetch textbook ID associated with the selected course
        textbook_id = course.get('textbook_id')
        if not textbook_id:
            print("No textbook assigned to this course.")
            return
        while True:
            # Display menu options as per the requirements in the image
            print("\nActive Course Menu:")
            print("1. View Worklist")
            print("2. Approve Enrollment")
            print("3. View Students")
            print("4. Add New Chapter")
            print("5. Modify Chapters")
            print("6. Add TA")
            print("7. Go Back")
            
            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            
            # Call appropriate handler methods for each option (placeholders if not yet implemented)
            if choice == 1:
                self.handle_view_worklist(course_id)
            elif choice == 2:
                self.handle_approve_enrollment(course_id)
            elif choice == 3:
                self.handle_view_students(course_id)
            elif choice == 4:
                self.handle_add_chapter(textbook_id)
            elif choice == 5:
                self.handle_modify_chapter(textbook_id)
            elif choice == 6:
                self.handle_add_ta(course_id)
            elif choice == 7:
                print("Returning to Faculty Menu.")
                break
            else:
                print("Invalid choice. Please try again.")

    def handle_go_to_eval_course(self):
        course_id = input("Enter Course ID: ")
        
        # Retrieve the course information using course_id
        course = coursecrud.get_course_by_id(course_id)
        
        if not course:
            print("The provided Course ID does not exist.")
            return
        
        # Check if the course is an Evaluation course
        if course['course_category'] != "Evaluation":
            print("The provided Course ID is not an Evaluation Course.")
            return
        
        textbook_id = course.get('textbook_id')
        if not textbook_id:
            print("No textbook assigned to this course.")
            return        
        # Display the menu for Evaluation Course
        while True:
            print("\nEvaluation Course Menu:")
            print("1. Add New Chapter")
            print("2. Modify Chapters")
            print("3. Go Back")

            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            
            if choice == 1:
                self.handle_add_chapter(textbook_id)
            elif choice == 2:
                self.handle_modify_chapter(textbook_id)
            elif choice == 3:
                # Go back to Faculty Menu
                print("Returning to Faculty Menu.")
                return
            else:
                print("Invalid choice. Please try again.")

    def handle_view_courses(self):
        """Display assigned courses for the faculty."""
        
        # Fetch courses assigned to the faculty
        courses = coursecrud.get_courses_by_faculty(self.user_id)  # Assuming `self.user_id` is the faculty's ID

        if not courses:
            print("No courses assigned to you.")
            return

        # Display the list of assigned courses in a formatted table
        headers = ['Course ID', 'Course Name', 'Start Date', 'End Date', 'Category']
        max_widths = [len(header) for header in headers]

        for course in courses:
            max_widths[0] = max(max_widths[0], len(course['course_id']))
            max_widths[1] = max(max_widths[1], len(course['course_name']))
            max_widths[2] = max(max_widths[2], len(str(course['start_date'])))
            max_widths[3] = max(max_widths[3], len(str(course['end_date'])))
            max_widths[4] = max(max_widths[4], len(course['course_category']))

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
                str(course['start_date']),
                str(course['end_date']),
                course['course_category']
            ))

        print(header_line)

        # Provide the Go Back option
        while True:
            print("\n1. Go Back")
            choice = input("Choose an option: ")
            if choice == '1':
                print("Returning to Faculty Landing Page.")
                break
            else:
                print("Invalid choice. Please select 1 to go back.")
    
    def handle_add_question(self):
        #print acitvities
        activity_id = input("")
        #take question input
        
    
    def handle_view_students(self, course_id):
        """Displays the list of students enrolled in the given course."""
        students = enrollmentcrud.get_enrolled_students(course_id)
        
        if not students:
            print("No students found in this course.")
            return
        
        # Display the header
        print("\nEnrolled Students:")
        print(f"{'Student User ID':<20} | {'Enrollment Status':<15}")
        print("-" * 40)

        # Display each enrolled student
        for student in students:
            print(f"{student['student_user_id']:<20} | {student['enrollment_status']:<15}")
        
        # Display the Go Back option
        print("\n1. Go back")
        input("Choose an option: ")

    def handle_view_worklist(self, course_id):
        """Display the waiting list of students for the given active course."""
        # Fetch pending enrollments for the course
        pending_enrollments = enrollmentcrud.get_pending_enrollments(course_id)
        
        # Define column headers and widths
        headers = ["Student User ID", "Enrollment Status"]
        col_widths = [max(len(headers[0]), 15), max(len(headers[1]), 18)]
        
        # Display the list header
        print("\nPending Enrollment Worklist:")
        print(f"{headers[0]:<{col_widths[0]}} | {headers[1]:<{col_widths[1]}}")
        print("-" * (col_widths[0] + col_widths[1] + 3))  # +3 for separators
        
        # Display each enrollment entry in a formatted row
        if not pending_enrollments:
            print("No students in the waiting list.")
        else:
            for enrollment in pending_enrollments:
                print(f"{enrollment['student_user_id']:<{col_widths[0]}} | {enrollment['enrollment_status']:<{col_widths[1]}}")
        
        # Display the menu to go back
        while True:
            print("\n1. Go Back")
            choice = input("Choose an option: ")
            
            if choice == "1":
                print("Returning to Active Course Menu.")
                break
            else:
                print("Invalid option. Please select '1' to go back.")

    def handle_approve_enrollment(self, course_id):
        # Get Student ID input
        student_user_id = input("Enter the User ID of the student to approve enrollment: ")
        
        # Display the Save/Cancel menu
        while True:
            print("\n1. Save")
            print("2. Cancel")
            choice = input("Choose an option: ")
            
            if choice == "1":
                # Attempt to approve the enrollment
                if enrollmentcrud.enroll_student(course_id, student_user_id, enrollment_status="Enrolled"):
                    print("Enrollment approved successfully.")
                else:
                    print("Failed to approve enrollment. Please check if the student is already enrolled or if there was an error.")
                break
            elif choice == "2":
                print("Enrollment approval canceled.")
                break
            else:
                print("Invalid choice. Please select 1 to Save or 2 to Cancel.")



    def handle_add_chapter(self, textbook_id):
        """
        Handle adding a new chapter to a textbook for faculty.
        """
        print("Enter Chapter Details:")
        chapter_id = input("A. Unique Chapter ID: ")
        chapter_title = input("B. Chapter Title: ")
        
        # Confirm if the chapter should be hidden
        is_hidden = input("Is the chapter hidden (yes/no)? ").strip().lower() == 'yes'
        
        # Add the chapter to the database
        try:
            chaptercrud.add_chapter(textbook_id, chapter_id, chapter_title, is_hidden)
            print("Chapter added successfully.")
        except Exception as e:
            print(f"Error adding chapter: {e}")
        
        while True:
            # Display the menu
            print("\n1. Add New Section")
            print("2. Go Back")
            
            choice = input("Choose an option: ")
            if choice == "1":
                # Placeholder for handling adding a new section, which we’ll implement later
                self.handle_add_section(textbook_id, chapter_id)
            elif choice == "2":
                print("Going back to the previous menu.")
                return
            else:
                print("Invalid choice. Please choose 1 or 2.")



    def handle_modify_chapter(self, textbook_id):
        """Display menu for modifying a chapter with options as per requirements."""
        chapter_id = input("Enter Unique Chapter ID to modify: ")

        # Display the menu options as per the requirements
        while True:
            print("\nModify Chapter Menu:")
            print("1. Hide Chapter")
            print("2. Delete Chapter")
            print("3. Add New Section")
            print("4. Modify Section")
            print("5. Go Back")

            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == 1:
                self.handle_hide_chapter(textbook_id, chapter_id)
            elif choice == 2:
                self.handle_delete_chapter(textbook_id, chapter_id)
            elif choice == 3:
                self.handle_add_section(textbook_id, chapter_id)
            elif choice == 4:
                self.handle_modify_section(textbook_id, chapter_id)
            elif choice == 5:
                print("Returning to the previous menu.")
                break
            else:
                print("Invalid choice. Please try again.")

        print("Modify Chapter complete.")

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

    def handle_hide_chapter(self, textbook_id, chapter_id):
        """Hide a chapter based on user confirmation."""

        # Display the hide chapter confirmation menu
        print("Hide Chapter Menu:")
        print("1. Save")
        print("2. Cancel")

        choice = input("Choose an option: ")
        
        if choice == "1":
            # Attempt to hide the chapter
            success = chaptercrud.hide_chapter(textbook_id, chapter_id)
            if success:
                print("Chapter hidden successfully.")
            else:
                print("Failed to hide chapter. Please check the chapter details.")
        elif choice == "2":
            print("Hide chapter operation canceled.")
        else:
            print("Invalid choice. Please select 1 or 2.")

    def handle_delete_chapter(self, textbook_id, chapter_id):
        """Delete a chapter based on user confirmation."""

        # Display the delete chapter confirmation menu
        print("Delete Chapter Menu:")
        print("1. Save")
        print("2. Cancel")

        choice = input("Choose an option: ")
        
        if choice == "1":
            # Attempt to delete the chapter
            success = chaptercrud.delete_chapter(textbook_id, chapter_id)
            if success:
                print("Chapter deleted successfully.")
            else:
                print("Failed to delete chapter. Please check the chapter details.")
        elif choice == "2":
            print("Delete chapter operation canceled.")
        else:
            print("Invalid choice. Please select 1 or 2.")

    

    def handle_modify_section(self, textbook_id, chapter_id):
        print("Modifying a section...")
        section_number = input("Enter Section Number to modify: ")
        sections = sectioncrud.get_sections_by_chapter_and_textbook(chapter_id, textbook_id)  # Updated function
        selected_section = next((section for section in sections if str(section['section_id']) == section_number), None)

        if selected_section:
            while True:
                print("\nModify Section Menu:")
                print("1. Hide Section")
                print("2. Delete Section")
                print("3. Add New Content Block")
                print("4. Modify Content Block")
                print("5. Go Back")
                print("6. Landing Page")

                try:
                    choice = int(input("Choose an option: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == 1:
                    self.handle_hide_section(textbook_id, chapter_id, section_number)
                elif choice == 2:
                    self.handle_delete_section(textbook_id, chapter_id, section_number)
                elif choice == 3:
                    self.handle_add_content_block(textbook_id, chapter_id, section_number)
                elif choice == 4:
                    self.handle_modify_content_block(textbook_id, chapter_id, section_number)
                elif choice == 5:
                    print("Going back to the previous menu.")
                    break
                elif choice == 6:
                    return
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Section Number not found.")
    
    def handle_hide_section(self, textbook_id, chapter_id, section_id):
        """Handles hiding a section."""
        while True:
            print("\nHide Section Menu:")
            print("1. Save")
            print("2. Cancel")

            choice = input("Choose an option: ")

            if choice == "1":
                # Hide the section by updating the `hidden` field
                success = sectioncrud.hide_section(textbook_id, chapter_id, section_id)
                if success:
                    print("Section hidden successfully.")
                else:
                    print("Failed to hide section. Please check the section details.")
                return  # Exit after attempting to save

            elif choice == "2":
                print("Hide section canceled.")
                return  # Exit without saving
            else:
                print("Invalid choice. Please select 1 or 2.")


    def handle_delete_section(self, textbook_id, chapter_id, section_id):
        """Handles deleting a section."""
        while True:
            print("\nDelete Section Menu:")
            print("1. Save")
            print("2. Cancel")

            choice = input("Choose an option: ")

            if choice == "1":
                # Delete the section from the database
                success = sectioncrud.delete_section(textbook_id, chapter_id, section_id)
                if success:
                    print("Section deleted successfully.")
                else:
                    print("Failed to delete section. Please check the section details.")
                return  # Exit after attempting to delete

            elif choice == "2":
                print("Delete section canceled.")
                return  # Exit without deleting
            else:
                print("Invalid choice. Please select 1 or 2.")
    

    
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
                print("1. Hide Content Block")
                print("2. Delete Content Block")
                print("3. Add Text")
                print("4. Add Picture")
                print("5. Hide Activity")
                print("6. Delete Activity")
                print("7. Add New Activity")
                print("8. Go Back")
                print("9. Landing Page")

                try:
                    choice = int(input("Choose an option: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == 1:
                    self.handle_hide_content_block(textbook_id, chapter_id, section_number, content_block_id)
                elif choice == 2:
                    self.handle_delete_content_block(textbook_id, chapter_id, section_number, content_block_id)
                elif choice == 3:
                    self.handle_add_text(content_block_id, section_number, chapter_id, textbook_id)
                elif choice == 4:
                    self.handle_add_picture(content_block_id, section_number, chapter_id, textbook_id)
                elif choice == 5:
                    activity_id = input("Enter Activity ID to hide: ")
                    self.handle_hide_activity(content_block_id, section_number, chapter_id, textbook_id, activity_id)
                elif choice == 6:
                    activity_id = input("Enter Activity ID to delete: ")
                    self.handle_delete_activity(content_block_id, section_number, chapter_id, textbook_id, activity_id)
                elif choice == 7:
                    self.handle_add_activity(content_block_id, section_number, chapter_id, textbook_id)
                elif choice == 8:
                    print("Going back to the previous menu.")
                    break
                elif choice == 9:
                    print("Returning to User Landing Page.")
                    return
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Content Block ID not found.")

    def handle_hide_content_block(self, textbook_id, chapter_id, section_number, content_block_id):
        print("\nHide Content Block Menu:")
        print("1. Save")
        print("2. Cancel")
        choice = input("Choose an option: ")
        
        if choice == "1":
            success = contentblockcrud.hide_content_block(content_block_id)
            if success:
                print("Content Block hidden successfully.")
            else:
                print("Failed to hide Content Block.")
        elif choice == "2":
            print("Cancelled hiding Content Block.")

    def handle_delete_content_block(self, textbook_id, chapter_id, section_number, content_block_id):
        print("\nDelete Content Block Menu:")
        print("1. Save")
        print("2. Cancel")
        choice = input("Choose an option: ")
        
        if choice == "1":
            success = contentblockcrud.delete_content_block(content_block_id)
            if success:
                print("Content Block deleted successfully.")
            else:
                print("Failed to delete Content Block.")
        elif choice == "2":
            print("Cancelled deleting Content Block.")

    def handle_hide_activity(self, content_block_id, section_number, chapter_id, textbook_id, activity_id):
        print("\nHide Activity Menu:")
        print("1. Save")
        print("2. Cancel")
        choice = input("Choose an option: ")
        
        if choice == "1":
            success = activity_crud.hide_activity(activity_id)
            if success:
                print("Activity hidden successfully.")
            else:
                print("Failed to hide Activity.")
        elif choice == "2":
            print("Cancelled hiding Activity.")

    def handle_delete_activity(self, content_block_id, section_number, chapter_id, textbook_id, activity_id):
        print("\nDelete Activity Menu:")
        print("1. Save")
        print("2. Cancel")
        choice = input("Choose an option: ")
        
        if choice == "1":
            success = activity_crud.delete_activity(activity_id)
            if success:
                print("Activity deleted successfully.")
            else:
                print("Failed to delete Activity.")
        elif choice == "2":
            print("Cancelled deleting Activity.")

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


    def handle_add_ta(self, course_id):
        print("Enter TA Details:")
        first_name = input("A. First Name: ")
        last_name = input("B. Last Name: ")
        email = input("C. Email: ")
        default_password = input("D. Default Password: ")

        while True:
            print("\n1. Save")
            print("2. Cancel")
            choice = input("Choose an option: ")
            
            if choice == "1":
                # Use the specialized function to create a TA user
                success = usercrud.create_ta_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=default_password
                )
                
                if success:
                    # Fetch the newly created TA's user_id
                    ta_user = usercrud.fetch_user_by_email(email)
                    if ta_user:
                        ta_id = ta_user['user_id']
                        faculty_id = self.user_id
                        
                        print(f"Assigning TA to course {course_id} under faculty {faculty_id}")
                        
                        # Assign TA to the course in CourseTAs table
                        assign_success = coursetacrud.assign_ta_to_course(ta_id, course_id, faculty_id)
                        if assign_success:
                            print("TA added and assigned to the course successfully.")
                        else:
                            print("Failed to assign TA to the course. Please check the course ID and faculty ID.")
                    else:
                        print("Error retrieving TA user ID. Check if user creation was successful.")
                else:
                    print("Failed to create TA. Please check the details.")
                return

            elif choice == "2":
                print("TA addition canceled.")
                return
            else:
                print("Invalid choice. Please select 1 or 2.")


    
    def handle_view_course(self):
        courses = coursecrud.get_all_courses()
        if not len(courses):
            print("No Courses Found.")
            return
        headings = ['']
        print_list_as_table(headings=headings, rows=courses)

        
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
                print("Returning to Faculty Landing Page without updating password.")
                return  # Exit the function to go back

            else:
                print("Invalid choice. Please try again.")
        
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





    def handle_show_content_block(self):
        print("Showing a content block...")
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