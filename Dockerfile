FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["sh", "-c", "python db_server.py & streamlit run App.py"]
