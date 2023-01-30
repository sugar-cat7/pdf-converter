# Replace this line to use python official image as a base.
FROM jjanzic/docker-python3-opencv
RUN apt-get update
RUN apt-get -y install \
    tesseract-ocr \
    tesseract-ocr-jpn
RUN apt-get clean
RUN python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
# RUN ir -p /root/opt/sample
EXPOSE 8000
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
