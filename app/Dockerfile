#FROM public.ecr.aws/docker/library/python:3.11.6-slim
#COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter
#WORKDIR /var/task
#COPY . ./
#
#RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu && \
#    rm -rf /var/lib/apt/lists/*
#
## Remover
##EXPOSE 8080
#
#CMD ["gunicorn", "-b=:8080", "-w=1", "app:app"]


# Stage 1: Builder
FROM public.ecr.aws/docker/library/python:3.11.6-slim AS builder

WORKDIR /app

# Copy only requirements to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Stage 2: Final Image
FROM public.ecr.aws/docker/library/python:3.11.6-slim

WORKDIR /var/task

# Copy Lambda adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Clean up unnecessary files to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache

CMD ["gunicorn", "-b=:8080", "-w=1", "app:app"]