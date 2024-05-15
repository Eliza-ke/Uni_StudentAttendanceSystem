from flask import flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from Website.models import Student, Admin
from Website.config import db

# student side  
def studentLogin():
    if request.method == 'POST':
        emailogin = request.form.get('emailogin')
        passwordlogin = request.form.get('passwordlogin')
        
        student = Student.query.filter_by(email=emailogin).first()
        if student:
            if check_password_hash(student.password, passwordlogin):
                session['student_id'] = student.id
                return jsonify(success=True, redirect=url_for('stattendance'))
            else:
                return jsonify(success=False, message='Incorrect password')
        else:
            return jsonify(success=False, message='Invalid email')
        

def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get("name")
        year = request.form.get("year")
        batch = request.form.get("batch")
        phone = request.form.get("phone")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        student_info = Student.query.filter_by(email=email).first()
        if student_info:
            return jsonify(success=False, message='email is already exist')
        elif len(email) < 4:
            return jsonify(success=False, message='Invalid email')
        elif len(name) < 2:
            return jsonify(success=False, message='Name must be longer than 2 letters')
        elif len(batch) < 2:
            return jsonify(success=False, message='Batch must be longer than 2 letters')
        elif len(phone) < 5:
            return jsonify(success=False, message='Phone number must be greater than 5')
        elif password1 != password2:
            return jsonify(success=False, message='password does not match')
        elif len(password1) < 7:
            return jsonify(success=False, message='password must be greater than 7')
        else:
            profileImg = "defaultprofile.png"
            new_student = Student(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'), year=year, batch=batch, phone=phone,profile=profileImg)
            db.session.add(new_student)
            db.session.commit()
            student = Student.query.filter_by(email=email).first()
            session['student_id'] = student.id
            return jsonify(success=True, redirect=url_for('stattendance'))
        
# admin side
def adminlogin():
    if request.method == 'POST':
        emailadmin = request.form.get('emailogin')
        passwordadmin = request.form.get('passwordlogin')
        admin = Admin.query.filter_by(email=emailadmin).first()
        if admin:
            if check_password_hash(admin.password, passwordadmin):
                myadmin = {
                            "admin_id": admin.id,
                            "admin_name": admin.name,
                            "admin_email": admin.email,
                            "admin_profile": admin.profile,
                            "admin_rolecode": admin.roleCode,
                        }
                session['admin_id'] = admin.id
                session['admin'] = myadmin
                return jsonify(success=True, redirect=url_for('adminStudentInfo'))
            else:
                return jsonify(success=False, message='Incorrect Password')
        else:
            return jsonify(success=False, message='Email does not exist')    
    return render_template("adminlogin.html")
            

def adminsignup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get("name")
        rolecode = request.form.get("rolecode")
        phone = request.form.get("phone")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        admin_info = Admin.query.filter_by(email=email).first()
        if admin_info:
            return jsonify(success=False, message='Email already exist')
        elif len(email) < 4:
            return jsonify(success=False, message='Invalid Email')
        elif len(name) < 2:
            return jsonify(success=False, message='Name must be longer than 2 letters')
        elif len(phone) < 5:
            return jsonify(success=False, message='Phone number must be greater than 5')
        elif password1 != password2:
            return jsonify(success=False, message='Password does not match')
        elif len(password1) < 7:
            return jsonify(success=False, message='Password must be greater than 7')
        else:
            if not rolecode:
                rolecode = "F1001" # faculty code
                profileImg = "defaultprofile.png" # default image
                new_admin = Admin(email=email, name=name, phone=phone, password=generate_password_hash(password1, method='pbkdf2:sha256'), roleCode=rolecode, profile=profileImg)
                db.session.add(new_admin)
                db.session.commit()
                admin = Admin.query.filter_by(email=email).first()
                myadmin = {
                    "admin_id": admin.id,
                    "admin_name": admin.name,
                    "admin_email": admin.email,
                    "admin_profile": admin.profile,
                    "admin_rolecode": admin.roleCode,
                }
                session['admin_id'] = admin.id
                session['admin'] = myadmin

                return jsonify(success=True, redirect=url_for('adminStudentInfo'))
            if rolecode:
                if rolecode == "S1001": #system admin code
                    profileImg = "defaultprofile.png"
                    new_admin = Admin(email=email, name=name, phone=phone, password=generate_password_hash(password1, method='pbkdf2:sha256'), roleCode=rolecode, profile=profileImg)
                    db.session.add(new_admin)
                    db.session.commit()
                    admin = Admin.query.filter_by(email=email).first()
                    myadmin = {
                        "admin_id": admin.id,
                        "admin_name": admin.name,
                        "admin_email": admin.email,
                        "admin_profile": admin.profile,
                        "admin_rolecode": admin.roleCode,
                    }
                    session['admin_id'] = admin.id
                    session['admin'] = myadmin

                    flash("Created Successfully", category='success')
                    
                    return jsonify(success=True, redirect=url_for('adminStudentInfo'))
            else:
                return jsonify(success= False, message='Incorrect role code')
                
    return render_template("adminSignUp.html")