from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pandas as pd
import numpy as np
from random import shuffle
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

    print (form.errors)
    if request.method == 'POST':
        name=request.form['rest_name']
        zip_code = request.form['zipcode']
        businesses = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/business.csv')
        restaurants = businesses[(businesses['categories'].str.contains('Restaurants'))]
        spec_businesses = restaurants[(restaurants['postal_code'] == zip_code) & (restaurants['name'] == name)]
        chipotle = spec_businesses.iloc[0, :]
        chipotle_biz_id = chipotle['business_id']
        chipotle_lattitude = chipotle['latitude']
        chipotle_longitude = chipotle['longitude']
        reviews = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/review.csv')
        chipotle_reviews = reviews.loc[reviews['business_id'] == chipotle_biz_id]
        closeBy=restaurants[(restaurants['latitude']>=chipotle_lattitude-.5) & (restaurants['latitude']<=chipotle_lattitude+.5) & (restaurants['longitude']>=chipotle_longitude-.5) & (restaurants['longitude']<=chipotle_longitude+.5)]
        good_reviews = chipotle_reviews.loc[(chipotle_reviews['stars'] == 4)]
        closeBy_biz_id = closeBy['business_id']
        users_who_liked = set(good_reviews['user_id'])
        all_good_reviews = reviews.loc[(reviews['user_id'].isin(users_who_liked)) & (reviews['stars'] >= 4)]
        all_good_reviews_biz_id = set(all_good_reviews['business_id'])
        all_good_names1 = restaurants.loc[(restaurants['business_id'].isin(all_good_reviews_biz_id)) & (restaurants['business_id'].isin(closeBy_biz_id))]

        #max 3 ??
        #avegStars-list, sort, print out the 3 largest


        #uses the business ids from the all good names list
        #for x in all_good_names_biz_id:
        #    stars_id=reviews.iloc(reviews['business_id'] == x)
        #    stars=set(float(stars_id['stars']) & stars_id['business_id'])
        #    print(stars)

        #     average=(x_stars.sum(axis=0)/len(x_stars))
        #     if average > max:
        #         max=average;
        #         three_business[x]
        #
        # three_business_loc=businesses.loc[businesses['business_id']]
        # three_business_name=set(three_business_loc['name'])
        # print(three_business)

        sponsors = ["Subway", "McDonald's", "Burger King", "Panda Express", "Taco Bell", "Chik-Fil-A"]
        shuffle(sponsors)

        all_good_addresses = set(all_good_names1['address'])
        address_list = []
        for x in all_good_addresses:
            address_list.append(x)

        all_good_names2 = set(all_good_names1['name'])
        names = []
        for x in all_good_names2:
            names.append(x)

        all_good_zipcodes = set(all_good_names1['postal_code'])
        zipcodes = []
        for x in all_good_zipcodes:
            zipcodes.append(x)

        all_good_cities = set(all_good_names1['city'])
        cities = []
        for x in all_good_cities:
            cities.append(x)

        all_good_states = set(all_good_names1['state'])
        states = []
        for x in all_good_states:
            states.append(x)

        shuffle(names)
        shuffle(address_list)
        shuffle(zipcodes)
        shuffle(cities)
        shuffle(states)

        return render_template('output.html', output=names, sponsors=sponsors, address=address_list, zips=zipcodes, cities=cities, states=states)


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