package main

import (
	"log/slog"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"rustydoggobytes.com/rustycommandcenter/db"
	"rustydoggobytes.com/rustycommandcenter/services"
)

func main() {
	db := db.NewDatabase()
	services.NewItemService(db)

	r := chi.NewRouter()
	r.Use(middleware.Logger)
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("welcome"))
	})

	slog.Info("Starting on port 3000")
	http.ListenAndServe(":3000", r)
}
