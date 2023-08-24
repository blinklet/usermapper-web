# Use the Python Docker image's bookwork tag
# because we need an image that also has git installed
FROM python:alpine
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN apk update && apk add git
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# The application expects a "downloads" directory
RUN mkdir ./downloads
ENTRYPOINT [ "flask" ]
CMD ["run" ]