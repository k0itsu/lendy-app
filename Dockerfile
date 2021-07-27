FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT ["python"]
CMD ["lendy.py"]
