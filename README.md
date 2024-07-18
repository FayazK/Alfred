# Alfred

### Instruction to run the app

1. clone the repo.

2. Create virtual environment (optional)

3. activate virtal environment

4. cd into root directory and then install the required dependecies using the command pip install -r requirements.txt.

5. run falsk server using command pthon db_server.py (setup credentials first)

3. run the app using command streamlit run App.py

### Note
Setup you tasking.ai credentials which include (Tasking ai API, chat model id, embedings model id, FLASK_PORT, FLASK_HOST).

example:

TASKING_API_KEY = tkxxxxxxxxxxxxxxxxxxxxxxxxxx

MODEL_ID = Txxxxxxx

EMBED_MODEL_ID = Txxxxxxx

FLASK_PORT=5000

FLASK_HOST=127.0.0.1

### WSGI server for production


1. create service file name.service

[Unit]

Description=Gunicorn instance to serve my Flask app

After=network.target

[Service]

User=youruser

Group=www-data

WorkingDirectory=/path/to/your/app

Environment="PATH=/path/to/your/venv/bin"

ExecStart=/path/to/your/venv/bin/gunicorn --workers 3 --bind unix:myapp.sock -m 007 wsgi:app

[Install]

WantedBy=multi-user.target


2. start and enable gunicorn service

sudo systemctl daemon-reload

sudo systemctl start myapp.service

sudo systemctl enable myapp.service

3. configure to Nginx

server {

    listen 80;
 
    server_name your_domain_or_IP;


    location / {

        include proxy_params;

        proxy_pass http://unix:/path/to/your/app/myapp.sock;

    }

}

4. Enable and the Nginx configuration and also test and restart