from flask import jsonify, request, Blueprint
from models.karaoke import db, User, Song
from flask_login import current_user

songs_blueprint=Blueprint('songs', __name__, template_folder='templates')

@songs_blueprint.route('/add', methods=['POST'])
def add():
    print('print request.json: ', request.json)
    user = User.query.filter_by(username=request.json['username']).first()
    new_song = Song(user_id=user.id,
                    song_id=request.json['song_id'],
                    title=request.json['title'],
                    thumbnail=request.json['thumbnail'])

    db.session.add(new_song)
    db.session.commit()

    return jsonify({'message': 'song added to database!'})