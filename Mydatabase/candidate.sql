
CREATE DATABASE job_applications;

USE job_applications;

CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    position VARCHAR(100),
    resume_path VARCHAR(255)
);
show tables;
select * from applications;