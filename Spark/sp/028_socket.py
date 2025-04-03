from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
import sys
conf=SparkConf().setMaster('local[2]').setAppName('a')
sc=SparkContext(conf=conf)

ssc=StreamingContext(sc,5)  #响应时间
data=ssc.socketTextStream(sys.argv[1],int(sys.argv[2]))
res=data.flatMap(lambda x:x.split(' ')).map(lambda x: (x,1)).reduceByKey(lambda x,y:x+y)
res.pprint()#流数据要用pprint打印
ssc.start()
ssc.awaitTermination()

sc.stop()
ssc.stop()