FROM nginx

RUN mkdir -p /data/www && mkdir -p /etc/nginx/certs
COPY nginx.conf /etc/nginx/nginx.conf
COPY static_html /data/www
COPY ./cacert.pem ./serverkey.pem ./servercert.pem /etc/nginx/certs/
EXPOSE 443
