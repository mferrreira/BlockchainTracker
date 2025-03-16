FROM python:3.9-slim

# Define the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot files
COPY . /app

# Run the bot
CMD ["python", "bot.py"]
