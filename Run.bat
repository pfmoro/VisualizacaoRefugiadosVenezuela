@echo off
SET VENV_PATH=.\Scripts\activate

call %VENV_PATH%

python -m streamlit run Front.py
