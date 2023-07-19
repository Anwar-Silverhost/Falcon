from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
import requests
import csv
from django.http import JsonResponse

import pandas as pd

from django.urls import reverse
import qrcode
from django.conf import settings
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone


#         Username     Password
# ------------------------------
# admin =  falcon       falcon



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['Adm_id'] = user.id
            return redirect('admin_dashboard')

        if user_registration.objects.filter( username=username, password=password).exists():
            user = user_registration.objects.get(username = request.POST['username'],password = request.POST['password'])
            request.session['User_id'] = user.id
            return redirect('user_dashboard')
        else:
            return render(request,'login.html',{'error':'INVALID CREDENTIALS'})
    else:
        return render(request, 'login.html')

def admin_navbar(request):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)
        return render(request,'admin_navbar.html',{'admin':admin}) 
    else:
        return redirect('/')
 


def admin_dashboard(request):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)

        flight = flight_charts.objects.all()
        aircraft_count = Aircraft.objects.all().count()
        flight_chart = flight_charts.objects.all().order_by('-id')[:10]




        return render(request,'admin_dashboard.html',{'admin':admin,'flight':flight,'aircraft_count':aircraft_count,'flight_chart':flight_chart}) 
    else:
        return redirect('/')








def admin_user(request):
    if request.method == 'POST':
        firstname = request.POST['fn']
        lastname = request.POST['ln']
        username = request.POST['un']
        password = request.POST['pswd']
        email = request.POST['email']
        phonenumber = request.POST['ph']
        dateofbirth = request.POST['dob']
        gender = request.POST['gen']
        user = user_registration(firstname=firstname,lastname=lastname,username=username,password=password,email=email,phone=phonenumber,date_of_birth=dateofbirth,gender=gender)
        user.save()

        logsave=Logs()
        logsave.texts = 'New User Successfully Added by the Administrator'
        logsave.added_date_time = timezone.now()
        logsave.save()

        return redirect('admin_user')

    if 'Adm_id' in request.session:
            if request.session.has_key('Adm_id'):
                    Adm_id = request.session['Adm_id']
            admin = User.objects.filter(id=Adm_id)

    user = user_registration.objects.all()
    return render(request,'admin_user.html',{'user':user,'admin':admin})

def admin_airport(request):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)

        Airport = airport.objects.all()
        return render(request,'admin_airport.html',{'admin':admin,'Airport':Airport}) 
    else:
        return redirect('/')


def airport_save(request):
    if request.method == 'POST':
        icao_code = request.POST.get('icao_code')
        iata_code = request.POST.get('iata_code')
        airport_name = request.POST.get('airport_name')
        Airport = icao_code+" ("+iata_code+" - "+airport_name+")"

        air = airport()
        air.icao_code = icao_code
        air.iata_code = iata_code
        air.airport_name = airport_name
        air.airport = Airport
        air.save()

        logsave=Logs()
        logsave.texts = 'New Airport Successfully Added by the Administrator'
        logsave.added_date_time = timezone.now()
        logsave.save()


        return redirect(admin_airport)

def admin_flight(request):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)

        air = Aircraft.objects.all()

        
        return render(request,'admin_flight.html',{'admin':admin,'air':air}) 
    else:
        return redirect('/')

def admin_flight_save(request):
    if request.method == 'POST':
        airline_name = request.POST['f_n']
        manufacture = request.POST['manufacture']
        model = request.POST['model']
        reg_no = request.POST['r_n']
        year = request.POST['y_o_m']
        seat = request.POST['s_c']
        fuel = request.POST['f_c']
        engin = request.POST['e_t']
        classes = request.POST['t_c']

        air = Aircraft()
        air.name=airline_name
        air.manufacturer=manufacture
        air.model=model
        air.registration_number=reg_no
        air.year_of_manufacture=year
        air.seating_capacity=seat
        air.fuel_capacity=fuel
        air.engine_type=engin
        air.class_=classes
        air.save()


        logsave=Logs()
        logsave.texts = 'New Flight Added Admin'
        logsave.added_date_time = timezone.now()
        logsave.save()


    return redirect("admin_flight")












#==================== AJAX ===============
def validate(request):

    if request.method == 'GET':
        nick_name = request.GET['nick_name']
        if user_registration.objects.filter(username=nick_name).exists():
            return HttpResponse("Success!")

def airport_validate(request):
    nick_name = request.GET.get('nick_name')

    url = 'https://raw.githubusercontent.com/6285anwar/airports/main/airports.dat'
    response = requests.get(url)

    if response.status_code == 200:
        content = response.content.decode('utf-8').splitlines()
        reader = csv.reader(content)
        search_query = nick_name
        for row in reader:
            iata_code = row[4]
            icao_code = row[5]
            airport_name = row[1]
            if search_query.upper() == iata_code or search_query.upper() == icao_code or search_query.lower() in airport_name.lower():
                data = {
                    'icao_code': icao_code,
                    'iata_code': iata_code,
                    'airport_name': airport_name
                }
                return JsonResponse(data)
        else:
            print("No airport found for the provided search query.")
            return JsonResponse({'error': 'No airport found'})
    else:
        print("Failed to fetch the airport data.")
        
    
    return JsonResponse({'error': 'No airport found'})  # Return an error response if no airport is found




def airport_save_ajax(request):
    if request.method == 'POST':
        icao_code = request.POST.get('icao_code')
        iata_code = request.POST.get('iata_code')
        airport_name = request.POST.get('airport_name')
        Airport = icao_code+" ("+iata_code+" - "+airport_name+")"

        air = airport()
        air.icao_code = icao_code
        air.iata_code = iata_code
        air.airport_name = airport_name
        air.airport = Airport
        air.save()
        response_data = {
            'message': 'Data received successfully'
        }
        
        return JsonResponse(response_data)



def real_time_counts(request):
    scheduled = 'scheduled'
    departure = 'departure'

    scheduled_flights_count = flight_charts.objects.filter(flight_status=scheduled).count() 
    departure_flights_count = flight_charts.objects.filter(flight_status=departure).count()
    data = {
        'scheduled_flights_count': scheduled_flights_count,'departure_flights_count':departure_flights_count
    }

    return JsonResponse(data)




def import_file(request):
    if request.method == 'POST' and request.FILES.get('file-import') and request.POST.get('flight_chart_id'):
        flight_chart_id = request.POST['flight_chart_id']
        file = request.FILES['file-import']
        print(file)
        print('its working')

        df = pd.read_excel(file)
        df = df.fillna('')
        for index, row in df.iterrows():
            print('its not workd')
            seqno = row['Seq No']
            sex = row['Sex']
            surname = row['Surname']
            firstname = row['FirstName']
            date_ob = row['DateofBirth']
            nation = row['Nationality']
            issuingcountry = row['IssuingCountry']
            dc_no = row['Document Number']
            dc_type = row['DocumentType']
            dc_exp = row['Document Expiry']
            address = row['Address']
            seat = row['Seat']

            seat_class = row['Class']
            crew_or_pax = row['Crew/Pax']
            onward_flight = row['Onward Flight']
            destination = row['Destination']
            final_destination = row['Final Destination']
            company = row['Company']
            Check_In_Time = row['Check In Time']
            Board_Time = row['Board Time']
            Offload_Time = row['Offload Time']
            Special_Notes = row['Special Notes']

            # print('seqno',seqno)
            # print('sex',sex)
            # print('surname',surname)
            # print('firstname',firstname)
            # print('date_ob',date_ob)
            # print('nation',nation)
            # print('issuingcountry',issuingcountry)
            # print('dc_no',dc_no)
            # print('dc_type',dc_type)
            # print('dc_exp',dc_exp)
            # print('address',address)
            # print('seat',seat)
            # print('seat_class',seat_class)
            # print('crew_or_pax',crew_or_pax)
            # print('onward_flight',onward_flight)
            # print('destination',destination)
            # print('final_destination',final_destination)
            # print('company',company)
            # print('Check_In_Time',Check_In_Time)
            # print('Board_Time',Board_Time)
            # print('Offload_Time',Offload_Time)
            # print('Special_Notes',Special_Notes)
            # print('-------------')


    




            f_id = flight_charts.objects.get(id=flight_chart_id)
            pass_db = Passenger_db()

            pass_db.seq_no = seqno
            pass_db.gender = sex
            pass_db.surname = surname
            pass_db.fullname = firstname
            pass_db.date_of_birth = date_ob
            pass_db.nationality = nation
            pass_db.issuingcountry = issuingcountry
            pass_db.documentnumber = dc_no
            pass_db.documenttype = dc_type
            pass_db.documentexpiry = dc_exp 
            pass_db.address = address
            pass_db.seat_no = seat
            pass_db.seat_class = seat_class
            pass_db.crew_or_pax = crew_or_pax
            pass_db.onward_flight = onward_flight
            pass_db.destination = destination
            pass_db.final_destination = final_destination
            pass_db.company = company
            pass_db.check_in = Check_In_Time
            pass_db.board_time = Board_Time
            pass_db.offload_time = Offload_Time
            pass_db.special_notes = Special_Notes

            pass_db.flight_id = f_id
            pass_db.save()


        logsave=Logs()
        logsave.texts = 'Passangers added to '+ f_id.flight_number
        logsave.added_date_time = timezone.now()
        logsave.save()




        return JsonResponse({'message': 'File uploaded successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)



def checkin_addpassorid(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        surname = request.POST.get('surname')
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        paxtype = request.POST.get('paxtype')
        documenttype = request.POST.get('documenttype')
        documentnumber = request.POST.get('documentnumber')
        documentexp = request.POST.get('documentexp')
        combany = request.POST.get('combany')


        passenger = Passenger_db.objects.get(id=id)
        passenger.fullname = fullname
        passenger.surname = surname
        passenger.gender = gender
        passenger.pax_type = paxtype
        passenger.documenttype = documenttype
        passenger.documentnumber = documentnumber
        passenger.documentexpiry = documentexp
        passenger.combany = combany
        passenger.save()

        return JsonResponse({'message': 'Data received successfully'})

def checkin_addpassweight(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        passweight = request.POST.get('pass_weight')
        edit = request.POST.get('edit')

        if edit == 'EDIT':
            passenger = Passenger_db.objects.get(id=id)
            passenger.pax_weight = passweight
            passenger.save()
            return redirect(str('/passenger_edit/'+id))

        
        else:
            passenger = Passenger_db.objects.get(id=id)
            passenger.pax_weight = passweight
            passenger.save()
            return JsonResponse({'message': 'Data received successfully'})




def checkin_holdbagweight(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        holdbagweight = request.POST.get('holdbagweight')

        pas = Passenger_db.objects.get(id=id)
        pass_id = pas
        fly_id = pas.flight_id

        pass_bag = Passenger_lagage()
        pass_bag.flight_id = fly_id
        pass_bag.passenger = pass_id
        pass_bag.bag_type = 'hold'
        pass_bag.weight = holdbagweight
        pass_bag.save()

        
        pass_bag.tag =str(pass_bag.id).zfill(10)
        pass_bag.save()

        return JsonResponse({'message': 'Data received successfully'})

def checkin_handbagweight(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        handbagweight = request.POST.get('handbagweight')

        pas = Passenger_db.objects.get(id=id)
        pass_id = pas
        fly_id = pas.flight_id

        pass_bag = Passenger_lagage()
        pass_bag.flight_id = fly_id
        pass_bag.passenger = pass_id
        pass_bag.bag_type = 'hand'
        pass_bag.weight = handbagweight
        pass_bag.save()

        
        pass_bag.tag =str(pass_bag.id).zfill(10)
        pass_bag.save()

        return JsonResponse({'message': 'Data received successfully'})



def checkin_holdbagremove(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print(id)
        pass_id = Passenger_lagage.objects.get(id=id)
        pass_id.delete()

        return JsonResponse({'message': 'Data received successfully'})

def checkin_handbagremove(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print(id)
        pass_id = Passenger_lagage.objects.get(id=id)
        pass_id.delete()

        return JsonResponse({'message': 'Data received successfully'})




def pass_flight_seat(request):
    if request.method == 'POST':
        seat = request.POST.get('button_value')
        pass_id = request.POST.get('pass_id')

        passen = Passenger_db.objects.get(id=pass_id)
        if passen.seat_no != '':
            seet = passen.seat_no
            flightz1=passen.flight_id
            f_seats = 's_'+seet
            pass_fly = Flight_seat.objects.get(flight_id=flightz1.id)
            setattr(pass_fly, f_seats, '0')
            pass_fly.save()

        passen.seat_no = seat
        passen.save()

        flightz=passen.flight_id

        seats = 's_'+seat
        column_name = Flight_seat._meta.get_field(seats).column
        print(column_name)

        F_seat = Flight_seat.objects.get(flight_id=flightz.id)
        setattr(F_seat, column_name, pass_id)  
        F_seat.save()
        


        return JsonResponse({'message': 'Data received successfully','seat':seat})



def boarding_pass(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')

        user = user_registration.objects.filter(id=User_id)
        passenger = Passenger_db.objects.filter(id=id)
        p = Passenger_db.objects.get(id=id)

        # p.qrcode.delete()


        if not p.qrcode:
            qr = qrcode.QRCode(
                        version=2,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=12,
                        border=1,
                    )
            qr.add_data(p.qrid)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Generate a unique filename for the QR code image
            filename = f"qrcode_{p.id}.png"
            file_path = os.path.join(settings.MEDIA_ROOT, "qrcodes", filename)

            # Save the QR code image to a temporary buffer
            buffer = BytesIO()
            qr_image.save(buffer)
            buffer.seek(0)

            # Create a ContentFile from the buffer
            content_file = ContentFile(buffer.read())

            # Assign the content file to the 'qrcode' field of the Passenger_db model
            p.qrcode.save(filename, content_file)
            p.save()




    # return render(request,'user/BOARDING_PASS.html',{'user':user,'passenger':passenger})
    return render(request,'user/Boarding-pass.html',{'user':user,'passenger':passenger})




























































































#======================  User Side =====================

def user_navbar(request):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')

        user = user_registration.objects.filter(id=User_id)
        return render(request,'user/user_navbar.html',{'user':user})
    else:
        return redirect('/')

def user_dashboard(request):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')

        user = user_registration.objects.filter(id=User_id)

        return render(request,'user/user_dashboard.html',{'user':user})
    else:
        return redirect('/')

def user_logout(request):
    if 'User_id' in request.session:
        request.session.flush()
    return redirect('/')

#--------------------- flight administration ---------------

def flight_administration(request):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        
        user = user_registration.objects.filter(id=User_id)
        airports = airport.objects.all()

        flight = flight_charts.objects.filter(flight_status__in=['open', 'scheduled'])


        air = Aircraft.objects.all()

        return render(request,'user/flight_administration.html',{'user':user,'airports':airports,'flight':flight,'air':air})
    else:
        return redirect('/')

def flight_save(request):
    if request.method == 'POST':
        airline = request.POST["airline"]
        flight_no = request.POST["flight_number"]
        aircraft_reg = request.POST["a_r"]
        from_airport = request.POST["from_airport"]
        to_airport = request.POST["to_airport"]
        departure_date = request.POST["from_date"]
        departure_time = request.POST["from_time"]
        arrival_date = request.POST["to_date"]
        arrival_time = request.POST["to_time"]
        flight_category = request.POST["f_c"]
        fligth_type = request.POST["f_t"]
        v1 = request.POST["v1"]
        v2 = request.POST["v2"]
        v3 = request.POST["v3"]

        fa = airport.objects.get(id=from_airport)
        ta = airport.objects.get(id=to_airport)

        reg = Aircraft.objects.get(id=aircraft_reg)

        

        fc = flight_charts()
        fc.operator = airline
        fc.flight_number = flight_no
        fc.aircraft_reg = reg
        fc.departure_airport_from = fa
        fc.arrival_airport_to = ta
        fc.departure_time = f"{departure_date} {departure_time}:00"
        fc.arrival_time = f"{arrival_date} {arrival_time}:00"
        fc.departure_date = departure_date
        fc.arrival_date = arrival_date
        fc.flight_category = flight_category
        fc.flight_type = fligth_type
        fc.Via1 = v1
        fc.Via2 = v2
        fc.Via3 = v3


        fc.flight_status = 'scheduled'
        fc.flight_passengers = '0'
        fc.task_status = '0'

        fc.flight_passengers_check_in = '0'
        fc.flight_passengers_to_check_in = '0'

        fc.save()

        f_seat = Flight_seat()
        f_seat.flight_id = fc
        f_seat.save()


        logsave=Logs()
        logsave.texts = 'New Flight Added'
        logsave.added_date_time = timezone.now()
        logsave.save()






        


        # flight = flight_charts()

        # flight.airline_name=air
        # flight.flight_number=fligth_no
        # flight.aircraft_reg=aircraft_reg
        # flight.departure_airport_from=fa
        # flight.arrival_airport_to=ta

        # # flight.departure_date=departure_date
        # # flight.departure_time=departure_time
        # # flight.arrival_date=arrival_date
        # # flight.arrival_time=arrival_time
        # flight.departure_date = departure_date
        # flight.departure_time = f"{departure_date} {departure_time}:00"
        # flight.arrival_date = arrival_date
        # flight.arrival_time = f"{arrival_date} {arrival_time}:00"
        # flight.flight_category=flight_category
        # flight.flight_type=fligth_type
        # flight.v1=v1
        # flight.v2=v2
        # flight.v3=v3
        # flight.flight_status = 'scheduled'
        # flight.flight_passengers = '0'
        # flight.task_status = '0'

        # flight.save()



    return redirect(flight_administration)


def flight_Passengers_Crew(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        
        user = user_registration.objects.filter(id=User_id)
        # airports = airport.objects.all()
        # flight = flight_charts.objects.all().order_by("-id")

      

        flight_id = flight_charts.objects.get(id=id)
        
        id_f=flight_id.id
        passenger = Passenger_db.objects.filter(flight_id=id_f)
        


        flight_id_count = flight_charts.objects.get(id=id)
        passenger_count = Passenger_db.objects.filter(flight_id=id_f).count()
        flight_id_count.flight_passengers=passenger_count
        flight_id_count.flight_passengers_to_check_in = passenger_count
        flight_id_count.save()


        # pass_count = Passenger_db.objects.filter(flight_id=id_f).count()

        # flight_id.flight_passengers = pass_count
        # flight_id.save()





        return render(request,'user/flight_Passengers_Crew.html',{'user':user,'flight_id':flight_id,'passenger':passenger})
    else:
        return redirect('/')



def check_in(request):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        flight_chart = flight_charts.objects.all()

        f = flight_charts.objects.all()
        for fl in f:
            count = Passenger_db.objects.filter(flight_id = fl).count()
            fl.flight_passengers_check_in = Passenger_db.objects.filter(flight_id = fl,check_in='1').count()
            fl.flight_passengers_to_check_in = count - (Passenger_db.objects.filter(flight_id = fl,check_in='1').count())
            fl.save()
            


            



        return render(request,'user/check-in.html',{'user':user,'flight_chart':flight_chart})
    else:
        return redirect('/')


# FLIGHT PASSANGER CHECKIN
def flight_check_in(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        flight_id = flight_charts.objects.get(id=id)
        flight_id.flight_status = 'open'
        flight_id.save()

        if Logs.objects.filter(texts=flight_id.flight_number+' is open').exists():
            print('already exist')
        else: 
            logsave=Logs()
            logsave.texts = flight_id.flight_number+' is open'
            logsave.added_date_time = timezone.now()
            logsave.save()
     

        flight = flight_charts.objects.get(id=id)

        flight_pass = Passenger_db.objects.filter(flight_id=flight)
        # flight_pass = Passenger_db.objects.filter(flight_id=flight).filter(check_in = '')


        for f in flight_pass:
            pl = sum(float(luggage.weight) for luggage in Passenger_lagage.objects.filter(passenger=f.id, bag_type='hold') if luggage.weight)
            ph = sum(float(luggage.weight) for luggage in Passenger_lagage.objects.filter(passenger=f.id, bag_type='hand') if luggage.weight)
            f.bag_weight = pl
            f.hand_bag = ph
            f.save()

        
        f = flight_charts.objects.all()
        for fl in f:
            count = Passenger_db.objects.filter(flight_id = fl).count()
            fl.flight_passengers_check_in = Passenger_db.objects.filter(flight_id = fl,check_in='1').count()
            fl.flight_passengers_to_check_in = count - (Passenger_db.objects.filter(flight_id = fl,check_in='1').count())
            fl.save()


        fly_seat = Flight_seat.objects.filter(flight_id=flight)
            





        return render(request,'user/flight_check-in.html',{'user':user,'flight':flight,'flight_pass':flight_pass,'fly_seat':fly_seat})
    else:
        return redirect('/')


def passenger_checkin(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        passenger = Passenger_db.objects.get(id=id)


        if passenger.qrid == '0':
            passenger.qrid = "FA" + \
                str(passenger.id).zfill(5)
            passenger.save()
           
        bags = Passenger_lagage.objects.filter(passenger=passenger).filter(bag_type='hold')
        bags_count = Passenger_lagage.objects.filter(passenger=passenger).filter(bag_type='hold').count()
        handbags = Passenger_lagage.objects.filter(passenger=passenger).filter(bag_type='hand')
        handbags_count = Passenger_lagage.objects.filter(passenger=passenger).filter(bag_type='hand').count()
        return render(request,'user/passenger_checkin.html',{'user':user,'passenger':passenger,'bags':bags,'bags_count':bags_count,'handbags':handbags,'handbags_count':handbags_count})

    else:
        return redirect('/')
def passenger_edit(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        passenger = Passenger_db.objects.filter(id=id)


        return render(request,'user/passenger_edit.html',{'user':user,'passenger':passenger})
    else:
        return redirect('/')


def passenger_seat(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        passenger = Passenger_db.objects.get(id=id)
        p_id = passenger.id
        print(p_id)
        fliy = passenger.flight_id

        f_seat = Flight_seat.objects.filter(flight_id=fliy)

        pass_seats = passenger.seat_no
        print(pass_seats)


        return render(request,'user/passenger_seat.html',{'user':user,'passenger':passenger,'f_seat':f_seat,'p_id':p_id,'pass_seats': pass_seats})
    else:
        return redirect('/')
def passenger_remove_seat(request,id):
    passenger = Passenger_db.objects.get(id=id)
    seat = passenger.seat_no
    passenger.seat_no = ''
    passenger.save()
    f_id = passenger.flight_id
    f_seats = 's_'+seat
    pass_fly = Flight_seat.objects.get(flight_id=f_id)
    setattr(pass_fly, f_seats, '0')
    pass_fly.save()

    print('removed')
    logsave=Logs()
    logsave.texts = passenger.fullname+' Seat Removed'
    logsave.added_date_time = timezone.now()
    logsave.save()
    return redirect('/passenger_seat/'+str(id))

    



def passenger_boarding_pass(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        passenger = Passenger_db.objects.filter(id=id)
        passenger2 = Passenger_db.objects.get(id=id)


        bag_count = Passenger_lagage.objects.filter(passenger=id).count()
        pas = Passenger_db.objects.get(id=id)
        pas.bags = bag_count
        pas.save()
       


        return render(request,'user/passenger_boarding_pass.html',{'user':user,'passenger':passenger,'passenger2':passenger2})
    else:
        return redirect('/')

def passenger_boardingpass_collect_and_gotochekinpage(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        passenger = Passenger_db.objects.get(id=id)

        passenger.check_in = '1'
        passenger.status = '1'

        passenger.save()

        fly = passenger.flight_id.id
        print(fly)

        logsave=Logs()
        logsave.texts = passenger.fullname+' Checkin Completed'
        logsave.added_date_time = timezone.now()
        logsave.save()

        return redirect(reverse('flight_check_in', args=[fly]))








def flight_details(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        fly = flight_charts.objects.filter(id=id)
        flight = flight_charts.objects.get(id=id)

        flight_pass = Passenger_db.objects.filter(flight_id=flight)

        return render(request,'user/flight_details.html',{'user':user,'fly':fly,'flight_pass':flight_pass})
    else:
        return redirect('/')







def logs(request):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)
        logs = Logs.objects.all()

        return render(request,'user/logs.html',{'user':user,'logs':logs})
    else:
        return redirect('/')




def flight_reports(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        fly = flight_charts.objects.filter(id=id)
        passe = Passenger_db.objects.filter(flight_id=id).filter(check_in=1)
        check_pass_count = passe.count()

        return render(request,'user/flight_reports.html',{'user':user,'fly':fly,'passe':passe,'check_pass_count':check_pass_count})
    else:
        return redirect('/')


def flight_status_change(request,id):
    fly = flight_charts.objects.get(id=id)
    print(fly.flight_number)

    if request.method == "POST":
        status = request.POST["status"]
        print(status)
        fly.flight_status = status
        fly.save()
    return redirect(flight_administration)



def passanger_board(request,id):
    pas = Passenger_db.objects.get(id=id)
    pas.status = '100'
    pas.save()

    logsave=Logs()
    logsave.texts = pas.fullname+' is boarded'
    logsave.added_date_time = timezone.now()
    logsave.save()



    return redirect('/passenger_edit/'+str(id))

def passanger_deboard(request,id):
    pas = Passenger_db.objects.get(id=id)
    pas.status = '1'
    pas.save()

    logsave=Logs()
    logsave.texts = pas.fullname+' is deboarded'
    logsave.added_date_time = timezone.now()
    logsave.save()



    return redirect('/passenger_edit/'+str(id))






def scanner(request):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        flight = flight_charts.objects.filter(flight_status = 'finalized')

        return render(request,'user/SCANNER.html',{'user':user,'flight':flight})
    else:
        return redirect('/')


def scan_to_board(request,id):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)

        flight = flight_charts.objects.filter(id=id)
        passe = Passenger_db.objects.filter(flight_id = id)
       


        return render(request,'user/SCANTOBOARD.html',{'user':user,'passe':passe})
    else:
        return redirect('/')


def passboard_idcheck(request,qrid):
    passe = Passenger_db.objects.get(qrid = qrid)
    if passe.status == '1':
        passe.status = '100'
        passe.board_dateandtime = timezone.now()
        passe.save()
    return HttpResponse("Success!")
    



def user_settings(request):
    if 'User_id' in request.session:
        if request.session.has_key('User_id'):
            User_id = request.session['User_id']
        else:
            return redirect('/')
        user = user_registration.objects.filter(id=User_id)
        return render(request,'user/user_settings.html',{'user':user})
    else:
        return redirect('/')


    