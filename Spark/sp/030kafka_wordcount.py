import sys
from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
conf=SparkConf().setMaster('local[2]').setAppName('a')
sc=SparkContext(conf=conf)

ssc=StreamingContext(sc,1)
zkQuorum,topic=sys.argv[1:]
kvs=KafkaUtils.\
    createStream(ssc,zkQuorum,"suibian",{topic:1})
data=kvs.map(lambda x:x[1]).flatMap(lambda x:x.split(' '))\
    .map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y)
data.pprint()
ssc.start()
ssc.awaitTermination()

ssc.stop()
sc.stop()