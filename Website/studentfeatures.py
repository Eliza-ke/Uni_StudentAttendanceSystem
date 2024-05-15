from flask import jsonify, session,redirect, render_template, request, url_for
from flask_login import current_user
from datetime import datetime

from Website.models import Attendance, Period, Student, Year
from Website.config import db, create_app
from werkzeug.utils import secure_filename
import os
        
app = create_app()

def attendance():
    user_id = session.get('student_id')
    current_user = Student.query.filter_by(id= user_id).first()
    current_date = str(datetime.now().date())
    periods = Period.query.all()
    
    allyear = Year.query.all()
    years = {year.id: year.year_name for year in allyear}
    
    if request.method == 'POST':
        yearid = request.form.get("yearid")
        period = request.form.get("period")
        status = request.form.get("status")
        leaveletter = request.form.get("leaveletter")

        if not leaveletter:
            leaveletter = "-"
        if not period: 
            return jsonify(success=False, message='Please select period timetable')
        elif not status:
            return jsonify(success=False, message='Please select present or absent')     
            
        attendance_exists = Attendance.query.filter_by(period_id=period, date=current_date, student_id=user_id).first()
        if attendance_exists:
            return jsonify(success=False, message='You already record attendance')
        else:
            new_attendance = Attendance(date=current_date, leave_letter=leaveletter, status=status, student_id=user_id, period_id = period, year_id=yearid)
            db.session.add(new_attendance)
            db.session.commit()
            return jsonify(success=True, message="Attendance Recorded Successfully")

    return render_template('studentattendance.html', user=current_user, current_date=current_date, periods=periods, years=years) 


# student profile
UPLOAD_FOLDER = 'Website/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def studentprofile():
    user_id = session.get('student_id')
    student = Student.query.get(user_id)
    student_year = Year.query.get(student.year).year_name
    years = Year.query.all()
    if request.method == 'POST':
        if 'profileImage' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['profileImage']
        
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                student.profile = filename
                db.session.commit()
                print("successfully uploaded")
                return redirect(url_for('studentProfile'))

    return render_template('studentProfile.html', user=student, student_year=student_year, years=years)


def updateProfile():
    user_id = session.get('student_id')
    current_user = Student.query.filter_by(id= user_id).first()
    student = Student.query.get(user_id)
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        year = request.form.get('year')
        batch = request.form.get('batch')
        phone = request.form.get('phone')
        
        if len(email) < 4:
            return jsonify(success=False, message='Invalid email')
        elif len(name) < 2:
            return jsonify(success=False, message='Name must be longer than 2 letters')
        elif len(batch) < 2:
            return jsonify(success=False, message='Batch must be longer than 2 letters')
        elif len(phone) < 5:
            return jsonify(success=False, message='Phone number must be greater than 5')
        else:
            student.email = email
            student.name = name
            student.year = year
            student.batch = batch
            student.phone = phone
            db.session.commit()
            print("updated successfully")
            return jsonify(success=True, redirect=url_for('studentProfile'))