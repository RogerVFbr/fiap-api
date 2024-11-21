FROM public.ecr.aws/docker/library/python:3.11.6-slim
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task
COPY . ./

#RUN python -m pip install -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

RUN rm -rf /var/lib/apt/lists/*

CMD ["gunicorn", "-b=:8080", "-w=1", "app:app"]
