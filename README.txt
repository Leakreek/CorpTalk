# CorpTalk króki opis cnie

CorpTalk to wewnętrzna aplikacja komunikacyjna stworzona w Django, przeznaczona do użytku w firmie.

## Funkcje główne:
- Czat pomiędzy użytkownikami w czasie rzeczywistym (WebSocket + Redis)
- Status użytkownika: dostępny / zajęty / niedostępny
- Widok listy pracowników z aktualnym statusem
- Możliwość generowania i przeglądania raportów aktywności
- Kalendarz z wydarzeniami (możliwość dodawania i usuwania)

## Role użytkowników:
- **Administrator**
  - Pełny dostęp do systemu
  - Dodawanie i zarządzanie użytkownikami
  - Przeglądanie raportów wszystkich pracowników
  - Podgląd i edycja kalendarza

- **Sekretariat**
  - Dostęp do listy pracowników
  - Podgląd i edycja kalendarza wydarzeń
  - Podgląd raportów pracowników
  - Podgląd i edycja kalendarza


- **Użytkownik**
  - Dostęp do czatu i własnych konwersacji
  - Możliwość zmiany własnego statusu
  - Widok własnych raportów
  - Widok kalendarza

## Technologia
- Django 5.x
- Django Channels (WebSocket)
- Redis (komunikacja czatu)
- Daphne (ASGI server)
- Docker + Docker Compose (do uruchamiania aplikacji)



Instrukcja uruchomienia aplikacji CorpTalk (lokalnie przez Docker)
Zainstaluj Docker Desktop

    Uruchom Docker Desktop (musi być włączony by aplikacja działała)

    Pobierz folder projektu CorpTalk z githuba

    Otwórz terminal w katalogu z projektem

    Uruchom aplikację
    W katalogu z plikiem docker-compose.yml, uruchom komendę:

docker-compose up --build

Jak docker to przemieli to można wejść na strone pod linkiem: 
http://127.0.0.1:8000

Żeby zamknąć serwer wystarczy kliknąć ctrl+c w konsoli z serwerem i wpisać komendę: docker-compose down

Żeby otworzyć ponownie serwer po zamknięciu wystarczy wpisać w cmd w katalogu aplikacji: docker-compose up


przykładowi użytkownicy jacy są dodani to (użytkowników dodaje się przez zalogowanie się do admina i dodanie użytkownika):
Login: user Hasło: user

Login: admin Hasło: admin

Login: secretariat Hasło: secretariat