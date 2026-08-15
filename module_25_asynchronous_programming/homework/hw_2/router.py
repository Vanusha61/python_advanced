from flask import Flask, Response
import time

from PIL import Image
import io
app = Flask(__name__)

@app.route('/my_test')
def my_test():
    time.sleep(0.2)
    img = Image.new('RGB', (800, 600), color='red')
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return Response(buf.getvalue(), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)