from  flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import Blog

blog_bp=Blueprint(
    "blogs",
    __name__,
    url_prefix="/api/blogs"
)

@blog_bp.route("",methods=["POST"])
@jwt_required()
def create_blog():
    data=request.get_json()

    if not data:
        return jsonify({
            "error": "request body is required"
        }), 400

    title=data.get("title")
    content=data.get("content")

    if not title or not content:
        return jsonify({
            "error":"title and content are required"
        }), 400

    user_id = get_jwt_identity()

    blog = Blog(
        title=title,
        content=content,
        author_id=int(user_id),
        status="draft"
    )

    db.session.add(blog)
    db.session.commit()

    return jsonify({
        "message": "Blog created successfully",
        "blog": {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "author_id": blog.author_id,
            "status": blog.status,
            "created_at": blog.created_at.isoformat()
                if blog.created_at else None,
            "updated_at": blog.updated_at.isoformat()
                if blog.updated_at else None,
            "published_at": blog.published_at
                if blog.published_at else None
        }
    }), 201

@blog_bp.route("/<int:blog_id>",methods=["GET"])
@jwt_required(optional=True)
def get_blog(blog_id):
    blog= db.session.get(Blog,blog_id)

    if not blog:
        return jsonify({
            "error":"Blog not found"
        }),404

    if blog.status == "draft":
        user_id = get_jwt_identity()

        if user_id is None:
            return jsonify({
                "error": "Authentication required"
            }),401

        if int(user_id) != blog.author_id:
            return jsonify({
                "error": "You are not allowed to view this draft"
            }), 403

    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "author_id": blog.author_id,
        "status": blog.status,
        "created_at": blog.created_at.isoformat()
            if blog.created_at else None,
        "updated_at": blog.updated_at.isoformat()
            if blog.updated_at else None,
        "published_at": blog.published_at.isoformat()
            if blog.published_at else None
    }), 200    




@blog_bp.route("", methods=["GET"])
def get_all_blogs():
    blogs = Blog.query.filter_by(
        status="published"
    ).order_by(
        Blog.published_at.desc()
    ).all()

    return jsonify({
        "blogs": [
            {
                "id": blog.id,
                "title": blog.title,
                "content": blog.content,
                "author_id": blog.author_id,
                "status": blog.status,
                "created_at": blog.created_at.isoformat()
                    if blog.created_at else None,
                "updated_at": blog.updated_at.isoformat()
                    if blog.updated_at else None,
                "published_at": blog.published_at.isoformat()
                    if blog.published_at else None
            }
            for blog in blogs
        ]
    }), 200



@blog_bp.route("/<int:blog_id>",methods=["PUT"])
@jwt_required()
def update_blog(blog_id):
    blog=db.session.get(Blog,blog_id)

    if not blog:
        return jsonify({
            "error": "Blog not found"
        }), 404

    user_id = get_jwt_identity()

    if int(user_id) != blog.author_id:
        return jsonify({
            "error": "You are not allowed to edit this blog"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({
            "error": "Title and content are required"
        }), 400

    blog.title = title
    blog.content = content

    db.session.commit()

    return jsonify({
        "message": "Blog updated successfully",
        "blog": {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "author_id": blog.author_id,
            "status": blog.status,
            "created_at": blog.created_at.isoformat()
                if blog.created_at else None,
            "updated_at": blog.updated_at.isoformat()
                if blog.updated_at else None,
            "published_at": blog.published_at.isoformat()
                if blog.published_at else None
        }
    }), 200

