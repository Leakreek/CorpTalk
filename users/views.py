from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import logout
from .models import WorkSession
from django.utils.timezone import now
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from .models import Message
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Message

# Strona główna
def index_view(request):
    return render(request, 'auth/index.html')

# Niestandardowy widok logowania z przekierowaniem na podstawie roli
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        user.status = 'available'
        user.save()
        WorkSession.objects.create(user=user, login_time=now())
        return response

    def get_success_url(self):
        user = self.request.user
        print("ROLA:", user.rola)
        if user.rola == 'administrator':
            return '/administrator/mainpage/'
        elif user.rola == 'secretariat':
            return '/secretariat/mainpage/'
        else:
            return '/user/mainpage/'



# Zmiana statusu
@login_required
def change_status(request):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['available', 'busy', 'offline']:
            request.user.status = new_status
            request.user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Widoki panelu usera
@login_required
def user_mainpage(request):
    return render(request, 'users/user_mainpage.html')

@login_required
def user_message(request):
    return render(request, 'users/user_message.html')

@login_required
def user_conversations(request):
    return render(request, 'users/user_conversations.html')

@login_required
def user_list(request):
    users = User.objects.all().order_by('last_name')
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_raport(request):
    return render(request, 'users/user_raport.html')

# Widoki panelu sekretariatu
@login_required
def secretariat_mainpage(request):
    return render(request, 'secretariat/secretariat_mainpage.html')

@login_required
def secretariat_raport(request):
    return render(request, 'secretariat/secretariat_raport.html')

@login_required
def secretariat_conversations(request):
    return render(request, 'secretariat/secretariat_conversations.html')

@login_required
def secretariat_list(request):
    users = User.objects.all().order_by('last_name')
    return render(request, 'secretariat/secretariat_list.html', {'users': users})

@login_required
def secretariat_message(request):
    return render(request, 'secretariat/secretariat_message.html')

@login_required
def secretariat_alert(request):
    return render(request, 'secretariat/secretariat_alert.html')

# Widoki panelu administratora
@login_required
def administrator_mainpage(request):
    return render(request, 'administrator/administrator_mainpage.html')

@login_required
def administrator_adduser(request):
    return render(request, 'administrator/administrator_adduser.html')

@login_required
def administrator_deleteuser(request):
    return render(request, 'administrator/administrator_deleteuser.html')

@login_required
def administrator_edituser(request):
    return render(request, 'administrator/administrator_edituser.html')

@login_required
def administrator_blockuser(request):
    return render(request, 'administrator/administrator_blockuser.html')

@login_required
def administrator_raport(request):
    return render(request, 'administrator/administrator_raport.html')

# API: statusy użytkowników w JSON (dla JS)
@login_required
@require_GET
def user_statuses_json(request):
    users = User.objects.all().values('username', 'status')
    return JsonResponse(list(users), safe=False)

# Pobranie modelu użytkownika
User = get_user_model()

def custom_logout(request):
    user = request.user

    # zamknięcie aktywnej sesji
    from .models import WorkSession
    last_session = WorkSession.objects.filter(user=user, logout_time__isnull=True).last()
    if last_session:
        last_session.logout_time = now()
        last_session.save()

    # status offline
    user.status = 'offline'
    user.save()
    logout(request)
    return redirect('login')


@login_required
def user_raport(request):
    sessions = WorkSession.objects.filter(user=request.user)
    total_duration = sum([s.duration() for s in sessions], start=now() - now())

    total_seconds = int(total_duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return render(request, 'users/user_raport.html', {
        'sessions': sessions,
        'total_duration': total_duration,
        'hours': hours,
        'minutes': minutes
    })

@login_required
def secretariat_raport(request):
    sessions = WorkSession.objects.select_related('user').all()

    from collections import defaultdict
    grouped_sessions = defaultdict(list)
    for s in sessions:
        grouped_sessions[s.user].append(s)

    user_data = []
    for user, sess_list in grouped_sessions.items():
        total = sum([s.duration() for s in sess_list], start=now() - now())
        seconds = int(total.total_seconds())
        user_data.append({
            "user": user,
            "duration": total,
            "sessions": sess_list,
            "hours": seconds // 3600,
            "minutes": (seconds % 3600) // 60
        })

    # SORTUJ I DODAJ last_name_letter
    user_data = sorted(user_data, key=lambda x: x["user"].last_name.lower())
    for data in user_data:
        data["last_name_letter"] = data["user"].last_name[0].upper()

    return render(request, 'secretariat/secretariat_raport.html', {
        'user_data': user_data
    })


@login_required
def administrator_raport(request):
    sessions = WorkSession.objects.select_related('user').all()

    from collections import defaultdict
    grouped_sessions = defaultdict(list)
    for s in sessions:
        grouped_sessions[s.user].append(s)

    user_data = []
    for user, sess_list in grouped_sessions.items():
        total = sum([s.duration() for s in sess_list], start=now() - now())
        seconds = int(total.total_seconds())
        user_data.append({
            "user": user,
            "duration": total,
            "sessions": sess_list,
            "hours": seconds // 3600,
            "minutes": (seconds % 3600) // 60
        })

    # SORTUJ I DODAJ last_name_letter (PODSTAWA!)
    user_data = sorted(user_data, key=lambda x: x["user"].last_name.lower())
    for data in user_data:
        data["last_name_letter"] = data["user"].last_name[0].upper()

    return render(request, 'administrator/administrator_raport.html', {
        'user_data': user_data
    })

#czaty
from django.db.models import Q
from django.urls import reverse

from django.db.models import Count, Case, When, IntegerField

@login_required
def messages_view(request):
    # Domyślna strona powrotu
    return_url = '/user/mainpage/'
    if request.user.rola == 'administrator':
        return_url = '/administrator/mainpage/'
    elif request.user.rola == 'secretariat':
        return_url = '/secretariat/mainpage/'

    # Lista wszystkich użytkowników (do alfabetycznego wyświetlania)
    all_users = User.objects.exclude(id=request.user.id).order_by('last_name', 'first_name')

    # Ostatnie rozmowy – znajdź unikalne ID rozmówców
    message_history = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    last_user_ids = {msg.sender.id for msg in message_history}.union({msg.receiver.id for msg in message_history})
    last_user_ids.discard(request.user.id)

    # Pobierz użytkowników z którymi była rozmowa + zlicz nieprzeczytane wiadomości
    recent_users = User.objects.filter(id__in=last_user_ids).annotate(
        unread_count=Count(Case(
            When(sent_messages__receiver=request.user, sent_messages__is_read=False, then=1),
            output_field=IntegerField()
        ))
    )

    selected_user = None
    conversation = []

    # Jeśli wybrano użytkownika z listy
    if request.GET.get('user'):
        selected_user = get_object_or_404(User, username=request.GET['user'])

        # Oznacz wiadomości jako przeczytane (odebrane od selected_user)
        Message.objects.filter(
            sender=selected_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

        # Pobierz historię rozmowy
        conversation = Message.objects.filter(
            Q(sender=request.user, receiver=selected_user) |
            Q(sender=selected_user, receiver=request.user),
            deleted=False
        ).order_by('timestamp')

    return render(request, 'messages/conversations.html', {
        'recent_users': recent_users,
        'all_users': all_users,
        'selected_user': selected_user,
        'messages': conversation,
        'return_url': return_url
    })


from django.http import JsonResponse

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('message')
        receiver = get_object_or_404(User, username=receiver_username)
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


from django.http import JsonResponse
from django.core.serializers import serialize

def ajax_get_messages(request):
    user = get_object_or_404(User, username=request.GET.get('user'))
    conversation = Message.objects.filter(
        Q(sender=request.user, receiver=user) |
        Q(sender=user, receiver=request.user),
        deleted=False
    ).order_by('timestamp')

    data = [
        {
            'id': msg.id,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M')
        }
        for msg in conversation
    ]
    return JsonResponse(data, safe=False)


from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, JsonResponse

@require_POST
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.sender != request.user:
        return HttpResponseForbidden("Nie możesz usunąć tej wiadomości.")

    message.deleted = True
    message.save()
    return JsonResponse({'status': 'success'})

from django.contrib.auth.decorators import login_required
from .models import Event
from datetime import date
from calendar import monthrange

@login_required
def calendar_view(request):
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))
    days_in_month = monthrange(year, month)[1]
    events = Event.objects.filter(date__year=year, date__month=month)

    events_by_day = {}
    for event in events:
        events_by_day.setdefault(event.date.day, []).append(event)

    calendar_days = []
    for day in range(1, days_in_month + 1):
        calendar_days.append({
            "day": day,
            "events": events_by_day.get(day, [])
        })

        if request.user.rola == "administrator":
            return_url = "/administrator/mainpage/"
        elif request.user.rola == "secretariat":  # <- poprawione
            return_url = "/secretariat/mainpage/"
        else:
            return_url = "/user/mainpage/"


    half = len(calendar_days) // 2
    left_days = calendar_days[:half]
    right_days = calendar_days[half:]

    return render(request, "calendar/calendar.html", {
        "year": year,
        "month": month,
        "calendar_days": calendar_days,
        "left_days": left_days,
        "right_days": right_days,
        "return_url": return_url,
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import Event

from django.http import HttpResponseForbidden
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Event

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Event

@login_required
def add_event(request):
    print("Rola użytkownika:", request.user.rola)
    print("Czy jest staff:", request.user.is_staff)

    if not (request.user.is_staff or request.user.rola == 'sekretariat'):
        print("Nie masz uprawnień do dodania wydarzenia.")
        return redirect('calendar')  # tu możesz dać HttpResponseForbidden dla testów

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date_str = request.POST.get("date")

        if title and date_str:
            Event.objects.create(
                title=title,
                description=description,
                date=date_str,
                created_by=request.user
            )
            print("Wydarzenie dodano poprawnie.")
        else:
            print("Brakuje tytułu lub daty wydarzenia.")

    return redirect("calendar")


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Event
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Tylko autor może usunąć swój event
    if event.created_by != request.user:
        return HttpResponseForbidden("Nie możesz usunąć tego wydarzenia.")

    # Opcjonalnie: ograniczenie do admina/sekr:
    if not (request.user.is_staff or getattr(request.user, 'rola', None) == 'sekretariat'):
        return HttpResponseForbidden("Nie masz uprawnień.")

    event.delete()
    return redirect('calendar')

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

User = get_user_model()
from django.contrib.auth import get_user_model

@login_required
def administrator_adduser(request):
    if request.user.rola != 'administrator':
        return redirect('home')  # lub zwróć 403

    User = get_user_model()

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get("email")
        password = request.POST.get('password')
        rola = request.POST.get('rola')

        if not all([username, first_name, last_name, email, password, rola]):
            return render(request, 'administrator/administrator_adduser.html', {
                'error': 'Wszystkie pola są wymagane.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'administrator/administrator_adduser.html', {
                'error': 'Użytkownik o takiej nazwie już istnieje.'
            })

        # automatycznie przypisz is_staff jeśli rola = sekretariat lub administrator
        is_staff = rola in ['administrator', 'sekretariat']

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            rola=rola.lower().strip(),  # zabezpieczenie na literówki i spacje
            email=email,
            is_staff=is_staff
        )
        user.set_password(password)
        user.save()

        return render(request, 'administrator/administrator_adduser.html', {
            'success': True
        })

    return render(request, 'administrator/administrator_adduser.html')

@login_required
def administrator_edituser(request):
    if request.user.rola != 'administrator':
        return redirect('home')

    User = get_user_model()
    users = User.objects.all().order_by('last_name', 'first_name')
    selected_user = None
    success = False

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        selected_user = get_object_or_404(User, id=user_id)
    
        if action == 'save':
            selected_user.username = request.POST.get('username')
            selected_user.first_name = request.POST.get('first_name')
            selected_user.last_name = request.POST.get('last_name')
            selected_user.email = request.POST.get('email')
            selected_user.rola = request.POST.get('rola')

            password = request.POST.get('password')
            if password:
                selected_user.set_password(password)

            # Zapisz stan checkboxa aktywności
            selected_user.is_active = 'is_active' in request.POST

            selected_user.save()
            success = True


        elif action == 'block':
            selected_user.is_active = False
            selected_user.save()
            success = 'blocked'

        elif action == 'delete':
            selected_user.delete()
            return redirect('administrator_edituser')

    elif request.method == 'GET' and 'user_id' in request.GET:
        selected_user = get_object_or_404(User, id=request.GET.get('user_id'))

    return render(request, 'administrator/administrator_edituser.html', {
        'users': users,
        'selected_user': selected_user,
        'success': success
    })
