from flask import Flask, request, jsonify
from pymongo import MongoClient
import random
import string
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb+srv://manishjr2507:9HrcegdiUIu80Cbr@captcha.s5rejtk.mongodb.net/')
db = client['captcha_db']
captchas_collection = db['captchas']

@app.route('/generate-captcha', methods=['GET'])
def generate_captcha():
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    image = Image.new('RGB', (100, 40), color='white')
    font = ImageFont.truetype("arial.ttf", 24)
    draw = ImageDraw.Draw(image)
    draw.text((10, 5), text, font=font, fill='black')
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Store captcha in MongoDB
    captcha_data = {'captcha': text, 'image': img_io.getvalue().decode('latin-1')}
    captchas_collection.insert_one(captcha_data)
    
    return jsonify(captcha_data)

@app.route('/validate-captcha', methods=['POST'])
def validate_captcha():
    data = request.json
    stored_captcha = captchas_collection.find_one({'captcha': data['captcha']})
    if stored_captcha and data['input'] == stored_captcha['captcha']:
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failure'})

if __name__ == '__main__':
    app.run(debug=True)
