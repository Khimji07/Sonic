# Start from the base Debian image
FROM debian:buster-slim

# Install necessary packages
RUN apt-get update
# RUN apt-get install -y build-essential
RUN apt-get install -y supervisor
RUN apt-get install -y gdebi-core
RUN apt-get install -y python3
RUN apt-get install -y libhiredis0.14 
RUN apt-get install -y libnl-nf-3-200
RUN apt-get install -y libnl-genl-3-200
RUN apt-get install -y libpython3.
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the .deb files into the container
COPY libswsscommon_1.0.0_amd64.deb /tmp/
COPY python3-swsscommon_1.0.0_amd64.deb /tmp/
COPY stp_1.0.0_amd64.deb /tmp/

# Install the .deb packages
RUN gdebi -n /tmp/libswsscommon_1.0.0_amd64.deb
RUN gdebi -n /tmp/python3-swsscommon_1.0.0_amd64.deb
RUN gdebi -n /tmp/stp_1.0.0_amd64.deb
RUN rm -f /tmp/*.deb

# Set entrypoint
# ENTRYPOINT ["sonic-stpd"]