#!/usr/bin/python3
"""
place_reviews module

This module contains the views for handling Review objects in the API.
It defines routes for retrieving, creating, updating,
and deleting Review objects.
"""

from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    review_list = [
        review.to_dict()
        for review in storage.all(Review).values()
        if review.place_id == place_id]
    if review_list == []:
        abort(404)
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object using review_id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object if review_id exist
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create Review object"""
    obj_data = request.get_json()
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in obj_data:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in obj_data:
        return jsonify({"error": "Missing text"})

    user_obj = storage.get(User, obj_data['user_id'])
    if user_obj is None:
        abort(404)

    obj_data['place_id'] = place_id
    review = Review(**obj_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update Review object"""
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    obj_data = request.get_json()
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400

    review_obj.text = obj_data['text']
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
