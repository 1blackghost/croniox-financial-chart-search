'''
Main script of the website.

'''
#imports
from flask import *


app=Flask(__name__)

with app.app_context():
	#importing different views for the website.
	from views import *


#The '/' entrypoint
@app.route("/")
def root():
	return render_template("index.html")


if __name__=="__main__":
	app.run(debug=True)
