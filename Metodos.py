
from flask import Flask
from flask import render_template


app= Flask(__name__)

@app.route('/')
def principal():
    return render_template('Index.html')

@app.route('/publicacion')
def publ():
	return render_template('Publicacion.html')

if __name__=='__main__':
    app.run(debug=True, port=5000)
