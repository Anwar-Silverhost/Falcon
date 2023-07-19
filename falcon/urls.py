"""falcon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from falcon_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name="login"),
    path('admin_navbar',views.admin_navbar,name="admin_navbar"),
    path('admin_dashboard',views.admin_dashboard,name="admin_dashboard"),
    path('admin_user',views.admin_user,name="admin_user"),

    path('admin_airport',views.admin_airport,name="admin_airport"),
    path('airport_save',views.airport_save,name="airport_save"),
    path('admin_flight',views.admin_flight,name="admin_flight"),
    path('admin_flight_save',views.admin_flight_save,name="admin_flight_save"),






    #==================== A J A X ===================#
    path('validate', views.validate, name = "validate"),
    path('airport_validate',views.airport_validate,name="airport_validate"),
    path('airport_save_ajax',views.airport_save_ajax,name="airport_save_ajax"),
    path('real_time_counts',views.real_time_counts,name="real_time_counts"),
    path('import_file',views.import_file,name="import_file"),

    path('checkin_addpassorid',views.checkin_addpassorid,name='checkin_addpassorid'),
    path('checkin_addpassweight',views.checkin_addpassweight,name='checkin_addpassweight'),
    path('checkin_holdbagweight',views.checkin_holdbagweight,name='checkin_holdbagweight'),
    path('checkin_holdbagremove',views.checkin_holdbagremove, name='checkin_holdbagremove'),

    path('checkin_handbagweight',views.checkin_handbagweight,name='checkin_handbagweight'),
    path('checkin_handbagremove',views.checkin_handbagremove, name='checkin_handbagremove'),
    
    path('pass_flight_seat',views.pass_flight_seat,name="pass_flight_seat"),


    






    #================== user ===============#
    path('user_navbar',views.user_navbar,name="user_navbar"),
    path('user_dashboard',views.user_dashboard,name="user_dashboard"),
    path('user_logout',views.user_logout,name="user_logout"),




    #---------------- flight administration -----------
    path('flight_administration',views.flight_administration,name="flight_administration"),
    path('flight_save',views.flight_save,name="flight_save"),
    path('flight_Passengers_Crew/<int:id>',views.flight_Passengers_Crew,name="flight_Passengers_Crew"),

    path('check_in',views.check_in,name='check_in'),
    path('flight_check_in/<int:id>',views.flight_check_in,name='flight_check_in'),

    path('passenger_checkin/<int:id>',views.passenger_checkin,name='passenger_checkin'),
    path('passenger_edit/<int:id>',views.passenger_edit,name='passenger_edit'),

    path('passenger_seat/<int:id>',views.passenger_seat,name='passenger_seat'),
    path('passenger_remove_seat/<int:id>',views.passenger_remove_seat,name='passenger_remove_seat'),

    path('passenger_boarding_pass/<int:id>',views.passenger_boarding_pass,name="passenger_boarding_pass"),



    path('passenger_boardingpass_collect_and_gotochekinpage/<int:id>',views.passenger_boardingpass_collect_and_gotochekinpage,name="passenger_boardingpass_collect_and_gotochekinpage"),

    path('flight_details/<int:id>',views.flight_details,name="flight_details"),



    path('boarding_pass/<int:id>',views.boarding_pass,name="boarding_pass"),



    path('logs',views.logs,name="logs"),

    path('flight_reports/<int:id>',views.flight_reports,name="flight_reports"),
    path('flight_status_change/<int:id>',views.flight_status_change,name="flight_status_change"),
    path('passanger_board/<int:id>',views.passanger_board,name="passanger_board"),
    path('passanger_deboard/<int:id>',views.passanger_deboard,name="passanger_deboard"),


    path('scanner',views.scanner,name="scanner"),
    path('scan_to_board/<int:id>',views.scan_to_board,name="scan_to_board"),
    path('passboard_idcheck/<str:qrid>',views.passboard_idcheck,name="passboard_idcheck"),
    path('user_settings',views.user_settings,name="user_settings"),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

