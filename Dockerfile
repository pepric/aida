FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:1

# 1. Installazione pacchetti base e repository per Python 3.9 (PPA deadsnakes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    ca-certificates \
    curl \
    gnupg \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update

# 2. Installazione di Apache, PHP 8.3 (default su Ubuntu 24.04), Python 3.9 e strumenti X11
RUN apt-get install -y --no-install-recommends \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysql \
    php-gd \
    python3.9 \
    python3.9-dev \
    python3.9-distutils \
    build-essential \
    libhdf5-dev \
    saods9 \
    xvfb \
    xauth \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Abilitazione moduli Apache e PHP
# RUN a2enmod rewrite && phpenmod mysqli gd
RUN a2enmod rewrite cgi && phpenmod mysqli gd

# 3. Installazione e configurazione sicura di pip per Python 3.9
RUN curl -sS https://bootstrap.pypa.io/pip/3.9/get-pip.py | python3.9 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

# 4. Installazione delle librerie Python (compatibile con Python 3.9 per le wheels precompilate)
# Rimosso 'sklearn==0.0' che è un pacchetto fantoccio dismesso che fa fallire pip.
RUN python3.9 -m pip install --no-cache-dir --upgrade "pip<24.0" "setuptools<60.0" wheel && \
    python3.9 -m pip install --no-cache-dir --ignore-installed\
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
    #joblib==1.0.1 \
    joblib==1.2.0 \
    kiwisolver==1.3.1 \
    lxml==4.6.3 \
    matplotlib==3.4.1 \
    memory-profiler==0.58.0 \
    numpy==1.22.4 \
    Pillow==8.2.0 \
    psrecord==1.2 \
    psutil==5.8.0 \
    pycparser==2.20 \
    pyerfa==1.7.2 \
    PyMySQL==1.0.2 \
    pyparsing==2.4.7 \

    python-dateutil==2.8.1 \
    reportlab==3.5.67 \
    requests==2.26.0 \
    #scikit-learn==0.24.1 \
	scikit-learn==1.6.1 \
    scipy==1.6.2 \
    six==1.15.0 \
    svglib==1.1.0 \
    #threadpoolctl==2.1.0 \
	threadpoolctl==3.6.0 \
    tinycss2==1.1.0 \
    urllib3==1.26.7 \
    webencodings==0.5.1 \
    pypdf2==3.0.1 \
	#pandas \
	lsst_efd_client

# 5. Copia delle configurazioni
# Attenzione: su Ubuntu 24.04 il percorso predefinito di PHP 8.3 è /etc/php/8.3/apache2/php.ini
COPY apache2.conf /etc/apache2/apache2.conf
COPY php.ini /etc/php/8.3/apache2/php.ini
# Disable PHP session upload progress for security
RUN sed -i -E 's/^[[:space:]]*;?[[:space:]]*session\.upload_progress\.enabled[[:space:]]*=.*/session.upload_progress.enabled = Off/' \
    /etc/php/8.3/apache2/php.ini \
    /etc/php/8.3/cli/php.ini

# 6. Script di avvio per eseguire Xvfb in background corretto e Apache in foreground
RUN echo '#!/bin/bash\n\
set -e\n\
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1\n\
Xvfb :1 -screen 0 1024x768x16 &\n\
sleep 1\n\
exec apache2ctl -D FOREGROUND' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

EXPOSE 80
EXPOSE 3306

ENTRYPOINT ["/entrypoint.sh"]

# Verify runtime configuration and required executables
RUN test -f /etc/php/8.3/apache2/php.ini \
    && test -f /etc/php/8.3/cli/php.ini \
    && grep -Eq '^session\.upload_progress\.enabled *= *Off' /etc/php/8.3/apache2/php.ini \
    && grep -Eq '^session\.upload_progress\.enabled *= *Off' /etc/php/8.3/cli/php.ini \
    && command -v Xvfb \
    && command -v apache2ctl \
    && test -x /entrypoint.sh