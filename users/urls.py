from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView
from .views import custom_logout
from .views import send_message
from .views import (
    CustomLoginView,
    index_view,
    
    
    ##linki do usero
    user_raport,
    user_list,
    user_mainpage,
    user_message,
    
    #linki do admina
    administrator_mainpage,
    administrator_adduser,
    administrator_deleteuser,
    administrator_edituser,
    administrator_blockuser,
    administrator_raport,
    
    #linki do sekretariatu
    secretariat_mainpage,
    secretariat_list,
    secretariat_message,
    secretariat_alert,
    secretariat_raport,
    change_status,
    user_statuses_json,
    messages_view,
    delete_message
)

urlpatterns = [
    
    ##Strona tytułowa i login
    path('', index_view, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),    
    
    #Strona główna dla sekretariatu
    path('secretariat/mainpage/', secretariat_mainpage, name='secretariat_mainpage'),
    #podstrony sekretariatu
    path('secretariat/raport/', secretariat_raport, name='secretariat_raport'),
    path('secretariat/list/', secretariat_list, name='secretariat_list'),
    path('secretariat/message/', secretariat_message, name='secretariat_message'),
    path('secretariat/alert/', secretariat_alert, name='secretariat_alert'),


    
    
    
    #Storna główna usera
    path('user/mainpage/', user_mainpage, name='user_mainpage'),
    #podstrony usera
    path('user/message/', user_message, name='user_message'),
    path('user/list/', user_list, name='user_list'),
    path('user/raport/', user_raport, name='user_raport'),

    # Panele administratora
    path('administrator/mainpage/', administrator_mainpage, name='administrator_mainpage'),
    path('administrator/adduser/', administrator_adduser, name='administrator_adduser'),
    path('administrator/deleteuser/', administrator_deleteuser, name='administrator_deleteuser'),
    path('administrator/edituser/', administrator_edituser, name='administrator_edituser'),
    path('administrator/blockuser/', administrator_blockuser, name='administrator_blockuser'),
    path('administrator/raport/', administrator_raport, name='administrator_raport'),

    
    
    #zmiana statusów
    path('change_status/', change_status, name='change_status'),
    
    
    #lista użytkowków
    path('user/list/', views.user_list, name='user_list'),
    path('secretariat/list/', secretariat_list, name='secretariat_list'),
    path('status/json/', user_statuses_json, name='user_statuses_json'),
    
    #ściażka wiadomości
    path('messages/conversations', messages_view, name='messages'),
    path('messages/send/', send_message, name='send_message'),
    path('messages/ajax/', views.ajax_get_messages, name='ajax_get_messages'),    
    
    path('messages/delete/<int:message_id>/', delete_message, name='delete_message'),

    
    
]
from .views import calendar_view, add_event, delete_event
from .views import messages_view, send_message
from .views import calendar_view

urlpatterns += [
    path('messages/', messages_view, name='messages'),
    path('messages/send/', send_message, name='send_message'),
    path("calendar/", calendar_view, name="calendar"),
    path("calendar/add/", add_event, name="add_event"),
    path('calendar/delete/<int:event_id>/', delete_event, name='delete_event'),
    
]

