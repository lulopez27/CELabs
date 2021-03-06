from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from ce_labs_api import app

db = SQLAlchemy(app)

class User_Type(db.Model):
    __tablename__ = 'user_type'
    id_user_type = db.Column(db.Integer, primary_key = True)
    user_type = db.Column(db.String(15), nullable = False)
    children = db.relationship("User")

class User(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key=True)
    public_id_user = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable = False)
    lastname1 = db.Column(db.String(50), nullable = False)
    lastname2 = db.Column(db.String(50), nullable = False)
    id_number = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    phone_number = db.Column(db.Text(50), nullable = False)
    active = db.Column(db.Boolean, nullable = False)
    university_id = db.Column(db.String, nullable = False)
    user_type = db.Column(db.Integer, db.ForeignKey('user_type.id_user_type'), nullable = False)


class Reservation(db.Model):
    id_reservation = db.Column(db.Integer, primary_key = True)
    public_id_reservation = db.Column(db.String(50), unique = True)
    request_date = db.Column(db.BigInteger, nullable = False)
    requested_date = db.Column(db.BigInteger, nullable = False)
    init_time = db.Column(db.BigInteger, nullable = False)
    final_time = db.Column(db.BigInteger, nullable = False)
    last_mod_id = db.Column(db.Integer, nullable = False)
    last_mod_date = db.Column(db.BigInteger, nullable = False)
    subject = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(80), nullable = False)
    operator = db.Column(db.String(50), db.ForeignKey('user.id_user'), nullable = True)

class User_Reservation(db.Model):
    __tablename__="user_reservation"
    id_user_reservation = db.Column(db.Integer, primary_key=True)
    id_reservation = db.Column(db.Integer, db.ForeignKey('reservation.id_reservation'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)


class Reservation_Lab(db.Model):
    __tablename__ = "reservation_lab"
    id_reservation_lab = db.Column(db.Integer, primary_key=True)
    id_reservation = db.Column(db.Integer, db.ForeignKey('reservation.id_reservation'), nullable = False)
    id_lab = db.Column(db.Integer, db.ForeignKey('lab.id_lab'), nullable = False)

class Lab(db.Model):
    id_lab= db.Column(db.Integer, primary_key = True)
    public_id_lab = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(50), nullable = False)
    capacity = db.Column(db.Integer, nullable = False)

class FaultReport_Lab(db.Model):
    __tablename__ = "faultreport_lab"
    id_faultreport_lab = db.Column(db.Integer, primary_key = True)
    id_report = db.Column(db.Integer, db.ForeignKey('faultreport.id_report'), nullable = False)
    id_lab = db.Column(db.Integer, db.ForeignKey('lab.id_lab'), nullable = False)

class FaultReport(db.Model):
    __tablename__ = "faultreport"
    id_report= db.Column(db.Integer, primary_key = True)
    public_id_report = db.Column(db.String(50), unique = True)
    date_time = db.Column(db.BigInteger, nullable = False)
    id_fault_part = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(80), nullable = False)
    id_status = db.Column(db.Integer, db.ForeignKey('faultstatus.id_status'), nullable = False)

class FaultStatus(db.Model):
    __tablename__ = "faultstatus"
    id_status= db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(50), nullable = False)

class User_FaultReport(db.Model):
    __tablename__ = "user_faultreport"
    id_user_faultreport = db.Column(db.Integer, primary_key = True)
    id_report = db.Column(db.Integer, db.ForeignKey('faultreport.id_report'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)

class User_Worklog(db.Model):
    __tablename__="user_worklog"
    id_user_worklog = db.Column(db.Integer, primary_key = True)
    id_worklog = db.Column(db.Integer, db.ForeignKey('worklog.id_worklog'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)

class Worklog(db.Model):
    id_worklog = db.Column(db.Integer, primary_key = True)
    public_id_worklog = db.Column(db.String(50), unique = True)
    date_time = db.Column(db.BigInteger, nullable = False)
    init_time = db.Column(db.BigInteger, nullable = False)
    final_time = db.Column(db.BigInteger, nullable = False)
    description = db.Column(db.String(80), nullable = False)
    id_status = db.Column(db.Integer, db.ForeignKey('worklogstatus.id_status'), nullable = False)

class WorklogStatus(db.Model):
    __tablename__ = "worklogstatus"
    id_status= db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(50), nullable = False)

class InventoryReport_Lab(db.Model):
    __tablename__= "inventoryreport_lab"
    id_inventoryreport_lab = db.Column(db.Integer, primary_key = True)
    id_report = db.Column(db.Integer, db.ForeignKey('inventoryreport.id_report'), nullable = False)
    id_lab = db.Column(db.Integer, db.ForeignKey('lab.id_lab'), nullable = False)

class InventoryReport(db.Model):
    __tablename__="inventoryreport"
    id_report = db.Column(db.Integer, primary_key = True)
    public_id_report = db.Column(db.String(50), unique = True)
    date = db.Column(db.BigInteger, nullable = False)
    complete_computers = db.Column(db.Integer, nullable = False)
    incomplete_computers = db.Column(db.Integer, nullable = False)
    number_projectors = db.Column(db.Integer, nullable = False)
    number_chairs = db.Column(db.Integer, nullable = False)
    number_fire_extinguishers = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(80), nullable = False)

class User_InventoryReport(db.Model):
    __tablename__ = "user_inventoryreport"
    id_user_inventaryreport = db.Column(db.Integer, primary_key = True)
    id_report = db.Column(db.Integer, db.ForeignKey('inventoryreport.id_report'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)

class AllNighter(db.Model):
    __tablename__ = 'allnighter'
    id_allnighter = db.Column(db.Integer, primary_key = True)
    public_id_allnighter = db.Column(db.String(50), unique = True)
    request_date = db.Column(db.BigInteger, nullable = False)
    requested_date = db.Column(db.BigInteger, nullable = False)
    init_time = db.Column(db.BigInteger, nullable = False)
    final_time = db.Column(db.BigInteger, nullable = False)
    last_mod_id = db.Column(db.Integer, nullable = False)
    last_mod_date = db.Column(db.BigInteger, nullable = False)
    subject = db.Column(db.String(50), nullable = False)
    state = db.Column(db.Integer, nullable = False)

class AllNighter_Asistance(db.Model):
    _tablename_ = 'allnighter_asistance'
    id_allnighter_asistance = db.Column(db.Integer, primary_key = True)
    id_allnighter = db.Column(db.Integer, db.ForeignKey('allnighter.id_allnighter'), nullable = False)
    name = db.Column(db.String(50), nullable = False)
    lastname1 = db.Column(db.String(50), nullable = False)
    lastname2 = db.Column(db.String(50), nullable = False)
    university_id = db.Column(db.String, nullable = False)
    

class AllNighter_Lab(db.Model):
    __tablename__ = 'allnighter_lab'
    id_allnighter_lab = db.Column(db.Integer, primary_key = True)
    id_allnighter = db.Column(db.Integer, db.ForeignKey('allnighter.id_allnighter'), nullable = False)
    id_lab = db.Column(db.Integer, db.ForeignKey('lab.id_lab'), nullable = False)
    
class User_AllNighter(db.Model):
    __tablename__ = 'user_allnighter'
    id_user_allnighter = db.Column(db.Integer, primary_key = True)
    id_allnighter = db.Column(db.Integer, db.ForeignKey('allnighter.id_allnighter'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)

class User_Operator(db.Model):
    __tablename__ = "user_operator"
    id_user_operator = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)
    pending_hours = db.Column(db.Integer, nullable = False)
    approved_hours = db.Column(db.Integer, nullable = False)

class User_Asist_Admin(db.Model):
    id_user_asist_admin = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)

class User_Admin(db.Model):
    id_user_admin = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)

class User_Prof(db.Model):
    id_user_prof = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)

class User_Lab_Admin(db.Model):
    id_user_lab_admin = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable = False)

class Course(db.Model):
    id_course = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.Text, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    group = db.Column(db.Integer, nullable = False)

class Event(db.Model):
    __tablename__ = 'event'
    id_event = db.Column(db.Integer, primary_key = True)
    public_id_event = db.Column(db.String(50), unique = True)
    description = db.Column(db.String(50), nullable = False)
    init_time = db.Column(db.BigInteger, nullable = False)
    final_time = db.Column(db.BigInteger, nullable = False)
    week_day = db.Column(db.String, nullable = True)
    date = db.Column(db.String, nullable = True)
    is_repeatable = db.Column(db.Boolean, nullable = False)
    id_lab = db.Column(db.Integer, db.ForeignKey('lab.id_lab'))

class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    id_evaluation = db.Column(db.Integer, primary_key = True)
    public_id_evaluation = db.Column(db.String(50), unique = True)
    date_time = db.Column(db.Text, nullable = False)
    score = db.Column(db.BigInteger, nullable = False)
    comment = db.Column(db.String(50), nullable = False)
    comment2 = db.Column(db.String(50), nullable = False)

print("The database classes were successfully loaded")