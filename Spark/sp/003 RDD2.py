from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
ls=[1,2,3,4,5]
rdd1=sc.parallelize(ls)
print(rdd1.count(),rdd1.collect(),rdd1.first(),rdd1.take(3),rdd1.reduce(lambda x,y:x+y))
rdd1.foreach(print)
sc.stop()