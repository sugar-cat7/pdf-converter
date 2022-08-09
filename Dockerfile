# Replace this line to use python official image as a base.
FROM jjanzic/docker-python3-opencv
RUN python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN mkdir -p /root/opt/sample
