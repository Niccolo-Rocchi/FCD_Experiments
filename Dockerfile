FROM python:3.11

WORKDIR /workspace
COPY . .

RUN make install
CMD make
