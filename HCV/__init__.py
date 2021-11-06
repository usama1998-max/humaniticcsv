from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '1b09b9659df387d6baaba73e0719c61f'


from HCV.views.csv_file_reader import csv_reader

app.register_blueprint(csv_reader)
