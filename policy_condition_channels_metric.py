import requests, json
import datetime
import schedule
import time
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
pol_con_query = """query
{
  actor {
    account(id: """+accountId+""") {
      alerts {
        policiesSearch {
          totalCount
        }
        nrqlConditionsSearch {
          totalCount
        }
      }
    }
  }
}
"""
tags = '''{"env": "'''+nr_env+'''", "component": "newrelic"}'''

current_time = str(datetime.datetime.now())
logging.basicConfig(level=logging.INFO)

def policy_cond_count():
    r = requests.post(url, json={'query': pol_con_query}, headers=headers)
    res = r.json()
    policyCount = res['data']['actor']['account']['alerts']['policiesSearch']['totalCount']
    nrqlConditionsCount = res['data']['actor']['account']['alerts']['nrqlConditionsSearch']['totalCount']
    warnings.filterwarnings("ignore")
    logging.info("Publishing newrelic.policies.count metric Started at "+current_time+"")
    nr_metrics_publisher.publishCountMetrics("newrelic.policies.count", policyCount, tags)
    logging.info("Publishing newrelic.policies.count metric completed at "+current_time+"")
    logging.info("Publishing newrelic.nrql.conditions.count metric Started at "+current_time+"")
    nr_metrics_publisher.publishCountMetrics("newrelic.nrql.conditions.count", nrqlConditionsCount, tags)
    logging.info("Publishing newrelic.nrql.conditions.count metric completed at "+current_time+"")

def notificationChannelsCount():
    nextCursorCheck = True
    cursor = ""
    channelCountMap = {}
    while nextCursorCheck:
        pol_con_query = '''query
        {
        actor {
            account(id: '''+accountId+''') {
            alerts {
                notificationChannels(cursor: "'''+cursor+'''") {
                channels {
                    id
                    name
                    type
                }
                totalCount
                nextCursor
                }
            }
            }
        }
        }
        '''
        r = requests.post(url, json={'query': pol_con_query}, headers=headers)
        print(pol_con_query)
        res = r.json()
        channels = res['data']['actor']['account']['alerts']['notificationChannels']['channels']
        cursor = res['data']['actor']['account']['alerts']['notificationChannels']['nextCursor']
        
        for row in channels:
            channelId = row['id']
            channelName = row['name']
            channelType = row['type']
            
            if channelType in channelCountMap:
              channelCountMap[channelType] = channelCountMap[channelType]+1
            else:
              channelCountMap[channelType]=1
            
        if cursor is None:
            nextCursorCheck = False

    global tags
    tags = tags[:-1]+''', "channel_type":'''
    logging.info("Publishing newrelic.notification.channels.count metric Started at "+current_time+"")
    for key in channelCountMap:
        cardAttributes = tags+'''"'''+key+'''"'''+'}'
        warnings.filterwarnings("ignore")
        nr_metrics_publisher.publishCountMetrics("newrelic.notification.channels.count", channelCountMap[key], cardAttributes)
    logging.info("Publishing newrelic.notification.channels.count metric Completed at "+current_time+"")

def job_schedule():
    policy_cond_count()
    notificationChannelsCount()
