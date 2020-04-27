import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
#app.secret_key=b'w\xf3wh\xf1\xfd\x8a\x87\x9dtZ\xfeb\xbc\x85>\x1a\xc2\x0c\x1bC\xfd\xd9I'
app.secret_key=os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create/', methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		name = request.form['donor']
		amount = int(request.form['value']) 
		try:
			donor = Donor.select().where(Donor.name == name).get()
		except:
			Donor(name=name).save()
			donor = Donor.select().where(Donor.name == name).get()

		Donation(donor=donor, value=amount).save()
		return redirect(url_for('all'))

	else:
		return render_template('create.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

