@echo off
cd /d "c:\Users\Pavel Sukhov\Desktop\DevelopNEW\exampleNEW"
call venv\Scripts\activate.bat
python -m streamlit run app.py --server.headless true --server.port 8501