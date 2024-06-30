# Stage 1: Build Stage
FROM continuumio/miniconda3:latest AS builder

# Set environment variables for PROJ
ENV PROJ_LIB=/usr/share/proj
ENV PROJ_DIR=/usr
ENV PATH="/opt/conda/bin:$PATH"

# Set work directory
WORKDIR /app

# Install system dependencies and clean up APT lists
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    ncdu \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Update Conda, create environment, install packages, and clean up caches
RUN conda update -n base -c defaults conda && \
    conda install -y -c conda-forge python=3.12 hdf5 netcdf4 proj gdal geos && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    conda clean --all -y && \
    pip cache purge && \
    rm -rf /opt/conda/pkgs

# Install Gunicorn in the base Conda environment
RUN pip install gunicorn

# Copy the rest of your application files
COPY . .

# Stage 2: Final Stage
FROM continuumio/miniconda3:latest

# Set environment variables for PROJ
ENV PROJ_LIB=/usr/share/proj
ENV PROJ_DIR=/usr
ENV PATH="/opt/conda/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy the environment from the build stage
COPY --from=builder /opt/conda /opt/conda

# Copy application files
COPY --from=builder /app /app

# Expose the port the app runs on
EXPOSE 5001

# Run the application using Gunicorn with stdout/stderr logging
CMD ["gunicorn", "--workers", "1", "--threads", "1", "-b", "0.0.0.0:5001", "--capture-output", "--access-logfile", "-", "--error-logfile", "-", "app:app"]





