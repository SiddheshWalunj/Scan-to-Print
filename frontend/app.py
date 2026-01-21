import sys
import uuid
import time
from pathlib import Path
import streamlit.components.v1 as components


# -------------------------------------------------
# 🔧 Project root detection (bulletproof)
# -------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE
while not (PROJECT_ROOT / "backend").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from backend.models import PrintSettings
from backend.pricing import calculate_price
from backend.printer import send_to_printer
from utils.pdf_utils import get_pdf_page_count
from utils.qr_utils import generate_qr

# -------------------------------------------------
# ⚙️ Constants
# -------------------------------------------------
SCREEN = st.empty()

PRINT_DURATION_SECONDS = 10

BASE_URL = "http://192.168.0.107:8501"  # change if needed

UPLOAD_DIR = PROJECT_ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# -------------------------------------------------
# 🖥️ Page setup
# -------------------------------------------------
st.set_page_config(
    page_title="Scan to Print",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem;}
.centered {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 🔀 Routing
# -------------------------------------------------
query = st.query_params
mode = query.get("mode")          # None | upload | mobile_done
job_id = query.get("job_id")

if "printing" not in st.session_state:
    st.session_state.printing = False

# =================================================
# 📱 MOBILE — UPLOAD
# =================================================
if mode == "upload" and job_id:
    st.markdown("<div class='centered'>", unsafe_allow_html=True)
    st.markdown("## 📄 Upload PDF for Printing")

    uploaded_file = st.file_uploader("Select PDF", type=["pdf"])

    if uploaded_file:
        file_path = UPLOAD_DIR / f"{job_id}.pdf"
        meta_path = UPLOAD_DIR / f"{job_id}.meta"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        with open(meta_path, "w", encoding="utf-8") as meta:
            meta.write(uploaded_file.name)

        st.success("✅ File sent to printer")
        st.info("Scan the printer QR again to upload another file")

        time.sleep(5)

        st.query_params.clear()
        st.query_params.update({"mode": "mobile_done"})
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =================================================
# 📱 MOBILE — DONE / IDLE (REAL HTML RENDER)
# =================================================
if mode == "mobile_done":
    components.html(
    """
    <div style="
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        height:100vh;
        font-family:sans-serif;
        text-align:center;
    ">
        <h2>✅ File sent successfully</h2>
        <p>Your file has been received by the printer.</p>

        <!-- ANDROID GOOGLE LENS INTENT -->
        <a href="intent://lens.google.com/#Intent;scheme=https;package=com.google.ar.lens;end"
           style="
           margin-top:20px;
           padding:14px 26px;
           background-color:#2563eb;
           color:white;
           text-decoration:none;
           border-radius:12px;
           font-size:18px;
           font-weight:600;
           display:inline-block;">
           📷 Click here to scan the QR code again
        </a>

        <p style="margin-top:18px; font-size:14px;">
            🔹 Android: Opens Google Lens directly<br>
            🔹 iPhone: Open Camera app and scan the QR
        </p>
    </div>
    """,
    height=520
)

    st.stop()


# =================================================
# 🖨️ PRINTER MODE (DEFAULT)
# =================================================
if not job_id:
    job_id = str(uuid.uuid4())
    st.query_params.update({"job_id": job_id})

file_path = UPLOAD_DIR / f"{job_id}.pdf"
meta_path = UPLOAD_DIR / f"{job_id}.meta"

# =================================================
# 🖨️ STATE: PRINTING (FULL SCREEN, HARD STOP)
# =================================================
if st.session_state.printing:
    SCREEN.empty()

    with SCREEN.container():
        st.markdown("""
        <div class="centered" style="height:80vh;">
            <h2>🖨️ Printing in progress…</h2>
            <p style="font-size:18px;">Please wait</p>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(PRINT_DURATION_SECONDS)

    # ✅ HARD CLEANUP
    if file_path.exists():
        file_path.unlink()
    if meta_path.exists():
        meta_path.unlink()

    # ✅ RESET STATE
    st.session_state.printing = False
    st.query_params.clear()

    # FORCE FULL APP RESET
    st.rerun()
    st.stop()   # ⬅️ THIS IS CRITICAL

# =================================================
# 🖨️ STATE: WAITING FOR FILE (QR)
# =================================================
if not file_path.exists():
    upload_url = f"{BASE_URL}/?mode=upload&job_id={job_id}"

    st.markdown("<div class='centered'>", unsafe_allow_html=True)
    st.markdown("## 🖨️ Scan to Print")
    st.markdown("### 📲 Scan this QR to upload your PDF")
    st.image(generate_qr(upload_url), width=260)
    st.caption("⏳ Waiting for file upload…")
    st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(2)
    st.rerun()
    st.stop()

# =================================================
# 🖨️ STATE: FILE RECEIVED (CLEAN, NON-DIMMING)
# =================================================
with SCREEN.container():
    filename = meta_path.read_text(encoding="utf-8") if meta_path.exists() else "Uploaded Document.pdf"
    pages = get_pdf_page_count(file_path)

    st.markdown("""
    <div class="centered" style="margin-bottom:4px;">
        <h2 style="margin:0 0 4px 0;">📄 File Ready to Print</h2>
        <p style="font-size:16px; margin:0;">
            <strong>{}</strong> • {} pages
        </p>
    </div>
    <hr style="margin:6px 0 10px 0;">
    """.format(filename, pages), unsafe_allow_html=True)

    # st.markdown("<hr style='margin-bottom:10px;'>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 0.9])

    with left:
        st.subheader("🛠 Print Settings")

        color = st.toggle("🎨 Color Print", value=False)
        duplex = st.toggle("🔁 Back-to-back Printing", value=False, disabled=color)
        copies = st.number_input("📦 Number of copies", min_value=1, value=1)

        settings = PrintSettings(
            color=color,
            duplex=duplex,
            copies=copies,
            pages=pages
        )

    with right:
        amount = calculate_price(settings)

        st.subheader("💳 Payment")
        st.metric("Total Amount", f"₹ {amount}")

        payment_payload = (
                            f"upi://pay"
                            f"?pa=snwalunj007@ybl"
                            f"&pn=ScanToPrint.co"
                            f"&am={amount}"
                            f"&cu=INR"
                        )

        st.image(generate_qr(payment_payload), width=250)
        st.caption("📲 Scan to pay using any UPI app")

    st.markdown("<br>", unsafe_allow_html=True)

    center_btn = st.columns([1, 2, 1])[1]
    with center_btn:
        if st.button("✅ Print", use_container_width=True):
            st.session_state.printing = True
            SCREEN.empty()   
            st.rerun()
