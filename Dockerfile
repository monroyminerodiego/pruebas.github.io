# Uses a offical base image of Python
FROM python:3.9-slim

# The file that is going to be dockerized
WORKDIR /WS_app

# Copy the requirements of the container (WS_deployment)
COPY requirements.txt .

# Install all the requirements of Python
RUN pip install -r requirements.txt

# Copy the rest of the dependencies of the Flask framework
COPY . .

# Expose the port in which the application will be running
EXPOSE 5000

# Command to execute the Flask app
CMD ["flask", "run", "--host=127.0.0.1", "--port=5000"]
# CMD ["python","app.py"]