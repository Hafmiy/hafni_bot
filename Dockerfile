FROM python:3.10-buster as builder
RUN apt update && apt install -y git
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /tg_bot
RUN git init && git remote add origin https://github.com/Hafmiy/hafni_bot.git && git pull origin develop
RUN pip install --no-cache-dir -r  requirements.txt

FROM python:3.10-slim-buster
ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
VOLUME /log
VOLUME /config
EXPOSE 3000
COPY --from=builder tg_bot tg_bot
RUN apt update && apt remove -y imagemagick && apt install -y imagemagick
WORKDIR tg_bot
ENTRYPOINT ["python3", "-m", "app"]