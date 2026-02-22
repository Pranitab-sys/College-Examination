show databases;
CREATE DATABASE college_exam_db;
USE college_exam_db;
CREATE TABLE student (
  student_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  roll_no VARCHAR(20) UNIQUE,
  course VARCHAR(30),
  semester INT CHECK (semester BETWEEN 1 AND 6)
);
CREATE TABLE subject (
  subject_id INT AUTO_INCREMENT PRIMARY KEY,
  subject_name VARCHAR(50),
  semester INT,
  max_marks INT DEFAULT 100
);
CREATE TABLE exam (
  exam_id INT AUTO_INCREMENT PRIMARY KEY,
  exam_type VARCHAR(20),
  exam_year YEAR
);
CREATE TABLE marks (
  marks_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT,
  subject_id INT,
  exam_id INT,
  marks_obtained INT CHECK (marks_obtained BETWEEN 0 AND 100),
  FOREIGN KEY (student_id) REFERENCES student(student_id),
  FOREIGN KEY (subject_id) REFERENCES subject(subject_id),
  FOREIGN KEY (exam_id) REFERENCES exam(exam_id)
);
INSERT INTO student (name, roll_no, course, semester)
VALUES 
('Amit Patil','IT401','BSc IT',4),
('Neha Sharma','IT402','BSc IT',4);
INSERT INTO subject (subject_name, semester)
VALUES
('DBMS',4),
('Operating System',4);
INSERT INTO exam (exam_type, exam_year)
VALUES ('End Semester',2025);
INSERT INTO marks (student_id, subject_id, exam_id, marks_obtained)
VALUES
(1,1,1,78),
(1,2,1,85),
(2,1,1,66),
(2,2,1,72);
DELIMITER //

CREATE PROCEDURE generate_result()
BEGIN
  SELECT 
    s.roll_no,
    s.name,
    SUM(m.marks_obtained) AS total_marks,
    ROUND(SUM(m.marks_obtained)/COUNT(m.subject_id),2) AS percentage,
    CASE
      WHEN SUM(m.marks_obtained)/COUNT(m.subject_id) >= 75 THEN 'Distinction'
      WHEN SUM(m.marks_obtained)/COUNT(m.subject_id) >= 60 THEN 'First Class'
      WHEN SUM(m.marks_obtained)/COUNT(m.subject_id) >= 40 THEN 'Pass'
      ELSE 'Fail'
    END AS result
  FROM student s
  JOIN marks m ON s.student_id = m.student_id
  GROUP BY s.student_id;
END //

DELIMITER ;
CALL generate_result();
DELIMITER //

CREATE TRIGGER validate_marks
BEFORE INSERT ON marks
FOR EACH ROW
BEGIN
  IF (SELECT semester FROM student WHERE student_id = NEW.student_id) 
     != 
     (SELECT semester FROM subject WHERE subject_id = NEW.subject_id)
  THEN
     SIGNAL SQLSTATE '45000'
     SET MESSAGE_TEXT = 'Semester mismatch between student and subject';
  END IF;
END //

DELIMITER ;
CREATE VIEW result_view AS
SELECT 
  s.roll_no,
  s.name,
  sub.subject_name,
  m.marks_obtained
FROM student s
JOIN marks m ON s.student_id = m.student_id
JOIN subject sub ON m.subject_id = sub.subject_id;
SELECT * FROM result_view;
START TRANSACTION;

INSERT INTO marks (student_id, subject_id, exam_id, marks_obtained)
VALUES (1, 1, 1, 78);

COMMIT;

show tables;
SHOW PROCEDURE STATUS WHERE Db = 'college_exam_db';

SHOW TRIGGERS;
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SELECT * FROM student;
SELECT * FROM subject;
SELECT * FROM exam;
SELECT * FROM marks;

USE college_exam_db;
SELECT * FROM student;
DESCRIBE student;
ALTER TABLE student 
MODIFY roll_no VARCHAR(20) NOT NULL;
ALTER TABLE student AUTO_INCREMENT = 3;
SELECT * FROM marks
WHERE marks_id = 5;
CREATE OR REPLACE VIEW result_view AS
SELECT 
    s.student_id,
    s.roll_no,
    s.name,

    SUM(m.marks_obtained) AS total_marks,

    ROUND(AVG(m.marks_obtained), 2) AS percentage,

    CASE
        WHEN AVG(m.marks_obtained) >= 40 THEN 'PASS'
        ELSE 'FAIL'
    END AS result,

    CASE
        WHEN AVG(m.marks_obtained) >= 75 THEN 'DISTINCTION'
        WHEN AVG(m.marks_obtained) >= 60 THEN 'FIRST CLASS'
        WHEN AVG(m.marks_obtained) >= 50 THEN 'SECOND CLASS'
        WHEN AVG(m.marks_obtained) >= 40 THEN 'PASS CLASS'
        ELSE 'FAIL'
    END AS class

FROM student s
JOIN marks m ON s.student_id = m.student_id

GROUP BY s.student_id, s.roll_no, s.name;

ALTER TABLE student DROP PRIMARY KEY;
SELECT 
    ROW_NUMBER() OVER (ORDER BY student_id) AS Sr_No,
    student_id,
    name,
    roll_no,
    course,
    semester
FROM student;
show tables;
select * from student;
select * from subject;
select * from exam;
select * from marks;

CALL generate_result();
SHOW TRIGGERS;

