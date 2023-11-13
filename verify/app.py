from flask import Flask, render_template, request, redirect, session, send_from_directory,url_for
import os
from collections import defaultdict
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'temp123'

# Define the UPLOAD_FOLDER
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return redirect(url_for('upload'))

@app.route('/uploads', methods=['GET', 'POST'])
def upload():
    try:
        if request.method == 'POST':
            if 'monica_file' not in request.files or 'market_file' not in request.files:
                return redirect(request.url)

            monica_file = request.files['monica_file']
            market_file = request.files['market_file']

            if monica_file.filename == '' or market_file.filename == '':
                return redirect(request.url)

            if monica_file and market_file:

                monica_filename = secure_filename(monica_file.filename)
                market_filename = secure_filename(market_file.filename)
                # Use os.path.join with app.config['UPLOAD_FOLDER']
                monica_file_path = os.path.join(app.config['UPLOAD_FOLDER'], monica_filename)
                market_file_path = os.path.join(app.config['UPLOAD_FOLDER'], market_filename)

                monica_file.save(monica_file_path)
                market_file.save(market_file_path)

                ans_dict, account_set = create_lookup_dict(monica_file_path)
                mkt_set, diff = verify_mkt_res(market_file_path, ans_dict)

                res_data = []
                for i in account_set - mkt_set:
                    res_data.append([i, ans_dict[i][1], ans_dict[i][0]])

                result_df2 = pd.DataFrame(res_data, columns=['Item Number', 'Name', '應盤 Amount'])
                result_df1 = pd.DataFrame(diff, columns=['Item Number', 'Name', 'Amt by Account', 'Amt by Market', 'Barcode'])

                res = "res.xlsx"
                with pd.ExcelWriter(res, engine='openpyxl') as writer:
                    result_df1.to_excel(writer, sheet_name='difference', index=False)
                    result_df2.to_excel(writer, sheet_name='應盤但未盤到', index=False)

                result_path = os.path.abspath(res)
                result_filename = os.path.basename(res)

                session["res_file_name"] = result_path

                return render_template('res.html', result_path=result_path, result_filename=result_filename)
        return render_template('index.html')
    except Exception as e:
        # Handle the exception and render the error.html template
        return render_template('error.html', error_message=str(e))

def create_lookup_dict(file_path):
    lookup = defaultdict(list)
    account_set = set()
    df = pd.read_excel(file_path, header=None)
    for index, row in df.iterrows():
        if index == 0:
            continue

        itemN = str(row[0]).strip()
        pdt_chi_name = str(row[1]).strip()
        amount = str(row[4]).strip()
        try:
            lookup[itemN].extend([int(amount), pdt_chi_name])
            account_set.add(itemN)
        except ValueError:
            continue

        lookup[itemN].extend([int(amount), pdt_chi_name])

    return lookup, account_set

def verify_mkt_res(fp, ld):
    df = pd.read_excel(fp, header=None)
    mkt_set = set()
    diff = []
    for index, row in df.iterrows():
        if index == 0:
            continue
        item_n = str(row.iloc[1]).strip()
        bar_c = str(row.iloc[0]).strip()
        mkt_set.add(item_n)
        amt = str(row.iloc[3]).strip()
        if amt == "nan":
            continue
        if item_n in ld:
            if ld[item_n][0] != int(amt):
                diff.append([item_n, ld[item_n][1], ld[item_n][0], amt, bar_c])

        else:
            continue
    return mkt_set, diff




@app.route('/result')
def result():
    return render_template('result.html')

@app.route("/download_result")
def download_result():
    try:
        res_file_path = session.get("res_file_name")  # Get the BS result file path from the session
        print(res_file_path)
        if res_file_path:
            res_filename = os.path.basename(res_file_path)
            return send_from_directory(os.path.dirname(res_file_path), res_filename, as_attachment=True)
        else:
            return "Result file not available."
    except Exception as e:
        # Handle the exception and render the error.html template
        return render_template('error.html', error_message=str(e))

# Custom error handler for all other errors
@app.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html', error_message=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
