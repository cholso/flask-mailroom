import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor 

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == "POST": # List previous donors 
        donor_list = [each.name for each in Donor.select()]
    
        if request.form['name'] not in donor_list: # Redirect to /try-again if donor not in list
        
            return redirect(url_for('again'))

        elif request.form['name'] in donor_list:
    
            donor = Donor.select().where(Donor.name == request.form['name']).get()

            value = int(request.form['donation']) 
            Donation(donor=donor.id, value=value).save() # Save donor donation value

            return redirect(url_for('all'))

    elif request.method == "GET":

        return render_template('create.jinja2')

@app.route('/try-again/', methods=['GET', 'POST'])
def again():
    if request.method == "GET":        
        return render_template('try-again.jinja2')
    elif request.method == "POST":
        return redirect(url_for('all'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

