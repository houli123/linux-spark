from pyspark import SparkConf,SparkContext
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
ls=[("hadoop",2),("spark",1),("hive",1),("spark",1)]
rdd1=sc.parallelize(ls)
rdd1.foreach(print)
# print(rdd1.keys())  #return "PythonRDD[2] at RDD at PythonRDD.scala:53"
# rdd1.keys().foreach(print)  #generate a new rdd with rdd's keys()
# rdd1.values().foreach(print)
# rdd1.sortByKey().foreach(print)  #sort by first and second
# rdd2=rdd1.sortBy(lambda x:x[0],ascending=False)  # sort by x[?]
# rdd2.foreach(print)
rdd3=rdd1.mapValues(lambda x:x+10)
rdd3.foreach(print)
sc.stop()