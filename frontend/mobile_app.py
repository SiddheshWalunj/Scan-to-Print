# import sys
# import time
# from pathlib import Path

# # ---------- Project root detection ----------
# CURRENT_FILE = Path(__file__).resolve()
# PROJECT_ROOT = CURRENT_FILE
# while not (PROJECT_ROOT / "backend").exists():
#     PROJECT_ROOT = PROJECT_ROOT.parent
# sys.path.insert(0, str(PROJECT_ROOT))

# import streamlit as st

# UPLOAD_DIR = PROJECT_ROOT / "uploads"
# UPLOAD_DIR.mkdir(exist_ok=True)

# st.set_page_config(
#     page_title="Upload PDF",
#     layout="centered"
# )

# st.markdown("""
# <style>
# #MainMenu, footer, header {visibility: hidden;}
# .centered {
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
# }
# </style>
# """, unsafe_allow_html=True)

# query = st.query_params
# job_id = query.get("job_id")

# if not job_id:
#     st.markdown("<div class='centered'>", unsafe_allow_html=True)
#     st.markdown("## 📲 Ready to Upload")
#     st.markdown("Scan the QR on the printer to upload a PDF.")
#     st.markdown("</div>", unsafe_allow_html=True)
#     st.stop()

# st.markdown("<div class='centered'>", unsafe_allow_html=True)
# st.markdown("## 📄 Upload PDF")

# uploaded_file = st.file_uploader("Select PDF", type=["pdf"])

# if uploaded_file:
#     file_path = UPLOAD_DIR / f"{job_id}.pdf"
#     meta_path = UPLOAD_DIR / f"{job_id}.meta"

#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.read())

#     with open(meta_path, "w", encoding="utf-8") as meta:
#         meta.write(uploaded_file.name)

#     st.success("✅ File sent to printer")
#     st.markdown("### 🔄 Scan QR again to upload another file")

#     time.sleep(3)
#     st.query_params.clear()
#     st.rerun()

# st.markdown("</div>", unsafe_allow_html=True)
