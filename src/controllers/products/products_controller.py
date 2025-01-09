import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from src import db
from src.models.products_model import ProductDetail
from flask import send_from_directory


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/media/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/media/videos/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'wmv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/product/add', methods=['POST'])
def add_product():
    images = request.files.getlist('images')
    videos = request.files.getlist('videos')

    if not images and not videos:
        return jsonify({"error": "No media files provided", "status": False}), 400

    image_names = [save_file(image) for image in images if allowed_file(image.filename)]
    video_names = [save_file(video) for video in videos if allowed_file(video.filename)]

    try:
        new_product = ProductDetail(
            product_name=request.form.get('product_name', 'Default Name'),
            description=request.form.get('description', ''),
            category_id=int(request.form.get('category_id', 1)),
            price=float(request.form.get('price', 0)),
            discount_price=float(request.form.get('discount_price', 0)),
            sku=request.form.get('sku', 'Default SKU'),
            stock_quantity=int(request.form.get('stock_quantity', 0)),
            product_images=json.dumps(image_names),
            product_videos=json.dumps(video_names),
            vendor_id=int(request.form.get('vendor_id', 1)),
            status=request.form.get('status', 'Active')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully", "product_id": new_product.product_id, "status": True}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add product", "exception": str(e), "status": False}), 500

def save_file(file):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    original_filename = secure_filename(file.filename)
    filename = f"{timestamp}_{original_filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return filename


@app.route('/product/edit/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    product = ProductDetail.query.get_or_404(product_id)
    try:
        images = request.files.getlist('images')
        videos = request.files.getlist('videos')

        # Handling Images
        if images:
            old_images = json.loads(product.product_images) if product.product_images else []
            for image_name in old_images:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))
                except OSError as e:
                    print(f"Failed to delete {image_name}: {str(e)}")

            image_names = [save_file(image) for image in images if allowed_file(image.filename)]
            product.product_images = json.dumps(image_names)

        # Handling Videos
        if videos:
            old_videos = json.loads(product.product_videos) if product.product_videos else []
            for video_name in old_videos:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], video_name))
                except OSError as e:
                    print(f"Failed to delete {video_name}: {str(e)}")

            video_names = [save_file(video) for video in videos if allowed_file(video.filename)]
            product.product_videos = json.dumps(video_names)

        # Update other fields
        product.product_name = request.form.get('product_name', product.product_name)
        product.description = request.form.get('description', product.description)
        product.category_id = int(request.form.get('category_id', product.category_id))
        product.price = float(request.form.get('price', product.price))
        product.discount_price = float(request.form.get('discount_price', product.discount_price))
        product.sku = request.form.get('sku', product.sku)
        product.stock_quantity = int(request.form.get('stock_quantity', product.stock_quantity))
        product.vendor_id = int(request.form.get('vendor_id', product.vendor_id))
        product.status = request.form.get('status', product.status)

        db.session.commit()
        return jsonify({"message": "Product updated successfully", "status": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update product", "exception": str(e)}), 500
@app.route('/product/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = ProductDetail.query.get_or_404(product_id)
        product.status = "Inactive"
        db.session.commit()
        return jsonify({"message": "Product marked as inactive successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to mark product as inactive", "exception": str(e)}), 500

@app.route('/product/fetch', methods=['GET'])
def fetch_product():
    email = request.args.get('email')  
    if not email:
            return jsonify({"error": "Email is required"}), 400
    products = ProductDetail.query.filter_by(status='Active', user_id=email).all()
    product_list = []
    for product in products:
        product_images = json.loads(product.product_images) if product.product_images else []
        product_videos = json.loads(product.product_videos) if product.product_videos else []
        product_dict = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "description": product.description,
            "category_id": product.category_id,
            "price": product.price,
            "discount_price": product.discount_price,
            "sku": product.sku,
            "stock_quantity": product.stock_quantity,
            "vendor_id": product.vendor_id,
            "status": product.status,
            "product_images": [url_for('serve_image', filename=img, _external=True) for img in product_images],
            "product_videos": [url_for('serve_video', filename=vid, _external=True) for vid in product_videos]
        }
        product_list.append(product_dict)

    return jsonify(product_list)

