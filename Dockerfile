FROM python:3.9
COPY . .
RUN pip install -r requirements.txt
RUN python routes/cities_data.py
CMD ["python", "routes/main.py"]