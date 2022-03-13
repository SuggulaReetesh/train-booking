from flask import Flask, render_template, request
import json
import os
import random

app = Flask(__name__)


@app.route('/')
def Index():
    return render_template("index.html")


def getdata():
    data=[]
    if (not doesFileExists('Booking.json')):
        data=[]
        writedata(data)
        return data
    else:    
        f = open('Booking.json', "r")
        return json.loads(f.read())["Coaches"]


def writedata(data):
    coach = {
            "Coaches": data
        }
    json_object = json.dumps(coach, indent=4)
    with open("Booking.json", "w") as outfile:
            outfile.write(json_object)


@app.route('/admin/Seats/<status>', methods=['GET', 'POST'])
@app.route('/admin/Seats/<status>/<particular>')
def SeatsStatus(status,particular=None):
    data = getdata()
    bookedcount =0
    unbookedcount =0
    if(request.method == 'GET'):
        for dic in data:
                for key in dic:
                    if(key == status and particular =='booked'):
                        return ({"SeatsCount":dic[status]['SeatsCount'], 'SeatsBookedCount':dic[status]['SeatsBookedCount']})
                    elif(key==status and particular == 'unbooked'):
                         return ({"SeatsCount":dic[status]['SeatsCount'],'SeatsUnBookedCount': dic[status]['SeatsUnBookedCount']})
                    bookedcount = bookedcount + int(dic[key]['SeatsBookedCount'])
                    unbookedcount = unbookedcount + int(dic[key]['SeatsUnBookedCount'])
    if(particular == 'booked'):
        return ({'bookedSeatsOfAllCoaches':bookedcount})    
    elif(particular == 'unbooked'):
        return ({'unbookedSeatsofAllCoaches':unbookedcount})
    else:
        return ({'bookedSeatsOfAllCoaches':bookedcount, 'unbookedSeatsofAllCoaches':unbookedcount})    




@app.route('/admin', methods=['GET', 'POST'])
def AdminDashboard():
    data = getdata()
    if(request.method == 'POST'):
        seats = []
        for i in range(int(request.form.get('seats'))):
            seats.append({"bookedStatus": False,
                          "passengerName": "",
                          "bookeddate":""
                          })
        CoachId = str(request.form.get('coachtype') +
                      str(random.randint(100, 999)))
                      
        CoachDetails = {
            "CoachId": CoachId,
            "CoachType": request.form.get('coachtype'),
            "SeatsCount": request.form.get('seats'),
            "SeatsUnBookedCount": request.form.get('seats'),
            "SeatsBookedCount":0,
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

@app.route("/admin/update/<coach>/<seat>", methods=["GET"])
def updatecoach(coach,seat):
    data = getdata()
    if(request.method == 'GET'):
        found = 0
        seats = []
        for i in range(int(seat)):
            seats.append({"bookedStatus": False,
                          "passengerName": "",
                          "bookeddate":""
                          })
        for dic in data:
            for key in dic:
                if(key == coach):
                    dic[coach]['SeatDetails'] = seats
                    dic[coach]["SeatsUnBookedCount"] = seat
                    dic[coach]["SeatsCount"] = seat
                    dic[coach]["SeatsBookedCount"] = 0
                    found = 1
                    break
            if(found == 1):
                break
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
                        dic[coach]['SeatDetails'][int(seat)-1]['bookeddate'] = request.form.get('date')
                        dic[coach]['SeatsCount'] =  str(int(dic[coach]['SeatsCount']) -1)
                        dic[coach]['SeatsBookedCount'] =  str(int(dic[coach]['SeatsBookedCount']) +1)
                        dic[coach]['SeatsUnBookedCount'] =  str(int(dic[coach]['SeatsUnBookedCount']) -1)
                        break
        writedata(data)          
    return render_template("userdashboard.html", data = getdata())

def doesFileExists(filePathAndName):
    return os.path.exists(filePathAndName)

class PassengerDetails:
    Name=''
    Gender=''
    Age=''

class SeatDetails:
    bookedStatus = False
    bookedDate= ''
    passengerDetails = PassengerDetails()

class CoachDetails:
    coachId =''
    seatsCount=''
    seatDetails = SeatDetails()
    coachType=''
    SeatsBookedCount=''
    SeatsUnBookedCount=''

class Train:
    trainId=''
    noOfCoaches=''
    coachesAssigned=[]
    FromStation=''
    ToStation=''


    



if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)