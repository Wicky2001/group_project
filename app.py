import marshmallow
from flask import Flask, request,jsonify
from flask_restful import Resource, Api, fields, marshal_with, abort
import threading
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Add the parent directory to the sys path
# sys.path.append(os.path.abspath(".."))


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost:3306/vehicals"
db = SQLAlchemy(app)


class detections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    second = db.Column(db.Integer, nullable=False)
    number_plate = db.Column(db.String, nullable=True)
    in_or_out = db.Column(db.String, nullable=False)
    vehicle_type=db.Column(db.String,nullable=False)


# class EntryFieldSchema(marshmallow.Schema):
#
#     year = fields.Integer()
#     month = fields.Integer()
#     date = fields.Integer()
#     hour = fields.Integer()
#     minute = fields.Integer()
#     second = fields.Integer()
#     number_plate = fields.String()
#


class lastEntry(Resource):
    def get(self):
        print("Request received")
        last_entered = detections.query.filter_by(in_or_out="IN").order_by(detections.id.desc()).first()

        if not last_entered:
            abort(404, message="Couldn't find an entry")

        marshaled_entry = {
            'day': {
                'year': last_entered.year,
                'month': last_entered.month,
                'date': last_entered.date,
                'hour': last_entered.hour,
                'minute': last_entered.minute,
                'second': last_entered.second,
            },
            'number_plate': last_entered.number_plate,
            'vehicle_type':last_entered.vehicle_type,
            'status': last_entered.in_or_out
        }

        return jsonify(marshaled_entry)

class SearchSchema(Schema):
    day = fields.Str(required=False, allow_none=True)
    number_plate = fields.Str(required=True)  # Match the field name in the schema


class Search(Resource):


    def get(self):
        schema = SearchSchema()

        # Access data from query parameters (GET)
        day = request.args.get('day')
        number_plate = request.args.get('numberPlate')

        # Validate data using Schema's validate method
        errors = schema.validate({'day': day, 'number_plate': number_plate}, partial=True)
        if errors:
            print(errors)
            return {'error': str(errors)}, 400  # Bad Request
        else:
            entries = detections.query.filter_by(number_plate=number_plate).all()

            # entries.append(len(entries))
            print(entries)
        marshaled_entries = []
        for entry in entries:
            marshaled_entry = {
                'day': {
                    'year': entry.year,
                    'month': entry.month,
                    'date': entry.date,
                    'hour': entry.hour,
                    'minute': entry.minute,
                    'second': entry.second
                },
                'number_plate': entry.number_plate,
                'vehicle_type': entry.vehicle_type,
                'status':entry.in_or_out
            }
            marshaled_entries.append(marshaled_entry)
        marshaled_entries.append({'length': len(marshaled_entries)})
        response=jsonify(marshaled_entries)
        return response


class searchByDateSchema(Schema):
    startDate = fields.Date(required=True)
    endDate = fields.Date(required=True)
    startTime = fields.Time(required=True)
    endTime = fields.Time(required=True)
    statics:fields.Boolean(required=False)

class searchByDate(Resource):
    def get(self):
        # Instantiate the schema
        schema = searchByDateSchema()

        # Access data from query parameters (GET)
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        startTime = request.args.get('startTime')
        endTime = request.args.get('endTime')
        statics=request.args.get('statics')

        # Validate data using Schema's validate method
        data = {
            'startDate': startDate,
            'endDate': endDate,
            'startTime': startTime,
            'endTime': endTime
        }

        errors = schema.validate(data)
        if errors:
            return {'error': str(errors)}, 400  # Bad Request
        else:
            # Your logic for processing the validated data goes here
            # ....


            parsedStartDate = datetime.strptime(startDate, "%Y-%m-%d")
            parsedEndDate = datetime.strptime(endDate, "%Y-%m-%d")
            parsedStartTime = datetime.strptime(startTime, "%H:%M:%S")
            parsedEndTime = datetime.strptime(endTime, "%H:%M:%S")

            startYear = parsedStartDate.year
            startMonth = parsedStartDate.month
            startDay = parsedStartDate.day

            endYear = parsedEndDate.year
            endMonth = parsedEndDate.month
            endDay = parsedEndDate.day

            startHour = parsedStartTime.hour
            startMinute = parsedStartTime.minute
            startSecond = parsedStartTime.second

            endHour = parsedEndTime.hour
            endMinute = parsedEndTime.minute
            endSecond = parsedEndTime.second

            print("Debug: startYear, endYear:", startYear, endYear)
            print("Debug: startMonth, endMonth:", startMonth, endMonth)
            print("Debug: startDay, endDay:", startDay, endDay)
            print("Debug: startHour, endHour:", startHour, endHour)
            print("Debug: startMinute, endMinute:", startMinute, endMinute)
            print("Debug: startSecond, endSecond:", startSecond, endSecond)

            entries = detections.query.filter(
            detections.year >= startYear,
            detections.year <= endYear,
            detections.month >= startMonth,
            detections.month <= endMonth,
            detections.date >= startDay,
            detections.date <= endDay,
            detections.hour>=startHour,
            detections.hour<=endHour,
            detections.minute>=startMinute,
            detections.minute<=endMinute,
            detections.second >= startSecond,
            detections.second <= endSecond,


            # Add more conditions as needed for hour, second, etc.
        )
        print(entries)
        marshaled_entries = []
        for entry in entries:
            marshaled_entry = {
                'day': {
                    'year': entry.year,
                    'month': entry.month,
                    'date': entry.date,
                    'hour': entry.hour,
                    'minute': entry.minute,
                    'second': entry.second
                },
                'number_plate': entry.number_plate,
                'vehicle_type': entry.vehicle_type,
                'status':entry.in_or_out
            }
            marshaled_entries.append(marshaled_entry)
        marshaled_entries.append({'length': len(marshaled_entries)})
        response = jsonify(marshaled_entries)
        return response



class addEntrySchema(Schema):
    entryDate = fields.Date(required=True)
    entryTime =fields.Time(required=True)
    status= fields.String(required=False)
    numberPlate = fields.String(required=True)
    vehicleType =fields.String(required=False)



class addEntry(Resource):
    def post(self):
        json_data = request.json  # data is sent as JSON in the request body

        #ValidationError Handling: The load() method of the Marshmallow schema (addEntrySchema) can raise a ValidationError
        # if the incoming data does not match the schema's structure or fails any of the validation rules defined in
        # the schema. By using try and except, we can catch this specific exception and handle it gracefully.


        try:
            # Validate the incoming JSON data against the schema
            data = addEntrySchema().load(json_data)
            # At this point, data will contain validated and deserialized input


            entryDate = data.get('entryDate')
            entryTime = data.get('entryTime')
            numberPlate = data.get('numberPlate')
            vehicleType = data.get('vehicleType')
            in_or_out=data.get('status')

            # Ensure entryDate and entryTime are strings
            entryDate_str = str(entryDate)
            entryTime_str = str(entryTime)

            # Convert entryDate and entryTime strings to datetime objects
            parsedDate = datetime.strptime(entryDate_str, "%Y-%m-%d")
            parsedTime = datetime.strptime(entryTime_str, "%H:%M:%S")

            # Extract individual components
            entryYear = parsedDate.year
            entryMonth = parsedDate.month
            entryDay = parsedDate.day
            entryHour = parsedTime.hour
            entryMinute = parsedTime.minute
            entrySecond = parsedTime.second

            entry = detections(year=entryYear,month=entryMonth,date=entryDay ,hour=entryHour,minute=entryMinute,second=entrySecond ,in_or_out=in_or_out,  number_plate =numberPlate, vehicle_type=vehicleType)

            db.session.add(entry)
            db.session.commit()


            return {'message': 'Entry added successfully'}, 201  # HTTP status code 201 for Created
        except ValidationError as e:
            # Handle validation errors
            return {'message': 'Validation error', 'errors': e.messages}, 400  # HTTP status code 400 for Bad Request

api.add_resource(lastEntry, "/lastEntry")
api.add_resource(Search, "/Search")
api.add_resource(searchByDate, "/searchByDate")
api.add_resource(addEntry,"/addEntry")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    print("Server is running...")
