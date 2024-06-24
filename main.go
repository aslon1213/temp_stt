package main

import (
	"crypto/tls"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"os/signal"
	"time"

	"github.com/gorilla/websocket"
)

func PrintNumberOFConnections(number_of_connections chan int) {
	for {
		time.Sleep(time.Second * 5)
		n := <-number_of_connections

		fmt.Printf("##################################################\n##################################################\n##################################################\n##################################################\n################################################## \n Connections number %d ##################################################\n##################################################\n##################################################\n##################################################\n################################################## \n", n)

		number_of_connections <- n
	}

}

func SendRequests(filename string, routineID int, number_of_connections chan int) {
	// Read the file before entering the loop to avoid repeated file reading
	data, err := os.ReadFile(filename)
	if err != nil {
		log.Fatalf("Error reading %s: %s", filename, err)
	}

	// Define WebSocket server URL
	u := url.URL{Scheme: "ws", Host: "127.0.0.1:9000"}
	// log.Printf("Connecting to %s", u.String())

	// Dial the server

	headers := http.Header{}
	headers.Add("language_code", "ru")

	dialer := websocket.Dialer{
		Proxy: http.ProxyFromEnvironment,
		// Custom TLS configuration if needed
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: true, // Example: Skip certificate verification
		},
		// Set custom headers if needed
		HandshakeTimeout: 10000 * time.Second,
	}

	c, _, err := dialer.Dial(u.String(), headers)
	if err != nil {
		log.Fatalf("Dial error: %s", err)
	}
	defer func() {
		err := c.Close()
		n := <-number_of_connections
		n -= 1
		number_of_connections <- n
		if err != nil {
			log.Fatalf("Close error: %s", err)
		}
	}()

	// Handle interrupt signals to gracefully close the connection
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	// starting_time := time.Now().Unix()
	time_channel := make(chan time.Time)

	done := make(chan struct{})

	// Read messages in a separate goroutine
	go func(time_channel chan time.Time) {
		defer close(done)
		for {

			_, _, err := c.ReadMessage()
			if err != nil {
				log.Printf("Read error: %s", err)
				return
			}
			current_time := time.Now()
			started_time := <-time_channel
			fmt.Println("Time Taken: ", current_time.Sub(started_time).Milliseconds())
			// log.Printf("Received %d: %s", routineID, message)
		}
	}(time_channel)

	// Send initial state message

	// Log the size of the data being sent
	// log.Printf("Data size: %d bytes", len(data))

	// Use a ticker to control the sending frequency
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()
	for {
		select {
		case <-ticker.C:
			// fmt.Printf("Routine %d: In LOOP\n", routineID)
			starting_time := time.Now()

			// Send the file data as a binary message
			err = c.WriteMessage(websocket.BinaryMessage, data)
			if err != nil {
				log.Printf("Write error (data): %s", err)
				continue
			}
			time_channel <- starting_time
			// fmt.Printf("Routine %d: Data sent successfully\n", routineID)

		case <-interrupt:
			log.Printf("Routine %d: Interrupt received, closing connection", routineID)

			// Close the connection gracefully
			err := c.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
			if err != nil {
				log.Printf("Routine %d: Write close error: %s", routineID, err)
			}

			n := <-number_of_connections
			n -= 1
			number_of_connections <- n

			select {
			case <-done:
			case <-time.After(time.Second):
			}
			return
		}
	}
}

func SendRequestsUzbek(filename string, routineID int, number_of_connections chan int) {
	// Read the file before entering the loop to avoid repeated file reading
	data, err := os.ReadFile(filename)
	if err != nil {
		log.Fatalf("Error reading %s: %s", filename, err)
	}

	// Define WebSocket server URL
	u := url.URL{Scheme: "ws", Host: "127.0.0.1:9000"}
	// log.Printf("Connecting to %s", u.String())

	// Dial the server

	headers := http.Header{}
	headers.Add("language_code", "ru")

	dialer := websocket.Dialer{
		Proxy: http.ProxyFromEnvironment,
		// Custom TLS configuration if needed
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: true, // Example: Skip certificate verification
		},
		// Set custom headers if needed
		HandshakeTimeout: 10000 * time.Second,
	}

	c, _, err := dialer.Dial(u.String(), headers)
	if err != nil {
		log.Fatalf("Dial error: %s", err)
	}
	defer func() {
		err := c.Close()
		n := <-number_of_connections
		n -= 1
		number_of_connections <- n
		if err != nil {
			log.Fatalf("Close error: %s", err)
		}
	}()

	// Handle interrupt signals to gracefully close the connection
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	// starting_time := time.Now().Unix()
	time_channel := make(chan time.Time)

	done := make(chan struct{})

	// Read messages in a separate goroutine
	go func(time_channel chan time.Time) {
		defer close(done)
		for {

			_, _, err := c.ReadMessage()
			if err != nil {
				log.Printf("Read error: %s", err)
				return
			}
			current_time := time.Now()
			started_time := <-time_channel
			fmt.Println("Time Taken: ", current_time.Sub(started_time).Milliseconds())
			// log.Printf("Received %d: %s", routineID, message)
		}
	}(time_channel)

	// Send initial state message

	// Log the size of the data being sent
	// log.Printf("Data size: %d bytes", len(data))

	// Use a ticker to control the sending frequency
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()
	for {
		select {
		case <-ticker.C:
			// fmt.Printf("Routine %d: In LOOP\n", routineID)
			starting_time := time.Now()

			// Send the file data as a binary message
			err = c.WriteMessage(websocket.BinaryMessage, data)
			if err != nil {
				log.Printf("Write error (data): %s", err)
				continue
			}
			time_channel <- starting_time
			// fmt.Printf("Routine %d: Data sent successfully\n", routineID)

		case <-interrupt:
			log.Printf("Routine %d: Interrupt received, closing connection", routineID)

			// Close the connection gracefully
			err := c.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
			if err != nil {
				log.Printf("Routine %d: Write close error: %s", routineID, err)
			}

			n := <-number_of_connections
			n -= 1
			number_of_connections <- n

			select {
			case <-done:
			case <-time.After(time.Second):
			}
			return
		}
	}
}

func main() {

	number_of_i := 10

	if os.Args[1] == "uz" {
		number_of_connections := make(chan int)

		go PrintNumberOFConnections(number_of_connections)

		// Run 10 concurrent WebSocket clients
		for i := 0; i < number_of_i; i++ {
			go SendRequestsUzbek("test_audios/ilya.wav", i, number_of_connections)

		}

		// Wait for a signal to terminate the program
		signalChannel := make(chan os.Signal, 1)
		signal.Notify(signalChannel, os.Interrupt)
		<-signalChannel

		log.Println("Received interrupt signal, shutting down...")
	} else {
		number_of_connections := make(chan int)

		go PrintNumberOFConnections(number_of_connections)

		// Run 10 concurrent WebSocket clients
		for i := 0; i < number_of_i; i++ {
			go SendRequests("test_audios/ilya.wav", i, number_of_connections)

		}

		// Wait for a signal to terminate the program
		signalChannel := make(chan os.Signal, 1)
		signal.Notify(signalChannel, os.Interrupt)
		<-signalChannel

		log.Println("Received interrupt signal, shutting down...")
	}
}
