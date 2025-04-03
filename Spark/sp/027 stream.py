from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
conf=SparkConf().setMaster('local[2]').setAppName('a')  #涉及到流至少2个线程
sc=SparkContext(conf=conf)

ssc=StreamingContext(sc,5)  #响应时间
data=ssc.textFileStream('file:///home/hadoop/streaming')\
    .flatMap(lambda x:x.split(" "))\
    .map(lambda x: (x,1))
result=data.reduceByKey(lambda x,y:x+y)
result.pprint()  #流数据要用pprint打印
ssc.start()
ssc.awaitTermination()

sc.stop()
ssc.stop()