# System Rozpoznawania Gestów Dłoni

**Autorzy - zespół nr. 7**: Jakub Płowiec (gr. 3), Adrian Żerebiec (gr. 3), Michał Skałka (gr. 3), Jakub Barber (gr. 1), Radosław Kawa (gr. 1), Filip Dziurdzia (gr. 4)

---

## 1. Wprowadzenie

Projekt przedstawia system rozpoznawania gestów dłoni działający w czasie rzeczywistym. Wykorzystuje kamerę internetową do przechwytywania obrazu oraz biblioteki MediaPipe i OpenCV do jego analizy. Celem projektu było stworzenie interaktywnego interfejsu reagującego na naturalne gesty użytkownika, takie jak kciuk w górę, kciuk w dół oraz serce wykonane obiema dłońmi.


## 2. Przegląd literatury

1) Real-Time Hand Gesture Recognition: A Comprehensive Review of Techniques, Applications, and Challenges ~ Aws Saood Mohamed,  Nidaa Flaih Hassan, Abeer Salim Jamil (2024)

Tekst stanowi przegląd stanu wiedzy na temat technologii rozpoznawania gestów dłoni (HGR) w czasie rzeczywistym. Autorzy analizują ewolucję metod – od prostych algorytmów po zaawansowane sieci neuronowe – oraz omawiają ich szerokie zastosowanie (medycyna, bezpieczeństwo, język migowy). Głównym celem pracy jest zidentyfikowanie barier, takich jak wpływ otoczenia czy zapotrzebowanie na moc obliczeniową, oraz wyznaczenie kierunków rozwoju dla bardziej intuicyjnych systemów przyszłości.

2) MediaPipe Hands: On-device Real-time Hand Tracking ~ Fan Zhang, Valentin Bazarevsky, Andrey Vakunov, Andrei Tkachenka, George Sung, Chuo-Ling Chang, Matthias Grundmann (2020)

W ramach prac wykorzystano rozwiązanie MediaPipe Hands do śledzenia szkieletu dłoni w czasie rzeczywistym przy użyciu pojedynczej kamery RGB. System oparto na dwuetapowym potoku przetwarzania: detektorze wyznaczającym ramkę dłoni oraz modelu estymacji 21 punktów charakterystycznych. Rozwiązanie zapewnia wysoką precyzję i wydajność na mobilnych układach GPU, co jest kluczowe dla zastosowań w systemach AR/VR.

3) Real-Time Hand Tracking and Gesture Recognition with MediaPipe: Rerun Showcase ~ Andreas Naoum (2024)

Artykuł prezentuje połączenie biblioteki MediaPipe z narzędziem Rerun do wizualizacji śledzenia dłoni i gestów w czasie rzeczywistym. Przedstawia sposób przetwarzania obrazu z kamery na trójwymiarowe punkty charakterystyczne dłoni. Skupia się na praktycznym wdrożeniu systemu, który interpretuje ruchy użytkownika jako konkretne polecenia. Całość stanowi demonstrację budowy wydajnych i czytelnych interfejsów opartych na gestach.


## 3. Architektura Systemu

System składa się z czterech głównych modułów:

- HandDetector (`detector.py`) - Odpowiada za wykrywanie dłoni w strumieniu wideo. Wykorzystuje model MediaPipe Hand Landmarker, który identyfikuje 21 punktów charakterystycznych na każdej dłoni.
<div style="text-align:center">
<img width="300px" src="imgs/hand.png">
</div>

- GestureDetector (`gesture_detector.py`) - Analizuje pozycje wykrytych punktów charakterystycznych i rozpoznaje gesty.
- FrameDrawer (`visualizer.py`) - Rysuje szkielet dłoni (zielone linie między punktami, czerwone kropki na stawach), wyświetla status systemu (FPS, liczba wykrytych dłoni) oraz kolorowy wskaźnik rozpoznanego gestu.
- Main (`main.py`) - Główna pętla programu. Wizualizacja i przekazywanie obrazków z kamery do detektora co 50ms.

### 4. Działanie systemu

Proces detekcji odbywa się asynchronicznie w osobnym wątku, co pozwala uniknąć blokowania głównej pętli programu. Wyniki są buforowane i pobierane co 50 milisekund, zapewniając płynność działania nawet przy zmiennym obciążeniu procesora. Po otrzymaniu współrzędnych punktów charakterystycznych, moduł `GestureDetector` przeprowadza analizę geometryczną układu palców.

Dla gestu kciuka system porównuje współrzędną Y czubka kciuka (punkt 4) z jego podstawą (punkt 2). Jeśli różnica przekracza próg 0.05 jednostek znormalizowanych, gest zostaje rozpoznany jako kciuk w górę lub w dół, w zależności od kierunku. Przy geście serca algorytm wymaga wykrycia obu dłoni, następnie oblicza odległość euklidesową między kciukami oraz palcami wskazującymi obydwu rąk. Gest jest uznawany za poprawny, gdy obie odległości są mniejsze niż 0.12 jednostek, a jednocześnie rozpiętość między kciukiem a palcem wskazującym każdej ręki przekracza 0.08, co symuluje charakterystyczny kształt serca.

Projekt wykorzystuje menadżer pakietów **uv** do zarządzania środowiskiem wirtualnym Python oraz zależnościami. Konfiguracja została zautomatyzowana przez **Task** , czyli narzędzie pozwalające na definiowanie zadań w pliku `Taskfile.yml`. Przed pierwszym uruchomieniem Task automatycznie pobiera z serwerów Google model MediaPipe Hand Landmarker w wersji float16 (7.6 MB), który zawiera wytrenowaną sieć neuronową do detekcji dłoni. Wszystkie parametry systemu, takie jak częstotliwość próbkowania czy rozdzielczość kamery, są scentralizowane w klasie `AppConfig`, co ułatwia modyfikację bez ingerencji w kod źródłowy.

Co do wydajności, to system osiąga ~30 FPS na standardowym sprzęcie z kamerą 640×480. Asynchroniczne przetwarzanie z interwałem 50ms zapewnia płynne działanie bez większych opóźnień.

## 5. Prezentacja Działania

### Wykrywanie Dłoni

System wykrywa do 2 dłoni jednocześnie, rysując na nich 21 punktów charakterystycznych połączonych zielonymi liniami tworzącymi szkielet dłoni.

### Rozpoznane Gesty

1. **Kciuk w górę** - pozytywny gest rozpoznawany przez porównanie pozycji Y czubka i podstawy kciuka.

2. **Kciuk w dół** - negatywny gest wykorzystujący analogiczną metodę detekcji.

3. **Serce** - zaawansowany gest wymagający precyzyjnego ułożenia obu dłoni. System sprawdza odległość między kciukami, palcami wskazującymi oraz ich rozstawienie.

<div style="display: flex; justify-content: center; gap: 10px;">
  <img width="250px" src="imgs/thumb_up.png">
  <img width="250px" src="imgs/thumb_down.png">
  <img width="250px" src="imgs/heart.png">
</div>

## 6. Podsumowanie

W ramach projektu udało się stworzyć system, który rozpoznaje gesty dłoni w czasie rzeczywistym. Wykorzystuje on do tego biblioteki MediaPipe oraz OpenCV. Kluczowym osiągnięciem jest dość wydajnej architektury, która opiera się na asynchronicznym przetwarzaniu danych. Dzięki temu uzyskaliśmy stabilną płynność obrazu na poziomie 30 FPS. System skutecznie interpretuje gesty (kciuk w górę/dół, serce) poprzez analizę geometryczną 21 punktów charakterystycznych dłoni.
