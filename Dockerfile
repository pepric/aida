FROM httpd:bullseye

RUN apt-get update && apt-get install -y \
php \
libapache2-mod-php \
php-mysql \
php7.4-gd \
python3 \
python3-pip \
python-is-python3 \
saods9 \
xvfb

RUN a2enmod cgid

RUN phpenmod mysqli

RUN pip3 install \
astropy==4.2.1 \
certifi==2021.10.8 \
cffi==1.14.5 \
charset-normalizer==2.0.7 \
cryptography==3.4.7 \
cssselect2==0.4.1 \
cycler==0.10.0 \
DBUtils==2.0.1 \
h5py==3.2.1 \
idna==3.3 \
joblib==1.0.1 \
kiwisolver==1.3.1 \
lxml==4.6.3 \
matplotlib==3.4.1 \
memory-profiler==0.58.0 \
numpy==1.20.2 \
Pillow==8.2.0 \
psrecord==1.2 \
psutil==5.8.0 \
pycparser==2.20 \
pyerfa==1.7.2 \
PyMySQL==1.0.2 \
pyparsing==2.4.7 \
pypdf2==3.0.1 \
python-dateutil==2.8.1 \
reportlab==3.5.67 \
requests==2.26.0 \
scikit-learn==0.24.1 \
scipy==1.6.2 \
six==1.15.0 \
sklearn==0.0 \
svglib==1.1.0 \
threadpoolctl==2.1.0 \
tinycss2==1.1.0 \
urllib3==1.26.7 \
webencodings==0.5.1 


COPY apache2.conf /etc/apache2/apache2.conf
COPY php.ini /etc/php/7.4/apache2/php.ini
RUN export DISPLAY=:1
RUN Xvfb :1 -screen 0 1024x768x16 &

EXPOSE 80
EXPOSE 3306


CMD apache2ctl -D FOREGROUND
