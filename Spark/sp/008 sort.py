from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName("a")
sc=SparkContext(conf=conf)
#use * to load all "file*.txt" file
rdd1=sc.textFile("file:///home/hadoop/rdd/file*.txt")
rdd1.repartition(1) #partition again to 1 part.or use "collect" to collect two files
# rdd1.foreach(print)
#if use sortByKey,you will need a tuple type for it.
rdd2=rdd1.map(lambda x:int(x.split(",")[2])).sortBy(lambda x:x,ascending=False)
rdd2.foreach(print)
print(rdd2.take(5))  #'.take' will return a list type
sc.stop()