ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def check_file(file):
    if file and '.' in file.filename:
        extension = file.filename.split('.')[-1]
        if extension in ALLOWED_EXTENSIONS:
            return extension
    return None
