---
name: document-design-system-components
description: "Twórz dokumentację komponentów design systemu dla designerów na podstawie dokumentacji wizualnej istniejącego projektu strony: zrzutów ekranów, makiet, plansz lub specyfikacji wizualnej. Analizuj widoczne warianty, właściwości, anatomię, tokeny, odległości, typografię, zastosowania i dostępność. Pokaż pełny wynik do oceny. Używaj przy dokumentowaniu istniejącego interfejsu. Po ukończeniu dokumentacji dla designerów zaproponuj opcjonalny pakiet dla agenta: design.md, style lub komponenty oraz przykłady użycia; przygotuj go po zgodzie."
---

# Dokumentacja komponentów design systemu

Przygotuj dokumentację, która pomaga designerowi wybrać komponent, skonfigurować go i poprawnie zastosować w projekcie. Wejściem jest dostarczona przez użytkownika **dokumentacja wizualna istniejącego projektu strony**. Wynikiem jest pełna dokumentacja komponentów do oceny użytkownika.

## Wejście i wynik

- Przyjmuj screenshoty, makiety, plansze, wizualne style guide'y oraz dokumenty z obrazami i opisami, np. PDF lub HTML. Podstawą są dostarczone materiały; nie wymagaj dostępu do kodu ani działającej strony.
- **Nie korzystaj z Figmy jako źródła ani miejsca docelowego. Nie wymagaj linku do Figmy i nie wywołuj narzędzi Figma. Nie wysyłaj tam dokumentacji, także po jej akceptacji.**
- Przedstaw pełny wynik w rozmowie albo w formacie/pliku wskazanym przez użytkownika. Wersja lokalna nie wymaga uprzedniej zgody na publikację. Ocena i poprawki nie uruchamiają żadnego eksportu ani publikacji.
- Zachowaj źródłowe materiały. Etap dokumentacji dla designerów nie obejmuje zmiany projektu strony ani implementowania komponentów. Implementacja fundamentu stylów lub komponentów należy wyłącznie do opcjonalnego pakietu dla agenta po bramce w kroku 5.

## 1. Ustal zakres z materiałów

- Zinwentaryzuj pliki, strony dokumentu, ekrany i opisane stany. Zanotuj dostępne rozmiary widoków, tryby kolorystyczne i adnotacje projektowe. Poproś o brakujące źródło tylko wtedy, gdy uniemożliwia rozpoczęcie analizy.
- Rozpoznaj powtarzalne rodziny komponentów: porównaj anatomię, rolę i wygląd w różnych miejscach strony. Nie traktuj każdego wystąpienia ani całego ekranu jako oddzielnego komponentu.
- Przygotuj indeks rodzin i wspólnych zależności. Dla każdej rodziny twórz osobną kartę dokumentacji; wspólne tokeny i zasady można opisać raz z odsyłaczami.
- Domyślnie pisz po polsku, pozostawiając oryginalne nazwy z materiałów. Gdy nadajesz komponentowi lub właściwości nazwę roboczą, zaznacz to. Dostosuj język do prośby użytkownika lub dokumentacji zespołu.

## 2. Przeanalizuj dokumentację i zbierz dowody

Przeczytaj [procedurę analizy wizualnej](references/visual-analysis.md). Obejrzyj obrazy i istotne strony dokumentów, nie opieraj się wyłącznie na OCR, podpisach lub wyodrębnionym tekście. Dla plików wymagających odrębnego sposobu odczytu użyj odpowiedniej dostępnej umiejętności, np. `pdf:pdf` dla PDF.

Zbierz wszystkie warianty i właściwości widoczne lub jawnie opisane w dostarczonych materiałach. Dla dużych zbiorów dziel analizę na partie. Zakres kompletności to dostępna dokumentacja, nie nieznana biblioteka ani cały produkt.

Rozróżniaj statusy treści:

- **Potwierdzone w dokumentacji** — widoczne w materiale lub podane w jego specyfikacji; wskaż plik, stronę/ekran i element. Widok potwierdza wygląd, a nie nieopisane zachowanie lub API.
- **Szacunek z obrazu** — pomiar lub przybliżenie wizualne; podaj źródło, skalę, jeśli znana, i ograniczenie dokładności.
- **Rekomendacja** — proponowana zasada, nazwa tokenu lub model właściwości; nie przedstawiaj ich jako istniejącego standardu zespołu.
- **Do potwierdzenia** — brak danych, konflikt lub niepewny wniosek; nazwij konkretną lukę.
- **Do testu we wdrożeniu** — zachowanie wymagające działającego produktu, np. obsługa czytnika ekranu.

Używaj oznaczeń przy istotnych twierdzeniach lub grupach wierszy. Gdy podpisane wytyczne przeczą widokom, pokaż obie informacje i ich źródła. Nie naprawiaj ani nie ujednolicaj po cichu projektu podczas dokumentowania.

## 3. Napisz dokumentację dla designerów

Użyj [szablonu dokumentacji](references/documentation-template.md), dopasowując długość do rodziny. Zachowaj wszystkie obszary wymagane w szablonie; dla nieadekwatnych napisz krótko „Nie dotyczy” z uzasadnieniem, a dla niedostępnych danych „Do potwierdzenia”.

Każda karta obejmuje:

1. Przeznaczenie, zasady użycia i wybór względem podobnych komponentów.
2. Anatomię oraz komponenty składowe: części, wymagane i opcjonalne elementy, zależności i miejsca podmiany.
3. Warianty, rozmiary i stany z zastosowaniem oraz zaobserwowanymi kombinacjami.
4. Dostępne właściwości i atrybuty: typy, wartości, ustawienia domyślne, ograniczenia i zależności — w zakresie opisanym lub widocznym w dokumentacji. Proponowany model konfiguracji oznacz osobno.
5. Tokeny, style, tryby oraz miejsca ich zastosowania. Odróżnij tokeny podane w dokumentacji od powtarzalnych wartości i proponowanych nazw.
6. Wymiary, odległości i reguły układu, także zachowanie przy zmianie treści i szerokości.
7. Typografię według roli tekstu.
8. Zachowanie, treści i lokalizację, jeżeli dotyczą komponentu.
9. Zalecane i niewskazane praktyki z konkretnymi przykładami i uzasadnieniem.
10. Dostępność: ustalenia projektowe, rekomendacje i testy wymagające implementacji.
11. Źródła, zakres analizy, luki i pytania do właściciela systemu.

Przekładaj obserwacje na decyzje projektowe. Zamiast samego „wariant mały” wyjaśnij jego potwierdzone albo proponowane zastosowanie i ograniczenia. Nie wymyślaj nieoznaczonych jako propozycja limitów znaków, breakpointów, nazw tokenów czy reguł użycia. Nie blokuj całej dokumentacji dlatego, że obrazy nie ujawniają dokładnych wartości lub konfiguracji komponentu.

Zalecenia dostępności oprzyj na właściwym standardzie i wzorcu interakcji. Dla webu zweryfikuj aktualne materiały [WCAG](https://www.w3.org/WAI/WCAG22/quickref/) i odpowiedni wzorzec [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/patterns/). Podawaj konkretne kryteria, poziomy i wyjątki, gdy oceniasz wymóg; nie traktuj APG jako normatywnego kryterium WCAG. Sam dokument wizualny nie dowodzi zgodności produktu.

## 4. Sprawdź i pokaż pełny wynik

Przed przekazaniem do oceny sprawdź:

- Czy indeks obejmuje każdą rodzinę rozpoznaną w zakresie, a macierz wszystkie zaobserwowane lub opisane warianty i właściwości? Podaj pokrycie materiałów i ograniczenia analizy.
- Czy twierdzenia mają odsyłacze do odpowiedniego widoku, strony lub adnotacji? Czy szacunek z obrazu nie został przedstawiony jako dokładna wartość projektu?
- Czy tokeny, nazwy fontów, ustawienia domyślne i model konfiguracji mają źródło albo odpowiednie oznaczenie niepewności/propozycji?
- Czy zastosowania wariantów i do/don't pomagają podjąć konkretną decyzję? Czy opisano brakujące stany i testy dostępności bez deklarowania nieprzeprowadzonych testów?

Pokaż **pełną dokumentację**, nie samo streszczenie ani spis treści. Oznacz wersję, np. `v1`, podaj indeks, źródła i otwarte kwestie. Jeśli wynik jest plikiem, sprawdź jego zawartość oraz odsyłacze i udostępnij klikalny link. Nie zapisuj artefaktów użytkownika w katalogu instalacyjnym skilla.

Po uwagach popraw dokumentację i pokaż zaktualizowaną wersję. Akceptacja kończy etap oceny; nie jest zgodą ani sygnałem do wysyłania czegokolwiek do Figmy.

## 5. Zapytaj o pakiet dla agenta

Dopiero po ukończeniu dokumentacji dla człowieka, uwzględnieniu uwag i akceptacji wyniku zapytaj:

„Czy przygotować również pakiet dla agenta, który będzie na tej podstawie budował strony: `design.md`, style lub komponenty oraz przykłady użycia?”

Krótko wyjaśnij, że pakiet obejmuje zasady projektowania, gotowy fundament do wykorzystania w kodzie i działające przykłady. Jeśli kod już istnieje, wykorzystasz go; jeśli fundamentu brakuje, przygotujesz go na podstawie dokumentacji i sprawdzisz wizualnie. Zgoda na tak przedstawiony pakiet obejmuje tę implementację; nie proś o nią ponownie.

- Poczekaj na wyraźną zgodę. Nie przygotowuj pakietu automatycznie, przy pierwszym szkicu ani w trakcie poprawek dokumentacji dla człowieka. Przy odmowie zakończ na dokumentacji dla człowieka; bez odpowiedzi nie rozpoczynaj dodatkowego etapu.
- Jeśli użytkownik już wyraźnie zlecił cały pakiet, po ukończeniu dokumentacji dla człowieka przejdź dalej bez ponownego pytania.
- Po zgodzie przeczytaj [procedurę przygotowania pakietu dla agenta](references/agent-package.md). Zachowaj dokumentację dla człowieka jako szczegółową referencję.
