from flask import redirect, render_template, session, url_for
from Website.config import create_app
from Website.auth import studentLogin, register, adminlogin, adminsignup
from Website.studentfeatures import attendance, studentprofile, updateProfile
from Website.adminfeatues import adminattendancefilterbyyear, adminattendanceinfo, admindashboard, adminfacultyinfo, adminfilterbyyear, adminperiodinfo, adminprofile, adminstudentinfo, deletefacultyinfo, deleteperiodinfo, deleteyearinfo, eachattendance, filterbytoday, notloginedstudent, notloginedstudentbyyear, setabsent, updateadminprofile, updateperiodinfo, updateyearinfo, yearinfo
from Website.models import Year


app = create_app()

# Student Side
@app.route("/student/home", methods=['GET'])
def home():
    years = Year.query.all()
    return render_template("home.html", years=years)

@app.route('/student/login', methods=['POST'])
def stLogin():
    return studentLogin()


@app.route('/student/register', methods=['GET', 'POST'])
def stRegister():
    return register()


@app.route('/student/attendance', methods=['GET', 'POST'])
def stattendance():
    if 'student_id' not in session:
        return redirect(url_for('home'))
    else:
        return attendance()


@app.route('/student/profile', methods=['GET', 'POST'])
def studentProfile():
    if 'student_id' not in session:
        return redirect(url_for('home'))
    else:
        return studentprofile()


@app.route('/student/updateprofile', methods=['GET', 'POST'])
def updatedProfile():
    if 'student_id' not in session:
        return redirect(url_for('home'))
    else:
        return updateProfile()


@app.route('/student/logout')
def logout():
    session.pop('student_id', None)
    return redirect(url_for('home'))


# Admin Side
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminLogin():
    return adminlogin()


@app.route('/adminSignUp', methods=['GET', 'POST'])
def adminSignUp():
    return adminsignup()


@app.route('/adminlogout')
def adminlogout():
    session.pop('admin_id', None)
    return redirect(url_for('adminlogin'))

# student information
@app.route('/adminstudentInfo', methods=['GET', 'POST'])
def adminStudentInfo():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return adminstudentinfo()

@app.route('/adminfilterbyYear/<int:yearid>', methods=['GET', 'POST'])
def adminfilterbyYear(yearid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return adminfilterbyyear(yearid)

# year information


@app.route('/adminyearInfo', methods=['GET', 'POST'])
def adminyearInfo():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return yearinfo()


@app.route('/updateyearInfo/<int:yid>', methods=['GET', 'POST'])
def updateyearInfo(yid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return updateyearinfo(yid)


@app.route('/deleteyearInfo/<int:yid>', methods=['GET', 'POST', 'DELETE'])
def deleteyearInfo(yid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return deleteyearinfo(yid)

# period information


@app.route('/adminperiodInfo', methods=['GET', 'POST'])
def adminperiodInfo():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return adminperiodinfo()


@app.route('/updateperiodInfo/<int:pid>', methods=['GET', 'POST'])
def updateperiodInfo(pid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return updateperiodinfo(pid)


@app.route('/deleteperiodInfo/<int:pid>', methods=['GET', 'POST'])
def deleteperiodInfo(pid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return deleteperiodinfo(pid)

# admin profile
@app.route('/adminProfile', methods=['GET', 'POST'])
def adminProfile():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return adminprofile()


@app.route('/signout')
def sigout():
    session.pop('admin_id', None)
    session.pop('admin', None)

    return redirect(url_for('adminLogin'))


@app.route('/updateAdminProfile', methods=['GET', 'POST'])
def updatedAdminProfile():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return updateadminprofile()

@app.route('/adminfacultyInfo', methods=['GET', 'POST'])
def adminfacultyInfo():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return adminfacultyinfo()
    
@app.route('/deletefacultyInfo/<int:fid>', methods=['GET', 'POST'])
def deletefacultyInfo(fid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return deletefacultyinfo(fid)

# show each student's attendance 
@app.route('/eachAttendance/<int:stid>', methods=['GET', 'POST'])
def eachAttendance(stid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return eachattendance(stid)
    
@app.route('/filterbyToday/<int:stid>', methods=['GET', 'POST'])
def filterbyToday(stid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return filterbytoday(stid)
    
    
@app.route('/notLoginedStudent', methods=['GET', 'POST'])
def notLoginedStudent():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return notloginedstudent()
    
@app.route('/notLoginedStudentbyYear/<int:yrid>', methods=['GET', 'POST'])
def notLoginedStudentbyYear(yrid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return notloginedstudentbyyear(yrid)
    
@app.route('/setAbsent', methods=['GET'])
def setAbsent():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return setabsent()
    
    
@app.route('/adminattendanceInfo', methods=['GET', 'POST'])
def adminattendanceInfo():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return adminattendanceinfo()
    
@app.route('/adminattendancefilterbyYear/<int:yearid>', methods=['GET', 'POST'])
def adminattendancefilterbyYear(yearid):
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return adminattendancefilterbyyear(yearid)
    
    
@app.route('/adminDashboard', methods=['GET', 'POST'])
def adminDashboard():
    if 'admin_id' not in session:
        return redirect(url_for('adminLogin'))
    else:
        return admindashboard()
    
if __name__ == '__main__':
    app.run(debug=True)
