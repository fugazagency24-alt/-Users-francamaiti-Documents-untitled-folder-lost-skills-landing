FROM python:3.12-slim
WORKDIR /app
COPY orbita_ads ./orbita_ads
RUN useradd --uid 10001 --create-home orbita && mkdir -p /app/data && chown orbita:orbita /app/data
USER orbita
ENV HOST=0.0.0.0 PORT=8787 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
EXPOSE 8787
CMD ["python", "-m", "orbita_ads"]
