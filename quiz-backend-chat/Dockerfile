# Using the official Golang image to create a build artifact.
FROM golang:1.24-alpine AS builder

# Setting Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code into the container
COPY . .

# Build the Go app
RUN go build -o main .

# Starting new stage from scratch
FROM alpine:3.22.1

# Copy the Pre-built binary file from the previous stage
COPY --from=builder /app/main /app/main

# Running executable
CMD ["/app/main"]
