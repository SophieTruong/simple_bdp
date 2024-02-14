# pull official base image
FROM python:3.11-slim-bookworm

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Remove error when installing geopandas
RUN apt-get update
RUN apt-get install -y gdal-bin libgdal-dev g++


# install dependencies
RUN pip install --upgrade pip
ADD requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# move api source code
ADD gunicorn_config.py /usr/src/app
ADD input_data_process.py /usr/src/app
ADD app.py /usr/src/app

EXPOSE 8080

# run app
CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]