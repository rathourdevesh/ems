FROM python:3.8-alpine3.15
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY requirements.txt /backend/
RUN apk add --no-cache gcc libc-dev
ENV PATH="/.venv/bin:$PATH"
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
RUN pip install -r requirements.txt
COPY . /backend/