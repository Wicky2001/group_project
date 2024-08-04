from flask import Flask, request,jsonify
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, validates_schema
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import and_, or_,func

from .Utilities.parsedDateAndTime import parseDateTime

# from API.Utilities.parsedDateAndTime import parseDateTime
# from Utilities import parsedDateAndTime


app = Flask(__name__)
api = Api(app)
CORS(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/vehicals"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Mysql%40123@localhost/detections?charset=utf8mb4"

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

def filterDetections(dateTimeInfo):
    return detections.query.filter(
        and_(
            or_(
                and_(
                    dateTimeInfo['endYear'] == dateTimeInfo['startYear'],
                    or_(
                        and_(
                            dateTimeInfo['startMonth'] == dateTimeInfo['endMonth'],
                            detections.year == dateTimeInfo['startYear'],
                            detections.month == dateTimeInfo['startMonth'],
                            detections.month == dateTimeInfo['endMonth'],
                            detections.date >= dateTimeInfo['startDay'],
                            detections.date <= dateTimeInfo['endDay']
                        ),
                        and_(
                            detections.year == dateTimeInfo['startYear'],
                            dateTimeInfo['startMonth'] < dateTimeInfo['endMonth'],
                            or_(
                                and_(
                                    detections.month < dateTimeInfo['endMonth'],
                                    detections.month > dateTimeInfo['startMonth']
                                ),
                                and_(
                                    detections.month == dateTimeInfo['startMonth'],
                                    detections.date >= dateTimeInfo['startDay']
                                ),
                                and_(
                                    detections.month == dateTimeInfo['endMonth'],
                                    detections.date <= dateTimeInfo['endDay']
                                )
                            )
                        )
                    )
                ),
                and_(
                    dateTimeInfo['endYear'] > dateTimeInfo['startYear'],
                    or_(
                        and_(
                            detections.year > dateTimeInfo['startYear'],
                            detections.year < dateTimeInfo['endYear']
                        ),
                        and_(
                            detections.year == dateTimeInfo['startYear'],
                            detections.month > dateTimeInfo['startMonth']
                        ),
                        and_(
                            detections.year == dateTimeInfo['startYear'],
                            detections.month == dateTimeInfo['startMonth'],
                            detections.date >= dateTimeInfo['startDay']
                        ),
                        and_(
                            detections.year == dateTimeInfo['endYear'],
                            detections.month < dateTimeInfo['endMonth']
                        ),
                        and_(
                            detections.year == dateTimeInfo['endYear'],
                            detections.month == dateTimeInfo['endMonth'],
                            detections.date <= dateTimeInfo['endDay']
                        )
                    )
                )
            ),
            or_(
                and_(
                    dateTimeInfo['endHour'] == dateTimeInfo['startHour'],
                    or_(
                        and_(
                            dateTimeInfo['startMinute'] == dateTimeInfo['endMinute'],
                            detections.hour == dateTimeInfo['startHour'],
                            detections.minute == dateTimeInfo['startMinute'],
                            detections.minute == dateTimeInfo['endMinute'],
                            detections.second >= dateTimeInfo['startSecond'],
                            detections.second <= dateTimeInfo['endSecond']
                        ),
                        and_(
                            detections.hour == dateTimeInfo['startHour'],
                            dateTimeInfo['startMinute'] != dateTimeInfo['endMinute'],
                            or_(
                                and_(
                                    detections.minute < dateTimeInfo['endMinute'],
                                    detections.minute > dateTimeInfo['startMinute']
                                ),
                                and_(
                                    detections.minute == dateTimeInfo['startMinute'],
                                    detections.second >= dateTimeInfo['startSecond']
                                ),
                                and_(
                                    detections.minute == dateTimeInfo['endMinute'],
                                    detections.second <= dateTimeInfo['endSecond']
                                )
                            )
                        )
                    )
                ),
                and_(
                    dateTimeInfo['endHour'] != dateTimeInfo['startHour'],
                    or_(
                        and_(
                            detections.hour > dateTimeInfo['startHour'],
                            detections.hour < dateTimeInfo['endHour']
                        ),
                        and_(
                            detections.hour == dateTimeInfo['startHour'],
                            detections.minute > dateTimeInfo['startMinute']
                        ),
                        and_(
                            detections.hour == dateTimeInfo['startHour'],
                            detections.minute == dateTimeInfo['startMinute'],
                            detections.second >= dateTimeInfo['startSecond']
                        ),
                        and_(
                            detections.hour == dateTimeInfo['endHour'],
                            detections.minute < dateTimeInfo['endMinute']
                        ),
                        and_(
                            detections.hour == dateTimeInfo['endHour'],
                            detections.minute == dateTimeInfo['endMinute'],
                            detections.second <= dateTimeInfo['endSecond']
                        )
                    )
                )
            )
        )
    )




class TodaySummary(Resource):
    def get(self):
        today = datetime.now()
        today_entries = detections.query.filter(
            detections.year == today.year,
            db.cast(detections.month, db.Integer) == today.month,
            db.cast(detections.date, db.Integer) == today.day
        ).all()

        if not today_entries:
            return {'message': 'No entries found for today'},200

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

        return summary, 200


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

        dateTimeInfo = parseDateTime(startDate, endDate, startTime, endTime)

        if  not statics_bool:
            entries = filterDetections(dateTimeInfo).all()

            marshaledEntries = []
            if vehicleType.lower() == "all":
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
                    print("hhhhh")
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
                'result': marshaledEntries,
                'count': len(marshaledEntries),

            }
            response = jsonify(response_data)
        else:

            vehicleTypeInOrOutEntries = filterDetections(dateTimeInfo).group_by(
                detections.vehicle_type, detections.in_or_out
            ).with_entities(
                detections.vehicle_type,
                detections.in_or_out,
                func.count().label('total_entries')
            ).all()

            marshaledVehicleTypesStatics = [
                {
                    'vehicle_type': entry.vehicle_type,
                    'status': entry.in_or_out,
                    'total': entry.total_entries
                }
                for entry in vehicleTypeInOrOutEntries
            ]

            totalInOutEntries = filterDetections(dateTimeInfo).group_by(
                detections.in_or_out
            ).with_entities(
                detections.in_or_out,
                func.count().label('total_entries')
            ).all()

            totalIn, totalOut = 0, 0
            for entry in totalInOutEntries:
                if entry.in_or_out == 'IN':
                    totalIn = entry.total_entries
                else:
                    totalOut = entry.total_entries

            staticSummary = {
                'totalIn': totalIn,
                'totalOut': totalOut
            }

            responseData = {
                'result': marshaledVehicleTypesStatics,
                'summary': staticSummary,
                'length': len(marshaledVehicleTypesStatics)
            }
            response = jsonify(responseData)

        return response



class addEntrySchema(Schema):
    entryDate = fields.Date(required=True)
    entryTime = fields.Time(required=True)
    status = fields.String(required=True)
    numberPlate = fields.String(required=True)
    vehicleType = fields.String(required=True)

class addEntry(Resource):
    def post(self):
        if not request.is_json:
            return {'message': 'Content-Type must be application/json'}, 400  # Bad Request
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
            in_or_out=data.get('status').upper()

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

class sortTrafficSchema(Schema):
    hour = fields.Boolean(required=False)
    month = fields.Boolean(required=False)
    year = fields.Boolean(required=False)

    @validates_schema
    def validate_params(self, data, **kwargs):
        if not any(data.values()):
            raise ValidationError("At least one  field is required")

        true_count = sum(value for value in data.values())
        if true_count > 1:
            raise ValidationError("Only one query parameter can be true at a time")

class sortTraffic(Resource):
    def get(self):
        # Parse and validate query parameters
        schema = sortTrafficSchema()
        try:
            args = schema.load(request.args)
        except ValidationError as err:
            return {"message": err.messages}, 400


        requestObjWithParams = request.args.to_dict()

        true_params = [key for key, value in requestObjWithParams.items() if value.lower() == 'true']

        grouped_data = detections.query.group_by(getattr(detections, true_params[0]),detections.in_or_out).with_entities(
        getattr(detections, true_params[0]),detections.in_or_out, func.count().label("total")).all()

        # formatted_data = [(row[0], row[1],row[2]) for row in grouped_data]
        summary = []
        for row in grouped_data:
            summary.append({
                true_params[0]: row[0],
                "status": row[1],
                "total": row[2]
            })

        return {
            "summary": summary
        }, 200

api.add_resource(lastEntries, "/lastEntries")
api.add_resource(TodaySummary, "/TodaySummary")
api.add_resource(Search, "/Search")
api.add_resource(searchByDate, "/searchByDate")
api.add_resource(addEntry,"/addEntry")
api.add_resource(sortTraffic,"/sortTraffic")


if __name__ == "__main__":
    #changed
    app.run(debug=True, port=5002)
    print("Server is running...")

