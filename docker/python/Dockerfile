FROM python:3.8

RUN apt-get update -y && apt-get install sudo gdal-bin ffmpeg -y

RUN mkdir -p /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chown -R 1000:1000 /app

RUN groupadd -g 1000 appuser && \
  useradd -r -u 1000 -g appuser appuser && \
  usermod -aG sudo appuser && \
  usermod -aG root appuser && \
  echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER appuser

WORKDIR /app

CMD sleep infinity