from pyspark import SparkConf,SparkContext  
conf=SparkConf().setMaster("local").setAppName("aaaa")
sc=SparkContext(conf=conf)
rdd=sc.textFile("file:///home/hadoop/chapter4-data1.txt")\
.map(lambda x:x.split(","))
# rdd.foreach(print)
# （1）该系总共有多少名学生。
rdd1 = rdd.map(lambda x: x[0]) 
distinct_rdd1 = rdd1.distinct()  #去重操作
print(distinct_rdd1.count())  #取元素总个数
# （2）该系共开设多少门课程。
rdd2 = rdd.map(lambda x: x[1]) 
distinct_rdd2 = rdd2.distinct()  
print(distinct_rdd2.count())
# （3）Tom 同学的总成绩平均分是多少。
rdd3 = rdd.filter(lambda x:x[0]=='Tom')
rdd3.foreach(print) 
score = rdd3.map(lambda x:int(x[2])) 
num = rdd3.count() #选课门数
#有reduce和reduceByKey，reduce用于只有数据需要求和的列，reduceByKey是用于至少两列的第二数据列的求和
sum_score = score.reduce(lambda x,y:x+y) #总成绩
avg = sum_score/num
print(avg)
# （4）每名同学的选修的课程门数。
#按键值对分组统计，映射后分组统计
rdd4 = rdd.map(lambda x:(x[0],1)) 
each_rdd4 = rdd4.reduceByKey(lambda x,y: x+y) 
each_rdd4.foreach(print)
# （5）该系 DataBase 课程共有多少人选修。
rdd5 = rdd.filter(lambda x:x[1]=='DataBase')
num = rdd5.count() 
print(num)
# （6）各门课程的平均分是多少。
rdd6 = rdd.map(lambda x:(x[1],(int(x[2]),1))) 
t = rdd6.reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1])) 
avg = t.map(lambda x:(x[0], round(x[1][0]/x[1][1],2)))
avg.foreach(print)
# （7）使用累加器计算共有多少人选修 DataBase 这门课。
rdd7 = rdd.filter(lambda x:x[1]=="DataBase")
accum = sc.accumulator(0) 
rdd7.foreach(lambda x:accum.add(1))
print(accum.value)