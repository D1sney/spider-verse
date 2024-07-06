FROM python:3.11

WORKDIR /usr/src/app
# requirements устанавливается раньше всей основной директории чтобы при изменении кода мы каждый раз не устанавливали заново все библиотеки, это сделано для оптимизации
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]