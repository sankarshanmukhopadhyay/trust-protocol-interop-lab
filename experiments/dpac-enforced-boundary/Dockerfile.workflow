FROM python:3.13-alpine
WORKDIR /app
COPY workflow.py /app/workflow.py
USER 10001:10001
CMD ["python", "/app/workflow.py", "idle"]
