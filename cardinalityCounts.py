import requests, json
import datetime
import time
import schedule
import os
import nr_metrics_publisher
import logging
import warnings

apiKey = os.getenv('NEW_RELIC_API_KEY')
headers = { 'Content-Type': 'application/json', 'API-Key': apiKey }
url = 'https://api.newrelic.com/graphql'
accountId = os.getenv('ACCOUNT_ID')
nr_env = os.getenv('NR_ENV')

accountId = str(accountId)
input = "From Metric SELECT  cardinality(metricName) FACET metricName LIMIT MAX SINCE today WITH TIMEZONE 'UTC'"

nrql_query = '''query
{
  actor {
    account(id: '''+accountId+''') {
      nrql(query: "'''+input+'''") {
        nrql
        otherResult
        rawResponse
        totalResult
      }
    }
  }
}
'''
current_time = str(datetime.datetime.now())
logging.basicConfig(level=logging.INFO)
tags = '''{"env": "'''+nr_env+'''", "component": "newrelic", "target_metric_name":'''

def cardinality():
    r = requests.post(url, json={'query': nrql_query}, headers=headers)
    res = r.json()
    
    print("URL:",url)
    print("NRQL_QUERY:",nrql_query)
    print("HEADERS:",headers)
    print("RES:",res)
    if(res['data']['actor']['account']['nrql'] == None):
      logging.info("Error: NRQL result is null "+current_time+"")
      time.sleep(60)
    else:
      logging.info("Publishing newrelic.cardinality.count metric Started at "+current_time+"")
      facetData = res['data']['actor']['account']['nrql']['rawResponse']['facets']
      jsonString = json.dumps(facetData)
      jsonFile = open("data.json", "w")
      jsonFile.write(jsonString)
      jsonFile.close()
      count = 0
      print("cardinality data", facetData)
      for row in facetData:
          print("inside for loop cardinality")
          name = row['name']
          cardinality = row['results'][0]['cardinality']
          print(count)

  #        print(cardinality)
          cardAttributes = tags+'''"'''+name+'''"'''+'}' 
          warnings.filterwarnings("ignore")
          count = count + 1

          nr_metrics_publisher.publishCountMetrics("newrelic.cardinality.count", cardinality, cardAttributes)
      logging.info("Publishing newrelic.cardinality.count metric Completed at "+current_time+"")

# cardinality()
