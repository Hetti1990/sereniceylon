from flask import Blueprint, request, jsonify
from backend.models import db, Photo
import os

photos_bp = Blueprint('photos_bp', __name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@photos_bp.route('/photos', methods=['GET'])
def get_photos():
    photos = Photo.query.all()
    return jsonify([{'id': photo.id, 'image_url': photo.image_url, 'description': photo.description, 'category': photo.category} for photo in photos])

@photos_bp.route('/photos', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        new_photo = Photo(
            image_url=filename,
            description=request.form.get('description'),
            category=request.form.get('category')
        )
        db.session.add(new_photo)
        db.session.commit()
        return jsonify({'id': new_photo.id, 'image_url': new_photo.image_url, 'description': new_photo.description, 'category': new_photo.category}), 201

@photos_bp.route('/photos/<int:id>', methods=['DELETE'])
def delete_photo(id):
    photo = Photo.query.get(id)
    if photo:
        os.remove(photo.image_url)
        db.session.delete(photo)
        db.session.commit()
        return jsonify({'message': 'Photo deleted'}), 200
    return jsonify({'error': 'Photo not found'}), 404
