from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

class Playlist:
    db_name = 'playlist_hero'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.genres = db_data['genres']
        self.description = db_data['description']
        self.link = db_data['link']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.user = db_data['user']
        self.liked_by = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO playlists (title, genres, description, link, user_id) VALUES (%(title)s,%(genres)s,%(description)s, %(link)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM playlists JOIN users ON playlists.user_id = users.id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_playlists = []
        for row in results:
            user_data = {
                "id" : row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            this_user = User(user_data)
            row["user"] = this_user
            all_playlists.append( cls(row) )
        return all_playlists
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM playlists JOIN users ON playlists.user_id = users.id WHERE playlists.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        row = results[0]
        user_data = {
            "id" : row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "password": row["password"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            }
        row['user'] = User(user_data)
        return cls(row)

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

    @classmethod
    def like_playlist(cls,data):
        query = "INSERT INTO likes (user_id, playlist_id) VALUES (%(user_id)s, %(playlist_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod
    def read_playlist_with_likes(cls,data):
        query = "SELECT * FROM likes LEFT JOIN users ON likes.user_id = users.id LEFT JOIN playlists ON likes.playlist_id = playlists.id WHERE playlists.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        playlist_data = {
            "id" : results[0]["playlists.id"],
            "title" : results[0]["title"],
            "genres" : results[0]["genres"],
            "description" : results[0]["description"],
            "link" : results[0]["link"],
            "created_at": results[0]["playlists.created_at"],
            "updated_at": results[0]["playlists.updated_at"],
            "user_id" : results[0]["user_id"],
            "user" : User.get_by_id({"id": results[0]["playlists.user_id"]}),
        }
        this_playlist = cls(playlist_data)
        for row in results:
            user_data = {
                "id" : row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            this_playlist.liked_by.append(User(user_data))
        return this_playlist

