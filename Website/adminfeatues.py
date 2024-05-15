from flask import jsonify, redirect, render_template, request, session, url_for
from Website.models import Admin, Attendance, Period, Student, Year
from Website.config import create_app, db
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = create_app()

# student information
def adminstudentinfo():
    students = Student.query.all()
    allyears = Year.query.all()
    years = {year.id: year.year_name for year in allyears}
    student_year = ""
    return render_template("adminstudentInfo.html", students=students, allyears=allyears, years = years, student_year=student_year)
  
def adminfilterbyyear(yearid):
    students = Student.query.filter_by(year=yearid).all()
    allyears = Year.query.all()
    years = {year.id: year.year_name for year in allyears}
    student_year = Year.query.get(yearid).year_name
    return render_template("adminstudentInfo.html", students=students, allyears=allyears, years = years, student_year=student_year)

# year information
def yearinfo():
    if request.method == 'POST':
        yearvalue = request.form.get('year')
        year_info = Year.query.filter_by(year_name=yearvalue).first()
        if year_info:
            return jsonify(success=False, message='Data already exist')
        elif len(yearvalue) < 1:
            return jsonify(success=False, message='Data is empty')
        else:
            new_year = Year(year_name=yearvalue)
            db.session.add(new_year)
            db.session.commit()
            return jsonify(success=True, redirect=url_for('adminyearInfo'))

    years = Year.query.all()
    return render_template("adminyearInfo.html", years=years)


def updateyearinfo(yid):
    year = Year.query.get(yid)

    if year:
        if request.method == 'POST':
            yearvalue = request.form.get('year')
            if len(yearvalue) < 1:
                return jsonify(fail=True, message='Invalid Information')
            else:
                year.year_name = yearvalue
                db.session.commit()
                print("updated successfully in flask database")

                return jsonify(success=True, redirect=url_for('adminyearInfo'))

    return jsonify(success=True, redirect=url_for('adminyearInfo'))


def deleteyearinfo(yid):
    deleteyear = Year.query.get(yid)
    if deleteyear:
        students = Student.query.filter_by(year=yid)
        attendances = Attendance.query.filter_by(year_id=yid)
        
        for student in students:
            db.session.delete(student)
            db.session.commit()
        
        for attendance in attendances:
            db.session.delete(attendance)
            db.session.commit()
            
        db.session.delete(deleteyear)
        db.session.commit()

    return render_template("adminyearInfo.html", years=Year.query.all())

# period information
def adminperiodinfo():
    periods = Period.query.all()

    if request.method == 'POST':
        period_name = request.form.get('period_name')
        period_time = request.form.get('period_time')
        period_info = Period.query.filter_by(period_name=period_name).first()
        if period_info:
            return jsonify(success=False, message='Data already exist')
        elif len(period_name) < 2:
            return jsonify(success=False, message='Invalid period name')
        elif len(period_time) < 2:
            return jsonify(success=False, message='Invalid period time')
        else:
            new_period = Period(period_name=period_name,
                                period_time=period_time)
            db.session.add(new_period)
            db.session.commit()
            return jsonify(success=True, redirect=url_for('adminperiodInfo'))

    return render_template("adminperiodInfo.html", periods=periods)


def updateperiodinfo(yid):
    period = Period.query.get(yid)

    if period:
        if request.method == 'POST':
            period_name = request.form.get('periodName')
            period_time = request.form.get('periodTime')
            if len(period_name) < 1:
                return jsonify(fail=True, message='Invalid period name')
            elif len(period_time) < 1:
                return jsonify(fail=True, message='Invalid period time')
            else:
                period.period_name = period_name
                period.period_time = period_time
                db.session.commit()
                print("updated successfully in flask database")

                return jsonify(success=True, redirect=url_for('adminperiodInfo'))

    return jsonify(success=True, redirect=url_for('adminperiodInfo'))

def deleteperiodinfo(pid):
    deleteperiod = Period.query.get(pid)
    if deleteperiod:
        attendances = Attendance.query.filter_by(period_id=pid)
        for attendance in attendances:
            db.session.delete(attendance)
            db.session.commit()
            
        db.session.delete(deleteperiod)
        db.session.commit()

    return render_template("adminperiodInfo.html", periods=Period.query.all())



# admin profile
UPLOAD_FOLDER = 'Website/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
# admin profile upload           
def adminprofile():
    adminId = session.get('admin_id')
    admin = Admin.query.get(adminId)
    
    if request.method == 'POST':
        if 'profileImage' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['profileImage']
        
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                admin.profile = filename
                db.session.commit()

                admindict = {
                    "admin_id": admin.id,
                    "admin_name": admin.name,
                    "admin_email": admin.email,
                    "admin_profile": admin.profile,
                    "admin_rolecode": admin.roleCode,
                }
                session['admin'] = admindict
                print("profile image uploaded successfully")
                return redirect(url_for('adminProfile'))

    return render_template('adminProfile.html', user=admin)

def updateadminprofile():
    user_id = session.get('admin_id')
    current_user = Admin.query.filter_by(id= user_id).first()
    admin = Admin.query.get(user_id)
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        if len(email) < 4:
            return jsonify(success=False, message='Invalid email')
        elif len(name) < 2:
            return jsonify(success=False, message='Name must be longer than 2 letters')
        elif len(phone) < 5:
            return jsonify(success=False, message='Phone number must be greater than 5')
        else:
            admin.email = email
            admin.name = name
            admin.phone = phone
            db.session.commit()
            
            myadmin = Admin.query.filter_by(email=email).first()

            admindict = {
                "admin_id": myadmin.id,
                "admin_name": myadmin.name,
                "admin_email": myadmin.email,
                "admin_profile": myadmin.profile,
                "admin_rolecode": myadmin.roleCode,
            }
            session['admin'] = admindict
            return jsonify(success=True, redirect=url_for('adminProfile'))
        
# faculty 
def adminfacultyinfo():
    code = "F1001" # faculty code
    admins = Admin.query.filter_by(roleCode=code).all()
    return render_template("adminfacultyInfo.html", admins = admins)


def deletefacultyinfo(fid):
    deletefaculty = Admin.query.get(fid)
    code = "F1001"
    if deletefaculty:
        db.session.delete(deletefaculty)
        db.session.commit()

    admins = Admin.query.filter_by(roleCode=code).all()
    return render_template("adminfacultyInfo.html", admins = admins)

# attendance for each student
def eachattendance(stid):
    
    student = Student.query.get(stid)
    
    allyears = Year.query.all()
    years = {year.id: year.year_name for year in allyears}
    
    allperiod = Period.query.all()
    period = {period.id: period.period_name for period in allperiod}
    
    # piechart
    distinct_attendances = db.session.query(Attendance.status).distinct().all()
    attendance_counts = {}
    for attend_status in distinct_attendances:
        # print(attend_status[0])
        count = Attendance.query.filter_by(status=attend_status[0], student_id=stid).count()
        attendance_counts[attend_status[0]] = count
    
    statuslabels = list(attendance_counts.keys())
    statusvalues = list(attendance_counts.values())
    
    # filter by input date
    if request.method == 'POST':
        customdate = request.form.get('customdate')
        
        if customdate:
            # piechart
            distinct_attendances = db.session.query(Attendance.status).distinct().all()
            attendance_counts = {}
            for attend_status in distinct_attendances:
                # print(attend_status[0])
                count = Attendance.query.filter_by(status=attend_status[0], student_id=stid, date=customdate).count()
                attendance_counts[attend_status[0]] = count
            
            statuslabels = list(attendance_counts.keys())
            statusvalues = list(attendance_counts.values())
            
            attendances = Attendance.query.filter_by(student_id=stid,date=customdate).order_by(Attendance.id.desc()).all()
            return render_template("eachAttendance.html", student = student, years=years, period=period, attendances=attendances, datevalue=customdate, statuslabels=statuslabels, statusvalues=statusvalues)
    
    attendances = Attendance.query.filter_by(student_id=stid).order_by(Attendance.id.desc()).all()
    return render_template("eachAttendance.html", student = student, years=years, period=period, attendances=attendances, datevalue="", statuslabels=statuslabels, statusvalues=statusvalues)

# filter today date in each attendance
def filterbytoday(stid):
    
    student = Student.query.get(stid)
    
    allyears = Year.query.all()
    years = {year.id: year.year_name for year in allyears}
    
    allperiod = Period.query.all()
    period = {period.id: period.period_name for period in allperiod}
    
    date = datetime.now().date()
    
    # for piechart
    distinct_attendances = db.session.query(Attendance.status).distinct().all()
    attendance_counts = {}
    for attend_status in distinct_attendances:
        count = Attendance.query.filter_by(status=attend_status[0], student_id=stid, date=date).count()
        attendance_counts[attend_status[0]] = count
    
    statuslabels = list(attendance_counts.keys())
    statusvalues = list(attendance_counts.values())
    
    # filter by input date
    if request.method == 'POST':
        customdate = request.form.get('customdate')
        
        if customdate:
            # for piechart with filter by input date
            distinct_attendances = db.session.query(Attendance.status).distinct().all()
            attendance_counts = {}
            for attend_status in distinct_attendances:
                count = Attendance.query.filter_by(status=attend_status[0], student_id=stid, date=customdate).count()
                attendance_counts[attend_status[0]] = count
            
            statuslabels = list(attendance_counts.keys())
            statusvalues = list(attendance_counts.values())
            
            attendances = Attendance.query.filter_by(student_id=stid,date=date).order_by(Attendance.id.desc()).all()
            return render_template("eachAttendance.html", student = student, years=years, period=period, attendances=attendances, datevalue=customdate, statuslabels=statuslabels, statusvalues=statusvalues)
    
    attendances = Attendance.query.filter_by(student_id=stid,date=date).order_by(Attendance.id.desc()).all()
    return render_template("eachAttendance.html", student = student, years=years, period=period, attendances=attendances, datevalue="", statuslabels=statuslabels, statusvalues=statusvalues)

# no logined student
def notloginedstudent():
    
    allstudents = Student.query.all()
    allperiod = Period.query.all()
    
    allyears = Year.query.all()
    years = {year.id: year.year_name for year in allyears}
    
    # today date
    date = datetime.now().date()
    
    students = {}
    for eachstudent in allstudents: 
        student_period = []
        for period in allperiod:
            attendances = Attendance.query.filter_by(student_id=eachstudent.id,date=date,period_id=period.id).all()
            if not attendances:
                student_period.append(period.period_name)
        if student_period:
            students[eachstudent] = student_period
    
    return render_template("notLoginedStudent.html", students = students, years=years, periods= allperiod, allyears=allyears, selectedyear = "")

# no logined students filtered by year
def notloginedstudentbyyear(yrid):
    
    allstudents = Student.query.filter_by(year=yrid).all()
    
    allyears = Year.query.all()
    years = {year.id: year.year_name for year in allyears}
    selectedyear = Year.query.get(yrid).year_name
    allperiod = Period.query.all()
    # today date
    date = datetime.now().date()

    students = {}
    for eachstudent in allstudents: 
        student_period = []
        for period in allperiod:
            attendances = Attendance.query.filter_by(student_id=eachstudent.id,date=date,period_id=period.id).all()
            if not attendances:
                student_period.append(period.period_name)
        if student_period:
            students[eachstudent] = student_period
                
    return render_template("notLoginedStudent.html", students = students, years=years, periods= allperiod, allyears=allyears, selectedyear = selectedyear)    


def setabsent():
        
    stuid = request.args.get('id')
    yearid = request.args.get('yearid')
    allstudents = Student.query.all()
    allperiod = Period.query.all()
    
    # today date
    date = datetime.now().date()
    
    allyears = Year.query.all()
    years = {year.id: year.year_name for year in allyears}
    
    for period in allperiod:
        result = Attendance.query.filter_by(student_id=stuid,date=date,period_id=period.id).all()
        if not result:
            new_attendance = Attendance(date=date, leave_letter="-", status="absent", student_id=stuid, year_id=yearid, period_id = period.id)
            db.session.add(new_attendance)
            db.session.commit()
                
    selectedyear=""
    students = {}
    for eachstudent in allstudents: 
        student_period = []
        for period in allperiod:
            attendances = Attendance.query.filter_by(student_id=eachstudent.id,date=date,period_id=period.id).all()
            if not attendances:
                student_period.append(period.period_name)
        if student_period:
            students[eachstudent] = student_period
    
    return render_template("notLoginedStudent.html", students = students, years=years, periods= allperiod, allyears=allyears, selectedyear = selectedyear) 

# show attendance and filter with input date
def adminattendanceinfo():
    
    allstudents = Student.query.all()
    students = {student.id: student.name for student in allstudents}
    
    allyear = Year.query.all()
    years = {year.id: year.year_name for year in allyear}
    
    allperiod = Period.query.all()
    period = {period.id: period.period_name for period in allperiod}

    # filter by input date
    if request.method == 'POST':
        customdate = request.form.get('customdate')
        attendances = Attendance.query.filter_by(date=customdate).order_by(Attendance.id.desc()).all()
        return render_template("adminattendanceInfo.html", attendances = attendances, years= years, period=period, students=students, allyears = allyear, datevalue=customdate, student_year="")
        
    attendances = Attendance.query.order_by(Attendance.id.desc()).all()
        
    return render_template("adminattendanceInfo.html", attendances = attendances, years= years, period=period, students=students, allyears = allyear, datevalue="", student_year="")
    
# show attendance and filter by year with input date  
def adminattendancefilterbyyear(yrrid):
    
    allstudents = Student.query.all()
    students = {student.id: student.name for student in allstudents}
    
    allyear = Year.query.all()
    years = {year.id: year.year_name for year in allyear}

    allperiod = Period.query.all()
    period = {period.id: period.period_name for period in allperiod}
    student_year = Year.query.get(yrrid).year_name
    
    # filter by input date
    if request.method == 'POST':
        customdate = request.form.get('customdate')
        
        attendances = Attendance.query.filter_by(date=customdate, year_id=yrrid).order_by(Attendance.id.desc()).all()
        return render_template("adminattendanceInfo.html", attendances = attendances, years= years, period=period, students=students, allyears = allyear, datevalue=customdate, student_year=student_year)
        
    attendances = Attendance.query.filter_by(year_id=yrrid).order_by(Attendance.id.desc()).all()
    return render_template("adminattendanceInfo.html", attendances = attendances, years= years, period=period, students=students, allyears = allyear, datevalue="", student_year=student_year)


def admindashboard():
    
    # present count based on period
    periods = Period.query.all()
    period_counts = {period.id: 0 for period in periods}
    period_names = {period.id: period.period_name for period in periods}
    period_length = len(period_names) # length

    present_attendances = Attendance.query.filter_by(status='present').all()

    for attendance in present_attendances:
        period_counts[attendance.period_id] += 1

    labels = []
    keydata = list(period_counts.keys())
    for data in keydata:
        label = period_names.get(data, "Unknown")  # If period_names[data] is None or Undefined, set label to "Unknown"
        labels.append(label)

    values = list(period_counts.values())
    
    # absent count based on period
    period_counts2 = {period.id: 0 for period in periods}
    period_names2 = {period.id: period.period_name for period in periods}

    present_attendances2 = Attendance.query.filter_by(status='absent').all()

    for attendance in present_attendances2:
        period_counts2[attendance.period_id] += 1

    labels2 = []
    keydata2 = list(period_counts.keys())
    for data in keydata2:
        label = period_names2.get(data, "Unknown")  # If period_names[data] is None or Undefined, set label to "Unknown"
        labels2.append(label)

    values2 = list(period_counts2.values())
    
    # how many student are there in each class(year)
    years = Year.query.all()
    distinct_years = db.session.query(Student.year).distinct().all()
    year_names = {year.id: year.year_name for year in years}
    year_length = len(year_names)
    
    year_counts = {}
    for yearid in distinct_years:
        # print(yearid[0])  (1,) => 1, (3,) => 3
        count = Student.query.filter_by(year=yearid[0]).count()
        year_counts[yearid[0]] = count
        
    classlabels = []
    classkeys = list(year_counts.keys())
    for data in classkeys:
        label = year_names.get(data, "Unknown")  # If period_names[data] is None or Undefined, set label to "Unknown"
        classlabels.append(label)
    classvalues = list(year_counts.values())
        
    students = Student.query.count()
    return render_template("adminDashboard.html", labels=labels, values = values, labels2=labels2, values2 = values2, classlabels = classlabels, classvalues = classvalues, period_length=period_length, year_length=year_length, students=students)