from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os 
from werkzeug.security import generate_password_hash, check_password_hash
import threading

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("cred_disco-nirvana.json", scope)
client = gspread.authorize(creds)

sheet = client.open("ACC_Market_Inventory").sheet1
lock = threading.Lock()

# In-memory storage for barcode, amount, and remain
barcode_number = ""
amount_value = ""
# remain_value = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iphone')
def numpad_iphone():
    return render_template('numpad-ios.html')

@app.route('/android')
def numpad_android():
    return render_template('numpad-android.html')

@app.route('/update_values', methods=['POST'])
def update_values():
    try:
        
        data = request.get_json()
        # Get values from the frontend
        barcode_number = data.get('barcode_number', 'NO barcode number')
        # print(f"remaining hash map from the update_values : {remaining_map}")
        amount_value = data.get('amount', 'NONONONONONONON amount')
        # print(f' HEE amount_value : {amount_value} ')
        
        res = None
        with lock:
            try:
                cell = sheet.find(barcode_number)
                if cell is not None:
                    row_index = cell.row
                    product_value = sheet.cell(row_index, 4).value
                    
                    if product_value:
                        res = int(product_value) + int(amount_value)
                    else:
                        res = int(amount_value)
                    sheet.update_cell(row_index, 4, res)
                else:
                    print(f"CREATE A NEW ONE FOR THIS")
                    print(f"{barcode_number} :  {amount_value}")
                    sheet.append_row([str(barcode_number),int(amount_value)])
            except Exception as e:
                print(f"Error: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500

        return jsonify({
            'barcode': barcode_number,
            'amount_second': res,
            'status': 'success'
            })
    
    except ValueError as ve:
        return jsonify({'status': 'error', 'message': str(ve)}), 400  # Return 400 Bad Request for validation errors

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}),500

@app.route('/get_values/<barcode>', methods=['GET'])
def get_values(barcode):
    
    # print(f"this is the barcode: {barcode}")
    try:
        cell = sheet.find(barcode)
        if cell is not None:
            row_index = cell.row
            item_n = sheet.cell(row_index, 2).value
            amount_value = sheet.cell(row_index, 4).value
            pdt_name = sheet.cell(row_index, 3).value
            # print(f"=>>>>>>>>>>>>>>>>>>>>pdt_name>>>{pdt_name}")
            return jsonify({
                'barcode_number': barcode,
                'item_number' : item_n,
                'remain_first': amount_value,
                'product_name': pdt_name
            })
        else:
            # print(f"this is {barcode} and it is a newbie")
            return jsonify({
            'barcode_number': barcode,
            'item_number' : 'we need a item number for this barcode',
            'remain_first': 'newbie',  # Return 'newbie' when barcode is not found
            'product_name': 'we need a name for this barcode'
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

if __name__ == '__main__':
    # os.system('gunicorn -w 4 -b 0.0.0.0:8080 --log-level debug app:app')
    app.run(debug=True)
