import os
import socket
import ssl
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from transformers import pipeline

#classifier = pipeline("text-classification", model="finiteautomata/bertweet-base-sentiment-analysis")
classifier = pipeline("text-classification")

producer = KafkaProducer(bootstrap_servers=['redpanda-0:9092','redpanda-1:9092','redpanda-2:9092'])

consumer = KafkaConsumer('dbz.wordpress.wp_comments',
                         group_id='sentiment-analysis',
                         bootstrap_servers=['redpanda-0:9092','redpanda-1:9092','redpanda-2:9092'])

for message in consumer:
    message = json.loads(message.value.decode('utf-8'))
    comment = message['payload']['after']['comment_content']
    sentiment = classifier(comment)
    print(comment)
    print("label: " + sentiment[0]['label'])
    print("score: " + str(sentiment[0]['score']))
    print('\n')
    wp_comment_sentiment = {'comment': comment,
                            'sentiment': sentiment[0]['label'],
                            'score': sentiment[0]['score']
                            }
    producer.send('wp_comment_sentiment', json.dumps(wp_comment_sentiment).encode('utf-8'))


