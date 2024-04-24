FROM  ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Update repository
RUN	apt-get update
# Install required packages
RUN apt-get install -y git make wget software-properties-common dirmngr
# Install Python3
RUN apt-get install -y python3.11 python3-pip python3.10-venv
# Install R (latest)
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc \
 | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
RUN add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/"
RUN apt-get install -y r-base r-base-dev

WORKDIR /workspace
COPY . .

RUN make install
CMD bash
