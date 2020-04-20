import json
import numpy as np
#from importlib import reload
import pandas as pd
import sys
#sys.setdefaultencoding()
#reload(sys)
#sys.setdefaultencoding('UTF8')

desired_width=320
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)

# Read JSON file of restaurants
with open('Top60London.json') as json_file:
    allRestaurants = json.load(json_file)

# Create columns for DataFrame
columns = ["name", "locality", "city", "cuisines", "average_cost_for_two", 'aggregate_rating', 'rating_text', 'votes']

# Create empty DataFrame with above columns
restaurantTable = pd.DataFrame(columns=columns)
# This function loops through each restaurant dictionary in allRestaurants, grabs values for
# each restaurant which is then grouped into a Series that is appended to the DataFrame
for restaurantSet in allRestaurants:
    restaurants = restaurantSet['restaurants']
    for restaurant in restaurants:
        singleRow = [restaurant['restaurant']['name'],
               restaurant['restaurant']['location']['locality'],
               restaurant['restaurant']['location']['city'],
               restaurant['restaurant']['cuisines'],
               restaurant['restaurant']['average_cost_for_two'],
               restaurant['restaurant']['user_rating']['aggregate_rating'],
               restaurant['restaurant']['user_rating']['rating_text'],
               restaurant['restaurant']['user_rating']['votes']]
        newRow = pd.Series(singleRow, index=columns)
        restaurantTable = restaurantTable.append(newRow, ignore_index=True)

restaurantTable.index.name = 'id'
restaurantTable.to_csv('final_db_input.csv')

######Statistics for future scope
# Compute the mean for 'average_cost_for_two'
#costs = restaurantTable['average_cost_for_two']
#avgCosts = costs.mean()
#print("Average Cost for Two = £", avgCosts)


# Calculate the median and percentage of values that lie below the value.
#medianCost = costs.median()
#belowMedian = costs < medianCost
#numBelowMedian = belowMedian.sum()
#print("The median cost is = £", medianCost)
#print("The percentage of values below the median is ", numBelowMedian*100/costs.count(), "%")

