from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pandas as pd
import numpy as np
from random import shuffle
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
businesses = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/business.csv')
reviews = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/review.csv')

#@app.route("/error", methods=['GET'])
#def error():
#   return render_template('none.html')

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

    @app.route("/", methods=['GET', 'POST'])
    def showForm():
        form = ReusableForm(request.form)

        print (form.errors)
        if request.method == 'POST':
            name=request.form['rest_name']
            zip_code = request.form['zipcode']
            restaurants = businesses[(businesses['categories'].str.contains('Restaurants'))]
            spec_businesses = restaurants[(restaurants['postal_code'] == zip_code) & (restaurants['name'] == name)]

            if spec_businesses.empty:
                return render_template('none.html')

            chipotle = spec_businesses.iloc[0, :]
            chipotle_biz_id = chipotle['business_id']
            chipotle_lattitude = chipotle['latitude']
            chipotle_longitude = chipotle['longitude']
            chipotle_reviews = reviews.loc[reviews['business_id'] == chipotle_biz_id]
            closeBy=restaurants[(restaurants['latitude']>=chipotle_lattitude-.5) & (restaurants['latitude']<=chipotle_lattitude+.5) & (restaurants['longitude']>=chipotle_longitude-.5) & (restaurants['longitude']<=chipotle_longitude+.5)]
            good_reviews = chipotle_reviews.loc[(chipotle_reviews['stars'] == 4)]
            closeBy_biz_id = closeBy['business_id']
            users_who_liked = set(good_reviews['user_id'])
            all_good_reviews = reviews.loc[(reviews['user_id'].isin(users_who_liked)) & (reviews['stars'] >= 4)]
            all_good_reviews_biz_id = set(all_good_reviews['business_id']) 
            all_good_names1 = restaurants.loc[(restaurants['business_id'].isin(all_good_reviews_biz_id)) & (restaurants['business_id'].isin(closeBy_biz_id))]

            sponsors = ["Subway", "McDonald's", "Burger King", "Panda Express", "Taco Bell", "Chik-Fil-A"]
            shuffle(sponsors)


            names1 = all_good_names1['name']
            address_list1 = all_good_names1['address']
            zipcodes1 = all_good_names1['postal_code']
            cities1 = all_good_names1['city']
            states1 = all_good_names1['state']

            names = []
            for x in names1:
                names.append(x)

            address_list = []
            for x in address_list1:
                address_list.append(x)

            zipcodes = []
            for x in zipcodes1:
                zipcodes.append(x)

            cities = []
            for x in cities1:
                cities.append(x)

            states = []
            for x in states:
                states.append(x)

            

            return render_template('output.html', output=names, sponsors=sponsors, addresses=address_list, zips=zipcodes, cities=cities, states=states)

        if form.validate():
            #renders a template that returns the output
            #Save the comment here.
            flash('Hello')
        else:
            flash('All the form fields are required. ')

            return render_template('FormFilter.html', form=form)
#return redirect(url_for)

if __name__ == "__main__":
    app.run()