package services

import "rustydoggobytes.com/rustycommandcenter/db"

type ItemService struct {
	db *db.Database
}

func NewItemService(db *db.Database) *ItemService {
	return &ItemService{db: db}

}
