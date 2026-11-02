# Analiza dokumentacji wizualnej istniejącego projektu strony

Czytaj podczas analizy źródeł. Pracuj na materiałach dostarczonych do zadania, bez odczytów z Figmy. Nie wymagaj kodu, DOM ani dostępu do działającej strony, aby przygotować dokumentację.

## Źródła i pokrycie

1. Sporządź spis plików, stron PDF, plansz i ekranów. Oznacz ich wersje, rozmiary i tryby, jeśli podane. Nie uznawaj szerokości bitmapy za szerokość viewportu bez potwierdzenia.
2. Obejrzyj materiały w czytelnym rozmiarze. W długich dokumentach obejrzyj odpowiednie strony, nie tylko ekstrakcję tekstu. Dla lokalnych obrazów użyj narzędzia podglądu; dla innych formatów właściwej dostępnej umiejętności.
3. Nadaj źródłom krótkie identyfikatory, np. `S01 — home-desktop.png`, `S02 — guide.pdf, s. 8`. W ustaleniach podawaj źródło i obszar, np. „S01, nagłówek, przycisk Zapisz”.
4. Wyszukaj powtarzalne komponenty i zanotuj ich wystąpienia. Grupuj według wspólnej anatomii i roli; podobieństwo wizualne nie dowodzi, że elementy współdzielą implementację.
5. Zanotuj nieprzeanalizowane, nieczytelne lub sprzeczne materiały. Podaj liczbę przeanalizowanych ekranów/stron oraz rozpoznanych rodzin. Nie deklaruj pokrycia niewidocznych części produktu.

## Co ustalić

| Obszar | Dane oraz granica wnioskowania |
| --- | --- |
| Anatomia | Widoczne części, ich role, komponenty składowe i miejsca na treść lub ikony. Opcjonalność potwierdź opisem albo różnymi przykładami; nie myl uciętej części obrazu z jej brakiem w komponencie. |
| Warianty | Różnice hierarchii, zastosowania, wielkości, układu, gęstości, stanu i trybu. Przypisuj nazwę ze źródła albo nazwę roboczą. Nie nazywaj każdej różnicy treści nowym wariantem. |
| Właściwości i atrybuty | Widoczne lub opisane zmienne cechy: etykieta, ikona, rozmiar, stan, wybranie, obecność opisu itp. To nie dowodzi istnienia publicznego API. Osobno zapisz udokumentowaną konfigurację i proponowany model właściwości dla designerów. |
| Tokeny i style | Nazwy i wartości jawnie podane w dokumentacji oraz powtarzalne role kolorów, typografii, odległości, promieni i efektów. Powtarzalna wartość wizualna nie potwierdza istniejącego tokenu. |
| Wymiary i odległości | Wymiary z adnotacji lub oszacowane z obrazu; padding, gap, odstępy zewnętrzne, rozmiar ikon, promienie i obrysy. Zawsze zaznacz sposób pomiaru i źródło. |
| Typografia | Role tekstu, udokumentowane fonty i parametry oraz widoczna hierarchia, grubość, wyrównanie, interlinia, liczba wierszy i ucięcia. Same piksele nie potwierdzają rodziny fontu ani dokładnego weight. |
| Układ i responsywność | Wyrównanie, kolumny, zawijanie i zmiany między dostarczonymi widokami. Dwa rozmiary nie ustalają dokładnego breakpointu ani wszystkich reguł pomiędzy nimi. |
| Zachowanie | Stany i przejścia przedstawione na kolejnych ekranach lub opisane w adnotacjach. Statyczny wygląd nie potwierdza działania, focusu, hoveru, walidacji ani obsługi klawiatury. |

## Warianty, właściwości i ustawienia domyślne

- Zapisz wszystkie widoczne lub opisane wartości poszczególnych cech i ich rzeczywiste współwystępowanie. Nie generuj pełnego iloczynu kombinacji.
- Dla brakującej kombinacji napisz „nie pokazano w dostarczonych materiałach”, a nie „nie istnieje” lub „zabroniona”. Podobnie brak focusu lub błędu na planszy nie dowodzi, że produkt go nie obsługuje.
- Ustawienie domyślne podawaj wyłącznie, gdy dokumentacja je określa. Najczęściej pokazywany wariant nie staje się automatycznie domyślnym ani zalecanym.
- Dla cech widocznych w przykładach zapisz zakres obserwacji. Typ właściwości, dopuszczalne wartości, zależności i ograniczenia niepodane w źródle oznacz jako propozycję lub „Do potwierdzenia”.
- Oddziel zróżnicowanie treści, np. inny tekst etykiety, od zmiany zachowania lub struktury. Rozbieżności między podobnymi komponentami pokaż jako obserwację; ich ujednolicenie wymaga rekomendacji.

## Tokeny, pomiary i typografia

- Przepisuj nazwy tokenów, aliasy i wartości ze specyfikacji, jeśli występują. Jeżeli źródło ich nie podaje, nie twórz fikcyjnej listy „istniejących tokenów”. Możesz zaproponować semantyczne nazwy w jawnie oznaczonej części rekomendacji.
- Odróżnij wartość podaną w dokumentacji, pomiar bitmapy oraz rekomendowaną wartość systemową. Przy pomiarze bitmapy zaznacz jednostkę jako piksele obrazu; bez skali lub informacji o eksporcie nie utożsamiaj jej z CSS px/rem.
- Nie publikuj fałszywej precyzji: gdy materiał jest skalowany, kompresowany albo niewyraźny, użyj przybliżenia, zakresu lub opisu relacji. Zapisz znaną skalę; nie zakładaj DPR=1.
- Dla odległości nazwij oba elementy lub krawędzie. Oddziel przestrzeń wewnątrz komponentu od odstępu nadanego przez układ strony. Pojedynczy przykład nie ustanawia uniwersalnej reguły.
- Gdy font lub rozmiar nie są podane, dokumentuj widoczną rolę i relacje, a dokładne wartości oznacz „Do potwierdzenia”. Nie przedstawiaj fontu rozpoznanego na oko jako faktu.
- Nie przenoś wartości pomiędzy trybami, stanami i rozmiarami bez dowodu. Obraz jednego trybu nie pozwala odtworzyć pozostałych.

## Dostępność i ilustracje

- Przykładami dokumentacji mogą być odsyłacze do dostarczonych widoków i opis ich części. Nie doprojektowuj brakujących stanów tak, jakby pochodziły ze źródła. Proponowane przykłady do/don't oznacz jako rekomendacje.
- Dla kontrastu z obrazu podaj parę kolorów, tło, stan, tryb, metodę i ograniczenia. Antyaliasing, kompresja, przezroczystość oraz gradienty ograniczają wiarygodność próbkowania; nie publikuj pewnego wyniku zgodności na tej podstawie.
- Odróżnij widoczny kształt kontrolki od faktycznego celu dotykowego/klikalnego. Statyczna plansza nie dowodzi rozmiaru niewidocznego obszaru aktywnego.
- Czytnik ekranu, nazwa dostępna, role, kolejność focusu, obsługa klawiatury i komunikaty statusu wymagają potwierdzenia we wdrożeniu. Opisz wymagania i oczekiwane wyniki testów, nie ich rzekome zaliczenie.

Brak dokładnych danych nie zatrzymuje całej pracy. Opisz to, co widać lub podano, nazwij luki i przedstaw przydatne rekomendacje. Nie żądaj linku do Figmy, żeby uzupełnić brakujące metadane.
