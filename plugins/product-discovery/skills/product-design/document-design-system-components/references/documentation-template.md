# Szablon dokumentacji dla designerów

Czytaj przy pisaniu wyniku. Dopasuj długość do rodziny, zachowując poniższe obszary. Wpisuj dane z analizy; nie wymyślaj wartości, aby zapełnić tabelę. Dla braku danych użyj „Do potwierdzenia”, a dla nieadekwatnego obszaru „Nie dotyczy” z krótkim uzasadnieniem. Usuń instrukcje szablonu z gotowego dokumentu.

## Nagłówek i indeks projektu

**[Nazwa projektu] — dokumentacja komponentów · [wersja]**

- Materiały źródłowe: pliki, strony/ekrany, ich wersje, jeśli znane, oraz data analizy.
- Pokrycie: przeanalizowane materiały / dostarczone materiały; rozpoznane rodziny, warianty i właściwości. Nie jest to inwentaryzacja nieznanej biblioteki.
- Status: wersja do oceny / po poprawkach / zaakceptowana — zgodnie ze stanem faktycznym.
- Indeks: rodzina → przeznaczenie → karta i źródło.
- Legenda oznaczeń: potwierdzone w dokumentacji, szacunek z obrazu, rekomendacja, do potwierdzenia, do testu we wdrożeniu.

Wspólne zasady i tokeny umieść tutaj tylko wtedy, gdy faktycznie dotyczą całego zakresu. Poniższą kartę powtórz dla każdej rodziny.

## [Nazwa rodziny]

### Przeznaczenie i wybór

Jaki problem rozwiązuje komponent, w jakim kontekście go wybrać i jakie ma ograniczenia. Podaj zasady użycia oraz przypadki, w których lepiej sprawdzi się inny opisany komponent. Odwołuj się do wytycznych z materiałów; własne propozycje oznacz jako rekomendacje.

### Anatomia i komponenty składowe

Dodaj odsyłacz do czytelnego widoku i opis numerowanych części, jeśli pomocny. Nie przedstawiaj doprojektowanego przykładu jako źródła.

| Część / rola | Wymagana czy opcjonalna | Komponent składowy / źródło | Co można zmienić / status ustalenia |
| --- | --- | --- | --- |

Uwzględnij ikony, etykiety, pomocniczy tekst, kontenery, miejsca na treść i elementy składowe, jeżeli występują. Odróżnij widoczną kompozycję od niepotwierdzonej struktury implementacji. Nazwij warianty zmieniające anatomię.

### Warianty i ich zastosowanie

| Oś | Wartość / wariant | Kiedy użyć | Co się zmienia | Ograniczenia / status / źródło |
| --- | --- | --- | --- | --- |

Oddziel wariant semantyczny od rozmiaru i stanu. Dla dostępnego stanu opisz znaczenie, sygnał wizualny i kontekst. Gdy oczekiwanego stanu nie pokazano, napisz to; nie oznacza to jego braku w produkcie.

Dodaj macierz kombinacji zaobserwowanych lub opisanych w materiałach, z odsyłaczami do źródeł. Przy dużej liczbie wariantów pełną macierz przenieś do aneksu.

### Dostępne właściwości i atrybuty

| Właściwość / atrybut | Typ, jeśli podany | Pokazane lub opisane wartości | Domyślna, jeśli określona | Efekt zmiany i zastosowanie | Zależności / status / źródło |
| --- | --- | --- | --- | --- | --- |

Opisz udokumentowaną konfigurację oraz cechy zmienne widoczne w przykładach: etykietę, ikonę, rozmiar, stan, wybranie, tekst pomocniczy itp. Odróżnij je od publicznego API komponentu, którego istnienia obraz nie potwierdza. Jeśli proponujesz model właściwości dla designerów, pokaż go osobno i oznacz „Rekomendacja”. Nie zgaduj wartości domyślnych ani zamkniętej listy opcji.

### Tokeny i style

| Zastosowanie / rola | Nazwa tokenu lub stylu, jeśli podana | Tryb / wariant | Wartość i jednostka | Alias / źródło, jeśli opisane | Status / podstawa ustalenia |
| --- | --- | --- | --- | --- | --- |

Uwzględnij kolory, odległości, rozmiary, promienie, obrysy, typografię, opacity i efekty, które dotyczą komponentu. Jeżeli źródło nie podaje nazw tokenów, zaznacz to i opisz role oraz powtarzalne wartości. Proponowane nazwy pokaż jako rekomendacje. Oddziel dokładne wartości ze specyfikacji od szacunków z obrazu; nie deklaruj powiązania z tokenem na podstawie podobieństwa koloru.

### Wymiary, odległości i układ

| Elementy / krawędzie | Wariant lub rozmiar | Wartość i jednostka / relacja | Token, jeśli podany | Reguła / pomiar przykładu / źródło / dokładność |
| --- | --- | --- | --- | --- |

Opisz padding krawędzi, gap, odstępy między wierszami, rozmiary ikon i wyrównanie. Min/max i pozostałe reguły podaj, jeśli opisane. Oddziel przestrzeń wewnątrz komponentu od odstępów w układzie strony. Porównaj zawijanie, ucinanie i zachowanie treści między dostarczonymi widokami. Nie wyciągaj dokładnego breakpointu ani stałej wysokości rodziny z pojedynczego przykładu.

### Typografia

| Rola tekstu | Styl / token, jeśli podany | Font i odmiana / weight | Rozmiar | Interlinia i jednostka | Tracking i jednostka | Kolor / zachowanie / status / źródło |
| --- | --- | --- | --- | --- | --- | --- |

Pokaż hierarchię oraz różnice wariantów. Dokładne parametry podawaj ze specyfikacji, a nie z rozpoznania na oko. Dla brakujących danych opisz widoczne relacje i oznacz lukę. Zachowuj jednostki ze źródła. Nie wymyślaj limitu znaków.

### Zachowanie, treści i lokalizacja

Opisz przejścia między stanami, walidację, błędy, loading i feedback w zakresie pokazanym lub opisanym w materiałach. Dodaj adekwatne wskazówki pisania etykiet i komunikatów, obsługi długich tłumaczeń i RTL. Nieprzedstawione zachowanie opisz jako rekomendację lub wymaganie do potwierdzenia. Makieta nie potwierdza działania produktu.

### Zalecane i niewskazane praktyki

| Zalecane — konkretny przykład | Niewskazane — konkretny przykład | Powód / skutek / status reguły / źródło |
| --- | --- | --- |

Dobierz przykłady do rodziny: wybór wariantu, hierarchia, label, ikony, kompozycja, liczba elementów czy obsługa stanów. Każda para ma pomagać podjąć decyzję i wyjaśniać jej skutek. Nie dodawaj przypadkowych zakazów ani nie przedstawiaj propozycji jako istniejącej zasady zespołu.

### Dostępność

Podaj platformę i przyjęty cel dostępności. Gdy materiały nie określają celu, zaproponuj go jako rekomendację. Dobierz adekwatne kryteria WCAG i wzorzec APG, podając zweryfikowane oficjalne źródła.

| Obszar | Ustalenie lub wymaganie | Dowód / wynik / status | Kryterium i poziom lub wzorzec | Jak sprawdzić |
| --- | --- | --- | --- | --- |

Rozważ adekwatne obszary:

- Kontrast tekstu, elementów i stanów; para kolorów, tryb, tło, metoda oraz ograniczenia pomiaru z obrazu. Próg dobierz do rzeczywistego kryterium i jego wyjątków.
- Widoczny i niezasłonięty focus, obsługa klawiatury, kolejność i zarządzanie focusem.
- Nazwa dostępna, rola, wartość/stany, etykieta i powiązania z opisem lub błędem. Widoczny label nie potwierdza nazwy dostępnej we wdrożeniu.
- Rozmiar celu i odstępy, alternatywy dla złożonych gestów, niezależność informacji od samego koloru. Widoczny rozmiar kontrolki nie potwierdza całego obszaru aktywnego.
- Powiększenie, reflow, nadpisanie odstępów tekstu, tłumaczenia i kierunek pisma.
- Zmiany stanu, komunikaty błędów/statusu i animacje, jeżeli komponent ich używa.

Oddziel inspekcję dokumentacji wizualnej od testów we wdrożeniu. Gdy testu nie wykonano, napisz „Do testu we wdrożeniu” i określ oczekiwane zachowanie. Nie deklaruj zgodności produktu z WCAG na podstawie statycznych materiałów.

### Źródła i otwarte kwestie

- Pliki i numery stron, identyfikatory ekranów oraz obszary, na których oparto ustalenia; użyte oficjalne standardy.
- Luki: brakujący widok / niepodany token / niepotwierdzona zasada / test do wykonania → wpływ na korzystanie z komponentu.
- Pytania do właściciela tylko tam, gdzie odpowiedź zmienia dokumentację lub sposób użycia.

## Przekazanie do oceny

Podaj wersję, zakres dokumentacji, odsyłacz do pełnego wyniku, jeśli jest plikiem, i najważniejsze otwarte kwestie. Zbieraj uwagi i poprawiaj wynik. Ten etap nie obejmuje wysyłania dokumentacji do żadnego narzędzia projektowego.
