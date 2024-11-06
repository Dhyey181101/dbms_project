-- Summary of Insertion Order
-- Users
-- Textbooks
-- Chapters
-- Sections
-- ContentBlocks
-- Activities
-- Questions
-- Courses
-- Enrollments
-- StudentActivities
-- CourseTAs
INSERT INTO Users (user_id, first_name, last_name, email, password_hash, role) VALUES
('ErPe1024', 'Eric', 'Perrig', 'ez356@example.mail', 'qwdmq', 'Student'),
('AlAr1024', 'Alice', 'Artho', 'aa23@edu.mail', 'omdsws', 'Student'),
('BoTe1024', 'Bob', 'Temple', 'bt163@template.mail', 'sak+=', 'Student'),
('LiGa1024', 'Lily', 'Gaddy', 'li123@example.edu', 'cnaos', 'Student'),
('ArMo1024', 'Aria', 'Morrow', 'am213@example.edu', 'jwocals', 'Student'),
('KeRh1014', 'Kellan', 'Rhodes', 'kr21@example.edu', 'camome', 'Student'),
('SiHa1024', 'Sienna', 'Hayes', 'sh13@example.edu', 'asdqm', 'Student'),
('FiWi1024', 'Finn', 'Wilder', 'fw23@example.edu', 'f13mas', 'Student'),
('LeMe1024', 'Leona', 'Mercer', 'lm56@example.edu', 'ca32', 'Student'),
('JaWi1024', 'James', 'Williams', 'jwilliams@ncsu.edu', 'jwilliams@1234', 'Teaching_Assistant'),
('LiAl0924', 'Lisa', 'Alberti', 'lalberti@ncsu.edu', 'lalberti&5678@', 'Teaching_Assistant'),
('DaJo1024', 'David', 'Johnson', 'djohnson@ncsu.edu', 'djohnson%@1122', 'Teaching_Assistant'),
('ElCl1024', 'Ellie', 'Clark', 'eclark@ncsu.edu', 'eclark^#3654', 'Teaching_Assistant'),
('JeGi0924', 'Jeff', 'Gibson', 'jgibson@ncsu.edu', 'jgibson$#9877', 'Teaching_Assistant'),
('KeOg1024', 'Kemafor', 'Ogan', 'kogan@ncsu.edu', 'Ko2024!rpc', 'Faculty'),
('JoDo1024', 'John', 'Doe', 'john.doe@example.com', 'Jd2024!abc', 'Faculty'),
('SaMi1024', 'Sarah', 'Miller', 'sarah.miller@domain.com', 'Sm#Secure2024', 'Faculty'),
('DaBr1024', 'David', 'Brown', 'david.b@webmail.com', 'DbPass123!', 'Faculty'),
('EmDa1024', 'Emily', 'Davis', 'emily.davis@email.com', 'Emily#2024!', 'Faculty'),
('MiWi1024', 'Michael', 'Wilson', 'michael.w@service.com', 'Mw987secure', 'Faculty'),
('admin', 'admin', 'main', 'admin@example.com', 'admin123', 'Admin');


INSERT INTO Textbooks (textbook_id, title, created_by_admin, hidden) VALUES 
(101, 'Database Management Systems', 'admin', FALSE),
(102, 'Fundamentals of Software Engineering', 'admin', FALSE),
(103, 'Fundamentals of Machine Learning', 'admin', FALSE);


INSERT INTO Chapters (textbook_id, chapter_id, title, hidden) VALUES
(101, 'chap01', 'Introduction to Database', FALSE),
(101, 'chap02', 'The Relational Model', FALSE),
(102, 'chap01', 'Introduction to Software Engineering', FALSE),
(102, 'chap02', 'Introduction to Software Development Life Cycle (SDLC)', FALSE),
(103, 'chap01', 'Introduction to Machine Learning', FALSE);


INSERT INTO Sections (textbook_id, section_id, chapter_id, title, hidden) VALUES
(101, 'Sec01', 'chap01', 'Database Management Systems (DBMS) Overview', FALSE),
(101, 'Sec02', 'chap01', 'Data Models and Schemas', FALSE),
(101, 'Sec01', 'chap02', 'Entities, Attributes, and Relationships', FALSE),
(101, 'Sec02', 'chap02', 'Normalization and Integrity Constraints', FALSE),
(102, 'Sec01', 'chap01', 'History and Evolution of Software Engineering', FALSE),
(102, 'Sec02', 'chap01', 'Key Principles of Software Engineering', FALSE),
(102, 'Sec01', 'chap02', 'Phases of the SDLC', TRUE),
(102, 'Sec02', 'chap02', 'Agile vs. Waterfall Models', FALSE),
(103, 'Sec01', 'chap01', 'Overview of Machine Learning', TRUE),
(103, 'Sec02', 'chap01', 'Supervised vs Unsupervised Learning', FALSE);


INSERT INTO ContentBlocks (textbook_id, chapter_id, section_number, content_block_id, content_type, content, hidden) VALUES
(101, 'chap01', 'Sec01', 'Block01', 'text', 'A Database Management System (DBMS) is software that enables users to efficiently create, manage, and manipulate databases. It serves as an interface between the database and end users, ensuring data is stored securely, retrieved accurately, and maintained consistently. Key features of a DBMS include data organization, transaction management, and support for multiple users accessing data concurrently.', FALSE),
(101, 'chap01', 'Sec02', 'Block01', 'activity', 'ACT0', FALSE),
(101, 'chap02', 'Sec01', 'Block01', 'text', 'DBMS systems provide structured storage and ensure that data is accessible through queries using languages like SQL. They handle critical tasks such as maintaining data integrity, enforcing security protocols, and optimizing data retrieval, making them essential for both small-scale and enterprise-level applications. Examples of popular DBMS include MySQL, Oracle, and PostgreSQL.', FALSE),
(101, 'chap02', 'Sec02', 'Block01', 'picture', 'sample.png', FALSE),
(102, 'chap01', 'Sec01', 'Block01', 'text', 'The history of software engineering dates back to the 1960s, when the "software crisis" highlighted the need for structured approaches to software development due to rising complexity and project failures. Over time, methodologies such as Waterfall, Agile, and DevOps evolved, transforming software engineering into a disciplined, iterative process that emphasizes efficiency, collaboration, and adaptability.', FALSE),
(102, 'chap01', 'Sec02', 'Block01', 'activity', 'ACT0', FALSE),
(102, 'chap02', 'Sec01', 'Block01', 'text', 'The Software Development Life Cycle (SDLC) consists of key phases including requirements gathering, design, development, testing, deployment, and maintenance. Each phase plays a crucial role in ensuring that software is built systematically, with feedback and revisions incorporated at each step to deliver a high-quality product.', FALSE),
(102, 'chap02', 'Sec02', 'Block01', 'picture', 'sample2.png', FALSE),
(103, 'chap01', 'Sec01', 'Block01', 'text', 'Machine learning is a subset of artificial intelligence that enables systems to learn from data, identify patterns, and make decisions with minimal human intervention. By training algorithms on vast datasets, machine learning models can improve their accuracy over time, driving advancements in fields like healthcare, finance, and autonomous systems.', FALSE),
(103, 'chap01', 'Sec02', 'Block01', 'activity', 'ACT0', FALSE);


INSERT INTO Activities (activity_id, content_block_id, section_id, chapter_id, textbook_id, hidden) VALUES
('ACT0', 'Block01', 'Sec02', 'chap01', 101, FALSE),
('ACT0', 'Block01', 'Sec02', 'chap01', 102, FALSE),
('ACT0', 'Block01', 'Sec02', 'chap01', 103, FALSE);


INSERT INTO Questions (textbook_id, chapter_id, section_id, block_id, unique_activity_id, question_id, question_text, option_1, opt_1_exp, option_2, opt_2_exp, option_3, opt_3_exp, option_4, opt_4_exp, answer) VALUES
(101, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q1', 'What does a DBMS provide?', 'Data storage only', 'Incorrect: DBMS provides more than just storage', 'Data storage and retrieval', 'Correct: DBMS manages both storing and retrieving data', 'Only security features', 'Incorrect: DBMS also handles other functions', 'Network management', 'Incorrect: DBMS does not manage network infrastructure', 2),
(101, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q2', 'Which of these is an example of a DBMS?', 'Microsoft Excel', 'Incorrect: Excel is a spreadsheet application', 'MySQL', 'Correct: MySQL is a popular DBMS', 'Google Chrome', 'Incorrect: Chrome is a web browser', 'Windows 10', 'Incorrect: Windows is an operating system', 2),
(101, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q3', 'What type of data does a DBMS manage?', 'Structured data', 'Correct: DBMS primarily manages structured data', 'Unstructured multimedia', 'Incorrect: While some DBMS systems can handle it, it''s not core', 'Network traffic data', 'Incorrect: DBMS doesn’t manage network data', 'Hardware usage statistics', 'Incorrect: DBMS does not handle hardware usage data', 1),
(102, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q1', 'What was the "software crisis"?', 'A hardware shortage', 'Incorrect: The crisis was related to software development issues', 'Difficulty in software creation', 'Correct: The crisis was due to the complexity and unreliability of software', 'A network issue', 'Incorrect: It was not related to networking', 'Lack of storage devices', 'Incorrect: The crisis was not about physical storage limitations', 2),
(102, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q2', 'Which methodology was first introduced in software engineering?', 'Waterfall model', 'Correct: Waterfall was the first formal software development model', 'Agile methodology', 'Incorrect: Agile was introduced much later', 'DevOps', 'Incorrect: DevOps is a more recent development approach', 'Scrum', 'Incorrect: Scrum is a part of Agile, not the first methodology', 1),
(102, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q3', 'What challenge did early software engineering face?', 'Lack of programming languages', 'Incorrect: Programming languages existed but were difficult to manage', 'Increasing complexity of software', 'Correct: Early engineers struggled with managing large, complex systems', 'Poor hardware development', 'Incorrect: The issue was primarily with software, not hardware', 'Internet connectivity issues', 'Incorrect: Internet connectivity wasn''t a challenge in early software', 2),
(103, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q1', 'What is the primary goal of supervised learning?', 'Predict outcomes', 'Correct: The goal is to learn a mapping from inputs to outputs for prediction.', 'Group similar data', 'Incorrect: This is more aligned with unsupervised learning.', 'Discover patterns', 'Incorrect: This is not the main goal of supervised learning.', 'Optimize cluster groups', 'Incorrect: This is not applicable to supervised learning.', 1),
(103, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q2', 'Which type of data is used in unsupervised learning?', 'Labeled data', 'Incorrect: Unsupervised learning uses unlabeled data.', 'Unlabeled data', 'Correct: It analyzes data without pre-existing labels.', 'Structured data', 'Incorrect: Unlabeled data can be structured or unstructured.', 'Time-series data', 'Incorrect: Unsupervised learning does not specifically focus on time-series.', 2),
(103, 'chap01', 'Sec02', 'Block01', 'ACT0', 'Q3', 'In which scenario would you typically use supervised learning?', 'Customer segmentation', 'Incorrect: This is more relevant to unsupervised learning.', 'Fraud detection', 'Correct: Supervised learning is ideal for predicting fraud based on labeled examples.', 'Market basket analysis', 'Incorrect: This is generally done using unsupervised methods.', 'Anomaly detection', 'Incorrect: While applicable, it is less common than fraud detection in supervised learning.', 2);


INSERT INTO Courses (course_id, course_name, textbook_id, course_category, faculty_user_id, ta_user_id, start_date, end_date, access_token, max_enrollment) VALUES
('NCSUOganCSC440F24', 'CSC440 Database Systems', 101, 'Active', 'KeOg1024', 'JaWi1024', '2024-08-15', '2024-12-15', 'XYJKLM', 60),
('NCSUOganCSC540F24', 'CSC540 Database Systems', 101, 'Active', 'KeOg1024', 'LiAl0924', '2024-08-17', '2024-12-15', 'STUKZT', 50),
('NCSUSaraCSC326F24', 'CSC326 Software Engineering', 102, 'Active', 'SaMi1024', 'DaJo1024', '2024-08-23', '2024-10-23', 'LRUFND', 100),
('NCSUDoeCSC522F24', 'CSC522 Fundamentals of Machine Learning', 103, 'Evaluation', 'JoDo1024', NULL, '2025-08-25', '2025-12-18', NULL, NULL),
('NCSUSaraCSC326F25', 'CSC326 Software Engineering', 102, 'Evaluation', 'SaMi1024', NULL, '2025-08-27', '2025-12-19', NULL, NULL);


INSERT INTO Enrollments (course_id, student_user_id, enrollment_status) VALUES
('NCSUOganCSC440F24', 'ErPe1024', 'Enrolled'),
('NCSUOganCSC540F24', 'ErPe1024', 'Enrolled'),
('NCSUOganCSC440F24', 'AlAr1024', 'Enrolled'),
('NCSUOganCSC440F24', 'BoTe1024', 'Enrolled'),
('NCSUOganCSC440F24', 'LiGa1024', 'Enrolled'),
('NCSUOganCSC540F24', 'LiGa1024', 'Enrolled'),
('NCSUOganCSC540F24', 'ArMo1024', 'Enrolled'),
('NCSUOganCSC440F24', 'ArMo1024', 'Enrolled'),
('NCSUOganCSC440F24', 'SiHa1024', 'Enrolled'),
('NCSUSaraCSC326F24', 'FiWi1024', 'Enrolled'),
('NCSUOganCSC440F24', 'LeMe1024', 'Enrolled'),
('NCSUOganCSC440F24', 'FiWi1024', 'Pending'),
('NCSUOganCSC540F24', 'LeMe1024', 'Pending'),
('NCSUOganCSC540F24', 'AlAr1024', 'Pending'),
('NCSUOganCSC540F24', 'SiHa1024', 'Pending'),
('NCSUOganCSC540F24', 'FiWi1024', 'Pending');


INSERT INTO StudentActivities (student_id, course_id, textbook_id, section_id, chapter_id, block_id, unique_activity_id, question_id, points) VALUES
('ErPe1024', 'NCSUOganCSC440F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q1', 3),
('ErPe1024', 'NCSUOganCSC440F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q2', 1),
('ErPe1024', 'NCSUOganCSC540F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q1', 1),
('AlAr1024', 'NCSUOganCSC440F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q1', 3),
('BoTe1024', 'NCSUOganCSC440F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q1', 0),
('LiGa1024', 'NCSUOganCSC440F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q1', 3),
('LiGa1024', 'NCSUOganCSC440F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q2', 3),
('LiGa1024', 'NCSUOganCSC540F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q1', 3),
('ArMo1024', 'NCSUOganCSC440F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q1', 1),
('ArMo1024', 'NCSUOganCSC440F24', 101, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q2', 3),
('FiWi1024', 'NCSUSaraCSC326F24', 102, 'Sec02', 'chap01', 'Block01', 'ACT0', 'Q1', 1);


INSERT INTO CourseTAs (course_id, course_ta_id, faculty_id) VALUES
('NCSUOganCSC440F24', 'JaWi1024', 'KeOg1024'),
('NCSUOganCSC540F24', 'LiAl0924', 'KeOg1024'),
('NCSUSaraCSC326F24', 'DaJo1024', 'SaMi1024');
