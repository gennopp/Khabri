#!/usr/bin/python3
from flask import Flask, render_template, url_for, request, jsonify
import requests
import datetime
import json
import httplib2
from decimal import Decimal

app = Flask(__name__)

def first():
	#redirect default page to average
	pass

def toDate(dateString): 
    return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()

# check if the date is calender valid
def checkValidDate(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect Date, please enter valid date")

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


# khabri
@app.route("/average/api", methods = ['GET', 'POST'])
def average():
	data = request.get_json()
	date1 = data['date1']
	date2 = data['date2']
	country = data['country']
	print(date1, date2, country)
	if checkValidDate(date1) and checkValidDate(date2):
		allBases = []
		sumOfRates = 0
		finalResults = {}
		for base in country:
			allCurr = requests.get("https://api.exchangeratesapi.io/history?start_at={}&end_at={}&symbols={}".format(date1, date2, base))
			allBases.append(allCurr.json())
			val = allCurr.json();
			rates = extract_values(val, base)
			days = 0
			for rate in rates:
				days += 1
				sumOfRates += rate

			averageForBase = sumOfRates/days
			print(sumOfRates)
			finalResults[base] = averageForBase
		#return jsonify(allBases)
		return jsonify(finalResults)



if __name__ == "__main__":
    app.run(debug=True)
    