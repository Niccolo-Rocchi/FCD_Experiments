FROM  ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Update repository
RUN	apt-get update
# Install required packages
RUN apt-get install -y git make wget software-properties-common dirmngr
# Install Python
RUN apt-get install -y python3.11 python3-pip python3.10-venv

WORKDIR /workspace
COPY . .

RUN make install
CMD bash
