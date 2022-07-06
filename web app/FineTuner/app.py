import streamlit as st

st.header("Fine Tuner")
st.subheader("Give us your pre trained model, we fine tune it for you")

st.markdown("Machine learning models are getting more complex each day. This leads to increasing training time and larger amount of data "\
            "necessary to proper train it, and it can be a constraint for many cases. Having this in mind, we developped this web app that "\
            "takes yours data as input and uses it to fine tune a selected pretrained model")

select_model = st.selectbox("Pre-trained model", ['yolov5'])