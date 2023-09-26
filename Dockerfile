FROM python:3.9 

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

ENV GRADIO_SERVER_NAME=0.0.0.0

WORKDIR /usr/src/app 

COPY requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 
COPY images/ /images/

CMD [ "python", "hello.py" ] 