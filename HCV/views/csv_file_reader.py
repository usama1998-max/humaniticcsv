from flask import render_template, redirect, request, flash, Blueprint
import os
import json
import pandas as pd
import math

csv_reader = Blueprint("csv_reader", __name__)


# ------ For checking file extension ------
def check_ext(file_exe):
    split_txt = file_exe.split('.')
    if 'csv' not in split_txt:
        return False


@csv_reader.route('/', methods=['GET', 'POST'])
def csv_file_reader():
    categories_values = {}
    net = []
    current_file = "No file chosen"
    sum_net = 0

    # ---------------- File upload method ------------------------
    if request.method == 'POST':
        file = request.files['file_name']
        # checking filename
        if file.filename == "":
            flash("danger", "Please choose a file!")
            return redirect('/')

        # checking file extension
        check = check_ext(file.filename)
        if check is False:
            flash("danger", "Only CSV or .csv files are allowed!")
            return redirect('/')

        # ------ Saving file to csv_files directory ------
        file.save(file.filename)
        current_file = file.filename

        # ---------------- NET Calculation & Category detection ------------------------
        csv_file = pd.read_csv(os.path.join(file.filename))
        hevent_col = csv_file['hevent']
        categories = list(set(hevent_col))

        # ------ A loop for storing categories in a dictionary ------
        for i in range(len(categories)):
            categories_values[categories[i]] = 0

        # ------ A nested loop for matching and counting categories ------
        for k, v in categories_values.items():
            for i in range(len(hevent_col)):
                if hevent_col[i] == k:
                    categories_values[hevent_col[i]] = categories_values[hevent_col[i]] + 1

        # ------ A json file with categories and values ------
        with open("HCV/categories.json", "r+") as cat_jsn:
            jsn = json.loads(cat_jsn.read())

        # ------ A nested loop for matching and calculating net ------
        for k1, v1 in jsn['category'].items():
            for k2, v2 in categories_values.items():
                if k1 == k2:
                    result = v1 * v2
                    net.append(result)

        # ------ Total net ------
        sum_net = math.floor(sum(net))

        # ------ Removes file after calculations ------
        os.remove(file.filename)

    return render_template('csv_viewer.html',
                            total_net=sum_net,
                            categories_values=categories_values,
                            current_file=current_file)
