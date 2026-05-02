import streamlit as st
import joblib


# model load
model = joblib.load("app/data/model/model.pkl")

st.title("🚗 Ride Prediction")

col1, col2 = st.columns(2)

with col1:
    distance = st.slider("Distance (km)", 1, 20)

with col2:
    traffic = st.selectbox("Traffic Level", ["Low", "Medium", "High"])

traffic_map = {"Low": 0, "Medium": 1, "High": 2}
traffic = traffic_map[traffic]

if st.button("🚀 Check Ride"):
    prediction = model.predict([[distance, traffic]])

    if prediction[0] == 1:
        st.error("⚠️ Delay hone ka high chance hai")
    else:
        st.success("✅ Ride smooth rahegi")