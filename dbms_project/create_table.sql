-- User Table to store all users with various roles
CREATE TABLE Users (
    user_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Faculty', 'Student', 'Teaching_Assistant') NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

-- Textbooks Table for managing textbooks associated with Admins
CREATE TABLE Textbooks (
    textbook_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    created_by_admin VARCHAR(10) NOT NULL,
    hidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (created_by_admin) REFERENCES Users(user_id)
);

-- Chapter Table to store individual chapters for each textbook
CREATE TABLE Chapters (
    chapter_id INT PRIMARY KEY AUTO_INCREMENT,
    textbook_id INT NOT NULL,
    chapter_title VARCHAR(255) NOT NULL,
    hidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (textbook_id) REFERENCES Textbooks(textbook_id)
);

-- Section Table to manage sections within chapters
CREATE TABLE Sections (
    section_id INT PRIMARY KEY AUTO_INCREMENT,
    chapter_id INT NOT NULL,
    section_title VARCHAR(255) NOT NULL,
    hidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (chapter_id) REFERENCES Chapters(chapter_id)
);

-- Content Block Table to store content (text, picture, activities) within sections
CREATE TABLE ContentBlocks (
    content_block_id INT PRIMARY KEY AUTO_INCREMENT,
    section_number INT NOT NULL,
    chapter_id INT NOT NULL,
    textbook_id INT NOT NULL,
    content_type ENUM('text', 'picture', 'activities') NOT NULL,
    content TEXT,
    hidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (section_number) REFERENCES Sections(section_id),
    FOREIGN KEY (chapter_id) REFERENCES Chapters(chapter_id),
    FOREIGN KEY (textbook_id) REFERENCES Textbooks(textbook_id)
);

-- Activity Table to define interactive elements within content blocks
CREATE TABLE Activities (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    content_block_id INT NOT NULL,
    section_id INT NOT NULL,
    chapter_id INT NOT NULL,
    textbook_id INT NOT NULL,
    hidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (content_block_id) REFERENCES ContentBlocks(content_block_id),
    FOREIGN KEY (section_id) REFERENCES Sections(section_id),
    FOREIGN KEY (chapter_id) REFERENCES Chapters(chapter_id),
    FOREIGN KEY (textbook_id) REFERENCES Textbooks(textbook_id)
);

-- Question Table to store questions associated with activities
CREATE TABLE Questions (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    activity_id INT NOT NULL,
    question_text TEXT NOT NULL,
    correct_answer VARCHAR(255) NOT NULL,
    explanation_correct TEXT,
    answer_option_1 VARCHAR(255),
    explanation_option_1 TEXT,
    answer_option_2 VARCHAR(255),
    explanation_option_2 TEXT,
    answer_option_3 VARCHAR(255),
    explanation_option_3 TEXT,
    FOREIGN KEY (activity_id) REFERENCES Activities(activity_id)
);

-- Course Table to store course information and link to faculty, textbooks, and TAs
CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    textbook_id INT NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    faculty_user_id VARCHAR(10) NOT NULL,
    ta_user_id VARCHAR(10),
    start_date DATE,
    end_date DATE,
    course_category ENUM('Active', 'Evaluation') NOT NULL,
    access_token VARCHAR(10),
    max_enrollment INT,
    FOREIGN KEY (textbook_id) REFERENCES Textbooks(textbook_id),
    FOREIGN KEY (faculty_user_id) REFERENCES Users(user_id),
    FOREIGN KEY (ta_user_id) REFERENCES Users(user_id)
);

-- Enrollment Table to manage student enrollment status in courses
CREATE TABLE Enrollments (
    course_id INT NOT NULL,
    student_user_id VARCHAR(10) NOT NULL,
    enrollment_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (student_user_id) REFERENCES Users(user_id)
);

-- Student Activity Tracking Table for score and timestamp of each activity
CREATE TABLE StudentActivities (
    student_id VARCHAR(10) NOT NULL,
    course_id VARCHAR(20) NOT NULL,
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(10) NOT NULL,
    section_id VARCHAR(10) NOT NULL,
    block_id VARCHAR(10) NOT NULL,
    unique_activity_id VARCHAR(10) NOT NULL,
    question_id VARCHAR(10) NOT NULL,
    points INT DEFAULT 0 CHECK (points >= 0),
    activity_timestamp DATETIME NOT NULL,
    
    PRIMARY KEY (student_id, course_id, unique_activity_id, question_id),
    
    FOREIGN KEY (student_id) REFERENCES Users(user_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (textbook_id) REFERENCES Textbooks(textbook_id),
    FOREIGN KEY (chapter_id) REFERENCES Chapters(chapter_id),
    FOREIGN KEY (section_id) REFERENCES Sections(section_id),
    FOREIGN KEY (block_id) REFERENCES ContentBlocks(content_block_id),
    FOREIGN KEY (unique_activity_id) REFERENCES Activities(activity_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

-- Notifications Table for managing notifications sent to users
CREATE TABLE Notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    recipient_user_id VARCHAR(10) NOT NULL,
    notification_text TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipient_user_id) REFERENCES Users(user_id)
);

-- Course TA Assignment Table to link TAs with specific courses
CREATE TABLE CourseTAs (
    course_ta_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    ta_user_id VARCHAR(10) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (ta_user_id) REFERENCES Users(user_id)
);