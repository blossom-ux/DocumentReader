import numpy as np
from PIL import Image

import easyocr
import streamlit as st

st.set_page_config(
    page_title="Prism",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;600&display=swap');

        /* Глобальный стиль */
        .stApp {
            background-color: #f5f5f7;
        }

        main {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
        }

        h1, h2, h3, p, label, span, div {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
            color: #1d1d1f !important;
            -webkit-font-smoothing: antialiased;
        }

        .block-container {
            padding-top: 5rem;
            padding-bottom: 5rem;
            max-width: 750px;
        }


        .prism-hero {
            text-align: center;
            margin-bottom: 3.5rem;
        }

        .prism-title {
            font-size: 4rem;
            font-weight: 600;
            letter-spacing: -0.04em;
            margin-bottom: 0.5rem;
        }

        .prism-tagline {
            font-size: 1.4rem;
            font-weight: 300;
            color: #86868b !important;
            letter-spacing: -0.01em;
        }

        .apple-card {
            background: #ffffff;
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
            margin-bottom: 2rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .apple-card:hover {
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        }

        /* Загрузчик */
        div[data-testid="stFileUploader"] {
            background: #f5f5f7;
            border: 2px dashed #d2d2d7;
            border-radius: 18px;
            padding: 1.5rem;
            text-align: center;
        }

        div[data-testid="stFileUploader"] button {
            background-color: #0071e3 !important;
            color: #ffffff !important;
            border-radius: 980px !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            transition: background-color 0.2s ease;
        }

        div[data-testid="stFileUploader"] button:hover {
            background-color: #0077ed !important;
        }

        .prism-result-item {
            font-size: 1.05rem;
            line-height: 1.6;
            padding: 0.8rem 1rem;
            margin-bottom: 0.5rem;
            background: #f5f5f7;
            border-radius: 12px;
            color: #1d1d1f !important;
            font-weight: 400;
            word-wrap: break-word;
        }

        /* Скрываем лишнее */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="prism-hero">', unsafe_allow_html=True)
st.markdown('<div class="prism-title">Prism</div>', unsafe_allow_html=True)
st.markdown('<div class="prism-tagline">Текст из изображений. Просто и элегантно.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def get_engine():
    return easyocr.Reader(['ru', 'en'], gpu=False)

engine = get_engine()

st.markdown('<div class="apple-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Выберите изображение (JPG, PNG)",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    pil_image = Image.open(uploaded_file)
    
    with st.expander("Посмотреть исходное изображение", expanded=False):
        st.image(pil_image, use_container_width=True)

    with st.spinner("Обработка..."):
        raw_text = engine.readtext(np.array(pil_image), detail=0)

    if raw_text:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.markdown("### Результат")
        
        for line in raw_text:
            st.markdown(f'<div class="prism-result-item">{line}</div>', unsafe_allow_html=True)
        
        full_text = "\n".join(raw_text)
        st.text_area("Скопировать текст", value=full_text, height=100)
        
        filename = f"prism_{uploaded_file.name}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        st.caption(f"Файл сохранён: `{filename}`")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Текст не обнаружен. Попробуйте другое изображение.")