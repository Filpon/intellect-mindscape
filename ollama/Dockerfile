# Use the official Ollama image
FROM ollama/ollama:latest

# Set the working directory
WORKDIR /app
RUN apt update
RUN apt install -y curl

# Expose the port Ollama will run on
EXPOSE 11434

# Copy the startup script into the container
COPY start.sh .

# Make the script executable
RUN chmod +x start.sh
