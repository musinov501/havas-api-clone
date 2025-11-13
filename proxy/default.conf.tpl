server {
    listen ${LISTEN_PORT};
    server_name 188.166.165.119;

    location /static/ {
        alias /vol/static/;
    }

    location /media/ {
        alias /vol/static/media/;
    }

    location /health/ {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }
}