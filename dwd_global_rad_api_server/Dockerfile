ARG BUILD_FROM=ghcr.io/hassio-addons/base:16.0.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Add env
ENV TERM="xterm-256color"

# Install build tools, HDF5, netCDF, PROJ libraries, Python, and pip
RUN apk update && apk add --no-cache \
    build-base \
    cmake \
    ninja \
    hdf5 \
    hdf5-dev \
    netcdf \
    netcdf-dev \
    proj \
    proj-util \
    proj-dev \
    gdal \
    gdal-dev \
    python3 \
    python3-dev \
    py3-pip \
    && rm -rf /var/cache/apk/*

# Set environment variables for PROJ
ENV PROJ_LIB=/usr/share/proj
ENV PROJ_DIR=/usr
ENV PATH="/usr/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create and activate a virtual environment, then install Python dependencies
RUN python3 -m venv /app/venv \
    && . /app/venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . .

# Move services.d to the correct location for S6
RUN mkdir -p /etc/services.d \
    && cp -r /app/services.d/* /etc/services.d/ \
    && rm -rf /app/services.d

# Ensure the 'finish' and 'run' scripts are executable
RUN chmod +x /etc/services.d/dwd_global_rad_api_server/finish
RUN chmod +x /etc/services.d/dwd_global_rad_api_server/run

# Run the application using S6 init system
ENTRYPOINT ["/init"]

