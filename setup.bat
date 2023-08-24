@echo off
REM Install requirements
pip install -r requirements.txt

REM Run the Streamlit app
streamlit run app.py
