from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,Row
conf=SparkConf().setMaster('local').setAppName('a')
sc=SparkContext(conf=conf)

#spark的session对象
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()
#当前是rdd，还没有转换成dataframe
rdd1=sc.textFile("file:///opt/apps/spark/examples/src/main/resources/people.txt").map(lambda x:x.split(','))

#转换成row型，为了转dataframe
rdd2=rdd1.map(lambda x:Row(name=x[0],age=int(x[1])))
# row = Row(name="Alice", age=11)
# print(row)
#rdd转dataframe
df1=spark.createDataFrame(rdd2)
# df1.show()

#sql版本
df1.createOrReplaceTempView("people") #表需要同要查询的一样
df2=spark.sql("select * from people where age>20")
df2.show()

#dataframe转rdd
rdd3=df2.rdd.map(lambda x:x.name+","+str(x.age))
rdd3.foreach(print)

sc.stop()
spark.stop()