import streamlit as st

st.set_page_config(
    page_title="Tłumacz kodu",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Ustawienia")

model = st.sidebar.selectbox(
    "Model LLM",
    ["OpenAI", "Gemini"]
)

# 🔊 TTS toggle
use_tts = st.sidebar.checkbox("🔊 Włącz odsłuch (TTS)", value=False)

if use_tts:
    voice = st.sidebar.selectbox(
        "Głos (TTS)",
        ["pl-PL-Marek", "pl-PL-Zofia"]
    )
    st.sidebar.caption("🔊 Odpowiedź będzie czytana na głos")

detail_level = st.sidebar.slider(
    "Poziom szczegółowości",
    min_value=1,
    max_value=5,
    value=1
)

st.sidebar.markdown("---")
#st.sidebar.info("Projekt: Code Explainer")

# =========================
# MAIN
# =========================
st.title("🧠 Tłumacz kodu")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💻 Kod")
    code_input = st.text_area(
        label="",
        height=400,
        placeholder="Wklej tutaj kod..."
    )

with col2:
    st.subheader("📄 Wyjaśnienie")
    explanation_placeholder = st.empty()
    explanation_placeholder.markdown(
        "_Tutaj pojawi się wyjaśnienie w formacie Markdown..._"
    )

# =========================
# ACTIONS
# =========================
col_btn1, col_btn2 = st.columns([1, 3])

with col_btn1:
    explain_clicked = st.button("🚀 Wyjaśnij")

with col_btn2:
    st.caption(f"Model: {model} | Szczegółowość: {detail_level}")

# =========================
# AUDIO (warunkowe)
# =========================
if use_tts:
    st.subheader("🔊 Odsłuch")
    audio_placeholder = st.empty()

# =========================
# LOGIKA (mock - BEZPIECZNA)
# =========================
if explain_clicked:
    if not code_input.strip():
        st.warning("Wklej kod")
    else:
        with st.spinner("Analizuję..."):

            
            explanation = (
                "## 📘 Wyjaśnienie kodu\n\n"
                f"Wybrany model: **{model}**\n\n"
                "### 📌 Kod wejściowy:\n\n"
                "```python\n"
                f"{code_input}\n"
                "```\n\n"
                "### 🧠 Opis:\n"
                "To jest przykładowe wyjaśnienie. W kolejnym kroku podłączymy prawdziwe LLM.\n\n"
                f"Poziom szczegółowości: **{detail_level}**\n"
            )

        explanation_placeholder.markdown(explanation)

        if use_tts:
            audio_placeholder.audio(None)  # placeholder