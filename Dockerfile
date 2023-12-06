FROM ubuntu:latest

RUN apt update \
    && apt install -y python3 python3-pip

WORKDIR /usr/app/src

RUN pip3 install pygame
RUN pip3 install numpy

COPY project2cpu.py ./
COPY project2cpu_gui.py ./

CMD [ "python3", "./project2cpu.py", "./project2cpu_gui.py"]
