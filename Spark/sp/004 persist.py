from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
ls=["aa","bb","cc"]
rdd1=sc.parallelize(ls)
rdd1.cache()  #持久化操作。等价于rdd1.persist（MEMORY_ONLY)只存在内存
print(rdd1.count())
print(','.join(rdd1.collect()))
sc.stop()