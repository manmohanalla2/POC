FROM ubuntu:18.04

RUN apt-get update && \
	apt-get install -y python3-pip && \
	apt-get install -y nginx && \
	apt-get install -y supervisor && \
	apt-get install -y vim

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY nginx.conf /etc/nginx/sites-available/default

# Copy app
COPY ./app /app

RUN pip3 install -r /app/requirements.txt

# default command
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"] 
EXPOSE 5000
