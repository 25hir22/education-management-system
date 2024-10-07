from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
app.secret_key = 'your_secret_key'


# MySQL Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # replace with your MySQL username
        password="root",  # replace with your MySQL password
        database="education_management_copy"  # using the new database name
    )
    return conn
@app.route('/search_student', methods=['GET'])
def search_student():
    query = request.args.get('query')
    results = []  # Initialize results as an empty list


    if query:  # Check if there is a query
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Perform search query to find students matching the search term
            cursor.execute("SELECT * FROM students WHERE name LIKE %s OR reg_no LIKE %s", (f'%{query}%', f'%{query}%'))
            results = cursor.fetchall()  # Fetch all matching records
        except Error as e:
            flash(f"Error occurred: {e}", 'error')
        finally:
            cursor.close()
            conn.close()


    return render_template('search_results.html', students=results)


@app.route('/')
def home():
    return render_template('index.html')


# Route to handle student registration
@app.route('/register_student', methods=['POST'])
def register_student():
    reg_no = request.form['reg_no']
    name = request.form['name']
    course = request.form['course']
   
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
       
        # Insert new student into students table
        cursor.execute("INSERT INTO students (reg_no, name, course) VALUES (%s, %s, %s)", (reg_no, name, course))
        conn.commit()
        flash('Student registered successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f"Error occurred: {e}", 'error')
    finally:
        cursor.close()
        conn.close()


    return redirect(url_for('home'))


# Route to handle course enrollment
@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    reg_no = request.form['reg_no']
    course_name = request.form['course_name']


    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        # Check if the student exists
        cursor.execute("SELECT * FROM students WHERE reg_no = %s", (reg_no,))
        student = cursor.fetchone()
        if student is None:
            flash(f'Student with reg_no {reg_no} does not exist', 'error')
            return redirect(url_for('home'))


        # Insert data into student_courses table
        cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (%s, (SELECT course_id FROM courses WHERE course_name = %s))", (reg_no, course_name))
        conn.commit()
        flash('Course enrolled successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f"Error occurred: {e}", 'error')
    finally:
        cursor.close()
        conn.close()


    return redirect(url_for('home'))


# Route to handle attendance submission
@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    reg_no = request.form['reg_no']
    sem_no = request.form['sem_no']
    date = request.form['date']
    status = request.form['status']


    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        # Check if the student exists
        cursor.execute("SELECT * FROM students WHERE reg_no = %s", (reg_no,))
        student = cursor.fetchone()
        if student is None:
            flash(f'Student with reg_no {reg_no} does not exist', 'error')
            return redirect(url_for('home'))


        # Insert data into attendance table
        cursor.execute("INSERT INTO attendance (reg_no, sem_no, date, status) VALUES (%s, %s, %s, %s)", (reg_no, sem_no, date, status))
        conn.commit()
        flash('Attendance added successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f"Error occurred: {e}", 'error')
    finally:
        cursor.close()
        conn.close()


    return redirect(url_for('home'))


# Route to handle co-curricular activity submission
@app.route('/add_activity', methods=['POST'])
def add_activity():
    reg_no = request.form['reg_no']
    activity_name = request.form['activity_name']


    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        # Check if the student exists
        cursor.execute("SELECT * FROM students WHERE reg_no = %s", (reg_no,))
        student = cursor.fetchone()
        if student is None:
            flash(f'Student with reg_no {reg_no} does not exist', 'error')
            return redirect(url_for('home'))


        # Insert data into co-curricular activities table
        cursor.execute("INSERT INTO co_curricular_activities (reg_no, activity_name) VALUES (%s, %s)", (reg_no, activity_name))
        conn.commit()
        flash('Co-curricular activity added successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f"Error occurred: {e}", 'error')
    finally:
        cursor.close()
        conn.close()


    return redirect(url_for('home'))


# Route to handle IT events submission
@app.route('/add_it_event', methods=['POST'])
def add_it_event():
    reg_no = request.form['reg_no']
    event_name = request.form['event_name']
    event_type = request.form['event_type']  # e.g., 'Inter-University' or 'Intra-University'


    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        # Check if the student exists
        cursor.execute("SELECT * FROM students WHERE reg_no = %s", (reg_no,))
        student = cursor.fetchone()
        if student is None:
            flash(f'Student with reg_no {reg_no} does not exist', 'error')
            return redirect(url_for('home'))


        # Insert data into IT events table
        cursor.execute("INSERT INTO it_events (reg_no, event_name, event_type) VALUES (%s, %s, %s)", (reg_no, event_name, event_type))
        conn.commit()
        flash('IT Event added successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f"Error occurred: {e}", 'error')
    finally:
        cursor.close()
        conn.close()


    return redirect(url_for('home'))


# Route to handle CGPA addition
@app.route('/add_cgpa', methods=['POST'])
def add_cgpa():
    reg_no = request.form['reg_no']
    cgpa = request.form['cgpa']


    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        # Check if the student exists
        cursor.execute("SELECT * FROM students WHERE reg_no = %s", (reg_no,))
        student = cursor.fetchone()
        if student is None:
            flash(f'Student with reg_no {reg_no} does not exist', 'error')
            return redirect(url_for('home'))


        # Insert data into CGPA table
        cursor.execute("INSERT INTO cgpa (reg_no, cgpa) VALUES (%s, %s)", (reg_no, cgpa))
        conn.commit()
        flash('CGPA added successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f"Error occurred: {e}", 'error')
    finally:
        cursor.close()
        conn.close()


    return redirect(url_for('home'))


# Route to calculate score and performance metrics
@app.route('/calculate_performance', methods=['POST'])
def calculate_performance():
    reg_no = request.form['reg_no']
   
    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        # Calculate attendance score
        cursor.execute("""
            SELECT COUNT(*) FROM attendance WHERE reg_no = %s AND status = 'Present'
        """, (reg_no,))
        attendance_count = cursor.fetchone()[0]


        # Calculate total attendance
        cursor.execute("""
            SELECT COUNT(*) FROM attendance WHERE reg_no = %s
        """, (reg_no,))
        total_attendance = cursor.fetchone()[0]


        attendance_score = (attendance_count / total_attendance * 100) if total_attendance > 0 else 0


        # Calculate co-curricular activities score
        cursor.execute("""
            SELECT COUNT(*) FROM co_curricular_activities WHERE reg_no = %s
        """, (reg_no,))
        co_curricular_count = cursor.fetchone()[0]
       
        # Calculate IT events score
        cursor.execute("""
            SELECT COUNT(*) FROM it_events WHERE reg_no = %s
        """, (reg_no,))
        it_events_count = cursor.fetchone()[0]


        # Get CGPA score
        cursor.execute("""
            SELECT cgpa FROM cgpa WHERE reg_no = %s
        """, (reg_no,))
        cgpa = cursor.fetchone()
        cgpa_score = cgpa[0] if cgpa else 0


        # Calculate final performance score
        final_score = (float(attendance_score) +
               (float(co_curricular_count) * 5) +
               (float(it_events_count) * 5) +
               (float(cgpa_score) * 10)) / 100


        # Prepare performance metrics
        performance_metrics = {
            "attendance_score": attendance_score,
            "co_curricular_count": co_curricular_count,
            "it_events_count": it_events_count,
            "cgpa": cgpa_score,
            "final_score": final_score
        }
       
        flash(f"Performance Metrics for {reg_no}: {performance_metrics}", 'info')
    except Error as e:
        flash(f"Error occurred: {e}", 'error')
    finally:
        cursor.close()
        conn.close()


    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
