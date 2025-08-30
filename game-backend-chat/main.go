package main

import (
	"fmt"
	"log"
	"net/http"
	"math/rand"
	"os"
	"time"

	"github.com/segmentio/kafka-go"
)

func generateQuestion() (string, string) {
	rand.Seed(time.Now().UnixNano())

	// Generate two random numbers (1-99)
	numberFirst := rand.Intn(99) + 1
	numberSecond := rand.Intn(99) + 1

	// Randomly choose an operation
	operations := []string{"+", "-", "*"}
	op := operations[rand.Intn(len(operations))]

	var question string
	var answer float64

	// Create the question and calculate the answer based on the operation
	switch op {
	case "+":
		question = fmt.Sprintf("%d + %d", numberFirst, numberSecond)
		answer = float64(numberFirst + numberSecond)
	case "-":
		question = fmt.Sprintf("%d - %d", numberFirst, numberSecond)
		answer = float64(numberFirst - numberSecond)
	case "*":
		question = fmt.Sprintf("%d * %d", numberFirst, numberSecond)
		answer = float64(numberFirst * numberSecond)
	}

	return question, fmt.Sprintf("%.2f", answer)  // Return answer formatted to two decimal places
}

func main() {
	// Set up Kafka connection
	kafkaAddr := os.Getenv("KAFKA_ADDR")
	if kafkaAddr == "" {
		kafkaAddr = "kafka:9092"
	}
	r := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{kafkaAddr},
		Topic:    "game-answers",
		GroupID:  "game-backend-chat",
		MinBytes: 10e3, // 10KB
		MaxBytes: 10e6, // 10MB
	})
	defer r.Close()

	// Set up WebSocket handler
	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Println("Failed to upgrade connection:", err)
			return
		}
		defer conn.Close()

		for {
			// Generate a question
			question, correctAnswer := generateQuestion()

			// Send the question to the WebSocket
			err = conn.WriteJSON(map[string]string{"question": question, "correctAnswer": correctAnswer})
			if err != nil {
				log.Println("Failed to write message to WebSocket:", err)
				return
			}

			// Wait for the answer from the frontend
			var answerMessage AnswerMessage
			err = conn.ReadJSON(&answerMessage)
			if err != nil {
				log.Println("Failed to read message from WebSocket:", err)
			}
			log.Printf("Received Answer Message: %+v", answerMessage)

			// Send the result to Kafka
			err = sendMessageToKafka(answerMessage)
			if err != nil {
				log.Println("Failed to send message to Kafka:", err)
			}
		}
	})

	StartWebSocketServer();
}
