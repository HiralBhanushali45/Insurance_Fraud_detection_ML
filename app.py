import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ClaimGuard | Insurance Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------
# Global Styling
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

h1, h2, h3, .cg-hero-title {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: #0A0E17;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---------------- Hero ---------------- */
.cg-hero {
    background: linear-gradient(135deg, #101828 0%, #0D1420 100%);
    border: 1px solid #232C3D;
    border-radius: 14px;
    padding: 2.2rem 2.4rem;
    margin-bottom: 1.8rem;
}
.cg-eyebrow {
    color: #3DD9C4;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    margin-bottom: 0.4rem;
}
.cg-hero-title {
    color: #F2F5FA;
    font-size: 2.1rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    line-height: 1.15;
}
.cg-hero-sub {
    color: #8892A6;
    font-size: 1rem;
    max-width: 640px;
    line-height: 1.55;
    margin-bottom: 1.4rem;
}
.cg-stats {
    display: flex;
    gap: 2.2rem;
    flex-wrap: wrap;
    border-top: 1px solid #1F2A3D;
    padding-top: 1.1rem;
}
.cg-stat-num {
    color: #E8ECF4;
    font-size: 1.25rem;
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
}
.cg-stat-label {
    color: #667085;
    font-size: 0.78rem;
    margin-top: 0.1rem;
}

/* ---------------- Section headers ---------------- */
.cg-section {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.6rem 0 0.6rem 0;
}
.cg-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
}
.cg-section-title {
    color: #E8ECF4;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.02rem;
    font-weight: 600;
}
.cg-section-sub {
    color: #667085;
    font-size: 0.8rem;
    margin: -0.3rem 0 0.8rem 1.5rem;
}

/* ---------------- Form container ---------------- */
div[data-testid="stForm"] {
    background: #121826;
    border: 1px solid #232C3D;
    border-radius: 14px;
    padding: 1.6rem 1.8rem 1.2rem 1.8rem;
}

/* Inputs */
div[data-baseweb="select"] > div, .stNumberInput input {
    background-color: #0E1420 !important;
    border-color: #263042 !important;
    color: #E8ECF4 !important;
    border-radius: 8px !important;
}
label {
    color: #B4BCCC !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* Submit button */
.stButton > button, button[kind="primary"] {
    background: linear-gradient(135deg, #3DD9C4 0%, #21B6A8 100%) !important;
    color: #06110F !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.7rem 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.01em;
}
.stButton > button:hover {
    filter: brightness(1.08);
}

/* ---------------- Result ---------------- */
.cg-verdict {
    border-radius: 12px;
    padding: 1.4rem 1.7rem;
    margin: 1.4rem 0 1rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}
.cg-verdict-fraud {
    background: linear-gradient(135deg, rgba(242,84,91,0.14), rgba(242,84,91,0.05));
    border: 1px solid rgba(242,84,91,0.4);
}
.cg-verdict-genuine {
    background: linear-gradient(135deg, rgba(61,203,120,0.14), rgba(61,203,120,0.05));
    border: 1px solid rgba(61,203,120,0.4);
}
.cg-verdict-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
}
.cg-verdict-fraud .cg-verdict-label { color: #F2545B; }
.cg-verdict-genuine .cg-verdict-label { color: #3DCB78; }
.cg-verdict-note {
    color: #9AA4B8;
    font-size: 0.85rem;
    margin-top: 0.2rem;
}
.cg-verdict-prob {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #E8ECF4;
    text-align: right;
}
.cg-verdict-prob-label {
    color: #667085;
    font-size: 0.75rem;
    text-align: right;
}

/* Risk meter */
.cg-meter-wrap {
    background: #121826;
    border: 1px solid #232C3D;
    border-radius: 12px;
    padding: 1.1rem 1.4rem 1.3rem 1.4rem;
    margin-bottom: 1rem;
}
.cg-meter-label {
    display: flex;
    justify-content: space-between;
    color: #8892A6;
    font-size: 0.78rem;
    margin-bottom: 0.5rem;
}
.cg-meter-track {
    width: 100%;
    height: 10px;
    border-radius: 6px;
    background: #1B2334;
    overflow: hidden;
}
.cg-meter-fill {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #3DCB78 0%, #F0B429 55%, #F2545B 100%);
}

/* Footer */
.cg-footer {
    color: #4B5567;
    font-size: 0.78rem;
    text-align: center;
    margin-top: 2rem;
    padding-top: 1.2rem;
    border-top: 1px solid #1B2334;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Load Trained Model
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("fraud_logistic_regression.pkl")


try:
    pipeline = load_model()
except Exception as e:
    st.error("Unable to load the trained model.")
    st.error(f"Error: {e}")
    st.stop()


# --------------------------------------------------
# Hero
# --------------------------------------------------

st.markdown("""
<div class="cg-hero">
    <div class="cg-eyebrow">CLAIMGUARD &middot; RISK ANALYTICS</div>
    <div class="cg-hero-title">Insurance Fraud Detection</div>
    <div class="cg-hero-sub">
        Submit a vehicle insurance claim below and get an instant, model-backed
        fraud risk assessment &mdash; trained on historical claim outcomes rather than
        fixed rules.
    </div>
    <div class="cg-stats">
        <div>
            <div class="cg-stat-num">9,530</div>
            <div class="cg-stat-label">Claims used for training</div>
        </div>
        <div>
            <div class="cg-stat-num">Logistic Regression</div>
            <div class="cg-stat-label">Balanced, GridSearch-tuned</div>
        </div>
        <div>
            <div class="cg-stat-num">5-fold CV</div>
            <div class="cg-stat-label">Cross-validated</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Input Form
# --------------------------------------------------

with st.form("fraud_detection_form"):

    st.markdown("""
    <div class="cg-section">
        <div class="cg-dot" style="background:#3DD9C4;"></div>
        <div class="cg-section-title">Claim Details</div>
    </div>
    <div class="cg-section-sub">How, when, and where the claim was filed</div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        gender = st.selectbox("Gender", ["M", "F"])
    with c2:
        marital_status = st.selectbox("Marital Status", ["0", "1"])
    with c3:
        property_status = st.selectbox("Property Status", ["Own", "Rent"])
    with c4:
        claim_day_of_week = st.selectbox(
            "Claim Day", ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday", "Sunday"]
        )
    with c5:
        accident_site = st.selectbox("Accident Site", ["Local", "Parking Lot", "Highway"])

    c6, c7, c8, c9, c10 = st.columns(5)
    with c6:
        witness_present = st.selectbox("Witness Present", ["0", "1"])
    with c7:
        channel = st.selectbox("Claim Channel", ["Broker", "Phone", "Online"])
    with c8:
        police_report = st.selectbox("Police Report", ["0", "1"])
    with c9:
        vehicle_category = st.selectbox("Vehicle Category", ["Compact", "Medium", "Large"])
    with c10:
        vehicle_color = st.selectbox(
            "Vehicle Color", ["red", "gray", "black", "white", "silver", "other", "blue"]
        )

    st.markdown("""
    <div class="cg-section">
        <div class="cg-dot" style="background:#8B7FF0;"></div>
        <div class="cg-section-title">Driver &amp; Policy Profile</div>
    </div>
    <div class="cg-section-sub">Who's filing, and their history with the insurer</div>
    """, unsafe_allow_html=True)

    d1, d2, d3, d4, d5 = st.columns(5)
    with d1:
        age_of_driver = st.number_input("Driver Age", min_value=16, max_value=100, value=40)
    with d2:
        safety_rating = st.number_input("Safety Rating (0-100)", min_value=0, max_value=100, value=70)
    with d3:
        annual_income = st.number_input("Annual Income ($)", min_value=0, value=60000, step=1000)
    with d4:
        high_education = st.selectbox("High Education", ["0", "1"])
    with d5:
        address_change = st.selectbox("Recent Address Change", ["0", "1"])

    d6, d7, d8, d9 = st.columns(4)
    with d6:
        past_num_of_claims = st.number_input("Past Claims", min_value=0, max_value=20, value=0)
    with d7:
        liab_prct = st.number_input("Liability %", min_value=0, max_value=100, value=50)
    with d8:
        policy_deductible = st.number_input("Deductible ($)", min_value=0, value=1000, step=100)
    with d9:
        annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=50.0)

    st.markdown("""
    <div class="cg-section">
        <div class="cg-dot" style="background:#F0B429;"></div>
        <div class="cg-section-title">Vehicle &amp; Claim Amounts</div>
    </div>
    <div class="cg-section-sub">What's being claimed, and for how much</div>
    """, unsafe_allow_html=True)

    e1, e2, e3, e4, e5, e6 = st.columns(6)
    with e1:
        age_of_vehicle = st.number_input("Vehicle Age", min_value=0, max_value=30, value=5)
    with e2:
        vehicle_price = st.number_input("Vehicle Price ($)", min_value=0, value=22000, step=500)
    with e3:
        total_claim = st.number_input("Total Claim ($)", min_value=0, value=20000, step=500)
    with e4:
        injury_claim = st.number_input("Injury Claim ($)", min_value=0, value=5000, step=100)
    with e5:
        days_open = st.number_input("Days Open", min_value=0.0, value=9.0, step=1.0)
    with e6:
        form_defects = st.number_input("Form Defects", min_value=0, max_value=20, value=4)

    st.write("")
    submitted = st.form_submit_button("🔍  Run Fraud Assessment", use_container_width=True)


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if submitted:

    new_claim = pd.DataFrame({
        "gender": [gender],
        "marital_status": [marital_status],
        "property_status": [property_status],
        "claim_day_of_week": [claim_day_of_week],
        "accident_site": [accident_site],
        "witness_present": [witness_present],
        "channel": [channel],
        "police_report": [police_report],
        "vehicle_category": [vehicle_category],
        "vehicle_color": [vehicle_color],
        "age_of_driver": [age_of_driver],
        "safety_rating": [safety_rating],
        "annual_income": [annual_income],
        "age_of_vehicle": [age_of_vehicle],
        "past_num_of_claims": [past_num_of_claims],
        "liab_prct": [liab_prct],
        "vehicle_price": [vehicle_price],
        "total_claim": [total_claim],
        "injury_claim": [injury_claim],
        "policy_deductible": [policy_deductible],
        "annual_premium": [annual_premium],
        "days_open": [days_open],
        "high_education": [high_education],
        "address_change": [address_change],
        "form_defects": [form_defects],
    })

    try:
        prediction = pipeline.predict(new_claim)[0]
        probabilities = pipeline.predict_proba(new_claim)[0]
        classes = pipeline.named_steps["model"].classes_

        if "Y" in classes:
            fraud_index = list(classes).index("Y")
            fraud_probability = probabilities[fraud_index]
        else:
            fraud_probability = 0

        pct = fraud_probability * 100
        is_fraud = prediction == "Y"

        verdict_class = "cg-verdict-fraud" if is_fraud else "cg-verdict-genuine"
        verdict_text = "🚨 Fraudulent Claim" if is_fraud else "✅ Genuine Claim"
        verdict_note = (
            "This claim shows a risk pattern consistent with fraudulent claims in the training data."
            if is_fraud else
            "This claim's pattern is consistent with genuine claims in the training data."
        )

        st.markdown(f"""
        <div class="cg-verdict {verdict_class}">
            <div>
                <div class="cg-verdict-label">{verdict_text}</div>
                <div class="cg-verdict-note">{verdict_note}</div>
            </div>
            <div>
                <div class="cg-verdict-prob">{pct:.1f}%</div>
                <div class="cg-verdict-prob-label">FRAUD PROBABILITY</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="cg-meter-wrap">
            <div class="cg-meter-label">
                <span>Low Risk</span><span>High Risk</span>
            </div>
            <div class="cg-meter-track">
                <div class="cg-meter-fill" style="width:{pct:.1f}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("View Submitted Claim Details"):
            display_data = new_claim.T
            display_data.columns = ["Value"]
            st.table(display_data)

    except Exception as e:
        st.error("Prediction failed.")
        st.exception(e)

st.markdown("""
<div class="cg-footer">
    
</div>
""", unsafe_allow_html=True)
