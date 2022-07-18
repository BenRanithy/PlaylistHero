from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Playlist:
    db_name = 'playlist_hero'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.genres = db_data['genres']
        self.description = db_data['description']
        self.link = db_data['link']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO playlists (title, genres, description, link, user_id) VALUES (%(title)s,%(genres)s,%(description)s, %(link)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM playlists;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_playlists = []
        for row in results:
            print(row['genres'])
            all_playlists.append( cls(row) )
        return all_playlists
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM playlists WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE playlists SET title=%(title)s, genres=%(genres)s, description=%(description)s, link=%(link)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM playlists WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_playlist(playlist):
        is_valid = True
        if len(playlist['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters","playlist")
        if len(playlist['genres']) < 3:
            is_valid = False
            flash("Genres must be at least 3 characters","playlist")
        if len(playlist['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","playlist")
        if len(playlist['link']) < 3:
            is_valid = False
            flash("Link required","playlist")
        return is_valid
