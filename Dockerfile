FROM python:latest
LABEL maintainer = "DaveLin4026"

LABEL build_date = "2019-12-07"
RUN apt-get update -y && \
    apt-get upgrade -y

RUN git clone https://github.com/DaveLin4026/AppSec2.git

WORKDIR /AppSec2/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD [ "gunicorn", "AppSec2", "--bind", "0.0.0.0:8080", "--workers", "5" ]
