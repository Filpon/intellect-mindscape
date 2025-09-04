package main

import (
    "time"
)

// Message structure for sending to Kafka and WebSocket
type Message struct {
	Question       string `json:"question"`
	Answer         string `json:"answer"`
	Result         string `json:"result"`
	AnswerReceived string `json:"answer_received"`
	User           string `json:"user"`  // User field for tracking who sent the message
	Content        string `json:"content"`  // Content field for general messages
	SessionID      string `json:"session_id"`  // Session ID field for tracking game sessions
}

// Answer structure for game session answers
type Answer struct {
	SessionID int  `json:"game_session_id"`
	Answer string `json:"answer"`
}

// Answer structure for game session answers
type AnswerMessage struct {
    GameId int `json:"gameId"`
	Mode string `json:"mode"`
	Question string  `json:"question"`
    UserAnswer string  `json:"userAnswer"`
	CorrectAnswer string `json:"correctAnswer"`
    IsCorrect bool  `json:"isCorrect"`
	AnswerTime time.Time `json:"answerTime"`
}
