import re
import sys
import csv
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QComboBox, QTextEdit, QLabel, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class LoginWindow(QWidget):                         # class na tatawagin login window
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")                # Title ng window log in
        self.setGeometry(100, 100, 300, 100)
    
        self.users_file_path = "users_data.json"    # Path to the JSON file where user data will be stored

        # Load users from JSON file
        self.users = self.load_users_data()         # Load the users data at initialization

        self.init_ui()                              # pag set ng user interface

    def load_users_data(self):
        """Load users from a JSON file."""
        if os.path.exists(self.users_file_path):
            with open(self.users_file_path, 'r') as file:   
                return json.load(file)              # Load users data from the file
        else:
            # Return a default users dictionary if the file doesn't exist
            return {
                "admin": {"password": "password123", "role": "admin"},
                "eugene": {"password": "password123", "role": "student"}
            }

    def save_users_data(self):                       # function para sa save_users_data
        """Save users to a JSON file."""
        with open(self.users_file_path, 'w') as file:    # Buksan ang file para isulat ('w' mode) gamit ang path ng file ng mga users
            json.dump(self.users, file, indent=4)     # Save the users data to the JSON file, mag kakaroon na 4 space

    def init_ui(self):                                 # pag initialize sa user interface ng window
        layout = QVBoxLayout()                         # vertiacal lay out para sa mga widgets

        # Add Logo
        self.logo_label = QLabel(self)                  # para magpakita ng logo 
        pixmap = QPixmap("logo1.png")                   # Replace 'logo.png' with the path to your logo file
        self.logo_label.setPixmap(pixmap)               # setpixmap para sa logo
        self.logo_label.setAlignment(Qt.AlignCenter)    # para ma center ang logo
        layout.addWidget(self.logo_label)               # para ma dagdag ang logo sa layout
        
        # Login form
        form_layout = QFormLayout()                                     # QFormLayout para sa mga input fields like username and password

        self.username_input = QLineEdit(self)                           # QLineEdit para sa input na user name
        self.username_input.setPlaceholderText("Enter username")
        form_layout.addRow("Username:", self.username_input)            # addRow para magdadag nang row sa username

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)

        layout.addLayout(form_layout)                                   # addLayout para madagdag ang buong layout sa unang layout

        # Apply dark mode stylesheet to the LoginWindow                 
        self.setStyleSheet(self.get_dark_mode_stylesheet1())            # darkmode ang ang log in screen

        # Login button
        self.login_button = QPushButton("Login", self)                  # button para sa login 
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)                                          # pag set sa layout nang window 

    def login(self):                                                                        # function para sa pag login ng user
        """Validate login credentials"""
        username = self.username_input.text()
        password = self.password_input.text()

        # kung ang username ay nasa listahan ng mga user ito ay mag eexecute
        if username in self.users and self.users[username]["password"] == password:         
            self.accept_login(self.users[username]["role"], username)                       # pagtawag sa accept_login at ipasa ang role at username
        else:
            self.show_error("Invalid credentials. Please try again.")
        
    def accept_login(self, role, username):                                                         # function para sa accept_login kung
        """On successful login, open the StudentGradingSystem with the appropriate role"""
        self.main_window = StudentGradingSystem(role, username, self.users, self.users_file_path)   # para mag pasa ang role, username, self.users, self.users_file_path
        self.main_window.show()                                                                     # ito ay mag eexute kung tama lahat
        self.close()                                                                                # automatic mag sasara pag tapos mag log in

    def show_error(self, message):                      # function para sa error
        """Show error dialog"""                         
        QMessageBox.critical(self, "Error", message)    #QMEssageBOx.critical para sa conflict na mga error 

    def get_dark_mode_stylesheet1(self):            # darkmode style
        return """
            QWidget {                               
                background-color: #2E2E2E;
                color: green;
                font-weight: bold;
            }                                       
            QPushButton {
                background-color: #3A3A3A;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
            QLineEdit {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #FF6347;
            }
        """


class StudentGradingSystem(QWidget):
    def __init__(self, role, username, users, users_file_path):
        super().__init__()

        self.setWindowTitle("Student Grading System")
        self.setGeometry(100, 100, 800, 600)
        self.student_table = QTableWidget()  # Make sure it's initialized
        self.users = users  # Store users data
        self.users_file_path = users_file_path  # Store the file path for later use
        self.user_role = role  # Store the user's role
        self.username = username  # Store the student's username
        self.student_records = {}
        self.subjects = ["Math", "Science", "History", "Filipino"]
        self.is_dark_mode = False  # Default to light mode
        self.user_role = role  # Store the user's role
        
        # Initialize the users dictionary here
      
        self.init_ui()
        self.load_student_records()

    def init_ui(self):
        """Set up the user interface"""
        self.setStyleSheet(self.get_light_mode_stylesheet())  # Default to light mode

        layout = QVBoxLayout()

        # Input Form for Student
        form_layout = QFormLayout()
        self.student_name_input = QLineEdit(self)
        self.student_name_input.setPlaceholderText("Enter student name")
        form_layout.addRow("Student Name:", self.student_name_input)

        self.course_input = QLineEdit(self)
        self.course_input.setPlaceholderText("Enter course")
        form_layout.addRow("Course:", self.course_input)

        # Semester selection dropdown
        self.semester_select = QComboBox(self)
        self.semester_select.addItem("1st Semester")
        self.semester_select.addItem("2nd Semester")
        self.semester_select.addItem("3rd Semester")
        form_layout.addRow("Semester:", self.semester_select)

        self.grade_inputs = {}
        for subject in self.subjects:
            grade_input = QLineEdit(self)
            grade_input.setPlaceholderText(f"Enter {subject} grade")
            form_layout.addRow(f"{subject} Grade:", grade_input)
            self.grade_inputs[subject] = grade_input

        layout.addLayout(form_layout)

        # Button Layout
        button_layout = QHBoxLayout()

        # Disable actions for student role
        if self.user_role != "student":
            self.add_student_button = QPushButton("Add Student", self)
            self.add_student_button.clicked.connect(self.add_student)
            button_layout.addWidget(self.add_student_button)

            self.update_student_button = QPushButton("Update Student", self)
            self.update_student_button.clicked.connect(self.update_student)
            button_layout.addWidget(self.update_student_button)

            self.delete_student_button = QPushButton("Delete Student", self)
            self.delete_student_button.clicked.connect(self.delete_student)
            button_layout.addWidget(self.delete_student_button)

            self.generate_report_button = QPushButton("Generate Report", self)
            self.generate_report_button.clicked.connect(self.generate_report)
            button_layout.addWidget(self.generate_report_button)

            self.save_button = QPushButton("Save Records", self)
            self.save_button.clicked.connect(self.save_student_records)
            button_layout.addWidget(self.save_button)

            self.toggle_dark_mode_button = QPushButton("Toggle Dark Mode", self)
            self.toggle_dark_mode_button.clicked.connect(self.toggle_dark_mode)
            button_layout.addWidget(self.toggle_dark_mode_button)

            # Add the checkbox for filtering failing students
            self.filter_fail_checkbox = QCheckBox("Show only failing students", self)
            self.filter_fail_checkbox.stateChanged.connect(self.filter_fail_students)
            layout.addWidget(self.filter_fail_checkbox)

            # Search Bar
            self.search_input = QLineEdit(self)
            self.search_input.setPlaceholderText("Search student...")
            self.search_input.textChanged.connect(self.filter_students_by_name)
            layout.addWidget(self.search_input)
            
            # Add Register User UI for Admin
            self.register_user_button = QPushButton("Register New User", self)
            self.register_user_button.clicked.connect(self.show_register_form)
            button_layout.addWidget(self.register_user_button)

            layout.addLayout(button_layout)

        
        # Add Search Bar for Students to Search Their Own Record
        else:
            self.search_input = QLineEdit(self)
            self.search_input.setPlaceholderText("Enter your name to view grades...")
            self.search_input.textChanged.connect(self.filter_students_by_name)
            layout.addWidget(self.search_input)

            self.show_grades_button = QPushButton("Show My Grades", self)
            self.show_grades_button.clicked.connect(self.show_grades)
            button_layout.addWidget(self.show_grades_button)

        # Register New User Form (Visible only to Admin)
        self.register_form = self.create_register_form()
        layout.addWidget(self.register_form)  # Add the register form to the layout

        layout.addLayout(button_layout)

        # Student Table
        if self.user_role == "admin":
            self.student_table = QTableWidget(self)
            self.student_table.setColumnCount(len(self.subjects) + 5)  # Extra columns for course, semester, average, and letter grade
            self.student_table.setHorizontalHeaderLabels(["Student Name", "Course", "Semester"] + self.subjects + ["Average", "Letter Grade"])

            # Set fixed height for the table
            self.student_table.setFixedHeight(350)  # Set the height to 400px

            # Enable sorting by clicking the column header
            self.student_table.setSortingEnabled(True)                                  # to activate the sorting

            # Set column widths (you can adjust the width of each column here)
            column_widths = [150, 100, 130] + [80] * len(self.subjects) + [100, 100]    # Example widths

            for i, width in enumerate(column_widths):                                   # para sa bawat column
                self.student_table.setColumnWidth(i, width)                             
            
            # Add the table to the layout (only once)
            layout.addWidget(self.student_table)                                        # to add the ang student_table sa layout

        # Add QTextEdit widget for the report display
        self.report_text_edit = QTextEdit(self)
        self.report_text_edit.setReadOnly(True)                                         # hindi pwedeng baguhin
        layout.addWidget(self.report_text_edit)                                         # Add the report area to the layout
        
        self.setLayout(layout)                                                          # execute ang layout

    def create_register_form(self):                                             # function para sa register form
        """Create the registration form for admin to add new users."""
        register_form = QWidget(self)                                           # new widget for register form
        form_layout = QFormLayout()                                             # form layout para sa mga input fields

        self.new_username_input = QLineEdit(self)                               # QLineEdit para sa text input
        self.new_username_input.setPlaceholderText("Enter new username")
        form_layout.addRow("New Username:", self.new_username_input)

        self.new_password_input = QLineEdit(self)
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("New Password:", self.new_password_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_new_user)
        form_layout.addRow(self.register_button)

        register_form.setLayout(form_layout)
        register_form.setVisible(False)  # Initially hidden

        return register_form

    def show_register_form(self):                           # function para sa register form for admin
        """Show the registration form to the admin."""
        self.register_form.setVisible(True)                 # makikita ang register form pag true

    def save_users_data(self):                              # self isang parameter para tawagin ang save_users_data
        """Save users to a JSON file."""            
        with open(self.users_file_path, 'w') as file:       # and admin ang pwedeng mag bago sa file
            json.dump(self.users, file, indent=4)            # Save the users data to the JSON file, apat ang space

    def register_new_user(self):                                    # function para sa new user
        """Register a new user entered by the admin."""
        new_username = self.new_username_input.text().strip()
        new_password = self.new_password_input.text().strip()

        if not hasattr(self, 'users'):                              # pag print sa ng error kung walang attribute
            print("ERROR: 'users' attribute is missing")
        else:
            print("users attribute exists")

        if new_username and new_password:
            # Simulate adding the user (in practice, you would store this in a file or database)
            self.users[new_username] = {"password": new_password, "role": "student"}

            # Save the updated users dictionary to the JSON file
            self.save_users_data()
            
            QMessageBox.information(self, "Success", f"New user '{new_username}' registered successfully!")

            # Clear the form after successful registration
            self.new_username_input.clear()
            self.new_password_input.clear()
            self.register_form.setVisible(False)  # Hide the form again
        else:
            QMessageBox.warning(self, "Error", "Username and password cannot be empty!")

    def show_grades(self):
        """Show the student's grades based on their name"""
        student_name = self.search_input.text().strip()  # Get the name entered by the student

        # If the user is a student, they can only view their own data
        if self.user_role == "student":
            if student_name != self.username:  # Compare the entered name with the student's username
                self.report_text_edit.setText("This is not your data. Please enter your name to view your grades.")
                return  # Prevent further execution if the name doesn't match

        if student_name:
            student_data = self.student_records.get(student_name)  # Look up the student in records
            if student_data:
                self.display_student_grades(student_name, student_data)  # Display grades if found
            else:
                self.report_text_edit.setText("Student not found!")  # Display error if not found
        else:
            self.report_text_edit.setText("Please enter your name to view grades.")  # Display message if input is empty


        # Function to display grades for a student
    def display_student_grades(self, name, student_data):
        """Display the grades of the student"""
        report = f"Grades for {name}:\n\n"
        for semester, data in student_data.items():                                                     # mag loop sa bawat semester at mga data ng student
            grades = ", ".join([f"{subject}: {grade}" for subject, grade in data['grades'].items()])    # kunin ang mga data at gawing string
            avg_grade = sum(data['grades'].values()) / len(data['grades'])                              # calculate the grades divide how many subjects
            letter_grade = self.get_letter_grade(avg_grade)
            report += f"{semester} - {data['course']}\n"
            report += f"Grades: {grades}\n"
            report += f"Average: {avg_grade:.2f} ({letter_grade})\n\n"

        # Display the generated report in the QTextEdit widget
        self.report_text_edit.setText(report)
        
    def generate_report(self):
        """Generate and show a report"""
        report = "Student Report\n\n"
        for name, semesters in self.student_records.items():
            report += f"Student: {name}\n"
            for semester, data in semesters.items():
                grades = ", ".join([f"{subject}: {grade}" for subject, grade in data['grades'].items()])
                avg_grade = sum(data['grades'].values()) / len(data['grades'])
                letter_grade = self.get_letter_grade(avg_grade)
                report += f"{semester} - {data['course']}\n"
                report += f"Grades: {grades}\n"
                report += f"Average: {avg_grade:.2f} ({letter_grade})\n\n"

        # Display the generated report in the QTextEdit widget
        self.report_text_edit.setText(report)
   
    def filter_fail_students(self):
        """Filter and update the table to show only students with failing grades"""
        if self.filter_fail_checkbox.isChecked():
            # Filter only students with failing grades
            filtered_records = {
                name: semesters for name, semesters in self.student_records.items()
                if any(
                    any(grade < 60 for grade in semester_data['grades'].values())
                    for semester_data in semesters.values()
                )
            }
            self.update_student_table(filtered_records)
        else:
            # Show all students if the checkbox is not checked
            self.update_student_table()

    def update_student_table(self, records=None):
        """Update the student table with the given records"""
        if records is None:
            records = self.student_records
        self.student_table.setRowCount(0)

        for name, semesters in records.items():
            for semester, data in semesters.items():
                row = self.student_table.rowCount()
                self.student_table.insertRow(row)
                self.student_table.setItem(row, 0, QTableWidgetItem(name))
                self.student_table.setItem(row, 1, QTableWidgetItem(data["course"]))
                self.student_table.setItem(row, 2, QTableWidgetItem(semester))

                avg_grade = sum(data["grades"].values()) / len(data["grades"])
                letter_grade = self.get_letter_grade(avg_grade)
                self.student_table.setItem(row, len(self.subjects) + 3, QTableWidgetItem(f"{avg_grade:.2f}"))
                self.student_table.setItem(row, len(self.subjects) + 4, QTableWidgetItem(letter_grade))

                for i, subject in enumerate(self.subjects):
                    self.student_table.setItem(row, i + 3, QTableWidgetItem(str(data["grades"][subject])))              # i + 3 mag sisimula ang column na mag lagay na mga numbers

    def get_letter_grade(self, avg_grade):
        """Return the letter grade based on the average grade"""
        if avg_grade >= 90:
            return "A"
        elif avg_grade >= 80:
            return "B"
        elif avg_grade >= 70:
            return "C"
        elif avg_grade >= 60:
            return "D"
        else:
            return "F"

    def get_light_mode_stylesheet(self):
        return """
            QWidget {
                background-color: #FFFFFF;
                color: black;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                background-color: #f0f0f0;
                color: black;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #FF6347;
            }
        """
        
    def get_dark_mode_stylesheet(self):
        return """
            QWidget {
                background-color: #2E2E2E;
                color: red;
            }
            QPushButton {
                background-color: #3A3A3A;
                color: white;
                border-radius: 5px;
            }
            QTableWidget {
                background-color: #3A3A3A;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
            QLineEdit {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            /* Style for specific fields */
            QLineEdit#student_name_input {
                background-color: #FFD700;  /* SteelBlue */
                color: yellow;
            }
            QLineEdit#course_input {
                background-color: #FFD700;  /* LimeGreen */
                color: green;
            }
            QComboBox {
                background-color: #FFD700;  /* Gold */
                color: #00008B;  /* DarkBlue */
            }
            QLineEdit#math_grade_input {
                background-color: #FFD700; /* Gold */
                color: #8B4513; /* SaddleBrown */
            }
            QLineEdit#science_grade_input {
                background-color: #98FB98; /* PaleGreen */
                color: #006400; /* DarkGreen */
            }
            QLineEdit#history_grade_input {
                background-color: #ADD8E6; /* LightBlue */
                color: #00008B; /* DarkBlue */
            }
            QLineEdit#filipino_grade_input {
                background-color: #FF6347; /* Tomato */
                color: #8B0000; /* DarkRed */
            }
        """

    def get_light_mode_stylesheet(self):
        return """
            QWidget {
                background-color: #F0F0F0;
                color: green;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 3px;
            }
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #ddd;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                background-color: #fff;
                color: black;
                border-radius: 5px;
                padding: 5px;
            }
        """

    def load_student_records(self):
        """Load student records from CSV file"""
        try:
            if os.path.exists('student_records.csv'):
                with open('student_records.csv', 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header row
                    for row in reader:
                        name = row[0]
                        course = row[1]
                        semester = row[2]
                        grades = {self.subjects[i]: float(row[i + 3]) for i in range(len(self.subjects))}
                        if name not in self.student_records:
                            self.student_records[name] = {}
                        self.student_records[name][semester] = {'course': course, 'grades': grades}
                self.update_student_table()
           
        except Exception as e:
            self.show_error(f"Failed to load student records: {str(e)}")

    def save_student_records(self):
        """Save student records to CSV"""
        try:
            with open('student_records.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Student Name', 'Course', 'Semester'] + self.subjects + ['Average', 'Letter Grade'])
                for student_name, semesters in self.student_records.items():
                    for semester, data in semesters.items():
                        row = [student_name, data['course'], semester] + list(data['grades'].values())
                        
                        # Calculate the average grade
                        grades = data['grades'].values()
                        avg_grade = sum(grades) / len(grades)
                        row.append(f"{avg_grade:.2f}")  # Add average grade to the row
                    
                        # Get the letter grade
                        letter_grade = self.get_letter_grade(avg_grade)
                        row.append(letter_grade)  # Add letter grade to the row
        
                        writer.writerow(row)
            QMessageBox.information(self, "Success", "Student records have been saved.")
        except Exception as e:
            self.show_error(f"Failed to save student records: {str(e)}")

    def update_student_table(self, filtered_records=None):
        """Update the student table to reflect the current records, sorted by average grade"""
        self.student_table.setRowCount(0)

        # Use filtered records if provided, otherwise use all student records
        records_to_display = filtered_records if filtered_records else self.student_records

        # Sort students by their average grade across all semesters
        sorted_students = []

        for student_name, semesters in records_to_display.items():
            total_grades = []
            for semester, data in semesters.items():
                grades = data['grades']
                total_grades.append(sum(grades.values()) / len(grades))  # average grade per semester

            # Calculate the overall average for the student
            overall_average = sum(total_grades) / len(total_grades) if total_grades else 0
            sorted_students.append((student_name, semesters, overall_average))

        # Now sort the students based on the overall average
        sorted_students.sort(key=lambda x: x[2], reverse=True)

        for student_name, semesters, _ in sorted_students:
            for semester, data in semesters.items():
                row_position = self.student_table.rowCount()
                self.student_table.insertRow(row_position)
                self.student_table.setItem(row_position, 0, QTableWidgetItem(student_name))
                self.student_table.setItem(row_position, 1, QTableWidgetItem(data['course']))
                self.student_table.setItem(row_position, 2, QTableWidgetItem(semester))

                grades = data['grades']
                total_grade = 0
                for i, subject in enumerate(self.subjects):
                    grade = grades[subject]
                    grade_item = QTableWidgetItem(str(grade))
                    self.student_table.setItem(row_position, i + 3, grade_item)
                    total_grade += grade

                    # Highlight failing students in red
                    if grade < 60:
                        grade_item.setBackground(Qt.red)
                    else:
                        grade_item.setBackground(Qt.green)

                avg_grade = total_grade / len(self.subjects)
                avg_item = QTableWidgetItem(f"{avg_grade:.2f}")
                self.student_table.setItem(row_position, len(self.subjects) + 3, avg_item)

                # Convert average grade to letter grade
                letter_grade = self.get_letter_grade(avg_grade)
                self.student_table.setItem(row_position, len(self.subjects) + 4, QTableWidgetItem(letter_grade))

    def get_letter_grade(self, average):
        """Convert average grade to letter grade"""
        if average >= 90:
            return "A"
        elif average >= 87:
            return "A-"
        elif average >= 83:
            return "B+"
        elif average >= 80:
            return "B"
        elif average >= 77:
            return "B-"
        elif average >= 73:
            return "C+"
        elif average >= 70:
            return "C"
        elif average >= 67:
            return "C-"
        elif average >= 63:
            return "D+"
        elif average >= 60:
            return "D"
        else:
            return "F"

    def add_student(self):
        """Add a student to the student records"""
        name = self.student_name_input.text()
        course = self.course_input.text()
        semester = self.semester_select.currentText()

        # Validate name: only letters and spaces allowed
        if not name or not re.match("^[A-Za-z ]+$", name):
            self.show_error("Please enter a valid student name (letters and spaces only).")
            return
        
        if not name or not course:
            self.show_error("Please provide a valid student name and course.")
            return
        
        grades = {}

        for subject in self.subjects:
            grade_input = self.grade_inputs[subject].text()

            # Check if the grade input is a valid number
            try:
                grade = float(grade_input)
                grades[subject] = grade
            except ValueError:
                self.show_error(f"Please enter a valid number for the grade in {subject}.")
                return

        # Check if the student already has a record for the same semester
        if name in self.student_records and semester in self.student_records[name]:
            self.show_error(f"Student '{name}' already has a record for {semester}.")
            return

        if name not in self.student_records:
            self.student_records[name] = {}
        
        self.student_records[name][semester] = {'course': course, 'grades': grades}
        self.update_student_table()
        self.clear_form()

    def update_student(self):
        """Update student information"""
        name = self.student_name_input.text()
        if name not in self.student_records:
            self.show_error(f"Student '{name}' not found.")
            return

        semester = self.semester_select.currentText()
        grades = {subject: float(self.grade_inputs[subject].text()) for subject in self.subjects}
        course = self.course_input.text()

        # Check if the student exists for the given semester
        if name in self.student_records and semester in self.student_records[name]:
            # Allow update even if the semester is the same
            self.student_records[name][semester] = {'course': course, 'grades': grades}
            self.update_student_table()
            self.clear_form()
            QMessageBox.information(self, "Success", f"Student '{name}' updated for {semester}.")
            return

        # If the student doesn't already have a record for this semester, allow adding a new semester record
        self.student_records[name][semester] = {'course': course, 'grades': grades}
        self.update_student_table()
        self.clear_form()
        QMessageBox.information(self, "Success", f"New record added for {name} in {semester}.")
        
        # Check if the semester already exists for this student
        if semester in self.student_records[name]:
            self.show_error(f"Student '{name}' already has a record for {semester}. You cannot update the same semester.")
            return

        self.student_records[name][semester] = {'course': course, 'grades': grades}
        self.update_student_table()
        self.clear_form()

    def delete_student(self):
        """Delete student record"""
        name = self.student_name_input.text()

        # Confirm deletion with the user
        reply = QMessageBox.question(
            self,
            'Confirm Deletion',
            f"Are you sure you want to delete the student '{name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if name in self.student_records:
                del self.student_records[name]
                self.update_student_table()
                self.clear_form()
            else:
                self.show_error(f"Student '{name}' not found.")

    def filter_students_by_name(self):
        """Filter students by name"""
        # Ensure you're checking the role of the user
        if self.user_role == "admin":
            search_term = self.search_input.text()
            filtered_records = {
                name: semesters for name, semesters in self.student_records.items() if search_term in name.lower()
            }
            self.update_student_table(filtered_records)  # Update the table with filtered records
        elif self.user_role == "student":
            # Student should only be able to search for their own name, not other students
            student_name = self.search_input.text().strip()
            if student_name != self.username:           # If the name doesn't match, show an error
                self.report_text_edit.setText("This is not your data. Please enter your name to view your grades.")
            else:
                self.show_grades()              # Show grades if the name matches their username
            
    def show_error(self, message):
        """Show error message in a pop-up"""
        QMessageBox.critical(self, "Error", message)

    def clear_form(self):
        """Clear all form inputs"""
        self.student_name_input.clear()                     # mag cleclear ang input name
        self.course_input.clear()
        self.semester_select.setCurrentIndex(0)
        for grade_input in self.grade_inputs.values():
            grade_input.clear()

    def toggle_dark_mode(self):
        """Toggle between dark and light modes"""
        if self.is_dark_mode:
            self.setStyleSheet(self.get_light_mode_stylesheet())
        else:
            self.setStyleSheet(self.get_dark_mode_stylesheet())
        self.is_dark_mode = not self.is_dark_mode

  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
