from django.db import models



class user_registration(models.Model):
    firstname = models.CharField(max_length=240, null=True)
    lastname = models.CharField(max_length=240, null=True)
    username = models.CharField(max_length=240, null=True)
    email = models.EmailField(max_length=240, null=True)
    password = models.CharField(max_length=240, null=True)
    phone = models.CharField(max_length=240, null=True)
    gender = models.CharField(max_length=240, null=True)
    date_of_birth = models.CharField(max_length=240, null=True)
    

    def __str__(self):
        return self.firstname


class airport(models.Model):
    airport = models.CharField(max_length=240, null=True)
    airport_name = models.CharField(max_length=240, null=True)
    iata_code = models.CharField(max_length=240, null=True)
    icao_code = models.CharField(max_length=240, null=True)
    

    def __str__(self):
        return self.airport_name
    
class Aircraft(models.Model):
    name = models.CharField(max_length=240, null=True)
    manufacturer = models.CharField(max_length=240, null=True)
    model = models.CharField(max_length=240, null=True)
    registration_number = models.CharField(max_length=240, null=True)
    year_of_manufacture = models.CharField(max_length=240, null=True)
    seating_capacity = models.CharField(max_length=240, null=True)
    classes = models.CharField(max_length=240, null=True)
    fuel_capacity = models.CharField(max_length=240, null=True)
    engine_type = models.CharField(max_length=240, null=True)

    status = models.CharField(max_length=240, null=True)
    flight_status = models.CharField(max_length=240, null=True)
    



    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.registration_number})"


 


class flight_charts(models.Model):
    operator = models.CharField(max_length=240, null=True)
    flight_number = models.CharField(max_length=240, null=True)
    aircraft_reg = models.ForeignKey(Aircraft, on_delete=models.CASCADE, null=True)

    departure_airport_from = models.ForeignKey(airport, on_delete=models.CASCADE, related_name='departure_flights', null=True)
    arrival_airport_to = models.ForeignKey(airport, on_delete=models.CASCADE, related_name='arrival_flights', null=True)


    # departure_airport = models.CharField(max_length=240, null=True)
    # arrival_airport = models.CharField(max_length=240, null=True)
    
    # departure_time = models.CharField(max_length=240, null=True)
    # arrival_time = models.CharField(max_length=240, null=True)
    # departure_date = models.CharField(max_length=240, null=True)
    # arrival_date = models.CharField(max_length=240, null=True)



    departure_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)
    departure_date = models.DateField(null=True)
    arrival_date = models.DateField(null=True)

    flight_category = models.CharField(max_length=240, null=True)
    flight_type = models.CharField(max_length=240, null=True)
    Via1 = models.CharField(max_length=240, null=True)
    Via2 = models.CharField(max_length=240, null=True)
    Via3 = models.CharField(max_length=240, null=True)

    flight_status = models.CharField(max_length=240, null=True)
    flight_passengers = models.CharField(max_length=240, null=True)
    task_status = models.CharField(max_length=240, null=True)

    flight_passengers_check_in = models.CharField(max_length=240, null=True)
    flight_passengers_to_check_in = models.CharField(max_length=240, null=True)





    def __str__(self):
            return self.flight_number




class Passenger_db(models.Model):
    flight_id = models.ForeignKey(flight_charts, on_delete=models.CASCADE,null=True)
    fullname = models.CharField(max_length=240, null=True)
    surname = models.CharField(max_length=240, null=True)
    gender = models.CharField(max_length=240, null=True)
    date_of_birth = models.CharField(max_length=240, null=True)
    status = models.CharField(max_length=240, default='0')
    
    passport_number = models.CharField(max_length=240, null=True)

    seat_no = models.CharField(max_length=240, null=True)
    seat_class = models.CharField(max_length=240, null=True)

    destination = models.CharField(max_length=240, null=True)

    pax_type = models.CharField(max_length=240, null=True,  default='Adult')
    pax_weight = models.CharField(max_length=240, null=True)
    bags = models.CharField(max_length=240, null=True)
    bag_weight = models.CharField(max_length=240, null=True)
    hand_bag = models.CharField(max_length=240, null=True)
    

    seq_no = models.CharField(max_length=20, default='0')
    nationality = models.CharField(max_length=240, null=True)
    issuingcountry = models.CharField(max_length=240, null=True)
    documentnumber = models.CharField(max_length=240, null=True)
    documenttype = models.CharField(max_length=240, null=True)
    documentexpiry = models.CharField(max_length=240, null=True)
    address = models.CharField(max_length=240, null=True)
    documentexpiry = models.CharField(max_length=240, null=True)
    crew_or_pax = models.CharField(max_length=240, null=True)
    onward_flight = models.CharField(max_length=240, null=True)
    final_destination = models.CharField(max_length=240, null=True)
    company = models.CharField(max_length=240, null=True)
    check_in = models.CharField(max_length=240, default='0')
    board_time = models.CharField(max_length=240, null=True)
    offload_time = models.CharField(max_length=240, null=True)
    special_notes = models.CharField(max_length=240, null=True)

    qrcode = models.FileField(upload_to='qrcodes/', null=True, blank=True)
    

    qrid =  models.CharField(max_length=20, default='0')
    board_dateandtime = models.DateTimeField(null=True)
    def __str__(self):
        return self.fullname



class Passenger_lagage(models.Model):
    flight_id = models.ForeignKey(flight_charts, on_delete=models.CASCADE,null=True)
    passenger = models.ForeignKey(Passenger_db, on_delete=models.CASCADE,null=True)
    tag = models.CharField(max_length=100, default='0000000000')
    bag_type = models.CharField(max_length=240, null=True)
    weight = models.CharField(max_length=240, null=True)

    def __str__(self):
        return self.tag

    
class Flight_seat(models.Model):
    flight_id = models.ForeignKey(flight_charts, on_delete=models.CASCADE,null=True)
    s_1A = models.CharField(max_length=10, default='0')
    s_1B = models.CharField(max_length=10, default='0')
    s_1C = models.CharField(max_length=10, default='0')
    s_1D = models.CharField(max_length=10, default='0')

    s_2A = models.CharField(max_length=10, default='0')
    s_2B = models.CharField(max_length=10, default='0')
    s_2C = models.CharField(max_length=10, default='0')
    s_2D = models.CharField(max_length=10, default='0')

    s_3A = models.CharField(max_length=10, default='0')
    s_3B = models.CharField(max_length=10, default='0')
    s_3C = models.CharField(max_length=10, default='0')
    s_3D = models.CharField(max_length=10, default='0')

    s_4A = models.CharField(max_length=10, default='0')
    s_4B = models.CharField(max_length=10, default='0')
    s_4C = models.CharField(max_length=10, default='0')
    s_4D = models.CharField(max_length=10, default='0')

    s_5A = models.CharField(max_length=10, default='0')
    s_5B = models.CharField(max_length=10, default='0')
    s_5C = models.CharField(max_length=10, default='0')
    s_5D = models.CharField(max_length=10, default='0')

    s_6A = models.CharField(max_length=10, default='0')
    s_6B = models.CharField(max_length=10, default='0')
    s_6C = models.CharField(max_length=10, default='0')
    s_6D = models.CharField(max_length=10, default='0')

    s_7A = models.CharField(max_length=10, default='0')
    s_7B = models.CharField(max_length=10, default='0')
    s_7C = models.CharField(max_length=10, default='0')
    s_7D = models.CharField(max_length=10, default='0')

    s_8A = models.CharField(max_length=10, default='0')
    s_8B = models.CharField(max_length=10, default='0')
    s_8C = models.CharField(max_length=10, default='0')
    s_8D = models.CharField(max_length=10, default='0')

    s_9A = models.CharField(max_length=10, default='0')
    s_9B = models.CharField(max_length=10, default='0')
    s_9C = models.CharField(max_length=10, default='0')
    s_9D = models.CharField(max_length=10, default='0')

    s_10A = models.CharField(max_length=10, default='0')
    s_10B = models.CharField(max_length=10, default='0')
    s_10C = models.CharField(max_length=10, default='0')
    s_10D = models.CharField(max_length=10, default='0')

    s_11A = models.CharField(max_length=10, default='0')
    s_11B = models.CharField(max_length=10, default='0')
    s_11C = models.CharField(max_length=10, default='0')
    s_11D = models.CharField(max_length=10, default='0')

    s_12A = models.CharField(max_length=10, default='0')
    s_12B = models.CharField(max_length=10, default='0')
    s_12C = models.CharField(max_length=10, default='0')
    s_12D = models.CharField(max_length=10, default='0')

    s_13A = models.CharField(max_length=10, default='0')
    s_13B = models.CharField(max_length=10, default='0')
    s_13C = models.CharField(max_length=10, default='0')
    s_13D = models.CharField(max_length=10, default='0')

    s_14A = models.CharField(max_length=10, default='0')
    s_14B = models.CharField(max_length=10, default='0')
    s_14C = models.CharField(max_length=10, default='0')
    s_14D = models.CharField(max_length=10, default='0')

    s_15A = models.CharField(max_length=10, default='0')
    s_15B = models.CharField(max_length=10, default='0')
    s_15C = models.CharField(max_length=10, default='0')
    s_15D = models.CharField(max_length=10, default='0')

    s_16A = models.CharField(max_length=10, default='0')
    s_16B = models.CharField(max_length=10, default='0')
    s_16C = models.CharField(max_length=10, default='0')
    s_16D = models.CharField(max_length=10, default='0')

    s_17A = models.CharField(max_length=10, default='0')
    s_17B = models.CharField(max_length=10, default='0')
    s_17C = models.CharField(max_length=10, default='0')
    s_17D = models.CharField(max_length=10, default='0')

    s_18A = models.CharField(max_length=10, default='0')
    s_18B = models.CharField(max_length=10, default='0')
    s_18C = models.CharField(max_length=10, default='0')
    s_18D = models.CharField(max_length=10, default='0')

    s_19A = models.CharField(max_length=10, default='0')
    s_19B = models.CharField(max_length=10, default='0')
    s_19C = models.CharField(max_length=10, default='0')
    s_19D = models.CharField(max_length=10, default='0')

    s_20A = models.CharField(max_length=10, default='0')
    s_20B = models.CharField(max_length=10, default='0')
    s_20C = models.CharField(max_length=10, default='0')
    s_20D = models.CharField(max_length=10, default='0')

    


class Logs(models.Model):
    texts = models.CharField(max_length=240, null=True)
    added_date_time = models.DateTimeField(null=True)

    


