# CorpTalk – krótki opis cnie

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

## Instrukcja uruchomienia aplikacji CorpTalk

### Metoda 1 – Lokalnie przez Docker (localhost)

1. Zainstaluj Docker Desktop

2. Uruchom Docker Desktop (musi być włączony by aplikacja działała)

3. Pobierz folder projektu CorpTalk z GitHuba

4. Otwórz terminal w katalogu z projektem

5. Uruchom aplikację (w katalogu z plikiem `docker-compose.yml`)(to się pisze tylko raz jak się buduje docker):

   docker-compose up --build

6. Jak docker to przemieli to można wejść na stronę pod linkiem:  
   http://127.0.0.1:3000

7. Żeby zamknąć serwer wystarczy kliknąć `CTRL+C` w konsoli z serwerem i wpisać:  
   docker-compose down

8. Żeby otworzyć ponownie serwer po zamknięciu wystarczy wpisać w terminalu:  
   docker-compose up

### Metoda 2 – Udostępnienie aplikacji przez internet (LocalTunnel)

Ta metoda pozwala odpalić aplikację tak, by była dostępna online – np. do testowania z drugiego komputera na tel działa chujowo.

1. Zainstaluj Node.js (jeśli nie masz) – https://nodejs.org

2. Zainstaluj LocalTunnel globalnie:

   npm install -g localtunnel

3.Odpal dockera tak jak przy metodzie 1, w katalogu CorpTalk wpisz:

   docker-compose up

4. W nowym terminalu również w katalogu CorpTalk uruchom tunel:

   lt --port 3000 --subdomain corptalk

   Jeśli subdomena jest zajęta, wpisz inną, np.:

   lt --port 3000 --subdomain corptalk123

5. Pojawi się link, np.:  
   https://corptalk.loca.lt

   To jest publiczny link, który działa z każdego urządzenia z internetem.



Uwaga: LocalTunnel może wyświetlić ekran z prośbą o potwierdzenie – to normalne. Wystarczy kliknąć "Submit".

## Przykładowi użytkownicy:

(Użytkowników dodaje się przez zalogowanie się do admin panelu `/admin`)

Login: user   Hasło: user  
Login: admin  Hasło: admin  
Login: secretariat Hasło: secretariat
