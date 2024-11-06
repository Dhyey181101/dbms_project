from application_flow.flow import Flow
from database.Users import *
from database.Courses import *
from database.Enrollments import *
from database.ContentBlocks import *
from database.Sections import *
from database.Questions import *
from database.Activities import *
from database.StudentActivities import *
from utils.db_connector import *
from utils.utils import print_list_as_table

usercrud = UserCRUD(DatabaseConnectionManager.get_connection())
coursecrud = CourseCRUD(DatabaseConnectionManager.get_connection())
enrollcrud = EnrollmentCRUD(DatabaseConnectionManager.get_connection())
contentblockcrud = ContentBlockCRUD(DatabaseConnectionManager.get_connection())
sectioncrud = SectionCRUD(DatabaseConnectionManager.get_connection())
questioncrud = QuestionCRUD(DatabaseConnectionManager.get_connection())
activitycrud=ActivitiesCRUD(DatabaseConnectionManager.get_connection())
studentactivitycrud = StudentActivityCRUD(DatabaseConnectionManager.get_connection())

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
                        # Display Table of Contents if the user is signed in
                    print("\nTable of Contents (Enrolled Courses):")

                    # Fetch and display the hierarchical structure of enrolled courses
                    enrolled_courses = enrollcrud.get_enrolled_courses(self.user_id)
                    if not enrolled_courses:
                        print("No enrolled courses found.")
                        break

                    for course in enrolled_courses:
                        print(f"Course: {course['course_id']} - {course['course_name']}")

                        textbooks = coursecrud.get_textbooks_by_course(course['course_id'])
                        for textbook in textbooks:
                            print(f"  E-book {textbook['textbook_id']} - {textbook['title']}")

                            chapters = sectioncrud.get_chapters_by_textbook(textbook['textbook_id'])
                            for chapter in chapters:
                                print(f"    Chapter {chapter['chapter_id']} - {chapter['title']}")

                                sections = sectioncrud.get_sections_by_chapter(chapter['chapter_id'], textbook['textbook_id'], include_hidden=False)
                                for section in sections:
                                    print(f"      Section {section['section_id']} - {section['title']}")

                                    content_blocks = contentblockcrud.retrieve_content_blocks_for_section(course['course_id'], textbook['textbook_id'], chapter['chapter_id'], section['section_id'], include_hidden=False)
                                    for block in content_blocks:
                                        print(f"        Block {block['content_block_id']} - {block['content_type']}")
                    
                    print("Student Menu:")
                    print("1. View Section")
                    print("2. View Participation activity point")
                    print("3. Logout")
                    choice = int(input(""))
                    if choice==1:
                        self.handle_view_section()
                    elif choice==2:
                        self.view_participation_points()
                    elif choice==3:
                        self.handle_logout()
                        break
                
                    
    def handle_view_section(self):
        sections = sectioncrud.get_all_sections_associated_with_user(self.user_id)
        
        # Define column headings for display
        headings = ['Course ID', 'Course Name', 'Textbook ID', 'Chapter ID', 'Section ID', 'Section Title']
        header_row = " | ".join(headings)
        print("-" * (len(header_row) + 4))
        print("| " + header_row + " |")
        print("-" * (len(header_row) + 4))

        # Print each section in a formatted row with course and textbook details
        for section in sections:
            row = (
                f"| {section['course_id']} | {section['course_name']} | {section['textbook_id']} | "
                f"{section['chapter_id']} | {section['section_id']} | {section['section_title']} |"
            )
            print(row)

        print("-" * (len(header_row) + 4))
        
        # Prompt for course, textbook, chapter, and section details
        course_id = input("Enter Course ID: ")
        textbook_id = input("Enter Textbook ID associated with this course: ")
        chapter_id = input("Enter Chapter ID associated with this textbook: ")
        section_id = input("Enter Section ID associated with this chapter: ")
        
        # Once all inputs are gathered, display block menu
        while True:
            print("\nBlock Menu:")
            print("1. View Block")
            print("2. Go Back")
            choice = int(input("Enter your choice (1-2): "))

            if choice == 1:
                self.handle_view_block(course_id, textbook_id, chapter_id, section_id)
            elif choice == 2:
                break
            else:
                print("Invalid choice. Please select again.")
                continue
                

    def view_participation_points(self):
        """Display the total participation points and a go-back option."""
        total_points = studentactivitycrud.get_total_participation_points(self.user_id)
        print(f"\nTotal Participation Activity Points: {total_points}")
        
        # Display the menu to go back
        print("\n1. Go back")
        choice = int(input("Enter your choice (1): "))
        
        if choice == 1:
            print("Returning to the main menu...")


    def handle_view_block(self, course_id, textbook_id, chapter_id, section_id):
        """Fetch and display content blocks based on user inputs for course, textbook, chapter, and section."""
        # Fetch content blocks based on provided course, textbook, chapter, and section
        content_blocks = contentblockcrud.retrieve_content_blocks_for_section(
            course_id=course_id, 
            textbook_id=textbook_id, 
            chapter_id=chapter_id, 
            section_id=section_id
        )

        if not content_blocks:
            print("No content blocks found for the given section.")
            return

        # Iterate through each content block
        for i, block in enumerate(content_blocks):
            print("\nContent Block:")
            print(f"Block ID: {block['content_block_id']}")
            print(f"Content Type: {block['content_type']}")
            
            # Check if the content block is of type 'text' or 'activity'
            if block['content_type'] == 'text':
                # Display the content
                print(f"Content: {block['content']}")
                
                # Menu for text content
                while True:
                    print("\n1. Next/Submit")
                    print("2. Go Back")
                    choice = int(input("Enter your choice (1-2): "))

                    if choice == 1:
                        # Go to the next block or return to the landing page if it's the last block
                        if i == len(content_blocks) - 1:
                            print("This was the last content block. Returning to the landing page.")
                            return
                        break
                    elif choice == 2:
                        print("Returning to the previous page...")
                        return
                    else:
                        print("Invalid choice. Please select again.")
            
            elif block['content_type'] == 'activity':

                    # Retrieve the actual unique_activity_id for the activity from Activities table
                activity = activitycrud.get_activity_by_block_id(block['content_block_id'])
                if not activity:
                    print(f"No activity found for block ID {block['content_block_id']}. Skipping.")
                    continue  # Skip this block if no associated activity is found

                unique_activity_id = activity['activity_id']  # Set to actual activity ID
                # Fetch questions associated with this content block, including textbook_id for filtering
                questions = questioncrud.get_questions_by_block_id(
                    block_id=block['content_block_id'], 
                    section_id=section_id, 
                    chapter_id=chapter_id, 
                    textbook_id=textbook_id
                )

                # Display all questions associated with this block
                for question in questions:
                    print(f"\nQuestion: {question['question_text']}")
                    print(f"1. {question['option_1']}")
                    print(f"2. {question['option_2']}")
                    print(f"3. {question['option_3']}")
                    print(f"4. {question['option_4']}")
                    
                    # Get user answer
                    answer = int(input("Enter the correct answer (1-4): "))
                    
                    # Calculate points based on the answer
                    points = 3 if answer == question['answer'] else 1

                    # Store or update the score in StudentActivities
                    studentactivitycrud.update_or_insert_student_activity(
                        student_id=self.user_id,
                        course_id=course_id,
                        textbook_id=textbook_id,
                        section_id=section_id,
                        chapter_id=chapter_id,
                        block_id=block['content_block_id'],
                        unique_activity_id=unique_activity_id,  # Assuming unique_activity_id is the block ID here
                        question_id=question['question_id'],
                        points=points
                    )

                    # Check answer and show explanation
                    if answer == question['answer']:
                        print("Correct! Explanation:", question[f"opt_{answer}_exp"])
                    else:
                        correct_answer = question['answer']
                        print(f"Incorrect. The correct answer is {correct_answer}. Explanation:", question[f"opt_{correct_answer}_exp"])

                    # Menu for each question
                    while True:
                        print("\n1. Next Question")
                        print("2. Go Back")
                        choice = int(input("Enter your choice (1-2): "))

                        if choice == 1:
                            break  # Continue to the next question
                        elif choice == 2:
                            print("Returning to the previous page...")
                            return
                        else:
                            print("Invalid choice. Please select again.")

                # End of all questions in the activity block
                print("All questions in this activity have been completed.")


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
            enrollment_successful = enrollcrud.enroll_student_i(course_id=course_id, student_user_id=student_user_id, enrollment_status="Pending")

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