# TitovMaks_27/11/23
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Можно изменить базу
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', backref='appointments')
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student = db.relationship('Student', backref='appointments')
    notes = db.Column(db.String(255), nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=False)
    is_shown = db.Column(db.Boolean, nullable=False)

# Маршруты
@app.route('/api/v1/appointments', methods=['GET'])
def get_appointments():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'id')  # Default sort by id
    employee_id = request.args.get('employee_id', type=int)
    student_id = request.args.get('student_id', type=int)
    start_date = request.args.get('start_date', type=str)

    # Прим фильтры
    query = Appointment.query
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if student_id:
        query = query.filter_by(student_id=student_id)
    if start_date:
        query = query.filter(Appointment.start_date == start_date)

    # Сортировка и разбивка на страницы
    appointments = query.order_by(sort_by).paginate(page, per_page, error_out=False)

    # Конв в JSON
    appointments_data = [{
        'id': appointment.id,
        'start_date': appointment.start_date.isoformat(),
        'duration': appointment.duration,
        'employee_id': appointment.employee_id,
        'student_id': appointment.student_id,
        'notes': appointment.notes,
        'is_confirmed': appointment.is_confirmed,
        'is_shown': appointment.is_shown
    } for appointment in appointments.items]

    return jsonify({
        'appointments': appointments_data,
        'total_pages': appointments.pages,
        'current_page': appointments.page
    })

@app.route('/api/v1/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    # Запись на приём по ID
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment_data = {
        'id': appointment.id,
        'start_date': appointment.start_date.isoformat(),
        'duration': appointment.duration,
        'employee_id': appointment.employee_id,
        'student_id': appointment.student_id,
        'notes': appointment.notes,
        'is_confirmed': appointment.is_confirmed,
        'is_shown': appointment.is_shown
    }
    return jsonify({'appointment': appointment_data})

@app.route('/api/v1/appointments', methods=['POST'])
def create_appointment():
    # Создание новой встречи
    data = request.json
    new_appointment = Appointment(
        start_date=datetime.strptime(data['start_date'], '%d-%m-%YT%H:%M'),
        duration=data['duration'],
        employee_id=data['employee_id'],
        student_id=data['student_id'],
        notes=data.get('notes'),
        is_confirmed=data['is_confirmed'],
        is_shown=data['is_shown']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Встреча создана успешно'}), 201

@app.route('/api/v1/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    # Удаление встречи
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Встреча удалена успешно'})

from flask import Response

@app.route('/api/v1/appointments/<int:appointment_id>/icalendar.ics', methods=['GET'])
def get_icalendar(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id) # Генерация и возврат ICS

    from icalendar import Calendar, Event # Создаём событие iCalendar

    cal = Calendar()
    cal.add('prodid', '-//My Calendar//example.com//')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', f'Встреча с {appointment.employee.full_name} и {appointment.student.full_name}')
    event.add('description', f'Встреча с {appointment.employee.full_name} и {appointment.student.full_name}')
    event.add('dtstart', appointment.start_date)
    event.add('dtend', appointment.start_date + timedelta(minutes=appointment.duration))
    event.add('uid', str(appointment.id))

    cal.add_component(event)

    ical_data = cal.to_ical()  # Возвращаем ICS

    response = Response(ical_data, content_type='text/calendar')
    response.headers['Content-Disposition'] = f'attachment; filename=appointment_{appointment.id}.ics'

    return response

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)