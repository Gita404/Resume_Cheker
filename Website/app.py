"""
Resume Checker -- Streamlit app.

Upload up to 5 PDF resumes, pick a job description, click Analyze.
"""

import streamlit as st
import time
import html as html_mod
from utils import extract_text_from_pdf
from model import analyze_resume
from job_description import JOB_LISTINGS, get_listing_labels

MAX_FILES = 5

st.set_page_config(page_title="Resume Checker", layout="wide")


# -- Styling -------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background: #fff;
        color: #1a1a1a;
    }

    /* hide streamlit header bar so title is not cropped */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    /* ── Title ────────────────────────────────────── */
    .page-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111;
        margin-bottom: 1.2rem;
    }

    /* ── Section labels ──────────────────────────── */
    .section-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #888;
        margin-bottom: 0.5rem;
    }

    /* ── JD dropdown overrides ───────────────────── */
    div[data-testid="stExpander"] {
        border: 1px solid #ddd !important;
        border-radius: 8px !important;
        background: #fafafa !important;
    }
    div[data-testid="stExpander"] details {
        border: none !important;
    }
    div[data-testid="stExpander"] summary {
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        color: #333 !important;
        padding: 0.7rem 1rem !important;
    }
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
        padding: 0 1rem 1rem !important;
    }
    .jd-text {
        font-size: 0.88rem;
        color: #444;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* ── Radio button overrides ──────────────────── */
    div[data-testid="stRadio"] label p {
        font-size: 0.9rem !important;
    }

    /* ── File uploader ───────────────────────────── */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #ccc;
        border-radius: 8px;
        padding: 0.25rem;
        background: #fafafa;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #999;
    }
    div[data-testid="stFileUploader"] small { display: none !important; }
    div[data-testid="stFileUploader"] label p {
        color: #555 !important;
        font-size: 0.88rem !important;
    }

    /* ── File list (custom) ──────────────────────── */
    .file-list {
        margin: 0.5rem 0 0.75rem;
        padding: 0;
        list-style: none;
    }
    .file-list li {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.88rem;
        color: #333;
        padding: 0.45rem 0.6rem;
        border-bottom: 1px solid #eee;
    }
    .file-list li:last-child { border-bottom: none; }
    .file-idx {
        color: #999;
        font-size: 0.8rem;
        min-width: 1.2rem;
    }

    .file-count {
        font-size: 0.82rem;
        color: #888;
        margin-top: 0.3rem;
    }

    /* ── Buttons ──────────────────────────────────── */
    .stButton > button {
        background: #111;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-size: 0.88rem;
    }
    .stButton > button:hover {
        background: #333;
        color: #fff;
    }
    .stButton > button:disabled {
        background: #ccc !important;
        color: #888 !important;
        cursor: not-allowed;
    }

    /* ── Result cards ─────────────────────────────── */
    .res-card {
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.6rem;
        height: 100%;
    }
    .res-name {
        font-size: 1rem;
        font-weight: 600;
        color: #111;
        margin-bottom: 0.4rem;
    }
    .tag-pass {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        background: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #c8e6c9;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .tag-fail {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        background: #ffebee;
        color: #c62828;
        border: 1px solid #ffcdd2;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .tag-err {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        background: #fff8e1;
        color: #f57f17;
        border: 1px solid #ffecb3;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .res-reasons {
        margin: 0;
        padding-left: 1.1rem;
        color: #444;
        font-size: 0.88rem;
        line-height: 1.75;
    }
    .res-reasons li { margin-bottom: 0.1rem; }

    .analyzing-text {
        font-size: 0.88rem;
        color: #999;
    }

    .results-divider {
        border-top: 2px solid #eee;
        margin: 1.5rem 0 1rem;
    }

    hr { border-color: #e0e0e0 !important; }
</style>
""", unsafe_allow_html=True)


# -- Helper: render result card ------------------------------------------------

def render_card(item, container):
    """Render a single result card."""
    name = html_mod.escape(item["name"])

    if item.get("error"):
        container.markdown(
            f'<div class="res-card">'
            f'<div class="res-name">{name}</div>'
            f'<div class="tag-err">Error</div>'
            f'<ul class="res-reasons"><li>{html_mod.escape(item["error"])}</li></ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    tag = '<div class="tag-pass">Shortlisted</div>' if item["is_shortlisted"] \
        else '<div class="tag-fail">Not Shortlisted</div>'

    reasons = "".join(f"<li>{html_mod.escape(r)}</li>" for r in item["reasons"])

    container.markdown(
        f'<div class="res-card">'
        f'<div class="res-name">{name}</div>'
        f'{tag}'
        f'<ul class="res-reasons">{reasons}</ul>'
        f'</div>',
        unsafe_allow_html=True,
    )


# -- Session state init --------------------------------------------------------
if "files" not in st.session_state:
    st.session_state.files = []
if "results" not in st.session_state:
    st.session_state.results = []
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False


# -- Title ---------------------------------------------------------------------
st.markdown('<div class="page-title">Resume Checker</div>', unsafe_allow_html=True)


# -- Top row: JD selection (left) + Upload (right) ----------------------------
left_col, right_col = st.columns([2, 3], gap="large")


# ── LEFT: Job Description Selection ──────────────────────────────────────────
with left_col:
    st.markdown('<div class="section-label">Select Job Description</div>', unsafe_allow_html=True)

    labels = get_listing_labels()
    selected_idx = st.radio(
        "Pick the role to check resumes against",
        range(len(labels)),
        format_func=lambda i: labels[i],
        label_visibility="collapsed",
    )

    jd = JOB_LISTINGS[selected_idx]

    # Collapsible JD details
    with st.expander(f"{jd['title']}  --  {jd['company']}", expanded=False):
        st.markdown(
            f'<div class="jd-text">{html_mod.escape(jd["description"].strip())}</div>',
            unsafe_allow_html=True,
        )


# ── RIGHT: File Upload ──────────────────────────────────────────────────────
with right_col:
    st.markdown('<div class="section-label">Upload Resumes</div>', unsafe_allow_html=True)

    file_count = len(st.session_state.files)

    # Show uploader only if under the limit
    if file_count < MAX_FILES:
        uploaded = st.file_uploader(
            f"PDF only  --  {file_count} of {MAX_FILES} added",
            type=["pdf"],
            accept_multiple_files=True,
            key=f"uploader_{file_count}",
            label_visibility="visible",
        )

        if uploaded:
            existing = {f.name for f in st.session_state.files}
            remaining = MAX_FILES - file_count
            added = False
            for f in uploaded:
                if remaining <= 0:
                    break
                if f.name not in existing:
                    st.session_state.files.append(f)
                    existing.add(f.name)
                    remaining -= 1
                    added = True
            if added:
                st.session_state.results = []
                st.session_state.analyzed = False
                st.rerun()

    # Show uploaded file list
    if st.session_state.files:
        items = "".join(
            f'<li><span class="file-idx">{i+1}.</span> {html_mod.escape(f.name)}</li>'
            for i, f in enumerate(st.session_state.files)
        )
        st.markdown(f'<ul class="file-list">{items}</ul>', unsafe_allow_html=True)

        if file_count >= MAX_FILES:
            st.markdown(
                f'<div class="file-count">All {MAX_FILES} slots filled</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="file-count">{file_count} of {MAX_FILES} added</div>',
                unsafe_allow_html=True,
            )

        # Buttons
        btn_col1, btn_col2, _ = st.columns([1, 1, 3])
        with btn_col1:
            run_btn = st.button(
                "Analyze",
                use_container_width=True,
                disabled=st.session_state.analyzed,
            )
        with btn_col2:
            clear_btn = st.button("Clear all", use_container_width=True)

        if clear_btn:
            st.session_state.files = []
            st.session_state.results = []
            st.session_state.analyzed = False
            st.rerun()
    else:
        run_btn = False


# -- Analysis + Results (full width) -------------------------------------------
if run_btn and st.session_state.files:
    st.markdown('<div class="results-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    st.session_state.results = []

    # Create columns for results grid (2-3 cards per row)
    files = st.session_state.files
    cols_per_row = min(len(files), 3)
    result_cols = st.columns(cols_per_row)

    for i, f in enumerate(files):
        col = result_cols[i % cols_per_row]

        with col:
            holder = st.empty()
            holder.markdown(
                f'<div class="res-card">'
                f'<div class="res-name">{html_mod.escape(f.name)}</div>'
                f'<div class="analyzing-text">Analyzing...</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            time.sleep(0.3)

            try:
                text = extract_text_from_pdf(f)
                if not text or len(text.strip()) < 50:
                    result = {"name": f.name, "error": "Could not read enough text from this file."}
                else:
                    result = analyze_resume(text, jd)
                    result["name"] = f.name
                    result["error"] = None
            except Exception as e:
                result = {"name": f.name, "error": str(e)}

            st.session_state.results.append(result)
            holder.empty()
            render_card(result, holder)

    st.session_state.analyzed = True
    st.rerun()

# -- Show saved results --------------------------------------------------------
elif st.session_state.results:
    st.markdown('<div class="results-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    results = st.session_state.results
    cols_per_row = min(len(results), 3)
    result_cols = st.columns(cols_per_row)

    for i, r in enumerate(results):
        col = result_cols[i % cols_per_row]
        with col:
            render_card(r, st)
