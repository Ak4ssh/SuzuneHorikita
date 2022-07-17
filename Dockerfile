#choti bachi ho kya
FROM python:3.11.0b4

ENV PIP_NO_CACHE_DIR 1

RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# Pypi package Repo upgrade
RUN pip3 install --upgrade pip setuptools

# Copy Python Requirements to /root/SuzuneHorikita 
RUN git clone -b main https://github.com/desinobita/SuzuneHorikita /root/SuzuneHorikita
WORKDIR /root/SuzuneHorikita


#Copy config file to /root/SuzuneHorikita/SuzuneHorikita
COPY ./SuzuneHorikita/config.py ./SuzuneHorikita/config.py* /root/SuzuneHorikita/SuzuneHorikita/

ENV PATH="/home/bot/bin:$PATH"

# Install requirements

RUN pip3 install --no-cache-dir --upgrade --requirement

CMD bash start 
