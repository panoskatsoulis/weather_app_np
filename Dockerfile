FROM ubuntu:latest

# Update package list and install desired packages
RUN apt update && apt upgrade -y && \
    apt install -y \
    curl emacs sqlite3 \
    iputils-ping net-tools \
    python3 python3.12-venv python3-pip && \
    apt clean

RUN mkdir /weather_app_np
WORKDIR /weather_app_np
COPY backend backend
COPY station_sim station_sim

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install flask flask-cors requests pandas

# Set default shell
CMD ["/bin/bash"]
