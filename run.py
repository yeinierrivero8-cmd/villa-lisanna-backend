from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/availability', methods=['GET'])
def availability():
    return jsonify({'success': True, 'unavailable_dates': []})

@app.route('/api/quote', methods=['POST'])
def quote():
    return jsonify({
        'success': True,
        'nights': 3,
        'subtotal': 1500,
        'cleaning_fee': 295,
        'taxes': 215.40,
        'damage_deposit': 500,
        'deposit_amount': 1005.27,
        'balance_amount': 1504.13,
        'total_amount': 2010.40
    })

@app.route('/api/bookings', methods=['POST'])
def bookings():
    return jsonify({'success': True, 'checkout_url': 'https://checkout.stripe.com/pay/test'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
