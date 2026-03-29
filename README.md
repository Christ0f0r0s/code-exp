# 🧠 Code Explainer (Tłumacz kodu)

## 📌 Opis projektu

Projekt **Tłumacz kodu** jest zadaniem realizowanym w ramach **modułu 8 kursu „Od zera do AI”**.

Celem aplikacji jest stworzenie narzędzia, które wykorzystuje modele językowe (LLM) do tłumaczenia i wyjaśniania kodu w sposób czytelny dla użytkownika.

Aplikacja obsługuje wiele modeli (OpenAI oraz Gemini) oraz posiada tryb demonstracyjny działający bez kluczy API.

---

## 🚀 Funkcjonalności

### 💻 Analiza kodu

* użytkownik może wkleić kod źródłowy
* aplikacja została przygotowana i zoptymalizowana pod język Python
* możliwa jest również analiza innych języków programowania, jednak wyniki mogą być mniej precyzyjne

### 🧠 Wyjaśnienia generowane przez AI

* kod jest tłumaczony na zrozumiały opis
* odpowiedź generowana przez model językowy

### 🧾 Formatowanie Markdown

* odpowiedzi są prezentowane w czytelnej strukturze:

  * nagłówki
  * listy
  * bloki kodu

### 🎚️ Poziom szczegółowości

* użytkownik może wybrać poziom szczegółowości wyjaśnienia
* od ogólnego opisu do analizy krok po kroku

### 🔁 Wybór modelu LLM

* możliwość przełączania między modelami:

  * OpenAI
  * Gemini
* dostępne tylko jeśli podane są odpowiednie klucze API

### 🧪 Tryb demonstracyjny

* aplikacja działa nawet bez kluczy API
* zamiast analizy kodu wyświetlany jest opis działania aplikacji
* pozwala przetestować interfejs bez konfiguracji

---

## 🖥️ Interfejs użytkownika

Aplikacja posiada:

* panel boczny (ustawienia modelu i szczegółowości)
* pole do wprowadzania kodu
* sekcję wyświetlania wyjaśnienia
* możliwość eksportu do:

  * Markdown (.md)
  * HTML (.html)

---

## ⚙️ Technologie

* Python
* Streamlit
* OpenAI API
* Google Gemini API

---

## 🔐 Konfiguracja (klucze API)

Aby korzystać z pełnej funkcjonalności aplikacji, należy utworzyć plik `.env` w katalogu projektu.

### Przykład:

OPENAI_API_KEY=twój_klucz_openai
GEMINI_KEY=twój_klucz_gemini

### Ważne:

* jeśli podasz tylko jeden klucz:

  * aplikacja będzie działać tylko z jednym modelem
  * nie będzie możliwe przełączanie modeli

* jeśli podasz oba klucze:

  * możliwe będzie przełączanie między OpenAI i Gemini

* brak kluczy:

  * aplikacja działa w trybie demo

---

## 📦 Instalacja i uruchomienie (uv – rekomendowane)

Projekt wykorzystuje narzędzie **uv** do zarządzania środowiskiem i zależnościami.

### 🔧 Instalacja uv

#### Windows (PowerShell)

irm https://astral.sh/uv/install.ps1 | iex

#### macOS / Linux

curl -Ls https://astral.sh/uv/install.sh | sh

#### Alternatywnie (pip)

pip install uv

---

### ▶️ Uruchomienie projektu

Po pobraniu repozytorium:

cd nazwa_projektu
uv sync
uv run streamlit run app.py

👉 `uv sync` automatycznie:

* tworzy środowisko
* instaluje wszystkie zależności

---

## 🧰 Alternatywa bez uv

Jeśli nie chcesz korzystać z `uv`, możesz zainstalować zależności ręcznie:

pip install streamlit python-dotenv openai google-generativeai markdown

Następnie uruchom:

streamlit run app.py

---

## 🧠 Uwagi końcowe

* aplikacja została zaprojektowana głównie pod analizę kodu w języku Python
* możliwa jest analiza innych języków, jednak jakość wyników może być niższa
* tryb demo umożliwia sprawdzenie działania bez konfiguracji
* projekt ma charakter edukacyjny i demonstracyjny
