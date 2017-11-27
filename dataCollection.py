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

    print (form.errors)
    if request.method == 'POST':
        name=request.form['rest_name']
        zip_code = request.form['zipcode']
        businesses = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/business.csv')
        #restaurants = businesses['categories'][0] == 'Food'
        #print restaurants
        spec_businesses = businesses[(businesses['postal_code'] == zip_code) & (businesses['name'] == name)]
        chipotle = spec_businesses.iloc[0, :]
        chipotle_biz_id = chipotle['business_id']
        chipotle_lattitude = chipotle['latitude']
        chipotle_longitude = chipotle['longitude']
        reviews = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/review.csv')
        chipotle_reviews = reviews.loc[reviews['business_id'] == chipotle_biz_id]
        closeBy=businesses[(businesses['latitude']>=chipotle_lattitude-.5) & (businesses['latitude']<=chipotle_lattitude+.5) & (businesses['longitude']>=chipotle_longitude-.5) & (businesses['longitude']<=chipotle_longitude+.5)]
        good_reviews = chipotle_reviews.loc[(chipotle_reviews['stars'] == 5)]
        closeBy_biz_id = closeBy['business_id']
        users_who_liked = set(good_reviews['user_id'])
        all_good_reviews = reviews.loc[(reviews['user_id'].isin(users_who_liked)) & (reviews['stars'] >= 5)]
        all_good_reviews_biz_id = set(all_good_reviews['business_id'])
        all_good_names1 = businesses.loc[(businesses['business_id'].isin(all_good_reviews_biz_id)) & (businesses['business_id'].isin(closeBy_biz_id))]
        all_good_names2 = set(all_good_names1['name'])
        return render_template('output.html', output=all_good_names2)


        #compiles a list of all the business ID
        all_good_names_biz_id=set(all_good_names1['business_id'])
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