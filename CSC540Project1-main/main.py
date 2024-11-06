from database.db_queries import DBQueries
from utils.db_connector import DatabaseConnectionManager
from application_flow.role import RoleFlow
from application_flow.admin import AdminFlow
from application_flow.faculty import FacultyFlow
from application_flow.student import StudentFlow
from application_flow.ta import TAFlow

connection = DatabaseConnectionManager.get_connection()
role_flow = RoleFlow()
role_flow_map = {"student": StudentFlow, "admin": AdminFlow, "teaching_assistant": TAFlow, "faculty": FacultyFlow}
db_queries = DBQueries(connection)

def display_query_menu():
    """Display the query menu for executing database retrieval queries."""
    print("\nRun Queries Menu:")
    print("1. Number of sections in the first chapter of a textbook")
    print("2. Names of faculty and TAs of all courses with roles")
    print("3. Active courses with faculty and student count")
    print("4. Course with the largest waiting list")
    print("5. Contents of Chapter 02 of textbook 101")
    print("6. Incorrect answers for Q2 of Activity0")
    print("7. Books in 'Active' status by one instructor and 'Evaluation' by another")
    print("0. Return to Main Menu")
    
    try:
        query_choice = int(input("Select a query to run: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    execute_query(query_choice)

def execute_query(query_number):
    """Execute the selected query and print the results."""
    if query_number == 1:
        # Query 1: Number of sections in the first chapter of a textbook
        section_count = db_queries.get_first_chapter_section_count(textbook_id=101)  # assuming textbook ID is 101
        print("Number of sections in the first chapter:", section_count)
    elif query_number == 2:
        results = db_queries.get_faculty_and_tas()
        print("Faculty and TAs:")
        for record in results:
            print(f"{record['name']} - {record['role']}")
    elif query_number == 3:
        # Query 3: Active courses with faculty and total student count
        results = db_queries.get_active_courses_with_faculty_and_student_count()
        print("Active Courses with Faculty and Student Count:")
        for course in results:
            print(f"Course ID: {course['course_id']}, Faculty: {course['faculty']}, Students: {course['student_count']}")
    elif query_number == 4:
        # Query 4: Course with the largest waiting list
        result = db_queries.get_course_with_largest_waiting_list()
        if result:
            print(f"Course ID: {result['course_id']}, Waiting List Count: {result['waiting_list_count']}")
        else:
            print("No courses with a waiting list found.")
    elif query_number == 5:
        # Query 5: Contents of Chapter 02 of textbook 101
        content = db_queries.get_chapter_content(textbook_id=101, chapter_id="Chap02")
        print("Chapter 02 Content:")
        print("\n".join(content))
    elif query_number == 6:
        # Query 6: Incorrect answers and explanations for a specific question in an activity
        answers = db_queries.get_incorrect_answers_for_activity_question(textbook_id=101, chapter_id="Chap01", section_id="Sec02", activity_id="ACT0", question_id="Q2")
        print("Incorrect Answers and Explanations:")
        for answer in answers:
            print(f"Incorrect Answer: {answer['answer']}, Explanation: {answer['explanation']}")
    elif query_number == 7:
         # Query 7: Books with different statuses by different instructors
        results = db_queries.find_books_in_different_status_by_instructors()
        if results:
            print("Books with Different Statuses by Different Instructors:")
            for result in results:
                print(f"Textbook ID: {result['textbook_id']}, Instructor1: {result['instructor1']} (Status: {result['status1']}), "
                    f"Instructor2: {result['instructor2']} (Status: {result['status2']})")
        else:
            print("No books with different statuses by different instructors found.")
    elif query_number == 0:
        return
    else:
        print("Invalid query number. Please select a valid option.")
    
def main():
    """Main application entry point."""
    while True:
        # Main Menu
        print("\nMain Menu:")
        print("1. Login as specific role")
        print("2. Run Queries")
        print("0. Exit")

        choice = input("Please choose an option: ")

        if choice == "1":
            while True:
                role_flow.print_role_menu()
                valid_input = role_flow.get_role_input()
                if valid_input:
                    break
            if role_flow.exit:
                break
            login_result = [None, None]
            if role_flow.role != "student":
                login_result = role_flow.login()
                if not login_result:
                    continue
            user_id,email=login_result
            current_role_flow = role_flow_map[role_flow.role](user_id=user_id,email=email)
            
            while True:
                current_role_flow.print_menu()
                if current_role_flow.logout:
                    print("Logging Out ...")
                    break

        elif choice == "2":
            display_query_menu()
        
        elif choice == "0":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
