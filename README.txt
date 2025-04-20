Instrukcja uruchomienia aplikacji CorpTalk (lokalnie przez Docker)
Zainstaluj Docker Desktop

    Uruchom Docker Desktop
    Po instalacji upewnij się, że Docker jest włączony i działa w tle.

    Pobierz folder projektu CorpTalk

    Otwórz terminal w katalogu z projektem
    Przykład:
    D:\projekty\corptalk

    Uruchom aplikację
    W katalogu z plikiem docker-compose.yml, uruchom komendę:

docker-compose up --build

Docker zbuduje i uruchomi trzy kontenery:

    aplikację Django z Daphne

    usługę Redis

    zależności Pythona

Wejdź na stronę aplikacji
Po kilku sekundach aplikacja będzie działać lokalnie:

http://127.0.0.1:8000

przykładowi użytkownicy jacy są dodani to (userów dodaje się przez zalogowanie się do admina i dodanie użytkownika):
Login: user Hasło: user

Login: admin Hasło: admin

Login: secretariat Hasło: secretariat