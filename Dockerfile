FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DJANGO_DEBUG=False
ENV DJANGO_SECRET_KEY='django-insecure-b$4bni*=tlqb_0l%gw-e-giailb8ft7nd07-#$s)0-ht@_^4^_'


CMD ["gunicorn", "rustycommandcenter.wsgi"]