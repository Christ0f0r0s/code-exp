import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
import markdown
import re

# Biblioteka OpenAI – umożliwia komunikację z modelami GPT
from openai import OpenAI

# Biblioteka Google Gemini – alternatywny model językowy
from google import genai

# =========================
# Wczytanie zmiennych środowiskowych z pliku .env
# Plik ten zawiera klucze API wymagane do komunikacji z modelami LLM
# =========================

load_dotenv()

# Sprawdzenie, czy klucze API zostały zdefiniowane
OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))
GEMINI_AVAILABLE = bool(os.getenv("GEMINI_KEY"))

# =========================
# Konfiguracja aplikacji Streamlit (tytuł i układ strony)
# =========================

st.set_page_config(
    page_title="Tłumacz kodu",
    layout="centered"
)

# =========================
# Inicjalizacja klientów API (z wykorzystaniem cache)
# Dzięki temu klient API tworzony jest tylko raz, a nie przy każdym odświeżeniu aplikacji
# =========================


@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=os.getenv("GEMINI_KEY"))

# =========================
# Panel boczny aplikacji – ustawienia użytkownika
# Użytkownik może wybrać model oraz poziom szczegółowości analizy
# =========================


st.sidebar.title("⚙️ Ustawienia")

available_models = []

if OPENAI_AVAILABLE:
    available_models.append("OpenAI")

if GEMINI_AVAILABLE:
    available_models.append("Gemini")

# Jeśli brak kluczy API – dostępny jest tylko tryb demonstracyjny
if not available_models:
    available_models = ["Demo"]

model = st.sidebar.selectbox("Model LLM", available_models)

detail_level = st.sidebar.slider(
    "Poziom szczegółowości",
    1,
    5,
    2
)

# =========================
# Budowanie promptu dla modelu językowego
# Prompt określa strukturę odpowiedzi oraz sposób analizy kodu
# =========================


def build_prompt(code_input, detail_level):
    return f"""
Wyjaśnij kod w Markdown.

## Co robi kod
- Opis ogólny (2-4 zdania)

## Jak działa
- Podziel działanie na kroki (MINIMUM 4 punkty)
- KAŻDY punkt w osobnej linii

## Na co uważać
- MINIMUM 3 problemy

Szczegółowość: {detail_level}/5

Kod:
{code_input}
"""

# =========================
# Funkcja wysyłająca zapytanie do modelu OpenAI
# =========================


def explain_openai(code_input, detail_level):
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": build_prompt(code_input, detail_level)}
        ],
        temperature=0.2,
        max_tokens=900
    )

    return response.choices[0].message.content

# =========================
# Funkcja wysyłająca zapytanie do modelu Gemini
# =========================


def explain_gemini(code_input, detail_level):
    client = get_gemini_client()

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=build_prompt(code_input, detail_level)
    )

    return getattr(response, "text", "❌ Brak odpowiedzi")

# =========================
# Tryb demonstracyjny
# Wykorzystywany, gdy nie są dostępne klucze API
# Zamiast analizy kodu prezentowany jest opis działania aplikacji
# =========================


def explain_demo(code_input, detail_level):
    return """
## Co robi kod
- Aplikacja „Tłumacz kodu” umożliwia analizę fragmentów kodu źródłowego przy użyciu modeli językowych (LLM).
- Użytkownik wprowadza kod, a system generuje jego opis w uporządkowanej formie Markdown.
- Wynik podzielony jest na trzy sekcje: opis działania, szczegółowy przebieg oraz potencjalne problemy.
- Obecnie aplikacja działa w trybie demonstracyjnym, ponieważ nie wykryto kluczy API.

## Jak działa
1. Użytkownik wprowadza kod w polu tekstowym aplikacji.
2. Po kliknięciu przycisku „Wyjaśnij” tworzony jest prompt zawierający instrukcje dla modelu językowego.
3. Aplikacja sprawdza, czy dostępne są klucze API.
4. Jeśli klucz jest dostępny, zapytanie trafia do wybranego modelu (OpenAI lub Gemini).
5. Model generuje odpowiedź w formacie Markdown.
6. Wynik jest wyświetlany w aplikacji i może zostać zapisany do pliku.

## Na co uważać
- Aby uruchomić pełną funkcjonalność aplikacji, należy dodać plik `.env` do katalogu projektu.
- W pliku `.env` można zdefiniować jedną lub obie zmienne:

  OPENAI_API_KEY=twój_klucz_openai  
  GEMINI_KEY=twój_klucz_gemini  

- Jeśli podasz tylko jeden klucz:
  - aplikacja będzie działać tylko z jednym modelem
  - nie będzie możliwe przełączanie się między modelami

- Jeśli podasz oba klucze:
  - w panelu bocznym pojawi się możliwość wyboru modelu

- Po dodaniu pliku `.env` należy ponownie uruchomić aplikację.
"""

# =========================
# Wybór sposobu przetwarzania kodu
# Funkcja decyduje, czy użyć OpenAI, Gemini czy trybu demonstracyjnego
# =========================


def explain_code(code_input, detail_level, model):
    if model == "OpenAI" and OPENAI_AVAILABLE:
        return explain_openai(code_input, detail_level)

    if model == "Gemini" and GEMINI_AVAILABLE:
        return explain_gemini(code_input, detail_level)

    return explain_demo(code_input, detail_level)

# =========================
# Poprawa formatowania list numerowanych w Markdown
# Funkcja zapewnia poprawne wyświetlanie list w HTML
# =========================


def fix_lists(text):
    text = re.sub(r"(?<!\n)(\d+\.\s)", r"\n\1", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text

# =========================
# Generowanie pliku HTML na podstawie Markdown
# Wynik jest opakowany w prosty styl CSS zapewniający czytelność
# =========================


def generate_html(text):
    text = fix_lists(text)

    html_content = markdown.markdown(
        text,
        extensions=["fenced_code", "tables"]
    )

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tłumaczenie kodu</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 40px auto;
                line-height: 1.6;
                padding: 20px;
            }}
            h2 {{
                border-bottom: 1px solid #ccc;
                padding-bottom: 5px;
                margin-top: 30px;
            }}
            code {{
                background: #f4f4f4;
                padding: 2px 6px;
                border-radius: 4px;
            }}
            pre {{
                background: #f6f8fa;
                padding: 12px;
                border-radius: 6px;
                overflow-x: auto;
            }}
            ul, ol {{
                padding-left: 20px;
            }}
        </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """

# =========================
# Główna część interfejsu aplikacji
# Umożliwia wprowadzenie kodu oraz uruchomienie analizy
# =========================


st.title("🧠 Tłumacz kodu")

if not OPENAI_AVAILABLE and not GEMINI_AVAILABLE:
    st.info("Aplikacja działa w trybie demonstracyjnym (brak kluczy API)")

code_input = st.text_area(
    "Kod",
    height=300,
    placeholder="Wklej tutaj kod..."
)

# =========================
# Obsługa przycisku uruchamiającego analizę kodu
# =========================

if st.button("🚀 Wyjaśnij"):
    if not code_input.strip():
        st.warning("Wklej kod do analizy")
    else:
        result = explain_code(code_input, detail_level, model)
        st.session_state.explanation = result

# =========================
# Wyświetlenie wyników oraz opcje eksportu
# =========================

if "explanation" in st.session_state:

    st.markdown(st.session_state.explanation)

    # Przyciski eksportu ustawione obok siebie
    col1, col2 = st.columns(2)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with col1:
        st.download_button(
            label="📄 Pobierz MD",
            data=st.session_state.explanation,
            file_name=f"tlumaczenie_{timestamp}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:
        html = generate_html(st.session_state.explanation)

        st.download_button(
            label="🌐 Pobierz HTML",
            data=html,
            file_name=f"tlumaczenie_{timestamp}.html",
            mime="text/html",
            use_container_width=True
        )
