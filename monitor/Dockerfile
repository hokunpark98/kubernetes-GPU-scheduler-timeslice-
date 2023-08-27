FROM python:3.9
ENV APP_HOME=/home/
WORKDIR $APP_HOME
COPY monitor.py monitor.py
EXPOSE 8080
RUN apt-get update && apt-get install -y sudo
RUN chmod +w /etc/sudoers
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' | tee -a /etc/sudoers
RUN chmod -w /etc/sudoers
RUN pip3 install numpy
ENTRYPOINT ["python3", "monitor.py"]