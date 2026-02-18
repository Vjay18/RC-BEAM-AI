import streamlit as st
import numpy as np
import joblib

# Load AI model
model = joblib.load("fck_ai_model.pkl")

st.set_page_config(page_title="RC Beam AI Tool", layout="centered")

st.title("RC BEAM AI TOOL")
st.write("AI-based prediction of concrete strength and ultimate moment capacity")

st.warning(
    "Applicable ONLY for singly reinforced rectangular RC beams "
    "as per IS 456:2000 Annex G (Clause G-1.1(b))."
)

# ---------------- USER INPUTS ----------------
RN = st.number_input("Rebound Number (RN)", min_value=10.0, max_value=60.0)
UPV = st.number_input("UPV (km/s)", min_value=2.0, max_value=6.0)

b = st.number_input("Beam width b (mm)", min_value=150.0)
d = st.number_input("Effective depth d (mm)", min_value=200.0)
Ast = st.number_input("Area of tension steel Ast (mm²)", min_value=1.0)
steel_grade = st.selectbox(
    "Grade of Steel",
    ["Fe 250", "Fe 415", "Fe 500"]
)

if steel_grade == "Fe 250":
    fy = 250
elif steel_grade == "Fe 415":
    fy = 415
else:
    fy = 500

# ---------------- CALCULATION ----------------
if st.button("CALCULATE"):

    # AI prediction of fck
    X = np.array([[RN, UPV]])
    fck = model.predict(X)[0]

    st.success(f"Predicted Concrete Strength fck = {fck:.2f} MPa")

    # Concrete quality (based on UPV – IS 13311)
    if UPV >= 4.5:
        quality = "Excellent"
    elif UPV >= 3.5:
        quality = "Good"
    elif UPV >= 3.0:
        quality = "Medium"
    else:
        quality = "Poor"

    st.write(f"### Concrete Quality: {quality}")

    # -------- IS 456 Annex G (Option b) --------
    ratio = (Ast * fy) / (b * d * fck)

    if ratio >= 1:
        st.error(
            "Section exceeds singly reinforced limit. "
            "Redesign required as per IS 456:2000."
        )
    else:
        Mu = 0.87 * fy * Ast * d * (1 - ratio)
        Mu = Mu / 1e6  # Nmm → kN·m

        st.success(f"Ultimate Moment Capacity Mu = {Mu:.2f} kN·m")

        st.caption(
            "Note: Neutral axis depth is assumed within limiting depth "
            "(singly reinforced beam – IS 456 Annex G)."

        )
