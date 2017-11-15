import pandas as pd
import numpy as np

#businesses
businesses = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/business.csv')

#based on given name and zip code
spec_businesses = businesses[(businesses['postal_code'] == ('85257')) & (businesses['name'] == ('Chipotle Mexican Grill'))]

#first chipotle listed
chipotle = spec_businesses.iloc[0, :]

#business id for said chipotle
chipotle_biz_id = chipotle['business_id']

#reviews
reviews = pd.read_csv('/Users/ojaspatel/Documents/Yelp/dataset/review.csv')

#finds all users who reviewed the chipotle
chipotle_reviews = reviews.loc[reviews['business_id'] == chipotle_biz_id]

#filters out the good reviews
good_reviews = chipotle_reviews.loc[chipotle_reviews['stars'] == 5]

#finds their user ids
users_who_liked = set(good_reviews['user_id'])

# this will select all the reviews associated with any of these users
all_user_reviews = reviews.loc[(reviews['user_id'].isin(users_who_liked)) & (reviews['stars'] == 5)]

#chipotle_categories = chipotle.iloc

#This will select all good reviews from all_user_reviews
#all_good_reviews = all_user_reviews.loc[all_user_reviews['stars'] == 5]

#This will select the business ids of all_good_reviews
all_good_reviews_biz_id = set(all_good_reviews['business_id'])

#take those business id's and find the names of the restaurants
all_good_names1 = businesses.loc[businesses['business_id'].isin(all_good_reviews_biz_id)]
#all_good_names2 = all_good_names1.loc[businesses['categories'].contains('Restaurants')]
all_good_names3 = set(all_good_names1['name'])
print all_good_names3