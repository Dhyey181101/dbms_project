-- Users Table to store all users with various roles
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
    textbook_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_by_admin VARCHAR(10) NOT NULL,
    hidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (created_by_admin) REFERENCES Users(user_id)
);

-- Chapters Table to store individual chapters for each textbook
CREATE TABLE Chapters (
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    hidden BOOLEAN DEFAULT FALSE,
    
    PRIMARY KEY (textbook_id, chapter_id),
    
    FOREIGN KEY (textbook_id) REFERENCES Textbooks(textbook_id)
);

-- Sections Table to manage sections within chapters
CREATE TABLE Sections (
    textbook_id INT NOT NULL,
    section_id VARCHAR(10) NOT NULL,
    chapter_id VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    hidden BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (textbook_id, section_id, chapter_id),

    FOREIGN KEY (textbook_id) REFERENCES Textbooks(textbook_id),
    FOREIGN KEY (textbook_id, chapter_id) REFERENCES Chapters(textbook_id, chapter_id)
);

-- ContentBlocks Table to store content (text, picture, activities) within sections
CREATE TABLE ContentBlocks (
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(10) NOT NULL,
    section_number VARCHAR(10) NOT NULL,
    content_block_id VARCHAR(10) NOT NULL,
    content_type ENUM('text', 'activity', 'picture') NOT NULL,
    content TEXT,
    hidden BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (textbook_id, chapter_id, section_number, content_block_id),

    FOREIGN KEY (textbook_id, chapter_id, section_number) REFERENCES Sections(textbook_id, chapter_id, section_id)
);

-- Activities Table to define interactive elements within content blocks
CREATE TABLE Activities (
    activity_id VARCHAR(10) NOT NULL,
    content_block_id VARCHAR(10) NOT NULL,
    section_id VARCHAR(10) NOT NULL,
    chapter_id VARCHAR(10) NOT NULL,
    textbook_id INT NOT NULL,
    hidden BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (activity_id, content_block_id, section_id, chapter_id, textbook_id),

    FOREIGN KEY (textbook_id, chapter_id, section_id, content_block_id) REFERENCES ContentBlocks(textbook_id, chapter_id, section_number, content_block_id)
);

-- Questions Table to store questions associated with activities
CREATE TABLE Questions (
    question_id VARCHAR(10) NOT NULL,
    textbook_id INT NOT NULL,
    chapter_id VARCHAR(10) NOT NULL,
    section_id VARCHAR(10) NOT NULL,
    block_id VARCHAR(10) NOT NULL,
    unique_activity_id VARCHAR(10) NOT NULL,
    question_text TEXT NOT NULL,
    option_1 TEXT NOT NULL,
    opt_1_exp TEXT NOT NULL,
    option_2 TEXT NOT NULL,
    opt_2_exp TEXT NOT NULL,
    option_3 TEXT NOT NULL,
    opt_3_exp TEXT NOT NULL,
    option_4 TEXT NOT NULL,
    opt_4_exp TEXT NOT NULL,
    answer INT NOT NULL,
    
    PRIMARY KEY (question_id, textbook_id, chapter_id, section_id, block_id, unique_activity_id),
    
    FOREIGN KEY (textbook_id) REFERENCES Textbooks(textbook_id),
    FOREIGN KEY (textbook_id, chapter_id) REFERENCES Chapters(textbook_id, chapter_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id) REFERENCES Sections(textbook_id, chapter_id, section_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id, block_id) REFERENCES ContentBlocks(textbook_id, chapter_id, section_number, content_block_id)
);

-- Courses Table to store course information and link to faculty, textbooks, and TAs
CREATE TABLE Courses (
    course_id VARCHAR(255) PRIMARY KEY,
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

-- Enrollments Table to manage student enrollment status in courses
CREATE TABLE Enrollments (
    course_id VARCHAR(255) NOT NULL,
    student_user_id VARCHAR(10) NOT NULL,
    enrollment_status ENUM('Enrolled', 'Pending') DEFAULT 'Pending',
    
    PRIMARY KEY (course_id, student_user_id),
    
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (student_user_id) REFERENCES Users(user_id)
);

-- StudentActivities Table for score and timestamp of each activity
CREATE TABLE StudentActivities (
    student_id VARCHAR(10) NOT NULL,
    course_id VARCHAR(255) NOT NULL,
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
    FOREIGN KEY (textbook_id, chapter_id) REFERENCES Chapters(textbook_id, chapter_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id) REFERENCES Sections(textbook_id, chapter_id, section_id),
    FOREIGN KEY (textbook_id, chapter_id, section_id, block_id) REFERENCES ContentBlocks(textbook_id, chapter_id, section_number, content_block_id),
    FOREIGN KEY (unique_activity_id) REFERENCES Activities(activity_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

-- CourseTAs Table to link TAs with specific courses
CREATE TABLE CourseTAs (
    course_ta_id VARCHAR(10) NOT NULL,
    course_id VARCHAR(255) NOT NULL,
    faculty_id VARCHAR(10) NOT NULL,

    PRIMARY KEY (course_ta_id, course_id),
    
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (course_ta_id) REFERENCES Users(user_id),
    FOREIGN KEY (faculty_id) REFERENCES Users(user_id)    
);
