from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()

df2=spark.read.csv('file:///home/hadoop/students.txt',header=True,sep=' ')
# df1.createOrReplaceTempView("students")
#用sql查询，属于schema
# df2=spark.sql("select * from students")
df2.show()
#利用rdd的dataframe查询
df2.groupBy("sex").count().show()
df2.select(df2['name']).show()
df2.filter(df2.age>20).show()
df2.groupBy("major").count().show()
df2=df2.sort(df2.age.desc())
df2.show()
spark.stop()