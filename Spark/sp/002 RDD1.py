from pyspark import SparkConf,SparkContext
conf=SparkConf().setMaster("local").setAppName("b")
sc=SparkContext(conf=conf)
rdd1=sc.textFile("file:///home/hadoop/data1.txt")
#filter
rdd2=rdd1.filter(lambda x:"j" in x)
rdd2.foreach(print)
#map，映射单个结果
rdd3=rdd1.map(lambda x:x.split(' '))
rdd3.foreach(print)
#flatMap,映射多个结果 
rdd4=rdd1.flatMap(lambda x:x.split(' '))
rdd4.foreach(print)
#map高级
rdd5=rdd4.map(lambda x:(x,1))
rdd5.foreach(print)
#groupByKey,返回的不可输出的结果，可能需要配合聚合函数
rdd6=rdd5.groupByKey()
rdd6.foreach(print)
#reduceByKey
rdd7=rdd5.reduceByKey(lambda x,y:x+y)
rdd7.foreach(print)
sc.stop()