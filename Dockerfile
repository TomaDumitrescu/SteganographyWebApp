FROM alpine:edge
 
RUN apk add --update python3 py3-pip

WORKDIR /stegano

COPY . /stegano
 
RUN python3 -m venv venv && . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt
 
EXPOSE 5000
 
CMD ["/stegano/venv/bin/python", "-m", "flask", "run", "--host=0.0.0.0"]
