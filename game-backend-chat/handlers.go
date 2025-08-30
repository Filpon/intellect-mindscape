package main

import (
	"log"
	"net/http"
	"os"
	"fmt"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

// Global variable to hold WebSocket connections
var clients = make(map[*websocket.Conn]bool) // connected clients
var broadcast = make(chan Message)            // broadcast channel

// Start the WebSocket server
func StartWebSocketServer() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8005"
	}
	log.Printf("Starting WebSocket server on port %s", port)
	err := http.ListenAndServe(fmt.Sprintf(":%s", port), nil)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
