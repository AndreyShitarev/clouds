FROM python:3.11.4-slim

RUN addgroup --system svcgroup && adduser --system --ingroup svcgroup svcuser

WORKDIR /usr/src/app

COPY hello.py .

USER svcuser

CMD ["python", "hello.py"]
