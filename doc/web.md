# Perylune web interface

This is highly experimental and doesn't do anything useful yet.

## Installation instructions

1. Install apache2 and wsgi for python3: sudo apt install apache2 libapache2-mod-wsgi-py3

Make sure the wsgi module is loaded

cd /etc/apache2/mods-enabled
ln -s ../mods-available/wsgi.load
ln -s ../mods-available/wsgi.conf

systemctrl restart apache2

2. Copy backend/install/apache-site.conf to /etc/apache2/sites-enabled and tweak as
   necessary.

3. Make directory, e.g. /home/perylune/public_html.

4.




## Useful docs

- https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
- PEP3333 - https://www.python.org/dev/peps/pep-3333/