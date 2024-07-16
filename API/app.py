
import marshmallow
from flask import Flask, request,jsonify
from flask_restful import Resource, Api, abort
import threading
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import and_, or_

# import sys
import os

from sqlalchemy import func

# Add the parent directory to the sys path
# sys.path.append(os.path.abspath(".."))


app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Mysql%40123@localhost/detections?charset=utf8mb4"
#changed
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/detections?charset=utf8mb4"
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost:3306/detections"
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
    vehicle_type = db.Column(db.String,nullable=False)





class lastEntries(Resource):
    def get(self):
        print("Request received")
        lastEnteredEntries = detections.query.order_by(detections.id.desc()).limit(4 ).all()

        if not lastEnteredEntries:
            abort(404, message="Couldn't find an entry")

        result=[]

        for entry in lastEnteredEntries:
            marshaled_entry = {
                'day': {
                    'year': entry.year,
                    'month': entry.month,
                    'date': entry.date,
                    'hour': entry.hour,
                    'minute': entry.minute,
                    'second': entry.second,
                },
                'number_plate': entry.number_plate,
                'vehicle_type':entry.vehicle_type,
                'status': entry.in_or_out
            }
            result.append(marshaled_entry)

        response={
            'length':len(result),
            'result':result,
           # 'lastimg': lastEnteredEntries[0].img if lastEnteredEntries else None,
        }

        return response

class TodaySummary(Resource):
    def get(self):
        today = datetime.now()
        today_entries = detections.query.filter(
            detections.year == today.year,
            db.cast(detections.month, db.Integer) == today.month,
            db.cast(detections.date, db.Integer) == today.day
        ).all()

        if not today_entries:
            abort(404, message="No entries found for today")

        total_entered = sum(
            1 for entry in today_entries if entry.in_or_out.upper() == "IN"
        )
        total_left = sum(
            1 for entry in today_entries if entry.in_or_out.upper() == "OUT"
        )
        still_in_premise = total_entered - total_left

        summary = {
            "total_entered": total_entered,
            "total_left": total_left,
            "still_in_premise": still_in_premise,
            "anomalies": 0 # Keep commented for future development
        }

        return summary


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
        marshaledEntries = []
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
            marshaledEntries.append(marshaled_entry)
        marshaledEntries.append({'length': len(marshaledEntries)})
        response=jsonify(marshaledEntries)
        return response


class searchByDateSchema(Schema):
    startDate = fields.Date(required=True)
    endDate = fields.Date(required=True)
    startTime = fields.Time(required=True)
    endTime = fields.Time(required=True)
    vehicleType=fields.String(required=False,allow_none=True)
    statics = fields.Boolean(required=True)
    numberPlate=fields.String(required=False,allow_none=True)

class searchByDate(Resource):
    def get(self):
        # Instantiate the schema

        schema = searchByDateSchema()

        # Access data from query parameters (GET)
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        startTime = request.args.get('startTime')
        endTime = request.args.get('endTime')
        statics = request.args.get('statics')
        vehicleType=request.args.get('vehicleType')
        numberPlate=request.args.get('numberPlate')

        statics_bool = statics.lower() == 'true' if statics else False

        # Validate data using Schema's validate method
        data = {
            'startDate': startDate,
            'endDate': endDate,
            'startTime': startTime,
            'endTime': endTime,
            'statics': statics,
            'vehicleType':vehicleType,
            'numberPlate':numberPlate

        }

        errors = schema.validate(data)
        if errors:
            return {'error': str(errors)}, 400  # Bad Request
        else:

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


            if not statics_bool:

                entries = detections.query.filter(
                    and_(
                        or_(
                            and_(
                                endYear == startYear,
                                or_(
                                    and_(
                                        startMonth == endMonth,
                                        detections.year == startYear,
                                        detections.month == startMonth,
                                        detections.month == endMonth,
                                        detections.date >= startDay,
                                        detections.date <= endDay
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        startMonth < endMonth,
                                        or_(
                                            and_(
                                                detections.month < endMonth,
                                                detections.month > startMonth
                                            ),
                                            and_(
                                                detections.month == startMonth,
                                                detections.date >= startDay
                                            ),
                                            and_(
                                                detections.month == endMonth,
                                                detections.date <= endDay
                                            )
                                        )
                                    )
                                )
                            ),
                            and_(
                                endYear > startYear,
                                or_(
                                    and_(
                                        detections.year > startYear,
                                        detections.year < endYear
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        detections.month > startMonth
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        detections.month == startMonth,
                                        detections.date >= startDay
                                    ),
                                    and_(
                                        detections.year == endYear,
                                        detections.month < endMonth
                                    ),
                                    and_(
                                        detections.year == endYear,
                                        detections.month == endMonth,
                                        detections.date <= endDay
                                    )
                                )
                            )
                        ),
                        or_(
                            and_(
                                endHour == startHour,
                                or_(
                                    and_(
                                        startMinute == endMinute,

                                        detections.hour == startHour,
                                        detections.minute == startMinute,
                                        detections.minute == endMinute,
                                        detections.second >= startSecond,
                                        detections.second <= endSecond
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        startMinute != endMinute,
                                        or_(
                                            and_(
                                                detections.minute < endMinute,
                                                detections.minute > startMinute
                                            ),
                                            and_(
                                                detections.minute == startMinute,
                                                detections.second >= startSecond
                                            ),
                                            and_(
                                                detections.minute == endMinute,
                                                detections.second <= endSecond
                                            )
                                        )
                                    )
                                )
                            ),
                            and_(
                                endHour != startHour,
                                or_(
                                    and_(
                                        detections.hour > startHour,
                                        detections.hour < endHour
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        detections.minute > startMinute
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        detections.minute == startMinute,
                                        detections.second >= startSecond
                                    ),
                                    and_(
                                        detections.hour == endHour,
                                        detections.minute < endMinute
                                    ),
                                    and_(
                                        detections.hour == endHour,
                                        detections.minute == endMinute,
                                        detections.second <= endSecond
                                    )
                                )
                            )
                        )
                    )
                ).all()

                marshaledEntries = []
                if vehicleType == "All":
                    for entry in entries:
                        marshaledEntry = {
                            'id': entry.id,
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
                            'status': entry.in_or_out
                        }
                        marshaledEntries.append(marshaledEntry)
                else:
                    if(numberPlate):
                            for entry in entries:
                                if entry.vehicle_type == vehicleType and entry.number_plate == numberPlate:
                                    marshaledEntry = {
                                        'id': entry.id,
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
                                        'status': entry.in_or_out
                                    }
                                    marshaledEntries.append(marshaledEntry)
                    else:
                        for entry in entries:
                            if entry.vehicle_type == vehicleType:
                                marshaledEntry = {
                                    'id': entry.id,
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
                                    'status': entry.in_or_out
                                }
                                marshaledEntries.append(marshaledEntry)


                response_data = {
                    'count': len(marshaledEntries),
                    'result': marshaledEntries
                }
                response = jsonify(response_data)



            else:

                vehicleTypeInOrOutEntries =  detections.query.filter(
                    and_(
                        or_(
                            and_(
                                endYear == startYear,
                                or_(
                                    and_(
                                        startMonth == endMonth,
                                        detections.year == startYear,
                                        detections.month == startMonth,
                                        detections.month == endMonth,
                                        detections.date >= startDay,
                                        detections.date <= endDay
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        startMonth < endMonth,
                                        or_(
                                            and_(
                                                detections.month < endMonth,
                                                detections.month > startMonth
                                            ),
                                            and_(
                                                detections.month == startMonth,
                                                detections.date >= startDay
                                            ),
                                            and_(
                                                detections.month == endMonth,
                                                detections.date <= endDay
                                            )
                                        )
                                    )
                                )
                            ),
                            and_(
                                endYear > startYear,
                                or_(
                                    and_(
                                        detections.year > startYear,
                                        detections.year < endYear
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        detections.month > startMonth
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        detections.month == startMonth,
                                        detections.date >= startDay
                                    ),
                                    and_(
                                        detections.year == endYear,
                                        detections.month < endMonth
                                    ),
                                    and_(
                                        detections.year == endYear,
                                        detections.month == endMonth,
                                        detections.date <= endDay
                                    )
                                )
                            )
                        ),
                        or_(
                            and_(
                                endHour == startHour,
                                or_(
                                    and_(
                                        startMinute == endMinute,

                                        detections.hour == startHour,
                                        detections.minute == startMinute,
                                        detections.minute == endMinute,
                                        detections.second >= startSecond,
                                        detections.second <= endSecond
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        startMinute != endMinute,
                                        or_(
                                            and_(
                                                detections.minute < endMinute,
                                                detections.minute > startMinute
                                            ),
                                            and_(
                                                detections.minute == startMinute,
                                                detections.second >= startSecond
                                            ),
                                            and_(
                                                detections.minute == endMinute,
                                                detections.second <= endSecond
                                            )
                                        )
                                    )
                                )
                            ),
                            and_(
                                endHour != startHour,
                                or_(
                                    and_(
                                        detections.hour > startHour,
                                        detections.hour < endHour
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        detections.minute > startMinute
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        detections.minute == startMinute,
                                        detections.second >= startSecond
                                    ),
                                    and_(
                                        detections.hour == endHour,
                                        detections.minute < endMinute
                                    ),
                                    and_(
                                        detections.hour == endHour,
                                        detections.minute == endMinute,
                                        detections.second <= endSecond
                                    )
                                )
                            )
                        )
                    )
                ).group_by(detections.vehicle_type, detections.in_or_out
                ).with_entities(
                    detections.vehicle_type,
                    detections.in_or_out,
                    func.count().label('total_entries')
                ).all()



                marshalledStatics = []
                marshaledVehicleTypesStatics = []
                # print(vehicleTypeInOrOutEntries)

                for entry in  vehicleTypeInOrOutEntries:
                    marshaledEntry = {

                        'vehicle_type': entry.vehicle_type,
                        'status': entry.in_or_out,
                        'total': entry.total_entries
                    }
                    marshaledVehicleTypesStatics.append(marshaledEntry)



                marshalledStatics.append(marshaledVehicleTypesStatics)

                entries = detections.query.filter(
                    and_(
                        or_(
                            and_(
                                endYear == startYear,
                                or_(
                                    and_(
                                        startMonth == endMonth,
                                        detections.year == startYear,
                                        detections.month == startMonth,
                                        detections.month == endMonth,
                                        detections.date >= startDay,
                                        detections.date <= endDay
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        startMonth < endMonth,
                                        or_(
                                            and_(
                                                detections.month < endMonth,
                                                detections.month > startMonth
                                            ),
                                            and_(
                                                detections.month == startMonth,
                                                detections.date >= startDay
                                            ),
                                            and_(
                                                detections.month == endMonth,
                                                detections.date <= endDay
                                            )
                                        )
                                    )
                                )
                            ),
                            and_(
                                endYear > startYear,
                                or_(
                                    and_(
                                        detections.year > startYear,
                                        detections.year < endYear
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        detections.month > startMonth
                                    ),
                                    and_(
                                        detections.year == startYear,
                                        detections.month == startMonth,
                                        detections.date >= startDay
                                    ),
                                    and_(
                                        detections.year == endYear,
                                        detections.month < endMonth
                                    ),
                                    and_(
                                        detections.year == endYear,
                                        detections.month == endMonth,
                                        detections.date <= endDay
                                    )
                                )
                            )
                        ),
                        or_(
                            and_(
                                endHour == startHour,
                                or_(
                                    and_(
                                        startMinute == endMinute,

                                        detections.hour == startHour,
                                        detections.minute == startMinute,
                                        detections.minute == endMinute,
                                        detections.second >= startSecond,
                                        detections.second <= endSecond
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        startMinute != endMinute,
                                        or_(
                                            and_(
                                                detections.minute < endMinute,
                                                detections.minute > startMinute
                                            ),
                                            and_(
                                                detections.minute == startMinute,
                                                detections.second >= startSecond
                                            ),
                                            and_(
                                                detections.minute == endMinute,
                                                detections.second <= endSecond
                                            )
                                        )
                                    )
                                )
                            ),
                            and_(
                                endHour != startHour,
                                or_(
                                    and_(
                                        detections.hour > startHour,
                                        detections.hour < endHour
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        detections.minute > startMinute
                                    ),
                                    and_(
                                        detections.hour == startHour,
                                        detections.minute == startMinute,
                                        detections.second >= startSecond
                                    ),
                                    and_(
                                        detections.hour == endHour,
                                        detections.minute < endMinute
                                    ),
                                    and_(
                                        detections.hour == endHour,
                                        detections.minute == endMinute,
                                        detections.second <= endSecond
                                    )
                                )
                            )
                        )
                    )
                ).group_by(
                    detections.in_or_out
                ).with_entities(
                    detections.in_or_out,
                    func.count().label('total_entries')
                ).all()


                totalIn, totalOut = 0, 0
                for entry in entries:
                    if(entry.in_or_out =='IN'):
                        totalIn=entry.total_entries

                    else:
                        totalOut=entry.total_entries



                staticSummary={
                    'totalIn': totalIn,
                    'totalOut': totalOut
                }

                marshalledStatics.append(staticSummary)

                responseData={
                    'result':marshaledVehicleTypesStatics,
                    'summary':staticSummary,
                    'length':len(marshaledVehicleTypesStatics)

                }
                response = jsonify(responseData)


        return response



class addEntrySchema(Schema):
    entryDate = fields.Date(required=True)
    entryTime = fields.Time(required=True)
    status = fields.String(required=False)
    numberPlate = fields.String(required=True)
    vehicleType = fields.String(required=False)


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

api.add_resource(lastEntries, "/lastEntry")
api.add_resource(TodaySummary, "/daysummary")
api.add_resource(Search, "/Search")
api.add_resource(searchByDate, "/searchByDate")
api.add_resource(addEntry,"/addEntry")


if __name__ == "__main__":
    #changed
    app.run(debug=True, port=5002)
    print("Server is running...")

