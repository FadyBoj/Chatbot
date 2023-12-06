FROM tensorflow/tensorflow:latest-gpu

WORKDIR /app


RUN apt-get update && apt-get install -y git

RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey |  gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
     tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
  && \
     apt-get update

RUN apt-get install -y nvidia-container-toolkit
RUN nvidia-ctk runtime configure --runtime=docker
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN apt-get update
RUN apt-get -y install cuda-toolkit-12-3
COPY . /app

RUN pip install  -r requirements.txt


EXPOSE 5000

# Specify the command to run on container start
CMD ["python", "app.py"]
