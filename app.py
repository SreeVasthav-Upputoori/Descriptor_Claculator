import streamlit as st
import pandas as pd
import numpy as np
import io
from typing import Optional

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Descriptor Calculator",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
    animation: shimmer 4s infinite linear;
}
@keyframes shimmer {
    0%   { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 2px 15px rgba(0,0,0,0.3);
    position: relative;
}
.hero-sub {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.85);
    margin-top: 0.5rem;
    position: relative;
}
.hero-emoji {
    font-size: 2rem;
    margin-bottom: 0.3rem;
    display: block;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(102,126,234,0.3);
}
/* Sidebar labels only (not widget internals) */
section[data-testid="stSidebar"] label {
    color: #a5b4fc !important;
    font-weight: 600;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
/* Sidebar markdown text (our own headings and paragraphs) */
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4 {
    color: #a5b4fc !important;
}
/* Sidebar checkbox label span */
section[data-testid="stSidebar"] .stCheckbox span { color: #e2e8f0 !important; }
/* Sidebar slider current-value display */
section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
    color: #a5b4fc !important;
}
.sidebar-logo {
    text-align: center;
    padding: 1rem 0 1.5rem;
    border-bottom: 1px solid rgba(102,126,234,0.25);
    margin-bottom: 1.5rem;
}
.sidebar-logo h2 {
    color: #a5b4fc !important;
    font-family: 'Outfit', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0.3rem 0 0;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(102,126,234,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: border-color 0.3s ease;
}
.card:hover {
    border-color: rgba(102,126,234,0.5);
}
.card-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    color: #a5b4fc;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Stat chips ── */
.stat-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.stat-chip {
    background: linear-gradient(135deg, rgba(102,126,234,0.25), rgba(118,75,162,0.25));
    border: 1px solid rgba(102,126,234,0.4);
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.stat-num {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #a5b4fc;
}
.stat-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.6);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(102,126,234,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(102,126,234,0.6) !important;
}

/* ── Download buttons ── */
.stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #667eea, #f093fb) !important;
    border-radius: 10px !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* ── Status text ── */
.status-box {
    background: rgba(102,126,234,0.15);
    border-left: 3px solid #667eea;
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 1rem;
    color: #a5b4fc;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

/* ── Success box ── */
.success-box {
    background: rgba(52,211,153,0.12);
    border: 1px solid rgba(52,211,153,0.4);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #6ee7b7;
    font-weight: 500;
    margin-bottom: 1rem;
}

/* ── Warning ── */
.stAlert { border-radius: 12px !important; }

/* Only our own markdown headings in the main area */
[data-testid="stMarkdownContainer"] h3 { color: #c7d2fe !important; }
[data-testid="stMarkdownContainer"] h4 { color: #a5b4fc !important; }
/* Expander header */
[data-testid="stExpander"] summary span { color: #a5b4fc !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span style="font-size:2.2rem">⚗️</span>
        <h2>Descriptor Calculator</h2>
        <span style="font-size:0.75rem; color:rgba(165,180,252,0.6);">v1.0 · Cheminformatics Suite</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📋 Descriptor Types")
    descriptor_choices = st.multiselect(
        "Select what to calculate",
        options=["RDKit Descriptors", "Mordred Descriptors", "Morgan Fingerprints"],
        default=["RDKit Descriptors"],
        help="You can select multiple descriptor types. All will be merged into one output sheet.",
    )

    # Morgan options – only shown when needed
    morgan_radius = 2
    morgan_nbits = 2048
    morgan_use_counts = False
    if "Morgan Fingerprints" in descriptor_choices:
        st.markdown("---")
        st.markdown("#### 🔬 Morgan FP Settings")
        morgan_radius = st.slider("Radius", min_value=1, max_value=4, value=2, step=1)
        morgan_nbits = st.selectbox("nBits", options=[512, 1024, 2048], index=2)
        morgan_use_counts = st.checkbox("Use count vectors (vs bit)", value=False)

    st.markdown("---")
    st.markdown("#### ⚙️ Column Settings")
    smiles_col_hint = st.text_input(
        "SMILES column name (leave blank to auto-detect)",
        value="",
        placeholder="e.g. SMILES, smiles, canonical_smiles",
    )

    st.markdown("---")
    st.markdown(
        "<span style='font-size:0.75rem; color:rgba(165,180,252,0.5);'>"
        "Built with RDKit · Mordred · Streamlit</span>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <span class="hero-emoji">⚗️</span>
    <p class="hero-title">Descriptor Calculator</p>
    <p class="hero-sub">Calculate RDKit · Mordred · Morgan Fingerprints from your molecular dataset</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def detect_smiles_col(df: pd.DataFrame, hint: str) -> Optional[str]:
    if hint.strip():
        if hint.strip() in df.columns:
            return hint.strip()
        else:
            return None
    candidates = ["smiles", "canonical_smiles", "isomeric_smiles", "smi", "structure"]
    for col in df.columns:
        if col.strip().lower() in candidates:
            return col
    return None


def calc_rdkit(mol):
    from rdkit.Chem import Descriptors
    from rdkit.ML.Descriptors import MoleculeDescriptors
    desc_names = [d[0] for d in Descriptors.descList]
    calc = MoleculeDescriptors.MolecularDescriptorCalculator(desc_names)
    return dict(zip(desc_names, calc.CalcDescriptors(mol)))


def calc_mordred(mol):
    from mordred import Calculator, descriptors as mordred_desc
    calc = Calculator(mordred_desc, ignore_3D=True)
    result = calc(mol)
    return {str(k): (float(v) if not isinstance(v, Exception) else np.nan)
            for k, v in result.items()}


def calc_morgan(mol, radius, nbits, use_counts):
    from rdkit.Chem import AllChem
    if use_counts:
        fp = AllChem.GetHashedMorganFingerprint(mol, radius, nBits=nbits)
        arr = np.zeros(nbits, dtype=np.int32)
        from rdkit.DataStructs import ConvertToNumpyArray
        ConvertToNumpyArray(fp, arr)
    else:
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nbits)
        arr = np.zeros(nbits, dtype=np.int8)
        from rdkit.DataStructs import ConvertToNumpyArray
        ConvertToNumpyArray(fp, arr)
    return {f"Morgan_r{radius}_{i}": int(arr[i]) for i in range(nbits)}


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Descriptors")
    return buf.getvalue()


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


# ══════════════════════════════════════════════════════════════════════════════
#  FILE UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
col_upload, col_info = st.columns([2, 1])

with col_upload:
    st.markdown('<div class="card"><div class="card-title">📂 Upload CSV File</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag & drop or browse — must contain a SMILES column",
        type=["csv"],
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_info:
    st.markdown("""
    <div class="card" style="height:100%">
        <div class="card-title">💡 How it works</div>
        <ol style="color:#cbd5e1;font-size:0.88rem;line-height:1.8;padding-left:1.2rem;margin:0">
            <li>Upload your CSV file</li>
            <li>Choose descriptors in sidebar</li>
            <li>Click <b>Calculate</b></li>
            <li>Download results</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PREVIEW & RUN
# ══════════════════════════════════════════════════════════════════════════════
if uploaded_file:
    try:
        df_input = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read CSV: {e}")
        st.stop()

    smiles_col = detect_smiles_col(df_input, smiles_col_hint)
    if smiles_col is None:
        st.warning("⚠️ Could not detect a SMILES column. Specify it in the sidebar settings.")
        smiles_col = st.selectbox("Select the SMILES column manually:", options=df_input.columns.tolist())

    # Info row
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-chip"><span class="stat-num">{len(df_input)}</span><span class="stat-label">Molecules</span></div>
        <div class="stat-chip"><span class="stat-num">{len(df_input.columns)}</span><span class="stat-label">Input Columns</span></div>
        <div class="stat-chip"><span class="stat-num">{len(descriptor_choices)}</span><span class="stat-label">Descriptor Sets</span></div>
        <div class="stat-chip"><span class="stat-num">{uploaded_file.name}</span><span class="stat-label">File</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Preview
    with st.expander("🔍 Preview input data", expanded=False):
        st.dataframe(df_input.head(10), use_container_width=True)

    if not descriptor_choices:
        st.warning("⚠️ Please select at least one descriptor type from the sidebar.")
        st.stop()

    # ── RUN BUTTON ────────────────────────────────────────────────────────────
    run_col, _ = st.columns([1, 3])
    with run_col:
        run_btn = st.button("⚡ Calculate Descriptors", use_container_width=True)

    if run_btn:
        try:
            from rdkit import Chem
        except ImportError:
            st.error("❌ RDKit is not installed. Run: `pip install rdkit`")
            st.stop()

        smiles_list = df_input[smiles_col].astype(str).tolist()
        n = len(smiles_list)

        st.markdown("---")
        st.markdown("### ⚙️ Calculating Descriptors…")

        progress_bar = st.progress(0)
        status_text  = st.empty()
        mol_counter  = st.empty()

        records = []
        errors  = []

        for i, smi in enumerate(smiles_list):
            frac = (i + 1) / n
            progress_bar.progress(frac)
            mol_counter.markdown(
                f'<div class="status-box">🔬 Molecule {i+1} / {n} &nbsp;·&nbsp; '
                f'{frac*100:.1f}% complete</div>',
                unsafe_allow_html=True,
            )

            row = {smiles_col: smi}

            mol = Chem.MolFromSmiles(smi)
            if mol is None:
                errors.append(i + 1)
                for dc in descriptor_choices:
                    row[f"_error_{dc}"] = "Invalid SMILES"
                records.append(row)
                continue

            # ── RDKit ──────────────────────────────────────────────────────
            if "RDKit Descriptors" in descriptor_choices:
                status_text.markdown(
                    '<div class="status-box">📐 Computing RDKit descriptors…</div>',
                    unsafe_allow_html=True,
                )
                try:
                    row.update(calc_rdkit(mol))
                except Exception as e:
                    row["RDKit_error"] = str(e)

            # ── Mordred ────────────────────────────────────────────────────
            if "Mordred Descriptors" in descriptor_choices:
                status_text.markdown(
                    '<div class="status-box">🧬 Computing Mordred descriptors…</div>',
                    unsafe_allow_html=True,
                )
                try:
                    row.update(calc_mordred(mol))
                except ImportError:
                    row["Mordred_error"] = "mordred not installed"
                except Exception as e:
                    row["Mordred_error"] = str(e)

            # ── Morgan ─────────────────────────────────────────────────────
            if "Morgan Fingerprints" in descriptor_choices:
                status_text.markdown(
                    f'<div class="status-box">🔑 Computing Morgan FP '
                    f'(r={morgan_radius}, nBits={morgan_nbits})…</div>',
                    unsafe_allow_html=True,
                )
                try:
                    row.update(calc_morgan(mol, morgan_radius, morgan_nbits, morgan_use_counts))
                except Exception as e:
                    row["Morgan_error"] = str(e)

            records.append(row)

        # ── Finalise ───────────────────────────────────────────────────────
        progress_bar.progress(1.0)
        status_text.empty()
        mol_counter.empty()

        df_result = pd.DataFrame(records)

        # Merge other input columns (except SMILES, already in df_result)
        other_cols = [c for c in df_input.columns if c != smiles_col]
        if other_cols:
            df_result = pd.concat([df_input[other_cols].reset_index(drop=True), df_result], axis=1)

        st.session_state["df_result"] = df_result
        st.session_state["errors"]    = errors


# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if "df_result" in st.session_state:
    df_result = st.session_state["df_result"]
    errors    = st.session_state.get("errors", [])

    n_ok  = len(df_result) - len(errors)
    n_col = len(df_result.columns)

    st.markdown(f"""
    <div class="success-box">
        ✅ Calculation complete — <b>{n_ok}</b> molecules processed successfully,
        <b>{n_col}</b> columns in output
        {f"· ⚠️ {len(errors)} invalid SMILES (rows: {', '.join(map(str,errors[:10]))}{'…' if len(errors)>10 else ''})" if errors else ""}
    </div>
    """, unsafe_allow_html=True)

    # Result stats
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-chip"><span class="stat-num">{n_ok}</span><span class="stat-label">Valid Mols</span></div>
        <div class="stat-chip"><span class="stat-num">{len(errors)}</span><span class="stat-label">Errors</span></div>
        <div class="stat-chip"><span class="stat-num">{n_col}</span><span class="stat-label">Features</span></div>
        <div class="stat-chip"><span class="stat-num">{df_result.shape[0]}</span><span class="stat-label">Rows</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Preview result
    st.markdown("### 📊 Results Preview")
    st.dataframe(df_result.head(20), use_container_width=True, height=320)

    # ── DOWNLOAD ──────────────────────────────────────────────────────────────
    st.markdown("### 💾 Download Results")
    dl_col1, dl_col2, _ = st.columns([1, 1, 2])

    with dl_col1:
        excel_bytes = to_excel_bytes(df_result)
        st.download_button(
            label="📥 Download as Excel (.xlsx)",
            data=excel_bytes,
            file_name="descriptors.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with dl_col2:
        csv_bytes = to_csv_bytes(df_result)
        st.download_button(
            label="📥 Download as CSV (.csv)",
            data=csv_bytes,
            file_name="descriptors.csv",
            mime="text/csv",
            use_container_width=True,
        )

else:
    if not uploaded_file:
        st.markdown("""
        <div style="text-align:center; padding:4rem 0; color:rgba(255,255,255,0.35);">
            <div style="font-size:4rem">📂</div>
            <div style="font-size:1.1rem; margin-top:1rem;">Upload a CSV file to get started</div>
        </div>
        """, unsafe_allow_html=True)
