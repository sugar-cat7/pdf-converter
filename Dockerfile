FROM python:3.9

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    libcairo2-dev \
    pkg-config \
    youtube-dl

RUN pip install opencv-python-headless \
    pytesseract \
    fpdf

COPY main.py /app/main.py

RUN pip install opencv-python-headless pytesseract requests bs4 fpdf youtube-dl

WORKDIR /app

CMD ["python", "main.py"]
