FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

#set up environment
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt-get install unzip
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

# Copy our application code
WORKDIR /var/app

# . Here means current directory.
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install git+https://github.com/PrithivirajDamodaran/Parrot_Paraphraser.git
RUN pip3 install spacy download en_core_web_sm

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8


EXPOSE 80

# Start the app
CMD ["gunicorn", "-b", "0.0.0.0:80","app:app","--workers","1","-k","uvicorn.workers.UvicornWorker"]
