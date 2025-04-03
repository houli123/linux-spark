from pyspark import SparkConf,SparkContext
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
ls=[("hadoop",6),("spark",2),("hadoop",4),("spark",6)]
rdd1=sc.parallelize(ls).map(lambda x:(x[0],(x[1],1)))
rdd1.foreach(print)

#reduceByKey=only transform rdd's key
rdd2=rdd1.reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1]))  
rdd2.foreach(print)

rdd3=rdd2.map(lambda x:(x[0],x[1][0]/x[1][1]))
rdd3.foreach(print)
sc.stop()