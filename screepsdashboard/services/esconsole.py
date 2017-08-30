from datetime import datetime
from elasticsearch import Elasticsearch
import json
import time

def get_records(start_at = 'now-1m', max_records=100, order='asc'):
    es = Elasticsearch()
    results = es.search(index="screeps-console*", doc_type='log', body={
      "size": max_records,
      "query": {
        "bool" : {
            "filter" : {
                "range" : {
                    "timestamp" : {
                      "gt": start_at
                    }
                }
            }
        }
      },
      "sort": [
        {
          "timestamp": {
            "order": order
          }
        }
      ]
    })['hits']
    messages = []
    for hit in results['hits']:
      record = hit['_source']
      if isinstance(start_at, datetime):
          row_time = datetime.strptime(record['timestamp'],"%Y-%m-%dT%H:%M:%S.%f")
          if row_time < start_at:
              continue
          start_at = row_time
      else:
          start_at = datetime.strptime(record['timestamp'],"%Y-%m-%dT%H:%M:%S.%f")

      messages.append(record)
    return messages
