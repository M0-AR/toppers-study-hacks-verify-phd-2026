FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY experiments/ ./experiments/
COPY benchmarks/ ./benchmarks/
COPY data/ ./data/
COPY papers/ ./papers/
CMD ["python", "benchmarks/run_all.py"]
