FROM python:3.13.0b1-alpine3.18

RUN apk update
RUN pip3 install Flask
RUN pip3 install requests
RUN pip3 install python-dotenv

WORKDIR /app

COPY . .

RUN apk update && \
    apk add \
    docker-cli \
    bash

# Set the entrypoint to /bin/bash for interactive use
#ENTRYPOINT ["/bin/bash"]


CMD ["python","-u","app.py" ]