import marshmallow
from flask import Flask, request,jsonify
from flask_restful import Resource, Api, fields, marshal_with, abort
import threading
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
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
    year = db.Column(db.Integer, nullable=True)
    month = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Integer, nullable=True)
    hour = db.Column(db.Integer, nullable=True)
    minute = db.Column(db.Integer, nullable=True)
    second = db.Column(db.Integer, nullable=True)
    number_plate = db.Column(db.Integer, nullable=True)


class EntryFieldSchema(marshmallow.Schema):

    year = fields.Integer()
    month = fields.Integer()
    date = fields.Integer()
    hour = fields.Integer()
    minute = fields.Integer()
    second = fields.Integer()
    number_plate = fields.String()



class lastEntry(Resource):
    # @marshal_with(EntryFieldSchema)
    def get(self):
        print("req recieved")
        last_entered = detections.query.order_by(detections.id.desc()).first()

        if not last_entered:
            abort(404, message="couldn't find an entry")

        marshaled_entry = {
            'day': {
                'year': last_entered.year,
                'month': last_entered.month,
                'date': last_entered.date,
                'hour': last_entered.hour,
                'minute': last_entered.minute,
                'second': last_entered.second
            },
            'number_plate': last_entered.number_plate
        }

        response = jsonify(marshaled_entry)
        return response

class SearchSchema(Schema):
    day = fields.Str(required=False, allow_none=True)
    number_plate = fields.Str(required=True)  # Match the field name in the schema


class Search(Resource):

    # @marshal_with(entries_fields)
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
                'number_plate': entry.number_plate
            }
            marshaled_entries.append(marshaled_entry)
        response=jsonify(marshaled_entries)
        return response


class SearchByDateSchema(Schema):
    startDate = fields.Date(required=True)
    endDate = fields.Date(required=True)
    startTime = fields.Time(required=True)
    endTime = fields.Time(required=True)


class SearchByDate(Resource):
    def get(self):
        # Instantiate the schema
        schema = SearchByDateSchema()

        # Access data from query parameters (GET)
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        startTime = request.args.get('startTime')
        endTime = request.args.get('endTime')

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
            # ...

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
                'number_plate': entry.number_plate
            }
            marshaled_entries.append(marshaled_entry)
        response = jsonify(marshaled_entries)
        return response


api.add_resource(lastEntry, "/lastEntry")
api.add_resource(Search, "/Search")
api.add_resource(SearchByDate, "/SearchByDate")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    print("Server is running...")
