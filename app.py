from flask import Flask, render_template, request
import json
import os
import random

app = Flask(__name__)


@app.route('/')
def Index():
    return render_template("index.html")


def getdata():
    f = open('Booking.json', "r")
    return json.loads(f.read())["Coaches"]


def writedata(data):
    coach = {
            "Coaches": data
        }
    json_object = json.dumps(coach, indent=4)
    with open("Booking.json", "w") as outfile:
            outfile.write(json_object)


@app.route('/admin', methods=['GET', 'POST'])
def AdminDashboard():
    if (not doesFileExists('Booking.json')):
        coach = {
            "Coaches": []
        }
        json_object = json.dumps(coach, indent=4)
        with open("Booking.json", "w") as outfile:
            outfile.write(json_object)
    data = getdata()
    if(request.method == 'POST'):
        seats = []
        for i in range(int(request.form.get('seats'))):
            seats.append({"bookedStatus": False,
                          "passengerName": ""})
        CoachId = str(request.form.get('coachtype') +
                      str(random.randint(100, 999)))
                      
        CoachDetails = {
            "CoachId": CoachId,
            "CoachType": request.form.get('coachtype'),
            "SeatsCount": request.form.get('seats'),
            "SeatDetails": seats
        }
        data.append({CoachId: CoachDetails})
        writedata(data)
    return render_template("admindashboard.html", data=data)

@app.route("/admin/delete/<id>/", methods=["GET"])
def deletecoach(id):
    data = getdata()
    if(request.method == 'GET'):
        index = 0
        found = 0
        for dic in data:
            for key in dic:
                if(key == id):
                    found = 1
                    break
            if(found == 1):
                break
            else:
                index = index+1
        data.pop(index)
        writedata(data)
    return render_template("admindashboard.html", data=data)


@app.route('/user',methods=['GET', 'POST'] )
def UserDashBoard():
    if(request.method == 'POST'):
        seatDetails = request.form.getlist('seatdetails')
        data= getdata()
        for i in seatDetails:
            coach,seat = i.split("_")
            for dic in data:
                for key in dic:
                    if(key == coach):
                        dic[coach]['SeatDetails'][int(seat)-1]['bookedStatus'] = True
                        dic[coach]['SeatDetails'][int(seat)-1]['passengerName'] = request.form.get('fname')
                        dic[coach]['SeatsCount'] =  str(int(dic[coach]['SeatsCount']) -1)
                        break
        writedata(data)          
    return render_template("userdashboard.html", data = getdata())

def doesFileExists(filePathAndName):
    return os.path.exists(filePathAndName)


class SeatDetails:
    bookedStatus = False
    bookedDate= ''
    passengerName = ''

class CoachDetails:
    coachId =''
    seatsCount=''
    seatDetails = SeatDetails()
    coachType=''

class Train:
    trainId=''
    noOfCoaches=''
    coachesAssigned=''
    From=''
    To=''
class PassengerDetails:
    Name=''
    Gender=''
    Age=''

    



if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)