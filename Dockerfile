# Use a smaller base image with CUDA support
FROM nvidia/cuda:12.1.1-runtime-ubuntu20.04 


# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*
  
COPY . /app


RUN pip install  -r requirements.txt


# Copy your application code

# Set the default command
CMD ["python3", "app.py"]
