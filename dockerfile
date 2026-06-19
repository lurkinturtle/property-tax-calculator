FROM python:3.11-slim
WORKDIR /app
RUN pip install streamlit
COPY app.py /app/taxcalc_v2_app.py
EXPOSE 8501
CMD ["streamlit", "run", "taxcalc_v2_app.pyy", "--server.port=8501", "--server.address=0.0.0.0"]
