Copyright 2022 Toma-Ioan Dumitrescu


Stegano is a tool for encoding messages in images and decoding photos (where the message exists). It was created using Python for backend and html, css for frontend (Bootstrap 5 design links).

Requirements: python 3, html, css, IDE, Flask, numpy, PIL, io, Bootstrap 5

Run the webpage: flask run in terminal

Backend:

API: Redirections from navbar menu are done using url_for; response objects are created for returning the
encoded image (or the last encoded image) (the image is returned by encode_alg and then transformed in binary png file), the user will GET the encoded image anyway after submitting necessary data; the same idea works for decoding, with the mention that the output will be a web page alert with the string returned by the function decode_alg;
Showing last encoded/decoded images is done by using global variables (we expect a single user; more details
on the web page description); Image manipulation: PIL library

Encoding algorithm: Each message byte has 8 {0, 1} bits (b1, b2, ..., b8) and we take all pixels from
the image (starting from top left corner and continuing row by row) and we do: (color(i) & 0xFE) | b(i),
i having values from 1 to 8. Evidently, colors can be red, green or blue (in function of the order). I choose
to have the last bit untouched and to encode each byte of the message with 3 pixels (first 8/9 colors).

Decoding algorithm: We perform the inverse method (color ^ 1) to find the msg byte, since that is the only
one used in encoding process. We construct the ascii number by examining 3 pixels at an iteration (using base
2 to base 10 converting algorithm), then we transform it in a character that will concatenate with the
original message initially assigned with "".

Frontend:

Web pages are created using simple Bootstrap navbar, buttons, input designs with adapted GUI depending on
the device type. All web pages are derived from _base.html (they have the same code, additionaly what is in the
jinja block of the particular web page). Sending data: multiform (with one click all data saved).

Containerization:

For easily deploying the app, the Dockerfile install all dependencies. Commands:
docker build -t stegano
docker run -p 5000:5000 -it stegano

Bibliography and notes:

Encoded/Decoded images should be in the format filename.png and the output will be also filename.png with the
desired changes.
Python documentation
Boostrap documentation
