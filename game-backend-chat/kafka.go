package main

import (
	"context"
	"log"
	"os"
	"encoding/json"

	"github.com/segmentio/kafka-go"
)

// Function to send a message to Kafka
func sendMessageToKafka(answerMessage AnswerMessage) error {
	kafkaAddr := os.Getenv("KAFKA_ADDR")
	if kafkaAddr == "" {
		kafkaAddr = "kafka:9092"
	}

	log.Printf("KAFKA_ADDR: %s", kafkaAddr)

	w := kafka.NewWriter(kafka.WriterConfig{
		Brokers:  []string{kafkaAddr},
		Topic:    "game-answers",
		Balancer: &kafka.LeastBytes{},
	})
	defer w.Close()

	// Convert message to JSON
	log.Printf("Message: %s, ", answerMessage)
	msgBytes, err := json.Marshal(answerMessage)
	if err != nil {
		log.Println("Failed to marshal message to JSON:", err)
		return err
	}

	err = w.WriteMessages(context.Background(), kafka.Message{
		Value: msgBytes,
	})
	if err != nil {
		log.Println("Failed to write message to Kafka:", err)
		return err
	}

	return nil
}
