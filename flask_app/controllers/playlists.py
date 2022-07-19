from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.playlist import Playlist
from flask_app.models.user import User


@app.route('/new/playlist')
def new_playlist():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_playlist.html',user=User.get_by_id(data))


@app.route('/create/playlist',methods=['POST'])
def create_playlist():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Playlist.validate_playlist(request.form):
        return redirect('/new/playlist')
    data = {
        "title": request.form["title"],
        "genres": request.form["genres"],
        "description": request.form["description"],
        "link": request.form["link"],
        "user_id": session["user_id"]
    }
    Playlist.save(data)
    return redirect('/dashboard')

@app.route('/edit/playlist/<int:id>')
def edit_playlist(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_playlist.html",edit=Playlist.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/playlist',methods=['POST'])
def update_playlist():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Playlist.validate_playlist(request.form):
        return redirect('/new/playlist')
    data = {
        "title": request.form["title"],
        "genres": request.form["genres"],
        "description": request.form["description"],
        "link": request.form["link"],
        "id": request.form['id']
    }
    Playlist.update(data)
    return redirect('/dashboard')

@app.route('/playlist/<int:id>')
def show_playlist(id):
    this_playlist = Playlist.read_playlist_with_likes({"id": id})
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_playlist.html",playlist=this_playlist,user=User.get_by_id(user_data))

@app.route('/destroy/playlist/<int:id>')
def destroy_playlist(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Playlist.destroy(data)
    return redirect('/dashboard')

@app.route('/like/playlist/<int:id>')
def like_playlist(id):
    data = {
        "playlist_id": id,
        "user_id": session['user_id'],
    }
    Playlist.like_playlist(data)
    return redirect('/dashboard')