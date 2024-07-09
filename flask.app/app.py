from flask import Flask, render_template, request, send_file
#install pillow package first 
# import pillow package-this package is a forl of the PIL and is used for opening manipulating and saving many differnet image file formats
from PIL import Image
import io
import pyjokes


app = Flask(__name__)

#add index route which will render an HTML template(index.html) that provides
#the instructions and a form for the user to upload an image and selct the output format.
@app.route('/')
def index():
    return render_template('index.html')
 

# add a convert route here which will handle  the post request from the form and use package pillow to
# #convert the image and return the converted image.
@app.route('/convert', methods=['POST'])
# the post method here is to handle 1. image upload 2. image conversion
def convert():
    if 'image' not in request.files:
        return "No file part"
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    
    output_format = request.form['output_format']
    
    #we use pillow here to open the iploaded image
    image = Image.open(file)
    #define variable
    original_format = image.format
    # converet and save the image to a byteslo object

    img_io = io.BytesIO() 
    #this byteslo object used as an in memory binary stream to save the converted image
    image.save(img_io, output_format)
    # use pollow to save the image in the specified format(e.g., 'JPEG', 'PNG', etc.) into the img_io object.
    img_io.seek(0)
     # moves the file pointer to the beginning of the img_io stream, so it can be read from the start when sent to the client.
    
    message = f"Image successfully converted from {original_format} to {output_format}."
    return send_file(img_io, mimetype=f'image/{output_format.lower()}')
    #send the img_io object as a file to the client, setting the appropriate MIME type for the image format.

# Translate route
# Joke route
@app.route('/joke', methods=['GET'])
def get_joke():
    category = request.args.get('category', 'all')
    if category not in ['neutral', 'chuck', 'all']:
        return "Invalid category. Please use 'neutral', 'chuck', or 'all'."
    
    joke = pyjokes.get_joke(category=category)
    return f"Here's a joke for you: {joke}"
   

if __name__ == "__main__":
    app.run(debug=True)
