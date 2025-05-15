FROM python:3.12.3
RUN pip install pandas
WORKDIR /app
COPY . /app
ENTRYPOINT [ "python", "library_data_cleanse.py" ]