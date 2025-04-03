from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,HiveContext  #老版本，.config("hive.metastore.uris"这段可以去掉
spark=SparkSession.builder.config(conf=SparkConf()).config("hive.metastore.uris","thrift://127.0.0.1:9083").enableHiveSupport().getOrCreate()
hc=HiveContext(spark)
#第一种方法
# hc.sql("use spark")
# df1=hc.sql("select * from student")
# df1.show()
#第二种方法
df2=spark.sql("select * from spark.student")
df2.show()