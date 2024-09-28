from PIL import Image
import numpy, io

def encode_alg(file, message):
	# reading data from the file
	data = file.read()
	# conversion from binary file to PIL image
	image = Image.open(io.BytesIO(data))
	# using basic image processing theory
	matrix = numpy.array(image)
	# numpy basic matrix info
	# ch = type of channel (grayscale, rgb or rgba); only rgb functions
	# ch is ignored in this version
	# m = no of rows, n = no of columns
	r, c, ch = matrix.shape
	# color access: matrix[i, j, k] where k = 0, 1, 2
	act_r = 0; act_c = 0; length = len(message)
	for i in range(length):
		byte = message[i]
		_ascii_ = ord(byte)
		for j in range(8):
			dr = 7 - j
			mask = ((_ascii_ >> dr) & 1)
			color = matrix[act_r, act_c, j % 3]
			matrix[act_r, act_c, j % 3] = (color & 0xFE) | mask
			if j % 3 == 2 or j == 7:
				act_c += 1
				if act_c >= c:
					act_c = 0
					act_r += 1
		if i + 1 == length:
			for j in range(8):
				color = matrix[act_r, act_c, j % 3]
				# Take mask = 0
				matrix[act_r, act_c, j % 3] = color & 0xFE
				if j % 3 == 2 or j == 7:
					act_c += 1
					if act_c >= c:
						act_c = 0
						act_r += 1

	image = Image.fromarray(matrix)
	return image

def decode_alg(matrix):
	r, c, ch = matrix.shape
	message = ""
	ok = 0		# testing for '\0' terminator
	b = [0, 0, 0, 0, 0, 0, 0, 0]		# array for bits
	act_r = 0; act_c = 0; length = 0
	while True:
		for k in range(8):
			b[k] = matrix[act_r, act_c, k % 3] & 1
			if k % 3 == 2 or k == 7:
				act_c += 1
				if act_c >= c:
					act_c = 0
					act_r += 1
		_ascii_ = 0
		for k in range(8):
			_ascii_ += pow(2, 7 - k) * b[k]
		if _ascii_ == 0:
			message = message + '\0'
			break
		symbol = chr(_ascii_)
		message = message + symbol
		length += 1

	return message
