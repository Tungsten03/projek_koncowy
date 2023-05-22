
start_menu = """
            Aplikacja pozwala na zaciagniecie danych z API GIOS, ktore zostaną przechowane w bazie danych programu.

            Przed przystąpieniem do analizy danych w programie naciśnij przycisk START w celu zaktualizowania bazy danych.
            W razie wystąpienia problemów z dostępem do internetu aplikacja wykorzysta dane historyczne
            """
app_name = '---KRAQEN---'
app_name_analyze = '---KRAQEN---ANALIZA---'
app_full_name = '--Kacper Rajewski Air Quality Environment--'
status_start = 'Zaciąganie danych zamie około  20s'
status_prog = 'Zaciąganie danych proszę czekać'
status_done = 'Baza danych zaktualizowana'
status_history = 'Używasz historycznych danych'
show_map = 'Mapa stacji'
show_map_info = """Moduł pozwala na wyświetlenie wszystkich stacji na mapie
                Otworzy okno domyślnej przeglądarki"""
analyze_info = 'Moduł pozwala na pełną analizę danych z bazy'

popup_warn = """Wprowadzono błędne dane!
Upewnij się, że oba pola zawierają poprawnie wprowadzone dane np.:
Opis lokacji: Poznań, Naramowicka || W zasięgu: 25
"""

popup_connect = """ Brak dostępu do serwera openstreetmap 
Sprawdź połączenie z siecią lub status serwera pod adresem:
https://nominatim.openstreetmap.org/status.php
"""

gui_help = """ Witaj w module analizy danych.
Jest to główny moduł aplikacji, który pozwala na pełną analizę i prezentację graficzną danych z bazy.
1. Wybierz stację z listy dostępnej na dole okna (stacje poszeregowane wg. nazwy)
* Możesz również skorzystać z wyszukiwarki stacji po opisie lokacji i promieniu poszukiwań
- W tym celu w pole "Opis lokacji" wpisz krótki opis miejsca (np. Miasto, ulica lub nazwa własna jak UAM, Poznań)
- Następnie wpisz promień poszukiwania stacji (w km)
- Zatwierdź wybór przyciskiem "W zasięgu"
2. Zatwierdź wybór przyciskiem "Wybierz stacji" nad polem tekstowym z aktywnym ID
3. Teraz możesz przystąpić do analizy danych wybranej stacji pomiarowej.
* Zaznacz parametr, który chciałbyś analizować
* Przystąp do analizy wyników. W tym celu możesz:
- Dokonać prostej analizy poprzez naciśnięcie przycisku "Wylicz dane"
- Program wyliczy takie wartości jak: średnia pomiarów, maksymalną i minimalną oraz wskaże datę i godzinę pomiaru.
- Wyrysować dane na wykresie. Wykres zawiera również regresję liniową oraz wskazuję pomiar maksymalny i minimalny.
4. Przyciski do analizy danych dostępne są jedynie w trybie wyboru sensorów. 
5. Przycisk wyboru stacji jest dostępny jedynie w trybie wyboru/wyszukiwania stacji.
"""