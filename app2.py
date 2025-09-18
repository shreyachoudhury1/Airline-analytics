import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# USER LOGIN SYSTEM
# -----------------------------
USER_CREDENTIALS = {
    "admin": "admin123",
    "user": "user123"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.success("✅ Login successful!")
    else:
        st.error("❌ Invalid username or password")

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    model = joblib.load("satisfaction_model.pkl")
    features = joblib.load("model_features.pkl")
    return model, features

# -----------------------------
# LOGIN PAGE
# -----------------------------
if not st.session_state.authenticated:
    # Background image
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1583150647472-d239652a12f5?q=80&w=327&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    [data-testid="stSidebar"] {background: rgba(255,255,255,0.8);}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Welcome to the Airline Analytics")
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login(username, password)

# -----------------------------
# MAIN APP
# -----------------------------
else:
    st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
    

    # Navigation
    st.sidebar.subheader("Go to")
    page = st.sidebar.selectbox(
        "Navigation",
        ["Home", "Passenger Satisfaction Prediction"]
    )

    # -----------------------------
    # HOME PAGE
    # -----------------------------
    if page == "Home":
        # Background image
        page_bg_img = """
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://plus.unsplash.com/premium_photo-1680284163274-af6619beac02?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDF8fGFpcmxpbmUlMjBiYWNrZ3JvdW5kJTIwYmx1cnxlbnwwfHwwfHx8MA%3D%3D");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        [data-testid="stHeader"] {background: rgba(0,0,0,0);}
        [data-testid="stSidebar"] {background: rgba(255,255,255,0.8);}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
        st.title("📌 Business Context")
        st.write("""
        To analyze passenger feedback and operational performance metrics in order to 
        identify key drivers of airline customer satisfaction, improve service quality across 
        touchpoints (booking, check-in, in-flight, baggage handling), and enhance overall 
        customer loyalty, leading to increased retention and positive brand reputation.
        """)

        st.title("🎯 Objectives")
        st.markdown("""
        - Deliver a superior and consistent passenger experience across all service touchpoints.  
        - Identify and address pain points in the customer journey, from booking to arrival.  
        - Leverage passenger feedback to enhance service quality and operational efficiency.  
        - Increase customer loyalty and retention through targeted service improvements.  
        - Reduce operational delays and improve on-time performance.  
        - Utilize data-driven insights for strategic decision-making and resource allocation.  
        """)
    # Logout button at bottom
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

    # -----------------------------
    # PREDICTION PAGE
    # -----------------------------
    elif page == "Passenger Satisfaction Prediction":
     # Background image
     page_bg_img = """
     <style>
     [data-testid="stAppViewContainer"] {
         background-image: url("https://images.unsplash.com/photo-1735126601829-892ca00155da?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTh8fGFpcmxpbmUlMjBiYWNrZ3JvdW5kJTIwYmx1cnxlbnwwfHwwfHx8MA%3D%3D");
         background-size: cover;
         background-position: center;
         background-repeat: no-repeat;
     }
     [data-testid="stHeader"] {background: rgba(0,0,0,0);}
     [data-testid="stSidebar"] {background: rgba(255,255,255,0.8);}
     </style>
     """
     st.markdown(page_bg_img, unsafe_allow_html=True)
     st.title("🤖 Passenger Satisfaction Prediction")
     model, feature_cols = load_model()

    # -----------------------------
    # Collect inputs
    # -----------------------------
     age = st.slider("Age", 0, 120, 30)  
     flight_distance = st.number_input("Flight Distance", 0, 20000, 500)
     dep_delay = st.number_input("Departure Delay in Minutes", 0, 10000, 0)
     arr_delay = st.number_input("Arrival Delay in Minutes", 0, 10000, 0)
     travel_type = st.selectbox("Type of Travel", ["Business travel", "Personal Travel"])
     cust_type = st.selectbox("Customer Type", ["Loyal Customer", "disloyal Customer"])
     travel_class = st.selectbox("Class", ["Eco", "Eco Plus", "Business"])

    # -----------------------------
    # ✅ Outlier checks (must be here)
    # -----------------------------
     if age == 0:
        st.warning("⚠️ Age is set to 0. This might not be a valid passenger age. Defaulting to Age = 1.")
        age = 1   # auto-fix
     if dep_delay > 600:
        st.warning("⚠️ Departure Delay is extremely high (>600 mins). Model capped it at 600.")
        dep_delay = 600   # auto-cap
     if arr_delay > 600:
        st.warning("⚠️ Arrival Delay is extremely high (>600 mins). Model capped it at 600.")
        arr_delay = 600   # auto-cap

    # -----------------------------
    # Build input dataframe
    # -----------------------------
     input_data = pd.DataFrame({
        "Age": [age],
        "Flight Distance": [flight_distance],
        "Departure Delay in Minutes": [dep_delay],
        "Arrival Delay in Minutes": [arr_delay],
        "Type of Travel_Business travel": [1 if travel_type=="Business travel" else 0],
        "Customer Type_Loyal Customer": [1 if cust_type=="Loyal Customer" else 0],
        "Class_Eco Plus": [1 if travel_class=="Eco Plus" else 0],
        "Class_Business": [1 if travel_class=="Business" else 0]
    })

     input_data = input_data.reindex(columns=feature_cols, fill_value=0)

    # -----------------------------
    # Prediction
    # -----------------------------
     if st.button("Predict Satisfaction"):
        proba = model.predict_proba(input_data)[0]
        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.success("✅ Passenger is **Satisfied**")
        else:
            st.error("❌ Passenger is **Dissatisfied**")

        st.subheader("📊 Prediction Confidence")
        st.write(f"Satisfied: **{proba[1]*100:.2f}%**")
        st.progress(int(proba[1]*100))
        st.write(f"Dissatisfied: **{proba[0]*100:.2f}%**")
        st.progress(int(proba[0]*100))  
    
    # Logout button at bottom
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

 
