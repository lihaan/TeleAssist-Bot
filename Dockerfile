FROM python:3.10

# set a directory for the app
WORKDIR /Repositories/Competitions/hackgt/TeleAssistBot

# copy all the files to the container
COPY . .

# # install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the command
CMD ["python", "src/main.py"]