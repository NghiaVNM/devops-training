package main

import (
	"encoding/json"
  "log"
  "net/http"
  "os"
)

type Response struct {
  Message string `json:"message"`
  Version string `json:"version"`
}

type HealthResponse struct {
  Status string `json:"status"`
}

func main() {
  mux := http.NewServeMux()

  mux.HandleFunc("/", handleRoot)
  mux.HandleFunc("/healthz", handleHealth)

  port := os.Getenv("PORT")
  if port == "" {
    port = "80"
  }

  log.Printf("Server starting on port %s", port)
  if err := http.ListenAndServe(":"+port, mux); err != nil {
    log.Fatal(err)
  }
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
  log.Printf("%s %s", r.Method, r.URL.Path)

  w.Header().Set("Content-Type", "application/json")
  json.NewEncoder(w).Encode(Response{
    Message: "Hello World from Go!",
    Version: "1.0.0",
  })
}

func handleHealth(w http.ResponseWriter, r *http.Request) {
  w.Header().Set("Content-Type", "application/json")
  json.NewEncoder(w).Encode(HealthResponse{
    Status: "ok",
  })
}