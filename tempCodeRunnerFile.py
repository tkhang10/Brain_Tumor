        # Save the image with tumor box
        new_filename = 'colorize_' + secure_filename(file.filename)
        image_with_tumor_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        cv2.imwrite(image_with_tumor_path, image_with_tumor)

        # Convert the path to HTML URL format
        image_with_tumor_url = url_for('uploaded_file', filename=new_filename)
