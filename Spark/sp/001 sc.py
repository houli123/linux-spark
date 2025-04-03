from pyspark import SparkConf,SparkContext  #若没有开启pyspark必用该段
conf=SparkConf().setMaster("local").setAppName("aaaa")
sc=SparkContext(conf=conf)

# rdd1=sc.textFile("file:///home/hadoop/word.txt") #用本地的方式
# rdd1.foreach(print)
# rdd2=sc.textFile("hdfs://192.168.134.19:9000/test/word.txt") #用hdfs的方式
# rdd2.foreach(print)

ls=[22190494,"lsh",20,550]
rdd3=sc.parallelize(ls)  #并行化
rdd3.foreach(print)