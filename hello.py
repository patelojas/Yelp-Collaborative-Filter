from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pandas as pd
import numpy as np

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def showForm():
    form = ReusableForm(request.form)
 
    print form.errors
    if request.method == 'POST':
    	name=request.form['rest_name']
    	zip_code = request.form['zipcode']
    	businesses = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/business.csv')
    	spec_businesses = businesses[(businesses['postal_code'] == zip_code) & (businesses['name'] == name)]
    	chipotle = spec_businesses.iloc[0, :]
    	chipotle_biz_id = chipotle['business_id']
        chipotle_lattitude = chipotle['latitude']
        chipotle_longitude = chipotle['longitude']
    	reviews = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/review.csv')
    	chipotle_reviews = reviews.loc[reviews['business_id'] == chipotle_biz_id]


        closeBy=businesses[(businesses['latitude']>=chipotle_lattitude-1) & (businesses['latitude']<=chipotle_lattitude+1) & (businesses['longitude']>=chipotle_longitude-1) & (businesses['longitude']<=chipotle_longitude+1)]
    	good_reviews = chipotle_reviews.loc[(chipotle_reviews['stars'] == 5)]
    	closeBy_biz_id = closeBy['business_id']
        users_who_liked = set(good_reviews['user_id'])
    	#all_good_reviews = reviews.loc[(reviews['user_id'].isin(users_who_liked)) & (reviews['stars'] == 5) ]
        all_good_reviews = reviews.loc[(reviews['user_id'].isin(users_who_liked)) & (reviews['stars'] == 5)]
    	all_good_reviews_biz_id = set(all_good_reviews['business_id'])
    	all_good_names1 = businesses.loc[(businesses['business_id'].isin(all_good_reviews_biz_id)) & (businesses['business_id'].isin(closeBy_biz_id))]
    	all_good_names3 = set(all_good_names1['name'])
    	print all_good_names3
    	#handlebars
        if form.validate():
        	#renders a template that returns the output
            # Save the comment here.

            flash('Hello')
        else:
            flash('All the form fields are required. ')
 
    return render_template('FormFilter.html', form=form)
 
if __name__ == "__main__":
    app.run()
