# Pakiet do budowania stron przez agenta

Czytaj dopiero po zgodzie na pełny pakiet w kroku 5. Wynikiem są `design.md`, gotowe style lub komponenty oraz działające przykłady użycia, oparte na ukończonej dokumentacji dla człowieka.

## 1. Wykorzystaj istniejący fundament

Jeśli dostępny jest projekt z kodem, sprawdź jego style, tokeny i komponenty. Zachowaj stos technologiczny i wykorzystaj istniejące źródło zamiast tworzyć równoległą bibliotekę. Wprowadź tylko brakujące elementy potrzebne w udokumentowanym zakresie. Nie wymagaj kodu, jeśli wejściem są same materiały wizualne.

Gdy fundamentu nie ma, przygotuj lokalny, wielokrotnego użytku CSS oraz semantyczne przykłady HTML. Jeżeli użytkownik wskazał framework, dostosuj komponenty i przykłady do niego. Buduj udokumentowany interfejs; nie projektuj dodatkowej biblioteki niezwiązanej z materiałem. Zgoda na pakiet obejmuje jego lokalne pliki, bez automatycznej publikacji i wdrożenia.

## 2. Przygotuj trzy powiązane wyniki

### `design.md` — punkt wejścia

Opisz zakres, charakter wizualny, priorytety, hierarchię, zasady kompozycji całych stron, wybór komponentów, granice rozszerzania oraz sposób weryfikacji wyniku. Wskaż, które zasady są potwierdzone, a które stanowią rekomendacje lub decyzje implementacyjne pakietu. Wyjątków z pojedynczego widoku nie przedstawiaj jako normy. Zostaw konkretne otwarte kwestie, gdy materiały nie pozwalają rozstrzygnąć intencji.

Dodaj dokładne ścieżki importów, instrukcję uruchomienia przykładów, opis publicznych klas lub właściwości, wymaganej struktury elementów i dozwolonych rozszerzeń. Podlinkuj szczegółową dokumentację dla człowieka oraz pliki i przykłady pakietu. Agent powinien móc rozpocząć pracę bez czytania całej implementacji CSS.

### Style lub komponenty — wykonanie reguł

Dostarcz działające źródła, a przy wykorzystaniu istniejącej biblioteki wskaż jej konkretne moduły i sposób użycia. Sam spis kolorów lub link do dokumentacji nie zastępuje fundamentu w kodzie.

Obejmij typografię według ról, kolory, odstępy, powierzchnie, układy responsywne oraz potrzebne warianty i stany udokumentowanych komponentów. Oddziel wspólny fundament od geometrii konkretnej strony. Zachowaj istniejące nazwy API; nowe nazwy i niezbędne decyzje implementacyjne opisz jako część pakietu, nie jako odkryte tokeny źródłowe. Szacunki z obrazów zachowaj w dokumentacji z informacją o niepewności, nawet gdy kod wymaga konkretnej wartości. Nie dopisuj niepotwierdzonych reguł zespołu ani trybów, których zakres nie obejmuje.

### Przykłady — poprawne użycie

Przygotuj uruchamialne przykłady komponentów, istotnych wariantów i stanów oraz złożenia reprezentatywnej strony. Używaj dostarczonego fundamentu bez duplikowania jego stylów. Pokaż strukturę HTML/JSX, wymagane atrybuty, konfigurację i zachowanie przy zmianie szerokości oraz dłuższej treści. Odróżnij działające zachowania interfejsu od demonstracyjnych danych i brakujących integracji.

## 3. Sprawdź i przekaż pakiet

Uruchom przykłady i obejrzyj wynik w przeglądarce na szerokim i wąskim widoku. Porównaj z materiałem źródłowym: hierarchię, typografię, odstępy, kolory, anatomię oraz reflow. Sprawdź istotne interakcje i focus; samo istnienie CSS-u nie potwierdza działania komponentu. Napraw wykryte rozbieżności, sprawdź importy i odsyłacze.

Przekaż linki do `design.md`, źródeł stylów lub komponentów i przykładów, sposób uruchomienia oraz rzeczywisty zakres weryfikacji. Gdy uruchomienie lub kontrola wizualna są niemożliwe, nazwij konkretny brak i oznacz pakiet jako niezweryfikowany w tym zakresie.
