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

# Ustawienia strony
st.set_page_config(
    page_title="Tłumacz kodu",
    layout="centered",
    initial_sidebar_state="expanded"
)


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

# st.set_page_config(
#     page_title="Tłumacz kodu",
#     layout="centered"
# )

# =========================
# Prosty styl CSS dla aplikacji
# Zapewnia czytelność i estetykę interfejsu
# =========================


# Styl CSS – nowa wersja (bordowe tytuły, brak koloru ikon)
st.markdown("""
<style>
/* Ogólne ustawienia kolorystyki */
:root {
    --bg-primary: #f9f9f5;
    --bg-secondary: #f0f3ed;
    --text-primary: #800020;       /* Bordowy - główny kolor tytułów */
    --text-secondary: #4a5568;
    --accent: #48bb78;             /* Zielony — akcent, ale bez gradientu */
    --accent-hover: #38a169;
    --border-color: #d6e8c8;
    --card-bg: #ffffff;
    --shadow: 0 8px 24px rgba(150, 180, 140, 0.1);
    --highlight: #fff8d4;
}

/* Tło i kontenery */
body, .stApp {
    background-color: var(--bg-primary) !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

/* Nagłówki – tylko bordowy, bez gradientu */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    background: none !important;
    -webkit-background-clip: initial !important;
    -webkit-text-fill-color: inherit !important;
    background-clip: initial !important;
}

h1 {
    font-size: 2.2rem !important;
    text-shadow: none !important;
}

/* Przyciski – brak koloru ikon, akcent nie sięje się w ikonę */
.stButton > button {
    background-color: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 10px rgba(72, 187, 120, 0.2) !important;
}

.stButton > button:hover {
    background-color: var(--accent-hover) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(72, 187, 120, 0.3) !important;
}

/* Ikony w przyciskach – nie są kolorowane! */
.stButton > button svg {
    fill: currentColor !important;  /* Uwaga: CSS nie koloruje ikon w SVG, tylko używa obecnego koloru tekstu */
    color: white !important;
}

/* Pole tekstowe i inputy */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div > select {
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 12px !important;
    background-color: var(--card-bg) !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

/* Karty (np. st.container) */
.stContainer {
    background-color: var(--card-bg) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow) !important;
    padding: 20px !important;
    border: 1px solid var(--border-color) !important;
    margin-bottom: 16px !important;
}

/* Sidebar */
div[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
}

/* Podświetlenie tekstu */
.highlight {
    background-color: var(--highlight) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-weight: 500;
}

/* Alerty – bez gradientu, tylko cień i kolor tekstu */
.stAlert {
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    background-color: var(--bg-secondary) !important;
    color: var(--text-secondary) !important;
    font-size: 0.98rem !important;
}

/* Brak kolorowania ikon: dla wszystkich ikon z tła (np. strzałki, ikony bloków) */
div[data-testid="stIcon"] svg,
svg[fill="currentColor"] {
    fill: currentColor !important;
    color: inherit !important;
}
</style>
""", unsafe_allow_html=True)

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
