# import sys
# import uuid
# import time
# from pathlib import Path

# # ---------- Project root detection ----------
# CURRENT_FILE = Path(__file__).resolve()
# PROJECT_ROOT = CURRENT_FILE
# while not (PROJECT_ROOT / "backend").exists():
#     PROJECT_ROOT = PROJECT_ROOT.parent
# sys.path.insert(0, str(PROJECT_ROOT))

# import streamlit as st
# from backend.models import PrintSettings
# from backend.pricing import calculate_price
# from backend.printer import send_to_printer
# from utils.pdf_utils import get_pdf_page_count
# from utils.qr_utils import generate_qr

# PRINT_DURATION_SECONDS = 8

# st.set_page_config(
#     page_title="Scan to Print",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# st.markdown("""
# <style>
# #MainMenu, footer, header {visibility: hidden;}
# .block-container {padding-top: 2rem;}
# .centered {
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
# }
# </style>
# """, unsafe_allow_html=True)

# UPLOAD_DIR = PROJECT_ROOT / "uploads"
# UPLOAD_DIR.mkdir(exist_ok=True)

# if "printing" not in st.session_state:
#     st.session_state.printing = False

# # ---------- Job setup ----------
# if "job_id" not in st.session_state:
#     st.session_state.job_id = str(uuid.uuid4())

# job_id = st.session_state.job_id
# file_path = UPLOAD_DIR / f"{job_id}.pdf"
# meta_path = UPLOAD_DIR / f"{job_id}.meta"

# BASE_URL = "http://192.168.0.107"
# MOBILE_PORT = 8502
# upload_url = f"{BASE_URL}:{MOBILE_PORT}/?job_id={job_id}"

# # ---------- WAITING FOR FILE ----------
# if not file_path.exists():
#     st.markdown("<div class='centered'>", unsafe_allow_html=True)
#     st.markdown("## 🖨️ Scan to Print")
#     st.markdown("### 📲 Scan this QR to upload your PDF")
#     st.image(generate_qr(upload_url), width=260)
#     st.caption("⏳ Waiting for file upload…")
#     st.markdown("</div>", unsafe_allow_html=True)

#     time.sleep(2)
#     st.rerun()

# # ---------- FILE RECEIVED ----------
# filename = meta_path.read_text(encoding="utf-8") if meta_path.exists() else "Uploaded Document.pdf"
# pages = get_pdf_page_count(file_path)

# st.markdown("<div class='centered'>", unsafe_allow_html=True)
# st.markdown("## 📄 File Received")
# st.markdown(f"📁 **{filename}**")
# st.markdown(f"📄 Pages: **{pages}**")
# st.markdown("</div>", unsafe_allow_html=True)

# left, center, right = st.columns([1, 2, 1])

# with center:
#     st.subheader("🛠 Print Settings")

#     color = st.toggle("🎨 Color Print", value=False)
#     duplex = st.toggle("🔁 Back-to-back", value=False, disabled=color)
#     copies = st.number_input("📦 Copies", min_value=1, value=1)

#     settings = PrintSettings(
#         color=color,
#         duplex=duplex,
#         copies=copies,
#         pages=pages
#     )

#     amount = calculate_price(settings)
#     st.metric("💵 Amount", f"₹ {amount}")

#     payment_payload = f"upi://pay?pa=printer@upi&am={amount}&cu=INR"
#     st.image(generate_qr(payment_payload), width=200)

#     if st.button("✅ Paid & Print"):
#         send_to_printer(file_path, settings)
#         st.session_state.printing = True
#         st.rerun()

# # ---------- PRINTING & RESET ----------
# if st.session_state.printing:
#     st.markdown("<div class='centered'>", unsafe_allow_html=True)
#     st.markdown("## 🖨️ Printing…")
#     st.markdown("Please wait")
#     st.markdown("</div>", unsafe_allow_html=True)

#     time.sleep(PRINT_DURATION_SECONDS)

#     if file_path.exists():
#         file_path.unlink()
#     if meta_path.exists():
#         meta_path.unlink()

#     st.session_state.printing = False
#     st.session_state.job_id = str(uuid.uuid4())
#     st.rerun()
