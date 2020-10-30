FROM ncsa/datawolf:develop

RUN apk add --update \
    python3 \
    python3-dev \
    build-base \
    openjdk8-jre \
    gcc \
    gfortran \
    wget \
    freetype-dev \
    libpng-dev \
    openblas-dev \
    jpeg-dev

RUN cd /usr/bin \
	&& ln -s pydoc3 pydoc \
	&& ln -s python3 python \
	&& ln -s python3-config python-config \
	&& ln -s pip3 pip

RUN pip install --upgrade pip && pip install Cython && pip install numpy scipy pandas Click seaborn xlrd

WORKDIR /home/datawolf

VOLUME /home/datawolf/data

EXPOSE 8888

CMD /home/datawolf/bin/datawolf-service
