from unicodedata import name
from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/student_database'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
class studata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    contact_add = db.Column(db.String(50))
    stud_email = db.Column(db.String(50), unique=True)
    stud_pass = db.Column(db.Integer)
    tran_id = db.relationship('transa', backref='studata', lazy=True)
    schedules_id = db.relationship(
        'schedules', cascade='all, delete', backref='studata', lazy=True)
    
class courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50))
    course_desc = db.Column(db.String(100))
    school_yr = db.Column(db.Integer)
    subject_id = db.relationship(
        'subject', cascade='all, delete', backref='courses', lazy=True)
    schedules_id = db.relationship(
        'schedules', cascade='all, delete', backref='courses', lazy=True)
    
class instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    contact_add = db.Column(db.String(50))
    ins_email = db.Column(db.String(50), unique=True)
    ins_pass = db.Column(db.Integer)
    schedules_id = db.relationship(
         'schedules', cascade='all, delete', backref='instructor', lazy=True)    


class transa(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    trans_name = db.Column(db.String(50))
    trans_date = db.Column(db.DateTime,default=datetime.now)
    std_id = db.Column(db.Integer, db.ForeignKey('studata.id'))
    
    
class subject(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    schedules_id = db.relationship(
        'schedules', cascade='all, delete', backref='subject', lazy=True)

class schedules(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    time_start = db.Column(db.Integer)
    time_end = db.Column(db.Integer)
    day = db.Column(db.DateTime, default=datetime.now)
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    std_id = db.Column(db.Integer, db.ForeignKey('studata.id'))
    
@app.route("/")
def home():
    return {"msg": "ok"}

@app.route('/registerstudata', methods=["POST"])
def create_studata():
    try:
        data = request.json
        fname = data['fname']
        lname = data['lname']
        gender = data['gender']
        age = data['age']
        contact_add = data['contact_add']
        stud_email = data['stud_email']
        stud_pass = data['stud_pass']

        getdata = studata(fname=fname, lname=lname, gender=gender, age=age,
                              contact_add=contact_add, stud_email=stud_email, stud_pass=stud_pass)
        db.session.add(getdata)
        db.session.commit()

        return jsonify({"success": True, "response": "studata added"})
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getstudata', methods=['GET'])
def get_studata():
    try:
        all_data = []
        datas = studata.query.all()
        for data in datas:
            result = {
                "id": data.id,
                "fname": data.fname,
                "lname": data.lname,
                "gender": data.gender,
                "age": data.age,
                "contact_add": data.contact_add,
                "stud_email": data.stud_email,
                "stud_pass": data.stud_pass
            }
            all_data.append(result)

            return jsonify(
                {
                    "success": True,
                    "pets": all_data,
                    "total_pets": len(datas),
                }
            )
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/putstudata/<int:id>', methods=["PUT"])
def update_studata(id):

    try:
        id = studata.query.get(id)

        if id is None:
            return {"msg": "id not present"}

        else:
            fname = request.json['fname']
            lname = request.json['lname']
            gender = request.json['gender']
            age = request.json['age']
            contact_add = request.json['contact_add']
            stud_email = request.json['stud_email']
            stud_pass = request.json['stud_pass']
            id.fname = fname
            id.lname = lname
            id.gender = gender
            id.age = age
            id.contact_add = contact_add
            id.stud_email = stud_email
            id.stud_pass = stud_pass
            db.session.add(id)
            db.session.commit()

            return jsonify({"success": True, "response": "studata Details updated"})

    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getsdata/<int:id>', methods=["GET"])
def getstudata(id):
    id = studata.query.get(id)
    if id:
        fname = id.fname
        lname = id.lname
        gender = id.gender
        age = id.age
        contact_add = id.contact_add
        stud_email = id.stud_email
        return jsonify({'fname': fname, "lname": lname, " gender": gender, " age": age, " contact_add": contact_add, "stud_email": stud_email})
    else:
        return {"msg": "id may not present"}

@app.route('/deletedata/<int:id>', methods=['DELETE'])
def delete_studata(id):
    response = {}
    id = studata.query.get(id)
    response['id'] = id
    db.session.delete(id)
    db.session.commit()
    return jsonify({"success": True, "response": "Student Details Delete"})

@app.route('/registercourses', methods=["POST"])
def create_courses():
    try:
        data = request.json
        course_name = data['course_name']
        course_desc = data['course_desc']
        school_yr = data['school_yr']

        getdata = courses(course_name=course_name,
                          course_desc=course_desc, school_yr=school_yr)
        db.session.add(getdata)
        db.session.commit()

        return jsonify({"success": True, "response": "coueses added"})
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getcourses', methods=['GET'])
def get_courses():
    try:
        all_data = []
        datas = courses.query.all()
        for data in datas:
            result = {
                "id": data.id,
                "course_name": data.course_name,
                "course_desc": data.course_desc,
                "school_yr": data.school_yr,
            }
            all_data.append(result)

            return jsonify(
                {
                    "success": True,
                    "coueses": all_data,
                    "total_coueses": len(datas),
                }
            )
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/updatecourses/<int:id>', methods=["PUT"])
def update_courses(id):
    import pdb
    pdb.set_trace()
    try:
        id = courses.query.get(id)

        if id is None:
            return {"msg": "id not not present"}
        else:
            course_name = request.json['course_name']
            course_desc = request.json['course_desc']
            school_yr = request.json['school_yr']
            id.course_name = course_name
            id.course_desc = course_desc
            id.school_yr = school_yr
            db.session.add(id)
            db.session.commit()

            return jsonify({"success": True, "response": "coueses Details updated"})

    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getcoursesbyid/<int:id>', methods=["GET"])
def getscouese(id):
    id = courses.query.get(id)
    if id:
        course_name = id.course_name
        course_desc = id.course_desc
        school_yr = id.school_yr
        return jsonify({'course_name': course_name, "course_desc": course_desc, " school_yr": school_yr})
    else:
        return {"msg": "id may not present"}

@app.route('/deletecorses/<int:id>', methods=['DELETE'])
def delete_coueses(id):
    response = {}
    id = courses.query.get(id)
    response['id'] = id
    db.session.delete(id)
    db.session.commit()
    return jsonify({"success": True, "response": "courses Details Delete"})

@app.route('/createInstructor', methods=['POST'])
def create_Instructor():
    try:
        data = request.json
        fname = data['fname']
        lname = data['lname']
        gender = data['gender']
        age = data['age']
        contact_add = data['contact_add']
        ins_email = data['ins_email']
        ins_pass = data['ins_pass']

        getdata = instructor(fname=fname, lname=lname, gender=gender, age=age,
                             contact_add=contact_add, ins_email=ins_email, ins_pass=ins_pass)
        db.session.add(getdata)
        db.session.commit()

        return jsonify({"success": True, "response": "Instructor added"})
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getInstructor', methods=['GET'])
def get_Instructor():
    try:
        all_data = []
        datas = instructor.query.all()
        for data in datas:
            result = {
                "id": data.id,
                "fname": data.fname,
                "lname": data.lname,
                "gender": data.gender,
                "age": data.age,
                "contact_add": data.contact_add,
                "ins_email": data.ins_email,
                "ins_pass": data.ins_pass
            }
            all_data.append(result)

            return jsonify(
                {
                    "success": True,
                    "Instructor": all_data,
                    "total_Instructor": len(datas),
                }
            )
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/updateInstructor/<int:id>', methods=["PUT"])
def update_Instructor(id):
    try:
        id = instructor.query.get(id)

        if id is None:
            return {"msg": "id not present"}

        else:
            fname = request.json['fname']
            lname = request.json['lname']
            gender = request.json['gender']
            age = request.json['age']
            contact_add = request.json['contact_add']
            ins_email = request.json['ins_email']
            ins_pass = request.json['ins_pass']
            id.fname = fname
            id.lname = lname
            id.gender = gender
            id.age = age
            id.contact_add = contact_add
            id.ins_email = ins_email
            id.ins_pass = ins_pass
            db.session.add(id)
            db.session.commit()

            return jsonify({"success": True, "response": "studata Details updated"})

    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getbyidInstructor/<int:id>', methods=["GET"])
def getsInstructor(id):
    id = instructor.query.get(id)

    if id:
        fname = id.fname
        lname = id.lname
        gender = id.gender
        age = id.age
        contact_add = id.contact_add
        ins_email = id.ins_email
        return jsonify({'fname': fname, "lname": lname, " gender": gender, " age": age, " contact_add": contact_add, "ins_email": ins_email})
    else:
        return {"msg": "id may not present"}

@app.route('/deleteInstructor/<int:id>', methods=['DELETE'])
def delete_Instructor(id):
    response = {}
    id = instructor.query.get(id)
    response['id'] = id
    db.session.delete(id)
    db.session.commit()
    return jsonify({"success": True, "response": "Pet Details Delete"})

@app.route('/transa', methods=["POST"])
def create_transaction():
    try:
        data = request.json
        trans_name = data['trans_name']
        std_id = data['std_id']
        getdata = transa(trans_name=trans_name, trans_date="1970-01-02",std_id=std_id)
        db.session.add(getdata)
        db.session.commit()

        return jsonify({"success": True, "response": "Transaction added"})
    except Exception as e:
        return jsonify({"error": e.args})
    
@app.route('/getstransaction', methods=['GET'])
def get_transaction():
    try:
        all_data = []
        datas = transa.query.all()
        for data in datas:
            std_id=studata.query.get(data.std_id)
            result = {
                "id": data.id,
                "trans_name": data.trans_name,
                "trans_date": data.trans_date,
                "std_id" : {
                    "id":std_id.id,
                    "fname":std_id.fname,
                    "lname" : std_id.lname,
                    "gender" : std_id.gender,
                    "age" : std_id.age,
                    "contact_add" : std_id.contact_add,
                    "stud_email" : std_id.stud_email,
                    "stud_pass" : std_id.stud_pass
                }
            }
            all_data.append(result)

            return jsonify(
                {
                    "success": True,
                    "Transaction": all_data,
                    "total_Transaction": len(datas),
                }
            )
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/puttransaction/<int:id>', methods=["PUT"])
def update_transaction(id):

    try:
        id = transa.query.get(id)
        if id is None:
            return {"msg": "id not present"}
        else:
            trans_name = request.json['trans_name']
            trans_date = request.json['trans_date']
            id.trans_name = trans_name
            id.trans_date = trans_date
            db.session.add(id)
            db.session.commit()

            return jsonify({"success": True, "response": "Transaction Details updated"})

    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getstransaction/<int:id>', methods=["GET"])
def getstransaction(id):
    main_id=id
    id = transa.query.get(id)
    if id:
        trans_name = id.trans_name
        trans_date = id.trans_date
        std_id=studata.query.get(id.std_id)
        result={
            "id":std_id.id,
            "fname":std_id.fname,
            "lname" : std_id.lname,
            "gender" : std_id.gender,
            "age" : std_id.age,
            "contact_add" : std_id.contact_add,
            "stud_email" : std_id.stud_email,
            "stud_pass" : std_id.stud_pass
       }
        data={
            "id":main_id,
            "trans_date":trans_date,
            "trans_name":trans_name,
            "std_id":result  
        }
        return jsonify({"success": True, "response": data})
    else:
        return {"msg": "id may not present"}

@app.route('/delettransaction/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    response = {}
    id = transa.query.get(id)
    response['id'] = id
    db.session.delete(id)
    db.session.commit()
    return jsonify({"success": True, "response": "Transaction Details Delete"})

@app.route('/subject', methods=["POST"])
def create_subject():
    try:
        data = request.json
        name = data['name']
        getdata = subject(name=name)
        db.session.add(getdata)
        db.session.commit()

        return jsonify({"success": True, "response": "Subject added"})
    except Exception as e:
        return jsonify({"error": e.args})
    
@app.route('/getsubject', methods=['GET'])
def get_subject():
    try:
        all_data = []
        datas = subject.query.all()
        for data in datas:
            c_data=courses.query.get(data.courses_id)
            result = {
                "id": data.id,
                "name": data.name,
                "courses_id":{
                    "id" : c_data.courses_id,
                    "course_name" : c_data.course_name,
                    "course_desc" : c_data.course_desc,
                    "school_yr" : c_data.school_yr
                }
            }
            all_data.append(result)

            return jsonify(
                {
                    "success": True,
                    "subject": all_data,
                    "total_subject": len(datas),
                }
            )
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/updateSubject/<int:id>', methods=["PUT"])
def update_subject(id):
    try:
        id = subject.query.get(id)

        if id is None:
            return {"msg": "id not present"}

        else:
            name = request.json['name']
            id.name = name
            db.session.add(id)
            db.session.commit()
            
            return jsonify({"success": True, "response": "subject Details updated"})

    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getsubjects/<int:id>', methods=["GET"])
def getsubject(id):
    id = subject.query.get(id)
    if id:
        c_data = courses.query.get(id.courses_id)
        name = id.name
        data = {
            "name" : name,
            "courses_id" : result
        }
        result={
            "course_name" : c_data.course_name,
            "course_desc" : c_data.course_desc,
            "school_yr" : c_data.school_yr
        }
        return jsonify({"success": True, "response": data})
    else:
        return {"msg": "id may not present"}

@app.route('/deletesubject/<int:id>', methods=['DELETE'])
def delete_subject(id):
    response = {}
    id = subject.query.get(id)
    response['id'] = id
    db.session.delete(id)
    db.session.commit()
    return jsonify({"success": True, "response": "Subject Details Delete"})

@app.route('/createschedules', methods=['POST'])
def create_schedules():
    try:
        data = request.json
        day = data['day']
        time_start = data['time_start']
        time_end = data['time_end']

        getdata = schedules(day=day, time_start=time_start, time_end=time_end)
        db.session.add(getdata)
        db.session.commit()

        return jsonify({"success": True, "response": "schedules added"})
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getschedules', methods=['GET'])
def get_schedules():
    try:
        all_data = []
        datas = schedules.query.all()
        for data in datas:
            result = {
                "id": data.id,
                "day": data.day,
                "time_start": data.time_start,
                "time_end": data.time_end,
                "instructor_id" : data.instructor_id,
                "subject_id" : data.subject_id,
                "std_id" : data.std_id,
                "courses_id" : data.courses_id
            }
            all_data.append(result)

            return jsonify(
                {
                    "success": True,
                    "schedules": all_data,
                    "total_schedules": len(datas),
                }
            )
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/updateschedules/<int:id>', methods=["PUT"])
def update_schedules(id):
    try:
        id = schedules.query.get(id)

        if id is None:
            return {"msg": "id not present"}

        else:
            day = request.json['day']
            time_start = request.json['time_start']
            time_end = request.json['time_end']
           
            id.day = day
            id.time_start = time_start
            id.time_end = time_end
            db.session.add(id)
            db.session.commit()

            return jsonify({"success": True, "response": "studata Details updated"})

    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/getbyidschedules/<int:id>', methods=["GET"])
def getsschedules(id):
    id = schedules.query.get(id)

    if id:
        day = id.day
        time_start = id.time_start
        time_end = id.time_end
        return jsonify({'day': day, "time_start": time_start, " time_end": time_end})
    else:
        return {"msg": "id may not present"}

@app.route('/deleteshedules/<int:id>', methods=['DELETE'])
def delete_schedules(id):
    response = {}
    id = schedules.query.get(id)
    response['id'] = id
    db.session.delete(id)
    db.session.commit()
    return jsonify({"success": True, "response": "Pet Details Delete"})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)