"""
Resume Checker -- Streamlit app.

Upload up to 5 PDF resumes, click Analyze, and get a
shortlisted / not-shortlisted verdict with reasons.
"""

import streamlit as st
import time
from utils import extract_text_from_pdf
from model import analyze_resume
from job_description import JOB_TITLE, JOB_DESCRIPTION, COMPANY_NAME

MAX_FILES = 5

st.set_page_config(page_title="Resume Checker", layout="centered")


# ── Helpers ──────────────────────────────────────────────────────────────

def render_card(item, container):
    """Render a single result card."""
    if item.get("error"):
        reasons_html = f'<li>{item["error"]}</li>'
        container.markdown(
            f'<div class="res-card">'
            f'<div class="res-name">{item["name"]}</div>'
            f'<div class="tag-err">Error</div>'
            f'<ul class="res-reasons">{reasons_html}</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    if item["is_shortlisted"]:
        tag = '<div class="tag-pass">Shortlisted</div>'
    else:
        tag = '<div class="tag-fail">Not Shortlisted</div>'

    reasons_html = "".join(f"<li>{reason}</li>" for reason in item["reasons"])

    container.markdown(
        f'<div class="res-card">'
        f'<div class="res-name">{item["name"]}</div>'
        f'{tag}'
        f'<ul class="res-reasons">{reasons_html}</ul>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Styling ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background: #fafafa;
    }
    .block-container {
        max-width: 700px;
        padding-top: 2rem;
    }

    .hdr-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #111;
        margin-bottom: 0.15rem;
    }
    .hdr-sub {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 1.2rem;
    }

    .file-list {
        margin: 0.6rem 0 0.8rem;
        padding: 0;
        list-style: none;
    }
    .file-list li {
        font-size: 0.85rem;
        color: #333;
        padding: 0.35rem 0;
        border-bottom: 1px solid #eee;
    }
    .file-list li:last-child { border-bottom: none; }
    .file-idx {
        display: inline-block;
        width: 1.4rem;
        color: #999;
        font-size: 0.8rem;
    }

    .res-card {
        background: #fff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
    }
    .res-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #111;
        margin-bottom: 0.4rem;
    }
    .tag-pass {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        background: #e6f4ea;
        color: #1a7f37;
        border: 1px solid #a6d5b8;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.78rem;
        margin-bottom: 0.5rem;
    }
    .tag-fail {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        background: #fef0f0;
        color: #c33;
        border: 1px solid #f0c0c0;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.78rem;
        margin-bottom: 0.5rem;
    }
    .tag-err {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        background: #fff8e1;
        color: #8a6d00;
        border: 1px solid #e6d37e;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.78rem;
        margin-bottom: 0.5rem;
    }
    .res-reasons {
        margin: 0;
        padding-left: 1rem;
        color: #444;
        font-size: 0.82rem;
        line-height: 1.7;
    }
    .res-reasons li { margin-bottom: 0.1rem; }

    .stButton > button {
        background: #222;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.45rem 1.5rem;
        font-weight: 600;
        font-size: 0.84rem;
    }
    .stButton > button:hover {
        background: #444;
        color: #fff;
    }

    div[data-testid="stFileUploader"] small { display: none !important; }
    div[data-testid="stFileUploader"] section > div { font-size: 0.82rem !important; }

    .limit-note {
        font-size: 0.8rem;
        color: #888;
        margin: 0.5rem 0 0.2rem;
    }

    hr { border-color: #e5e5e5; }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────────────────
st.markdown(f'<div class="hdr-title">Resume Checker</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hdr-sub">Checking against: {JOB_TITLE} -- {COMPANY_NAME}</div>',
    unsafe_allow_html=True,
)

with st.expander("View full job description"):
    st.text(JOB_DESCRIPTION.strip())

st.divider()


# ── Session state ────────────────────────────────────────────────────────
if "files" not in st.session_state:
    st.session_state.files = []
if "results" not in st.session_state:
    st.session_state.results = []


# ── File uploader (hidden once limit reached) ───────────────────────────
count = len(st.session_state.files)

if count < MAX_FILES:
    uploaded = st.file_uploader(
        f"Upload resumes (PDF only) -- {count}/{MAX_FILES} added",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"up_{count}",
    )
    if uploaded:
        remaining = MAX_FILES - count
        for f in uploaded[:remaining]:
            existing_names = [x.name for x in st.session_state.files]
            if f.name not in existing_names:
                st.session_state.files.append(f)
        st.session_state.results = []
        st.rerun()
else:
    st.markdown(
        f'<div class="limit-note">Maximum of {MAX_FILES} resumes reached.</div>',
        unsafe_allow_html=True,
    )


# ── Show uploaded files + action buttons ─────────────────────────────────
if st.session_state.files:
    items_html = "".join(
        f'<li><span class="file-idx">{i+1}.</span> {f.name}</li>'
        for i, f in enumerate(st.session_state.files)
    )
    st.markdown(f'<ul class="file-list">{items_html}</ul>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        run_analysis = st.button("Analyze")
    with col_b:
        clear_all = st.button("Clear all")

    if clear_all:
        st.session_state.files = []
        st.session_state.results = []
        st.rerun()

    # ── Run analysis one-by-one ──────────────────────────────────────────
    if run_analysis:
        st.session_state.results = []
        st.divider()

        for f in st.session_state.files:
            holder = st.empty()
            holder.markdown(
                f'<div class="res-card">'
                f'<div class="res-name">{f.name}</div>'
                f'<div style="font-size:0.82rem;color:#888;">Analyzing...</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            time.sleep(0.3)

            try:
                text = extract_text_from_pdf(f)
                if not text or len(text.strip()) < 50:
                    result = {
                        "name": f.name,
                        "error": "Could not read enough text from this PDF.",
                    }
                else:
                    result = analyze_resume(text)
                    result["name"] = f.name
                    result["error"] = None
            except Exception as e:
                result = {"name": f.name, "error": str(e)}

            st.session_state.results.append(result)

            holder.empty()
            render_card(result, holder)

    # ── Show previous results if they exist ──────────────────────────────
    elif st.session_state.results:
        st.divider()
        for r in st.session_state.results:
            render_card(r, st)
