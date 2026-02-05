from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file:
        df = pd.read_csv(file)

        # Use first column as X and second numeric column as Y
        x_col = df.columns[0]
        y_col = df.select_dtypes(include='number').columns[0]

        plt.figure(figsize=(8,5))
        plt.bar(df[x_col], df[y_col])
        plt.xticks(rotation=45)
        plt.title(f"{y_col} by {x_col}")
        plt.tight_layout()

        plot_path = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')
        plt.savefig(plot_path)
        plt.close()

        return render_template('Index.html', plot_url='plot.png')

    return "No file uploaded"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

