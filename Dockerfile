FROM python:3.9.18 as builder

COPY ./requirements.txt ./
RUN pip3 install --target=/all_reqs -r requirements.txt --no-cache-dir

FROM python:3.9.18-slim

COPY --from=builder /all_reqs /all_reqs

WORKDIR /app

COPY ./src ./src
COPY ./main.py ./main.py

ENV PYTHONPATH="${PYTHONPATH}:/all_reqs"

CMD python3 main.py