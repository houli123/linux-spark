from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName('a')
sc=SparkContext(conf=conf)
a=sc.accumulator(0)  #initialize
ls=[1,2,3,4,5]
rdd1=sc.parallelize(ls)
rdd2=rdd1.map(lambda x:a.add(x))  #惰性
rdd2.count()  #需要任意一个转换操作
print(a.value)
sc.stop()