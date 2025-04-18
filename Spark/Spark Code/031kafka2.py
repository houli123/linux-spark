from __future__ import print_function
import sys
from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: KafkaWordCount.py <zk> <topic>", file=sys.stderr)
        exit(-1)
    conf=SparkConf().setMaster('local[2]').setAppName('a')
    sc=SparkContext(conf=conf)
    ssc = StreamingContext(sc, 1)
    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils. \
        createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()