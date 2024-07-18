FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 7991 7881

HEALTHCHECK CMD curl --fail http://localhost:7881/_stcore/health

CMD ["sh", "-c", "python db_server.py & streamlit run App.py --server.port 7881"]
