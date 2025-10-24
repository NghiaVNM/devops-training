#!/bin/sh
certbot renew --quiet --nginx
nginx -s reload