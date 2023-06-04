#specifing the docker image
FROM python:3.9-slim

#setting working directory where my app code is in.
WORKDIR /app

#copying requirements file from project woekdir to docker dir
COPY requirements.txt .

RUN pip install  -r requirements.txt

#copying the entire project code to the container
COPY main.py .

#copying the model to the docker dir
COPY key_comp  key_comp

#specfying the port that my fastapi is in
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]