package db

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Item struct {
	gorm.Model
	Code  string
	Price uint
}

type Database struct {
	db *gorm.DB
}

func NewDatabase() *Database {
	db, err := gorm.Open(sqlite.Open("data/test.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// Migrate the schema
	db.AutoMigrate(&Item{})
	return &Database{
		db: db,
	}

}
