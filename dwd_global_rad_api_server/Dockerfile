ARG BUILD_FROM=ghcr.io/hassio-addons/base:16.0.1
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Add env
ENV TERM="xterm-256color"

# Install build dependencies
RUN apk update && apk add --no-cache --virtual .build-dependencies \
    build-base=0.5-r3 \
    cmake=3.29.3-r0 \
    json-c-dev=0.17-r0 \
    libffi-dev=3.4.6-r0 \
    libuv-dev=1.48.0-r0 \
    openssl-dev=3.3.1-r0 \
    python3-dev=3.12.3-r1 \
    zlib-dev=1.3.1-r1 \
    && rm -rf /var/cache/apk/*

# Install runtime dependencies
RUN apk add --no-cache \
    hdf5 \
    hdf5-dev \
    netcdf \
    netcdf-dev \
    proj \
    proj-util \
    proj-dev \
    gdal \
    gdal-dev \
    python3=3.12.3-r1 \
    py3-pip=24.0-r2 \
    geos \
    geos-dev \
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
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && . /app/venv/bin/activate \
    && pip list

# Remove build dependencies after Python packages are installed
RUN apk del .build-dependencies

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
#ENTRYPOINT ["/init"]



