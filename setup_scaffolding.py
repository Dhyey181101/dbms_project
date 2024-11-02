import os

# Define the directory structure
directories = [
    "dbms_project/config",
    "dbms_project/src",
    "dbms_project/src/admin",
    "dbms_project/src/faculty",
    "dbms_project/src/student",
    "dbms_project/src/ta",
    "dbms_project/src/utils",
    "dbms_project/sql",
]

# Define the files to be created
files = {
    "dbms_project/config/db_config.py": "# Database configuration",
    "dbms_project/src/__init__.py": "",
    "dbms_project/src/main.py": "# Main entry point for the application",
    "dbms_project/src/admin/__init__.py": "",
    "dbms_project/src/admin/admin_menu.py": "# Admin menu logic",
    "dbms_project/src/admin/admin_operations.py": "# Admin operations",
    "dbms_project/src/faculty/__init__.py": "",
    "dbms_project/src/faculty/faculty_menu.py": "# Faculty menu logic",
    "dbms_project/src/faculty/faculty_operations.py": "# Faculty operations",
    "dbms_project/src/student/__init__.py": "",
    "dbms_project/src/student/student_menu.py": "# Student menu logic",
    "dbms_project/src/student/student_operations.py": "# Student operations",
    "dbms_project/src/ta/__init__.py": "",
    "dbms_project/src/ta/ta_menu.py": "# TA menu logic",
    "dbms_project/src/ta/ta_operations.py": "# TA operations",
    "dbms_project/src/utils/__init__.py": "",
    "dbms_project/src/utils/db_utils.py": "# Utility functions for database operations",
    "dbms_project/src/utils/query_utils.py": "# SQL query functions",
    "dbms_project/sql/DBMS_project_tables.sql": "-- SQL script to create tables",
    "dbms_project/sql/Queries.sql": "-- SQL file with predefined queries",
    "dbms_project/sql/sample_data.sql": "-- Sample data for testing",
}

# Create directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

# Create files with initial content
for filepath, content in files.items():
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Created file: {filepath}")

print("Scaffolding setup complete!")
