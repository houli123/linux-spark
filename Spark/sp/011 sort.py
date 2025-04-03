from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName('a')
sc=SparkContext(conf=conf)
rdd1=sc.textFile("file:///home/hadoop/file*.txt").repartition(1).map(lambda x:int(x))
rdd2=rdd1.sortBy(lambda x:x)
rdd2.foreach(print)
index=0
def getindex():
    global index
    index+=1
    return index
rdd3=rdd2.map(lambda x:(getindex(),x))
rdd3.foreach(print)
sc.stop()