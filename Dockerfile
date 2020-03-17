FROM python:3.8-slim-buster

ENV GL_ACCESS_TOKEN=_xDnW3ey38c7dx76d7Ga
ENV GL_SECRET=yoloswag
ENV GL_ACCOUNT=andreasevers

EXPOSE 8080

ADD bot.py /

RUN pip install gidgetlab[aiohttp]

CMD [ "python", "./bot.py" ]