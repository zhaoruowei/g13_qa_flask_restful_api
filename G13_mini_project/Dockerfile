FROM python:3.9
WORKDIR /G13_Project
COPY . /G13_Project
RUN pip install -r requirements.txt
ENV PROJECT_CONFIG /G13_Project/secret/secret_config.py
RUN chmod +x /G13_Project/run.sh
CMD ["/G13_Project/run.sh"]
EXPOSE 5000

