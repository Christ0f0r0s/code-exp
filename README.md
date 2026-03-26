# 🧠 Code Explainer (Tłumacz kodu)

## 📌 Opis projektu

Projekt **Tłumacz kodu** jest zadaniem realizowanym w ramach **modułu 8 kursu „Od zera do AI”**.

Celem aplikacji jest stworzenie narzędzia, które wykorzystuje modele językowe (LLM) do tłumaczenia i wyjaśniania kodu w sposób czytelny dla użytkownika.

---

## 🚀 Funkcjonalności

### 💻 Analiza kodu

* użytkownik może wkleić kod (Python)
* aplikacja analizuje jego działanie

### 🧠 Wyjaśnienia generowane przez AI

* kod jest tłumaczony na zrozumiały opis
* odpowiedź generowana przez model językowy (LLM)

### 🧾 Formatowanie Markdown

* odpowiedzi są prezentowane w czytelnej strukturze:

  * nagłówki
  * listy
  * bloki kodu
* poprawia to czytelność i UX

### 🎚️ Poziom szczegółowości

* użytkownik może wybrać poziom szczegółowości wyjaśnienia
* od krótkiego opisu do szczegółowego omówienia krok po kroku

### 🔁 Wybór modelu LLM

* możliwość przełączania między modelami (np. OpenAI / Gemini)

### 🔊 Odsłuch (TTS)

* opcjonalna funkcja czytania odpowiedzi na głos
* możliwość wyboru lektora

---

## 🖥️ Interfejs użytkownika

Aplikacja posiada:

* panel boczny (ustawienia)
* obszar wprowadzania kodu
* sekcję wyświetlania wyjaśnienia
* opcjonalny odtwarzacz audio

---

## ⚙️ Technologie

* Python
* Streamlit
* LangChain
* OpenAI / Gemini API
* Edge TTS


