CREATE TABLE User (
    UserID VARCHAR(8) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(255),
    Role ENUM('admin', 'faculty', 'student', 'teaching_assistant'),
    AccountCreationDate DATE DEFAULT CURRENT_DATE
);

CREATE TABLE Textbook (
    TextbookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255),
    AdminID VARCHAR(8),
    IsHidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (AdminID) REFERENCES User(UserID)
);

CREATE TABLE Chapter (
    ChapterID INT AUTO_INCREMENT PRIMARY KEY,
    TextbookID INT,
    Title VARCHAR(255),
    IsHidden BOOLEAN DEFAULT FALSE,
);

CREATE TABLE Section (
    SectionID INT AUTO_INCREMENT PRIMARY KEY,
    ChapterID INT,
    TextbookID INT,
    Title VARCHAR(255),
    SectionNumber VARCHAR(10),
    IsHidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (ChapterID) REFERENCES Chapter(ChapterID),
    FOREIGN KEY (TextbookID) REFERENCES Textbook(TextbookID)
);

/* for Contentblock, if ContentType is Activity, content should be one of the activity, */
CREATE TABLE ContentBlock (
    BlockID INT AUTO_INCREMENT PRIMARY KEY,
    SectionID INT,
    ChapterID INT,
    TextbookID INT,
    ContentType ENUM('text', 'image', 'activity'),
    Content TEXT,
    SequenceNumber INT,
    IsHidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (SectionID) REFERENCES Section(SectionID),
    FOREIGN KEY (ChapterID) REFERENCES Chapter(ChapterID),
    FOREIGN KEY (TextbookID) REFERENCES Textbook(TextbookID)
);

CREATE TABLE Activity (
    ActivityID INT AUTO_INCREMENT PRIMARY KEY,
    BlockID INT,
    SectionID INT,
    ChapterID INT,
    TextbookID INT,
    IsHidden BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (BlockID) REFERENCES ContentBlock(BlockID),
    FOREIGN KEY (SectionID) REFERENCES Section(SectionID),
    FOREIGN KEY (ChapterID) REFERENCES Chapter(ChapterID),
    FOREIGN KEY (TextbookID) REFERENCES Textbook(TextbookID)
);

CREATE TABLE Question (
    QuestionID INT AUTO_INCREMENT PRIMARY KEY,
    ActivityID INT,
    Question TEXT,
    CorrectAnswer TEXT,
    CorrectExplanation TEXT,
    WrongAnswer1 TEXT,
    WrongExplanation1 TEXT,
    WrongAnswer2 TEXT,
    WrongExplanation2 TEXT,
    WrongAnswer3 TEXT,
    WrongExplanation3 TEXT,
    FOREIGN KEY (ActivityID) REFERENCES Activity(ActivityID)
);

CREATE TABLE Course (
    CourseID INT PRIMARY KEY AUTO_INCREMENT,
    TextbookID INT,
    Title VARCHAR(255),
    FacultyID VARCHAR(8),
    StartDate DATE,
    EndDate DATE,
    CourseType ENUM('active', 'evaluation'),
    Token VARCHAR(7),
    Capacity INT,
    FOREIGN KEY (TextbookID) REFERENCES Textbook(TextbookID),
    FOREIGN KEY (FacultyID) REFERENCES User(UserID)
);

CREATE TABLE Enrollment (
    EnrollmentID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID INT,
    UserID VARCHAR(8),
    Status ENUM('pending', 'approved', 'rejected'),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE StudentActivity (
    StudentActivityID INT AUTO_INCREMENT PRIMARY KEY,
    UserID VARCHAR(8),
    ActivityID INT,
    CourseID INT,
    Score INT,
    Timestamp DATETIME,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ActivityID) REFERENCES Activity(ActivityID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE Notification (
    NotificationID INT AUTO_INCREMENT PRIMARY KEY,
    UserID VARCHAR(8),
    Message TEXT,
    Timestamp DATETIME,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE CourseTA (
    CourseTAID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID INT,
    TA_ID VARCHAR(8),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (TA_ID) REFERENCES User(UserID)
);
