cd /home/DEMMYPRINCE/mysite
source myenv/bin/activate
gunicorn GOSHEN_GATES.wsgi:application --bind 0.0.0.0:8000