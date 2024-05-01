FROM python:3.12

WORKDIR /workspace
COPY . .

RUN make install
CMD make
