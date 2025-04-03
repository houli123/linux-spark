from pyspark import SparkConf,SparkContext  
conf=SparkConf().setMaster("local").setAppName("a")
sc=SparkContext(conf=conf)

ls=['hello world']
rdd3=sc.parallelize(ls)  #并行化
rdd3.foreach(print)