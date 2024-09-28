from flask import Flask, request, render_template, redirect, Response
from PIL import Image
from utils import encode_alg, decode_alg
import io, numpy

app = Flask("Steganography Tool", static_url_path='/static', static_folder='static')

# Main variables we work with
enc_message = ""	# encoded message
dec_message = "Here goes the decoded message"	# decoded message
enc_image = None	# encoded image
dec_image = None	# decoded image
enc_last= None		# encoded image
dec_last = None		# decoded image
enc_file = None		# file for encoding
dec_file = None		# file for decoding
dec_matrix = None	# file for last decoded image

@app.route("/")		# front html page
def image():
	return render_template("image.html")

@app.route("/encode", methods = ["GET", "POST"])
def encode():
	global enc_image, enc_message, enc_file
	if request.method == "POST":
		# reference is done by html name attribute
		enc_message = request.form.get("save_encode_message")
		enc_file = request.files.get("image")
		if enc_message and enc_file and len(enc_message) < 100:
			enc_matrix = encode_alg(enc_file, enc_message)		# storing image matrix
			# transform matrix to an image
			enc_image = Image.fromarray(numpy.uint8(enc_matrix))
			# memory space to store the image (binary stream)
			binary_space = io.BytesIO()
			# save the image in that space, png format
			enc_image.save(binary_space, "PNG")
			# move at the start of the file
			binary_space.seek(0)
			# flask response with downloadable image
			dialog = Response(binary_space.read())
			dialog.headers["Content-Type"] = "image/png"
			dialog.headers["Content-Disposition"] = "attachment; filename=enc_image.png"
			return dialog

	return render_template("encode.html")

@app.route("/decode", methods = ["GET", "POST"])
def decode():
	if request.method == "POST":
		global dec_file, dec_message, dec_image, dec_matrix
		dec_file = request.files.get("image")
		if dec_file:
			data = dec_file.read()
			image = Image.open(io.BytesIO(data))
			dec_matrix = numpy.array(image)
			dec_message = decode_alg(dec_matrix)
	return render_template("decode.html", message=dec_message)

@app.route("/last")
def last():
	return render_template("last.html")

@app.route("/encoded", methods = ["GET", "POST"])
def encoded():
	# once encoded button is pressed, automatically download begins
	global enc_image
	if enc_image:
		binary_space = io.BytesIO()
		# save the image in that space, png format
		enc_image.save(binary_space, "PNG")
		# move at the start of the file
		binary_space.seek(0)
		# flask response with downloadable image
		dialog = Response(binary_space.read())
		dialog.headers["Content-Type"] = "image/png"
		dialog.headers["Content-Disposition"] = "attachment; filename=enc_image.png"
		return dialog
	return render_template("encoded.html")

@app.route("/decoded")
def decoded():
	global dec_matrix
	dec_image = Image.fromarray(numpy.uint8(dec_matrix))
	if dec_image:
		binary_space = io.BytesIO()
		dec_image.save(binary_space, "PNG")
		binary_space.seek(0)
		dialog = Response(binary_space.read())
		dialog.headers["Content-Type"] = "image/png"
		dialog.headers["Content-Disposition"] = "attachment; filename=dec_image.png"
		return dialog
	return render_template("decoded.html")
