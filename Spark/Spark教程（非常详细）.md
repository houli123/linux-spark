 [toc]

引言
===============================================================================================================================================================================================================================================================================================================

> **声明**：本文为大数据肌肉猿公众号的[《5W字总结Spark》](https://mp.weixin.qq.com/s/caCk3mM5iXy0FaXCLkDwYQ)的学习笔记，如有侵权请联系本人删除！

`Spark`[知识图谱](https://so.csdn.net/so/search?q=%E7%9F%A5%E8%AF%86%E5%9B%BE%E8%B0%B1&spm=1001.2101.3001.7020)如下：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/36b45cdd87c895c954e74e32f881794b.png)

Spark 基础
=========================================================================================================================================================================================================================================================================================================================

## Spark 为何物

**Spark 是当今大数据领域最活跃、最热门、最高效的大数据通用计算平台之一**。

> Hadoop 之父 Doug Cutting 指出：Use of MapReduce engine for Big Data projects will decline, replaced by Apache Spark (大数据项目的 MapReduce 引擎的使用将下降，由 Apache Spark 取代)。

## Spark VS Hadoop

尽管 `Spark` 相对于 `Hadoop` 而言具有较大优势，但 `Spark` 并不能完全替代 `Hadoop`，`Spark` 主要用于替代`Hadoop`中的 `MapReduce` 计算模型。存储依然可以使用 `HDFS`，但是中间结果可以存放在内存中；调度可以使用 `Spark` 内置的，也可以使用更成熟的调度系统 `YARN` 等。

|  | _Hadoop_ | _Spark_ |
| :-: | :-- | :-- |
| **类型** | 分布式基础平台, 包含计算, 存储, 调度 | 分布式计算工具 |
| **场景** | 大规模数据集上的批处理 | 迭代计算, 交互式计算, 流计算 |
| **价格** | 对机器要求低, 便宜 | 对内存有要求, 相对较贵 |
| **编程范式** | Map+Reduce, API 较为底层, 算法适应性差 | RDD 组成 DAG 有向无环图, API 较为顶层, 方便使用 |
| **数据存储结构** | MapReduce 中间计算结果存在 HDFS 磁盘上, 延迟大 | RDD 中间运算结果存在内存中 , 延迟小 |
| **运行方式** | Task 以进程方式维护, 任务启动慢 | Task 以线程方式维护, 任务启动快 |

实际上，`Spark` 已经很好地融入了 `Hadoop` 生态圈，并成为其中的重要一员，它可以借助于 `YARN` 实现资源调度管理，借助于 `HDFS` 实现分布式存储。

此外，`Hadoop` 可以使用廉价的、异构的机器来做分布式存储与计算，但是，`Spark` 对硬件的要求稍高一些，对内存与 `CPU` 有一定的要求。

## Spark 优势及特点

### 优秀的数据模型和丰富计算抽象

首先看看`MapReduce`，它提供了对数据访问和计算的抽象，但是对于数据的复用就是简单的将中间数据写到一个稳定的**文件系统**中(例如 `HDFS`)，所以会产生数据的复制备份，磁盘的`I/O`以及数据的序列化，所以在遇到需要在多个计算之间复用中间结果的操作时效率就会非常的低。而这类操作是非常常见的，例如迭代式计算，交互式数据挖掘，图计算等。

因此 `AMPLab` 提出了一个新的模型，叫做 **RDD**。

*   **RDD** 是一个可以容错且并行的数据结构（其实可以理解成分布式的集合，操作起来和操作本地集合一样简单)，它可以让用户显式的将中间结果数据集保存在 **内存** 中，并且通过控制数据集的分区来达到数据存放处理最优化。同时 `RDD` 也提供了丰富的 `API (map、reduce、filter、foreach、redeceByKey...)`来操作数据集。

**后来 `RDD` 被 `AMPLab` 在一个叫做 `Spark` 的框架中提供并开源。**

### 完善的生态圈-fullstack

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c23011086a0390f139a0636bd14f7529.png)

`Spark`有完善的生态圈，如下：

*   **Spark Core**：实现了 Spark 的基本功能，包含 RDD、任务调度、内存管理、错误恢复、与存储系统交互等模块。
*   **Spark SQL**：Spark 用来操作结构化数据的程序包。通过 Spark SQL，我们可以使用 SQL 操作数据。
*   **Spark Streaming**：Spark 提供的对实时数据进行流式计算的组件。提供了用来操作数据流的 API。
*   **Spark MLlib**：提供常见的机器学习(ML)功能的程序库。包括分类、回归、聚类、协同过滤等，还提供了模型评估、数据导入等额外的支持功能。
*   **GraphX(图计算)**：Spark 中用于图计算的 API，性能良好，拥有丰富的功能和运算符，能在海量数据上自如地运行复杂的图算法。
*   **集群管理器**：Spark 设计为可以高效地在一个计算节点到数千个计算节点之间伸缩计算。
*   **Structured Streaming**：处理结构化流,统一了离线和实时的 API。

### spark的特点

*   **快**：与 Hadoop 的 MapReduce 相比，Spark 基于内存的运算要快 100 倍以上，基于硬盘的运算也要快 10 倍以上。Spark 实现了[高效的](https://so.csdn.net/so/search?q=%E9%AB%98%E6%95%88%E7%9A%84&spm=1001.2101.3001.7020) DAG 执行引擎，可以通过基于内存来高效处理数据流。
    
*   **易用**：Spark 支持 Java、Python、R 和 Scala 的 API，还支持超过 80 种高级算法，使用户可以快速构建不同的应用。而且 Spark 支持交互式的 Python 和 Scala 的 shell，可以非常方便地在这些 shell 中使用 Spark 集群来验证解决问题的方法。
    
*   **通用**：Spark 提供了统一的解决方案。Spark 可以用于批处理、交互式查询([Spark SQL](https://so.csdn.net/so/search?q=Spark%20SQL&spm=1001.2101.3001.7020))、实时流处理(Spark Streaming)、机器学习(Spark MLlib)和图计算(GraphX)，这些不同类型的处理都可以在同一个应用中无缝使用。
    
*   **兼容性**：Spark 可以非常方便地与其他的开源产品进行融合。比如，Spark 可以使用 Hadoop 的 YARN 和 Apache Mesos 作为它的资源管理和调度器，并且可以处理所有 Hadoop 支持的数据，包括 HDFS、HBase 和 Cassandra 等。这对于已经部署 Hadoop 集群的用户特别重要，因为不需要做任何数据迁移就可以使用 Spark 的强大处理能力。
    

## Spark 运行模式

**① local 本地模式(单机)**

*   学习测试使用
*   分为 local 单线程和 local-cluster 多线程。

**② standalone 独立集群模式**

*   学习测试使用
*   典型的 Mater/slave 模式。

**③ standalone-HA 高可用模式**

*   生产环境使用
*   基于 standalone 模式，使用 zk 搭建高可用，避免 Master 是有单点故障的。

**④ on yarn 集群模式**

*   生产环境使用
*   运行在 yarn 集群之上，由 yarn 负责资源管理，Spark 负责任务调度和计算。
*   好处：计算资源按需伸缩，集群利用率高，共享底层存储，避免数据跨集群迁移。

**⑤ on mesos 集群模式**

*   国内使用较少
*   运行在 mesos 资源管理器框架之上，由 mesos 负责资源管理，Spark 负责任务调度和计算。

**⑥ on cloud 集群模式**

*   中小公司未来会更多的使用云服务
*   比如 AWS 的 EC2，使用这个模式能很方便的访问 Amazon 的 S3。

Spark Core
===========================================================================================================================================================================================================================================================================================================================

## RDD详解

### RDD概念

前面有提到`MapReduce` 框架采用非循环式的数据流模型，把中间结果写入到 `HDFS` 中，带来了大量的数据复制、磁盘 `IO` 和序列化开销。且这些框架只能支持一些特定的计算模式(`map/reduce`)，并没有提供一种通用的数据抽象。因此出现了RDD这个概念。

**RDD(Resilient Distributed Dataset)叫做弹性分布式数据集，是 Spark 中最基本的数据抽象，代表一个不可变、可分区、里面的元素可并行计算的集合**。

`RDD`单词拆解：

*   **Resilient** ：它是弹性的，RDD 里面的中的数据可以保存在内存中或者磁盘里面；
*   **Distributed** ： 它里面的元素是分布式存储的，可以用于分布式计算；
*   **Dataset**: 它是一个集合，可以存放很多元素。

### RDD属性

`RDD` 的源码描述如下：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/07ee5ecc62a9d9b0c29bab1d9d772ecf.png)

其含义如下：

*   **A list of partitions** ：一组分片(Partition)/一个分区(Partition)列表，即数据集的基本组成单位。对于 RDD 来说，每个分片都会被一个计算任务处理，分片数决定并行度。用户可以在创建 RDD 时指定 RDD 的分片个数，如果没有指定，那么就会采用默认值。
*   **A function for computing each split** ：一个函数会被作用在每一个分区。Spark 中 RDD 的计算是以分片为单位的，compute 函数会被作用到每个分区上。
*   **A list of dependencies on other RDDs** ：一个 RDD 会依赖于其他多个 RDD。RDD 的每次转换都会生成一个新的 RDD，所以 RDD 之间就会形成类似于流水线一样的前后依赖关系。在部分分区数据丢失时，Spark 可以通过这个依赖关系重新计算丢失的分区数据，而不是对 RDD 的所有分区进行重新计算。(Spark 的容错机制)
*   **Optionally, a Partitioner for key-value RDDs (e.g. to say that the RDD is hash-partitioned)**：可选项，对于 KV 类型的 RDD 会有一个 Partitioner，即 RDD 的分区函数，默认为 HashPartitioner。
*   **Optionally, a list of preferred locations to compute each split on (e.g. block locations for an HDFS file)**：可选项,一个列表，存储存取每个 Partition 的优先位置(preferred location)。对于一个 HDFS 文件来说，这个列表保存的就是每个 Partition 所在的块的位置。按照"移动数据不如移动计算"的理念，Spark 在进行任务调度的时候，会尽可能选择那些存有数据的 worker 节点来进行任务计算。

* * *

总结：**RDD 是一个数据集的表示，不仅表示了数据集，还表示了这个数据集从哪来，如何计算**，主要属性包括：

*   分区列表
*   计算函数
*   依赖关系
*   分区函数(默认是 `hash`)
*   最佳位置

分区列表、分区函数、最佳位置，这三个属性其实说的就是数据集在哪，在哪计算更合适，如何分区；

计算函数、依赖关系，这两个属性其实说的是数据集怎么来的。

### RDD API

#### RDD 的创建方式

**① 由外部存储系统的数据集创建，包括本地的文件系统，还有所有 `Hadoop` 支持的数据集，比如 `HDFS、Cassandra、HBase` 等：**

```
val rdd1 = sc.textFile("hdfs://node1:8020/wordcount/input/words.txt")

```

**② 通过已有的 RDD 经过算子转换生成新的 RDD：**

```
val rdd2=rdd1.flatMap(_.split(" "))

```

**③ 由一个已经存在的 Scala 集合创建：**

```
val rdd3 = sc.parallelize(Array(1,2,3,4,5,6,7,8))
或者
val rdd4 = sc.makeRDD(List(1,2,3,4,5,6,7,8))

```

`makeRDD` 方法底层调用了 `parallelize` 方法：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/59164c376b48c46d6f051fe1db6f44bb.png)

#### RDD 算子

RDD 的算子分为两类:

*   **Transformation转换操作**:返回一个新的 RDD
*   **Action动作操作**:返回值不是 RDD(无返回值或返回其他的)

> 注意:
> 
> 1.  RDD **不实际存储真正要计算的数据**，而是记录了数据的位置在哪里，数据的转换关系(调用了什么方法，传入什么函数)。
> 2.  RDD 中的**所有转换都是惰性求值/延迟执行**的，也就是说并不会直接计算。只有当发生一个要求返回结果给 `Driver` 的 `Action`动作时，这些转换才会真正运行。
> 3.  之所以使用惰性求值/延迟执行，是因为这样可以在 Action 时对 RDD 操作形成 DAG有向无环图进行 Stage 的划分和并行优化，这种设计让 Spark 更加有效率地运行。

* * *

**Transformation转换算子**：

| 转换算子 | 含义 |
| :-- | :-- |
| **map**(func) | 返回一个新的 RDD，该 RDD 由每一个输入元素经过 func 函数转换后组成 |
| **filter**(func) | 返回一个新的 RDD，该 RDD 由经过 func 函数计算后返回值为 true 的输入元素组成 |
| **flatMap**(func) | 类似于 map，但是每一个输入元素可以被映射为 0 或多个输出元素(所以 func 应该返回一个序列，而不是单一元素) |
| **mapPartitions**(func) | 类似于 map，但独立地在 RDD 的每一个分片上运行，因此在类型为 T 的 RDD 上运行时，func 的函数类型必须是 Iterator\[T\] => Iterator\[U\] |
| **mapPartitionsWithIndex**(func) | 类似于 mapPartitions，但 func 带有一个整数参数表示分片的索引值，因此在类型为 T 的 RDD 上运行时，func 的函数类型必须是(Int, Interator\[T\]) => Iterator\[U\] |
| sample(withReplacement, fraction, seed) | 根据 fraction 指定的比例对数据进行采样，可以选择是否使用随机数进行替换，seed 用于指定随机数生成器种子 |
| **union**(otherDataset) | 对源 RDD 和参数 RDD 求并集后返回一个新的 RDD |
| intersection(otherDataset) | 对源 RDD 和参数 RDD 求交集后返回一个新的 RDD |
| **distinct**(\[numTasks\])) | 对源 RDD 进行去重后返回一个新的 RDD |
| **groupByKey**(\[numTasks\]) | 在一个(K,V)的 RDD 上调用，返回一个(K, Iterator\[V\])的 RDD |
| **reduceByKey**(func, \[numTasks\]) | 在一个(K,V)的 RDD 上调用，返回一个(K,V)的 RDD，使用指定的 reduce 函数，将相同 key 的值聚合到一起，与 groupByKey 类似，reduce 任务的个数可以通过第二个可选的参数来设置 |
| aggregateByKey(zeroValue)(seqOp, combOp, \[numTasks\]) | 对 PairRDD 中相同的 Key 值进行聚合操作，在聚合过程中同样使用了一个中立的初始值。和 aggregate 函数类似，aggregateByKey 返回值的类型不需要和 RDD 中 value 的类型一致 |
| **sortByKey**(\[ascending\], \[numTasks\]) | 在一个(K,V)的 RDD 上调用，K 必须实现 Ordered 接口，返回一个按照 key 进行排序的(K,V)的 RDD |
| sortBy(func,\[ascending\], \[numTasks\]) | 与 sortByKey 类似，但是更灵活 |
| **join**(otherDataset, \[numTasks\]) | 在类型为(K,V)和(K,W)的 RDD 上调用，返回一个相同 key 对应的所有元素对在一起的(K,(V,W))的 RDD |
| cogroup(otherDataset, \[numTasks\]) | 在类型为(K,V)和(K,W)的 RDD 上调用，返回一个(K,(Iterable,Iterable))类型的 RDD |
| cartesian(otherDataset) | 笛卡尔积 |
| pipe(command, \[envVars\]) | 对 rdd 进行管道操作 |
| **coalesce**(numPartitions) | 减少 RDD 的分区数到指定值。在过滤大量数据之后，可以执行此操作 |
| **repartition**(numPartitions) | 重新给 RDD 分区 |

* * *

**Action 动作算子**：

| 动作算子 | 含义 |
| :-- | :-- |
| reduce(func) | 通过 func 函数聚集 RDD 中的所有元素，这个功能必须是可交换且可并联的 |
| collect() | 在驱动程序中，以数组的形式返回数据集的所有元素 |
| count() | 返回 RDD 的元素个数 |
| first() | 返回 RDD 的第一个元素(类似于 take(1)) |
| take(n) | 返回一个由数据集的前 n 个元素组成的数组 |
| takeSample(withReplacement,num, \[seed\]) | 返回一个数组，该数组由从数据集中随机采样的 num 个元素组成，可以选择是否用随机数替换不足的部分，seed 用于指定随机数生成器种子 |
| takeOrdered(n, \[ordering\]) | 返回自然顺序或者自定义顺序的前 n 个元素 |
| **saveAsTextFile**(path) | 将数据集的元素以 textfile 的形式保存到 HDFS 文件系统或者其他支持的文件系统，对于每个元素，Spark 将会调用 toString 方法，将它装换为文件中的文本 |
| **saveAsSequenceFile**(path) | 将数据集中的元素以 Hadoop sequencefile 的格式保存到指定的目录下，可以使 HDFS 或者其他 Hadoop 支持的文件系统 |
| saveAsObjectFile(path) | 将数据集的元素，以 Java 序列化的方式保存到指定的目录下 |
| **countByKey**() | 针对(K,V)类型的 RDD，返回一个(K,Int)的 map，表示每一个 key 对应的元素个数 |
| foreach(func) | 在数据集的每一个元素上，运行函数 func 进行更新 |
| **foreachPartition**(func) | 在数据集的每一个分区上，运行函数 func |

* * *

**统计操作**：

| 算子 | 含义 |
| :-- | :-- |
| count | 个数 |
| mean | 均值 |
| sum | 求和 |
| max | 最大值 |
| min | 最小值 |
| variance | 方差 |
| sampleVariance | 从采样中计算方差 |
| stdev | 标准差:衡量数据的离散程度 |
| sampleStdev | 采样的标准差 |
| stats | 查看统计结果 |

### RDD 持久化/缓存

某些 `RDD` 的计算或转换可能会比较耗费时间，如果这些 `RDD` 后续还会频繁的被使用到，那么可以将这些 `RDD` 进行持久化/缓存：

```
val rdd1 = sc.textFile("hdfs://node01:8020/words.txt")
val rdd2 = rdd1.flatMap(x=>x.split(" ")).map((_,1)).reduceByKey(_+_)
rdd2.cache //缓存/持久化
rdd2.sortBy(_._2,false).collect//触发action,会去读取HDFS的文件,rdd2会真正执行持久化
rdd2.sortBy(_._2,false).collect//触发action,会去读缓存中的数据,执行速度会比之前快,因为rdd2已经持久化到内存中了

```

#### persist 方法和 cache 方法

`RDD` 通过 `persist` 或 `cache` 方法可以将前面的计算结果缓存，但是并不是这两个方法被调用时立即缓存，而是触发后面的 `action` 时，该 `RDD` 将会被缓存在计算节点的内存中，并供后面重用。

通过查看 `RDD` 的源码发现 `cache` 最终也是调用了 `persist` 无参方法(默认存储只存在内存中)：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ad92e16f1c22b196eb469db4f820f7b3.png)

#### 存储级别

默认的存储级别都是仅在内存存储一份，`Spark` 的存储级别还有好多种，存储级别在 `object StorageLevel` 中定义的。

| 持久化级别 | 说明 |
| :-- | :-- |
| **MORY\_ONLY(默认)** | 将 RDD 以非序列化的 Java 对象存储在 JVM 中。如果没有足够的内存存储 RDD，则某些分区将不会被缓存，每次需要时都会重新计算。这是默认级别 |
| **MORY\_AND\_DISK(开发中可以使用这个)** | 将 RDD 以非序列化的 Java 对象存储在 JVM 中。如果数据在内存中放不下，则溢写到磁盘上．需要时则会从磁盘上读取 |
| MEMORY\_ONLY\_SER (Java and Scala) | 将 RDD 以序列化的 Java 对象(每个分区一个字节数组)的方式存储．这通常比非序列化对象(deserialized objects)更具空间效率，特别是在使用快速序列化的情况下，但是这种方式读取数据会消耗更多的 CPU |
| MEMORY\_AND\_DISK\_SER (Java and Scala) | 与 MEMORY\_ONLY\_SER 类似，但如果数据在内存中放不下，则溢写到磁盘上，而不是每次需要重新计算它们 |
| DISK\_ONLY | 将 RDD 分区存储在磁盘上 |
| MEMORY\_ONLY\_2, MEMORY\_AND\_DISK\_2 等 | 与上面的储存级别相同，只不过将持久化数据存为两份，备份每个分区存储在两个集群节点上 |
| OFF\_HEAP(实验中) | 与 MEMORY\_ONLY\_SER 类似，但将数据存储在堆外内存中。(即不是直接存储在 JVM 内存中) |

* * *

**总结：**

*   RDD 持久化/缓存的目的是为了提高后续操作的速度
*   缓存的级别有很多，默认只存在内存中,开发中使用 memory\_and\_disk
*   只有执行 action 操作的时候才会真正将 RDD 数据进行持久化/缓存
*   实际开发中如果某一个 RDD 后续会被频繁的使用，可以将该 RDD 进行持久化/缓存

### RDD 容错机制Checkpoint

**持久化的局限**：

*   持久化/缓存可以把数据放在内存中，虽然是快速的，但是也是最不可靠的；也可以把数据放在磁盘上，也不是完全可靠的！例如磁盘会损坏等。

**问题解决**：

*   `Checkpoint` 的产生就是为了更加可靠的数据持久化，在`Checkpoint`的时候一般把数据放在在 `HDFS` 上，这就天然的借助了 `HDFS` 天生的高容错、高可靠来实现数据最大程度上的安全，实现了 `RDD` 的容错和高可用。

**用法如下**：

```
SparkContext.setCheckpointDir("目录") //HDFS的目录

RDD.checkpoint

```

* * *

**总结：**

*   开发中如何保证数据的安全性性及读取效率：可以对频繁使用且重要的数据，先做缓存/持久化，再做 checkpint 操作。

**持久化和 Checkpoint 的区别：**

*   位置：Persist 和 Cache 只能保存在本地的磁盘和内存中(或者堆外内存–实验中) Checkpoint 可以保存数据到 HDFS 这类可靠的存储上。
*   生命周期：Cache 和 Persist 的 RDD 会在程序结束后会被清除或者手动调用 unpersist 方法 Checkpoint 的 RDD 在程序结束后依然存在，不会被删除。

### RDD 的依赖关系

`RDD`有两种依赖，分别为**宽依赖(`wide dependency/shuffle dependency`)**和**窄依赖(`narrow dependency`)** :

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d9471dc551cd24e60c2ccdaf3e3635c2.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0c1128b35f0a38043c0d91ca4b155b03.png)  
从上图可以看到：

*   **窄依赖**：父 RDD 的一个分区只会被子 RDD 的一个分区依赖；
*   **宽依赖**：父 RDD 的一个分区会被子 RDD 的多个分区依赖(涉及到 shuffle)。

* * *

**对于窄依赖：**

*   窄依赖的多个分区可以并行计算；
*   窄依赖的一个分区的数据如果丢失只需要重新计算对应的分区的数据就可以了。

* * *

**对于宽依赖：**

*   划分 Stage(阶段)的依据:对于宽依赖,必须等到上一阶段计算完成才能计算下一阶段。

### DAG 的生成和划分 Stage

#### DAG

**DAG(`Directed Acyclic Graph` 有向无环图)**：指的是数据转换执行的过程，有方向，无闭环(其实就是 RDD 执行的流程)；

> 原始的 RDD 通过一系列的转换操作就形成了 DAG 有向无环图，任务执行时，可以按照 DAG 的描述，执行真正的计算(数据被操作的一个过程)。

**DAG 的边界**:

*   **开始**：通过 SparkContext 创建的 RDD；
*   **结束**：触发 Action，一旦触发 Action 就形成了一个完整的 DAG。

#### DAG 划分Stage

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/07b5183c7be8bfe4b895c923b6a1d038.png)  
从上图可以看出：

*   一个 Spark 程序可以有多个 DAG(有几个 Action，就有几个 DAG，上图最后只有一个 Action（图中未表现）,那么就是一个 DAG);
*   一个 DAG 可以有多个 Stage(根据宽依赖/shuffle 进行划分)；
*   同一个 Stage 可以有多个 Task 并行执行(task 数=分区数，如上图，Stage1 中有三个分区 P1、P2、P3，对应的也有三个 Task)；
*   可以看到这个 DAG 中只 reduceByKey 操作是一个宽依赖，Spark 内核会以此为边界将其前后划分成不同的 Stage；
*   在图中 Stage1 中，从 textFile 到 flatMap 到 map 都是窄依赖，这几步操作可以形成一个流水线操作，通过 flatMap 操作生成的 partition 可以不用等待整个 RDD 计算结束，而是继续进行 map 操作，这样大大提高了计算的效率。

* * *

为什么要划分 Stage? --并行计算

*   一个复杂的业务逻辑如果有 shuffle，那么就意味着前面阶段产生结果后，才能执行下一个阶段，即下一个阶段的计算要依赖上一个阶段的数据。那么我们按照 shuffle 进行划分(也就是按照宽依赖就行划分)，就可以将一个 DAG 划分成多个 Stage/阶段，在同一个 Stage 中，会有多个算子操作，可以形成一个 pipeline 流水线，流水线内的多个平行的分区可以并行执行。

* * *

如何划分 DAG 的 stage？

*   对于窄依赖，partition 的转换处理在 stage 中完成计算，不划分(将窄依赖尽量放在在同一个 stage 中，可以实现流水线计算)。
*   对于宽依赖，由于有 shuffle 的存在，只能在父 RDD 处理完成后，才能开始接下来的计算，也就是说需要要划分 stage。

* * *

**总结：**

*   Spark 会根据 shuffle/宽依赖使用回溯算法来对 DAG 进行 Stage 划分，从后往前，遇到宽依赖就断开，遇到窄依赖就把当前的 RDD 加入到当前的 stage/阶段中。

具体的划分算法请参见 AMP 实验室发表的论文：[《Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing》](http://xueshu.baidu.com/usercenter/paper/show?paperid=b33564e60f0a7e7a1889a9da10963461&site=xueshu_se)

### RDD累加器和广播变量

> 在默认情况下，当 Spark 在集群的多个不同节点的多个任务上并行运行一个函数时，它会把函数中涉及到的每个变量，在每个任务上都生成一个副本。但是，有时候需要在多个任务之间共享变量，或者在任务(Task)和任务控制节点(Driver Program)之间共享变量。

为了满足这种需求，Spark 提供了两种类型的变量：

*   **累加器 （accumulators）**：累加器支持在所有不同节点之间进行累加计算(比如计数或者求和)。
*   **广播变量 （broadcast variables）**：广播变量用来把变量在所有节点的内存之间进行共享，在每个机器上缓存一个只读的变量，而不是为机器上的每个任务都生成一个副本。

#### 累加器

通常在向 `Spark` 传递函数时，比如使用 `map()` 函数或者用`filter()`传条件时，可以使用驱动器程序中定义的变量，但是集群中运行的每个任务都会得到这些变量的一份新的副本，更新这些副本的值也不会影响驱动器中的对应变量。这时使用累加器就可以实现我们想要的效果:

语法：`val xx: Accumulator[Int] = sc.accumulator(0)`

示例代码：

```
import org.apache.spark.rdd.RDD
import org.apache.spark.{Accumulator, SparkConf, SparkContext}

object AccumulatorTest {
  def main(args: Array[String]): Unit = {
    val conf: SparkConf = new SparkConf().setAppName("wc").setMaster("local[*]")
    val sc: SparkContext = new SparkContext(conf)
    sc.setLogLevel("WARN")

    //使用scala集合完成累加
    var counter1: Int = 0;
    var data = Seq(1,2,3)
    data.foreach(x => counter1 += x )
    println(counter1)//6

    println("+++++++++++++++++++++++++")

    //使用RDD进行累加
    var counter2: Int = 0;
    val dataRDD: RDD[Int] = sc.parallelize(data) //分布式集合的[1,2,3]
    dataRDD.foreach(x => counter2 += x)
    println(counter2)//0
    //注意：上面的RDD操作运行结果是0
    //因为foreach中的函数是传递给Worker中的Executor执行,用到了counter2变量
    //而counter2变量在Driver端定义的,在传递给Executor的时候,各个Executor都有了一份counter2
    //最后各个Executor将各自个x加到自己的counter2上面了,和Driver端的counter2没有关系

    //那这个问题得解决啊!不能因为使用了Spark连累加都做不了了啊!
    //如果解决?---使用累加器
    val counter3: Accumulator[Int] = sc.accumulator(0)
    dataRDD.foreach(x => counter3 += x)
    println(counter3)//6
  }
}

```

#### 广播变量

关键词：`sc.broadcast()`

```
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

object BroadcastVariablesTest {
  def main(args: Array[String]): Unit = {
    val conf: SparkConf = new SparkConf().setAppName("wc").setMaster("local[*]")
    val sc: SparkContext = new SparkContext(conf)
    sc.setLogLevel("WARN")

    //不使用广播变量
    val kvFruit: RDD[(Int, String)] = sc.parallelize(List((1,"apple"),(2,"orange"),(3,"banana"),(4,"grape")))
    val fruitMap: collection.Map[Int, String] =kvFruit.collectAsMap
    //scala.collection.Map[Int,String] = Map(2 -> orange, 4 -> grape, 1 -> apple, 3 -> banana)
    val fruitIds: RDD[Int] = sc.parallelize(List(2,4,1,3))
    //根据水果编号取水果名称
    val fruitNames: RDD[String] = fruitIds.map(x=>fruitMap(x))
    fruitNames.foreach(println)
    //注意:以上代码看似一点问题没有,但是考虑到数据量如果较大,且Task数较多,
    //那么会导致,被各个Task共用到的fruitMap会被多次传输
    //应该要减少fruitMap的传输,一台机器上一个,被该台机器中的Task共用即可
    //如何做到?---使用广播变量
    //注意:广播变量的值不能被修改,如需修改可以将数据存到外部数据源,如MySQL、Redis
    println("=====================")
    val BroadcastFruitMap: Broadcast[collection.Map[Int, String]] = sc.broadcast(fruitMap)
    val fruitNames2: RDD[String] = fruitIds.map(x=>BroadcastFruitMap.value(x))
    fruitNames2.foreach(println)

  }
}

```

Spark SQL
==========================================================================================================================================================================================================================================================================================================================

## Spark SQL 概述

Hive 是将 SQL 转为 MapReduce。

**SparkSQL 可以理解成是将 SQL 解析成：“RDD + 优化” 再执行**  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4923609622cf743b105c81a88878fe2a.png)  
在学习Spark SQL前，需要了解数据分类。

## 数据分类

数据分为如下几类：

|  | 定义 | 特点 | 举例 |
| :-- | :-- | :-- | :-- |
| 结构化数据 | 有固定的 Schema | 有预定义的 Schema | 关系型数据库的表 |
| 半结构化数据 | 没有固定的 Schema，但是有结构 | 没有固定的 Schema，有结构信息，数据一般是自描述的 | 指一些有结构的文件格式，例如 JSON |
| 非结构化数据 | 没有固定 Schema，也没有结构 | 没有固定 Schema，也没有结构 | 指图片/音频之类的格式 |

* * *

**总结：**

*   **RDD** 主要用于处理非结构化数据 、半结构化数据、结构化；
*   **SparkSQL** 是一个既支持 SQL 又支持命令式数据处理的工具；
*   **SparkSQL** 主要用于处理结构化数据(较为规范的半结构化数据也可以处理)。

## Spark SQL 数据抽象

### DataFrame 和 DataSet

Spark SQL数据抽象可以分为两类：

**① DataFrame**：DataFrame 是一种以 RDD 为基础的分布式数据集，类似于传统数据库的二维表格，带有 Schema 元信息(可以理解为数据库的列名和类型)。DataFrame = RDD ＋ 泛型 + SQL 的操作 + 优化

**② DataSet**：DataSet是DataFrame的进一步发展，它比RDD保存了更多的描述信息，概念上等同于关系型数据库中的二维表，它保存了类型信息，是强类型的，提供了编译时类型检查。调用 Dataset 的方法先会生成逻辑计划，然后被 spark 的优化器进行优化，最终生成物理计划，然后提交到集群中运行！DataFrame = Dateset\[Row\]

* * *

`RDD`、`DataFrame`、`DataSet`的关系如下：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/16105dc9e4343fe8e5df4a484fbe4650.png)

*   **RDD\[Person\]**：以 Person 为类型参数，但不了解其内部结构。
    
*   **DataFrame**：提供了详细的结构信息 schema 列的名称和类型。这样看起来就像一张表了。
    
*   **DataSet\[Person\]**：不光有 schema 信息，还有类型信息。
    

### 举例

假设 RDD 中的两行数据长这样：

```
RDD[Person]：

```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/66c1dd7a4e66f1e00bbea0d519d9ac25.png)  
那么 DataFrame 中的数据长这样

```
DataFrame = RDD[Person] - 泛型 + Schema + SQL 操作 + 优化

```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/be5a66fb925ed3fbef23a2ffca33a01c.png)  
那么 Dataset 中的数据长这样：

```
Dataset[Person] = DataFrame + 泛型：

```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0e63cf8736c24cd4b935a1b5b7b19d33.png)  
Dataset 也可能长这样:Dataset\[Row\]：

```
即 DataFrame = DataSet[Row]：

```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/86531a4b50a1a068545594861faba358.png)

* * *

**总结**：

*   DataFrame = RDD - 泛型 + Schema + SQL + 优化
*   DataSet = DataFrame + 泛型
*   DataSet = RDD + Schema + SQL + 优化

## Spark SQL 应用

### 创建 DataFrame/DataSet

**方式一：读取本地文件**

**① 在本地创建一个文件，有 id、name、age 三列，用空格分隔，然后上传到 hdfs 上。**

```
vim /root/person.txt

```

内容如下：

```
1 zhangsan 20
2 lisi 29
3 wangwu 25
4 zhaoliu 30
5 tianqi 35
6 kobe 40

```

**② 打开 spark-shell**

```
spark/bin/spark-shell

##创建 RDD

val lineRDD= sc.textFile("hdfs://node1:8020/person.txt").map(_.split(" ")) //RDD[Array[String]]

```

**③ 定义 case class(相当于表的 schema)**

```
case class Person(id:Int, name:String, age:Int)

```

**④ 将 RDD 和 case class 关联**

```
val personRDD = lineRDD.map(x => Person(x(0).toInt, x(1), x(2).toInt)) //RDD[Person]

```

**⑤ 将 RDD 转换成 DataFrame**

```
val personDF = personRDD.toDF //DataFrame

```

**⑥ 查看数据和 schema**

```
personDF.show

```

**⑦ 注册表**

```
personDF.createOrReplaceTempView("t_person")

```

**⑧ 执行 SQL**

```
spark.sql("select id,name from t_person where id > 3").show

```

**⑨ 也可以通过 SparkSession 构建 DataFrame**

```
val dataFrame=spark.read.text("hdfs://node1:8020/person.txt")
dataFrame.show //注意：直接读取的文本文件没有完整schema信息
dataFrame.printSchema

```

* * *

**方式二：读取 json 文件**

```
val jsonDF= spark.read.json("file:///resources/people.json")

```

接下来就可以使用 `DataFrame` 的函数操作

```
jsonDF.show

```

> 注意：直接读取 `json` 文件有`schema` 信息，因为`json`文件本身含有`Schema`信息，`SparkSQL` 可以自动解析。

* * *

**方式三：读取 parquet 文件**

```
val parquetDF=spark.read.parquet("file:///resources/users.parquet")

```

接下来就可以使用 `DataFrame` 的函数操作

```
parquetDF.show

```

> 注意：直接读取 `parquet` 文件有 `schema` 信息，因为 `parquet` 文件中保存了列的信息。

### 两种查询风格：DSL 和 SQL

DSL风格示例：

```
personDF.select(personDF.col("name")).show
personDF.select(personDF("name")).show
personDF.select(col("name")).show
personDF.select("name").show

```

SQL 风格示例:

```
spark.sql("select * from t_person").show

```

* * *

**总结**：

*   `DataFrame` 和 `DataSet` 都可以通过`RDD`来进行创建；
*   也可以通过读取普通文本创建–注意:直接读取没有完整的约束，需要通过 `RDD`+`Schema`；
*   通过 `josn/parquet` 会有完整的约束；
*   不管是 `DataFrame` 还是 `DataSet` 都可以注册成表，之后就可以使用 `SQL` 进行查询了! 也可以使用 `DSL`!

### Spark SQL 多数据源交互

读取 json 文件：

```
spark.read.json("D:\\data\\output\\json").show()

```

读取 csv 文件：

```
spark.read.csv("D:\\data\\output\\csv").toDF("id","name","age").show()

```

读取 parquet 文件：

```
spark.read.parquet("D:\\data\\output\\parquet").show()

```

读取 mysql 表：

```
val prop = new Properties()
    prop.setProperty("user","root")
    prop.setProperty("password","root")
spark.read.jdbc(
"jdbc:mysql://localhost:3306/bigdata?characterEncoding=UTF-8","person",prop).show()

```

* * *

写入 json 文件：

```
personDF.write.json("D:\\data\\output\\json")

```

写入 csv 文件：

```
personDF.write.csv("D:\\data\\output\\csv")

```

写入 parquet 文件：

```
personDF.write.parquet("D:\\data\\output\\parquet")

```

写入 mysql 表：

```
val prop = new Properties()
    prop.setProperty("user","root")
    prop.setProperty("password","root")
personDF.write.mode(SaveMode.Overwrite).jdbc(
"jdbc:mysql://localhost:3306/bigdata?characterEncoding=UTF-8","person",prop)

```

Spark Streaming
================================================================================================================================================================================================================================================================================================================================

**Spark Streaming 是一个基于 Spark Core 之上的实时计算框架，可以从很多数据源消费数据并对数据进行实时的处理，具有高吞吐量和容错能力强等特点。**  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/cc207b0ec1cef88969eff5a8be2d4807.png)  
Spark Streaming 的特点：

*   易用：可以像编写离线批处理一样去编写流式程序，支持 java/scala/python 语言。
*   容错：SparkStreaming 在没有额外代码和配置的情况下可以恢复丢失的工作。
*   易整合到 Spark 体系：流式处理与批处理和交互式查询相结合。

## 整体流程

*   **①** Spark Streaming 中，会有一个接收器组件 Receiver，作为一个长期运行的 task 跑在一个 Executor 上，Receiver 接收外部的数据流形成 input DStream。
*   **②** DStream 会被按照时间间隔划分成一批一批的 RDD，当批处理间隔缩短到秒级时，便可以用于处理实时数据流（时间间隔的大小可以由参数指定，一般设在 500 毫秒到几秒之间）。
*   **③** 对 DStream 进行操作就是对 RDD 进行操作，计算处理的结果可以传给外部系统。
*   **④** 接受到实时数据后，给数据分批次，然后传给 Spark Engine 处理最后生成该批次的结果。

## 数据抽象

Spark Streaming 的基础抽象是 DStream(Discretized Stream，离散化数据流，连续不断的数据流)，代表持续性的数据流和经过各种 Spark 算子操作后的结果数据流。

可以从以下多个角度深入理解 DStream：

**① DStream 本质上就是一系列时间上连续的 RDD**：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0e69423984c5f89e041c4c322709322e.png)

* * *

**② 对 DStream 的数据的进行操作也是按照 RDD 为单位来进行的**：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/78d107b74635bea0ee048ce438ece03e.png)

* * *

**③ 容错性，底层 RDD 之间存在依赖关系，DStream 直接也有依赖关系，RDD 具有容错性，那么 DStream 也具有容错性。**

* * *

**④ 准实时性/近实时性**

*   Spark Streaming 将流式计算分解成多个 Spark Job，对于每一时间段数据的处理都会经过 Spark DAG 图分解以及 Spark 的任务集的调度过程。
*   对于目前版本的 Spark Streaming 而言，其最小的 Batch Size 的选取在 0.5~5 秒钟之间。

所以 Spark Streaming 能够满足流式准实时计算场景，对实时性要求非常高的如高频实时交易场景则不太适合。

* * *

**总结：** 简单来说 DStream 就是对 RDD 的封装，你对 DStream 进行操作，就是对 RDD 进行操作。对于 DataFrame/DataSet/DStream 来说本质上都可以理解成 RDD。

## DStream 相关操作

**DStream 上的操作与 RDD 的类似，分为以下两种：**

*   Transformations(转换)
*   Output Operations(输出)/Action

### Transformations

以下是常见 Transformation—都是无状态转换：即每个批次的处理不依赖于之前批次的数据：

| Transformation | 含义 |
| :-- | :-- |
| map(func) | 对 DStream 中的各个元素进行 func 函数操作，然后返回一个新的 DStream |
| flatMap(func) | 与 map 方法类似，只不过各个输入项可以被输出为零个或多个输出项 |
| filter(func) | 过滤出所有函数 func 返回值为 true 的 DStream 元素并返回一个新的 DStream |
| union(otherStream) | 将源 DStream 和输入参数为 otherDStream 的元素合并，并返回一个新的 DStream |
| reduceByKey(func, \[numTasks\]) | 利用 func 函数对源 DStream 中的 key 进行聚合操作，然后返回新的(K，V)对构成的 DStream |
| join(otherStream, \[numTasks\]) | 输入为(K,V)、(K,W)类型的 DStream，返回一个新的(K，(V，W)类型的 DStream |
| **transform(func)** | 通过 RDD-to-RDD 函数作用于 DStream 中的各个 RDD，可以是任意的 RDD 操作，从而返回一个新的 RDD |

除此之外还有一类特殊的 Transformations—有状态转换：当前批次的处理需要使用之前批次的数据或者中间结果。

有状态转换包括基于追踪状态变化的转换(updateStateByKey)和滑动窗口的转换：

*   UpdateStateByKey(func)
*   Window Operations 窗口操作

### Output/Action

Output Operations 可以将 DStream 的数据输出到外部的数据库或文件系统。

当某个 Output Operations 被调用时，spark streaming 程序才会开始真正的计算过程(与 RDD 的 Action 类似)。

| Output Operation | 含义 |
| :-- | :-- |
| print() | 打印到控制台 |
| saveAsTextFiles(prefix, \[suffix\]) | 保存流的内容为文本文件，文件名为"prefix-TIME\_IN\_MS\[.suffix\]" |
| saveAsObjectFiles(prefix,\[suffix\]) | 保存流的内容为 SequenceFile，文件名为 “prefix-TIME\_IN\_MS\[.suffix\]” |
| saveAsHadoopFiles(prefix,\[suffix\]) | 保存流的内容为 hadoop 文件，文件名为"prefix-TIME\_IN\_MS\[.suffix\]" |
| foreachRDD(func) | 对 Dstream 里面的每个 RDD 执行 func |

Structured Streaming
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

> _Spark Streaming本质上是一种 micro-batch（微批处理）的方式处理，用批的思想去处理流数据，这种设计让Spark Streaming 面对复杂的流式处理场景时捉襟见肘。所以Structured Streaming就出现了。_

**Structured Streaming 是一个基于 Spark SQL 引擎的可扩展、容错的流处理引擎。统一了流、批的编程模型，你可以使用静态数据批处理一样的方式来编写流式计算操作。并且支持基于 event\_time 的时间窗口的处理逻辑。**

Structured Streaming 最核心的思想就是将实时到达的数据看作是一个不断追加的 unbound table 无界表，到达流的每个数据项(RDD)就像是表中的一个新行被附加到无边界的表中，这样用户就可以用静态结构化数据的批处理查询方式进行流计算，如可以使用 SQL 对到来的每一行数据进行实时查询处理。

## 数据抽象

Structured Streaming 是 Spark2.0 新增的可扩展和高容错性的实时计算框架，它构建于 Spark SQL 引擎，把流式计算也统一到 DataFrame/Dataset 里去了。

其实就类似于 Dataset 相比于 RDD 的进步:  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c785e115b95150a80f3ebb08fda67827.png)

## 应用场景

**Structured Streaming 将数据源映射为类似于关系数据库中的表，然后将经过计算得到的结果映射为另一张表，完全以结构化的方式去操作流式数据，这种编程模型非常有利于处理分析结构化的实时数据；**

下面举个例子。

### Source源端

**读取 Socket 数据：**

```
import org.apache.spark.SparkContext
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}

object WordCount {
  def main(args: Array[String]): Unit = {
    //1.创建SparkSession,因为StructuredStreaming的数据模型也是DataFrame/DataSet
    val spark: SparkSession = SparkSession.builder().master("local[*]").appName("SparkSQL").getOrCreate()
    val sc: SparkContext = spark.sparkContext
    sc.setLogLevel("WARN")
    //2.接收数据
    val dataDF: DataFrame = spark.readStream
      .option("host", "node01")
      .option("port", 9999)
      .format("socket")
      .load()
    //3.处理数据
    import spark.implicits._
    val dataDS: Dataset[String] = dataDF.as[String]
    val wordDS: Dataset[String] = dataDS.flatMap(_.split(" "))
    val result: Dataset[Row] = wordDS.groupBy("value").count().sort($"count".desc)
    //result.show()
    //Queries with streaming sources must be executed with writeStream.start();
    result.writeStream
      .format("console")//往控制台写
      .outputMode("complete")//每次将所有的数据写出
      .trigger(Trigger.ProcessingTime(0))//触发时间间隔,0表示尽可能的快
      //.option("checkpointLocation","./ckp")//设置checkpoint目录,socket不支持数据恢复,所以第二次启动会报错,需要注掉
      .start()//开启
      .awaitTermination()//等待停止
  }
}

```

* * *

**读取目录下文本数据：**

```
import org.apache.spark.SparkContext
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types.StructType
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}
/**
  * {"name":"json","age":23,"hobby":"running"}
  * {"name":"charles","age":32,"hobby":"basketball"}
  * {"name":"tom","age":28,"hobby":"football"}
  * {"name":"lili","age":24,"hobby":"running"}
  * {"name":"bob","age":20,"hobby":"swimming"}
  * 统计年龄小于25岁的人群的爱好排行榜
  */
object WordCount2 {
  def main(args: Array[String]): Unit = {
    //1.创建SparkSession,因为StructuredStreaming的数据模型也是DataFrame/DataSet
    val spark: SparkSession = SparkSession.builder().master("local[*]").appName("SparkSQL").getOrCreate()
    val sc: SparkContext = spark.sparkContext
    sc.setLogLevel("WARN")
    val Schema: StructType = new StructType()
      .add("name","string")
      .add("age","integer")
      .add("hobby","string")
    //2.接收数据
    import spark.implicits._
    // Schema must be specified when creating a streaming source DataFrame.
    val dataDF: DataFrame = spark.readStream.schema(Schema).json("D:\\data\\spark\\data")
    //3.处理数据
    val result: Dataset[Row] = dataDF.filter($"age" < 25).groupBy("hobby").count().sort($"count".desc)
    //4.输出结果
    result.writeStream
      .format("console")
      .outputMode("complete")
      .trigger(Trigger.ProcessingTime(0))
      .start()
      .awaitTermination()
  }
}

```

### Transform实时计算

获得到 `Source` 之后的基本数据处理方式和之前讲的 `DataFrame`、`DataSet` 一致，不再赘述。

官网示例代码：

```
case class DeviceData(device: String, deviceType: String, signal: Double, time: DateTime)
val df: DataFrame = ... // streaming DataFrame with IOT device data with schema { device: string, deviceType: string, signal: double, time: string }
val ds: Dataset[DeviceData] = df.as[DeviceData]    // streaming Dataset with IOT device data
// Select the devices which have signal more than 10
df.select("device").where("signal > 10")      // using untyped APIs
ds.filter(_.signal > 10).map(_.device)         // using typed APIs
// Running count of the number of updates for each device type
df.groupBy("deviceType").count()                 // using untyped API
// Running average signal for each device type
import org.apache.spark.sql.expressions.scalalang.typed
ds.groupByKey(_.deviceType).agg(typed.avg(_.signal))    // using typed API

```

### 输出

计算结果可以选择输出到多种设备并进行如下设定：

*   **output mode**：以哪种方式将 result table 的数据写入 sink,即是全部输出 complete 还是只输出新增数据；
*   **format/output sink 的一些细节**：数据格式、位置等。如 console；
*   **query name**：指定查询的标识。类似 tempview 的名字；
*   **trigger interval**：触发间隔，如果不指定，默认会尽可能快速地处理数据；
*   **checkpointLocation**：一般是 hdfs 上的目录。注意：Socket 不支持数据恢复，如果设置了，第二次启动会报错，Kafka 支持。

#### output mode

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0c0d446415540e1e7e7b27c70324448f.png)  
每当结果表更新时，我们都希望将更改后的结果行写入外部接收器。

这里有三种输出模型:

*   **Append mode**：默认模式，新增的行才输出，每次更新结果集时，只将新添加到结果集的结果行输出到接收器。仅支持那些添加到结果表中的行永远不会更改的查询。因此，此模式保证每行仅输出一次。例如，仅查询 select，where，map，flatMap，filter，join 等会支持追加模式。不支持聚合
*   **Complete mode**：所有内容都输出，每次触发后，整个结果表将输出到接收器。聚合查询支持此功能。仅适用于包含聚合操作的查询。
*   **Update mode**：更新的行才输出，每次更新结果集时，仅将被更新的结果行输出到接收器(自 Spark 2.1.1 起可用)，不支持排序

#### output sink

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/50c1988f786d304821e554a02aec72b6.png)  
**File sink**：输出存储到一个目录中。支持 parquet 文件，以及 append 模式。

```
writeStream
    .format("parquet")        // can be "orc", "json", "csv", etc.
    .option("path", "path/to/destination/dir")
    .start()

```

* * *

**Kafka sink**：将输出存储到 Kafka 中的一个或多个 topics 中。

```
writeStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
    .option("topic", "updates")
    .start()

```

* * *

**Foreach sink**：对输出中的记录运行任意计算

```
writeStream
    .foreach(...)
    .start()

```

* * *

**Console sink**：将输出打印到控制台

```
writeStream
    .format("console")
    .start()

```

Spark 两种核心 Shuffle
===================================================================================================================================================================================================================================================================================================================================

在 MapReduce 框架中，Shuffle 阶段是连接 Map 与 Reduce 之间的桥梁， Map 阶段通过 Shuffle 过程将数据输出到 Reduce 阶段中。**由于 `Shuffle` 涉及磁盘的读写和网络 `I/O`，因此 `Shuffle` 性能的高低直接影响整个程序的性能**。Spark 也有 Map 阶段和 Reduce 阶段，因此也会出现Shuffle。

**Spark Shuffle 分为两种：**

*   一种是基于 Hash 的 Shuffle；
*   另一种是基于 Sort 的 Shuffle。

## Hash Shuffle 解析

_以下的讨论都假设每个 Executor 有 1 个 cpu core。_

### HashShuffleManager

shuffle write 阶段，主要就是在一个 stage 结束计算之后，为了下一个 stage 可以执行 shuffle 类的算子（比如 reduceByKey），而将每个 task 处理的数据按 key 进行“划分”。所谓“划分”，**就是对相同的 key 执行 hash 算法**，从而将相同 key 都写入同一个磁盘文件中，而每一个磁盘文件都只属于下游 stage 的一个 task。在将数据写入磁盘之前，会先将数据写入内存缓冲中，当内存缓冲填满之后，才会溢写到磁盘文件中去。

下一个 stage 的 task 有多少个，当前 stage 的每个 task 就要创建多少份磁盘文件。比如:

> *   下一个 stage 总共有 100 个 task，那么当前 stage 的每个 task 都要创建 100 份磁盘文件。
> *   如果当前 stage 有 50 个 task，总共有 10 个 Executor，每个 Executor 执行 5 个 task，那么每个 Executor 上总共就要创建 500 个磁盘文件，所有 Executor 上会创建 5000 个磁盘文件。

由此可见，未经优化的 shuffle write 操作所产生的磁盘文件的数量是极其惊人的。

* * *

shuffle read 阶段，通常就是一个 stage 刚开始时要做的事情。此时该 stage 的**每一个 task 就需要将上一个 stage 的计算结果中的所有相同 key，从各个节点上通过网络都拉取到自己所在的节点上，然后进行 key 的聚合或连接等操作**。由于 shuffle write 的过程中，map task 给下游 stage 的每个 reduce task 都创建了一个磁盘文件，因此 shuffle read 的过程中，每个 reduce task 只要从上游 stage 的所有 map task 所在节点上，拉取属于自己的那一个磁盘文件即可。

shuffle read 的拉取过程是一边拉取一边进行聚合的。每个 shuffle read task 都会有一个自己的 buffer 缓冲，每次都只能拉取与 buffer 缓冲相同大小的数据，然后通过内存中的一个 Map 进行聚合等操作。聚合完一批数据后，再拉取下一批数据，并放到 buffer 缓冲中进行聚合操作。以此类推，直到最后将所有数据到拉取完，并得到最终的结果。

* * *

**HashShuffleManager 工作原理如下图所示：**  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9eb46d0001369c519e3a0d91322eb464.png)

### 优化的HashShuffleManager

为了优化 **HashShuffleManager** 我们可以设置一个参数：`spark.shuffle.consolidateFiles`，该参数默认值为 false，将其设置为 true 即可开启优化机制，通常来说，**如果我们使用 HashShuffleManager，那么都建议开启这个选项**。

开启 consolidate 机制之后，在 shuffle write 过程中，task 就不是为下游 stage 的每个 task 创建一个磁盘文件了，此时会出现 **shuffleFileGroup** 的概念，每个 shuffleFileGroup 会对应一批磁盘文件，磁盘文件的数量与下游 stage 的 task 数量是相同的。一个 Executor 上有多少个 cpu core，就可以并行执行多少个 task。而第一批并行执行的每个 task 都会创建一个 shuffleFileGroup，并将数据写入对应的磁盘文件内。

当 Executor 的 cpu core 执行完一批 task，接着执行下一批 task 时，**下一批 task 就会复用之前已有的 shuffleFileGroup，包括其中的磁盘文件**，也就是说，此时 task 会将数据写入已有的磁盘文件中，而不会写入新的磁盘文件中。因此，consolidate 机制允许不同的 task 复用同一批磁盘文件，这样就可以有效将多个 task 的磁盘文件进行一定程度上的合并，从而大幅度减少磁盘文件的数量，进而提升 shuffle write 的性能。

假设第二个 stage 有 100 个 task，第一个 stage 有 50 个 task，总共还是有 10 个 Executor（Executor CPU 个数为 1），每个 Executor 执行 5 个 task。那么原本使用未经优化的 HashShuffleManager 时，每个 Executor 会产生 500 个磁盘文件，所有 Executor 会产生 5000 个磁盘文件的。但是此时经过优化之后，每个 Executor 创建的磁盘文件的数量的计算公式为：**`cpu core的数量 * 下一个stage的task数量`**，也就是说，每个 Executor 此时只会创建 100 个磁盘文件，所有 Executor 只会创建 1000 个磁盘文件。

**优化后的 HashShuffleManager 工作原理如下图所示：**

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a3d652a5566a69b97d199b511d4b24c0.png)

### 优缺点

**优点：**

*   可以省略不必要的排序开销。
*   避免了排序所需的内存开销。

**缺点：**

*   生产的文件过多，会对文件系统造成压力。
*   大量小文件的随机读写带来一定的磁盘开销。
*   数据块写入时所需的缓存空间也会随之增加，对内存造成压力。

## SortShuffle 解析

**SortShuffleManager 的运行机制主要分成三种：**

*   普通运行机制；
*   bypass 运行机制：当 shuffle read task 的数量小于等于spark.shuffle.sort.bypassMergeThreshold参数的值时（默认为 200），就会启用 bypass 机制；
*   Tungsten Sort 运行机制：开启此运行机制需设置配置项 spark.shuffle.manager=tungsten-sort。开启此项配置也不能保证就一定采用此运行机制（后面会解释）。

### 普通运行机制

在该模式下，**数据会先写入一个内存数据结构中**，此时根据不同的 shuffle 算子，可能选用不同的数据结构。如果是 reduceByKey 这种聚合类的 shuffle 算子，那么会选用 Map 数据结构，一边通过 Map 进行聚合，一边写入内存；如果是 join 这种普通的 shuffle 算子，那么会选用 Array 数据结构，直接写入内存。接着，每写一条数据进入内存数据结构之后，就会判断一下，是否达到了某个临界阈值。如果达到临界阈值的话，那么就会尝试将内存数据结构中的数据溢写到磁盘，然后清空内存数据结构。

在溢写到磁盘文件之前，会先根据 key 对内存数据结构中已有的数据进行排序。排序过后，会分批将数据写入磁盘文件。默认的 batch 数量是 10000 条，也就是说，排序好的数据，会以每批 1 万条数据的形式分批写入磁盘文件。写入磁盘文件是通过 Java 的 BufferedOutputStream 实现的。**BufferedOutputStream 是 Java 的缓冲输出流，首先会将数据缓冲在内存中，当内存缓冲满溢之后再一次写入磁盘文件中，这样可以减少磁盘 IO 次数，提升性能**。

一个 task 将所有数据写入内存数据结构的过程中，会发生多次磁盘溢写操作，也就会产生多个临时文件。最后会将之前所有的临时磁盘文件都进行合并，这就是**merge** 过程，此时会将之前所有临时磁盘文件中的数据读取出来，然后依次写入最终的磁盘文件之中。此外，由于一个 task 就只对应一个磁盘文件，也就意味着该 task 为下游 stage 的 task 准备的数据都在这一个文件中，因此还会单独写一份**索引文件** ，其中标识了下游各个 task 的数据在文件中的 start offset 与 end offset。

SortShuffleManager 由于有一个磁盘文件 merge 的过程，因此大大减少了文件数量。比如第一个 stage 有 50 个 task，总共有 10 个 Executor，每个 Executor 执行 5 个 task，而第二个 stage 有 100 个 task。由于每个 task 最终只有一个磁盘文件，因此此时每个 Executor 上只有 5 个磁盘文件，所有 Executor 只有 50 个磁盘文件。

**普通运行机制的 SortShuffleManager 工作原理**如下图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/260aa4b1c1f9a3a3719ece9fe5fbc42a.png)

### bypass 运行机制

**Reducer 端任务数比较少的情况下，基于 Hash Shuffle 实现机制明显比基于 Sort Shuffle 实现机制要快，因此基于 Sort huffle 实现机制提供了一个回退方案，就是 bypass 运行机制**。对于 Reducer 端任务数少于配置属性`spark.shuffle.sort.bypassMergeThreshold`设置的个数时，使用带 Hash 风格的回退计划。

bypass 运行机制的触发条件如下：

shuffle map task 数量小于`spark.shuffle.sort.bypassMergeThreshold=200`参数的值。  
不是聚合类的 shuffle 算子。  
此时，每个 task 会为每个下游 task 都创建一个临时磁盘文件，并将数据按 key 进行 hash 然后根据 key 的 hash 值，将 key 写入对应的磁盘文件之中。当然，写入磁盘文件时也是先写入内存缓冲，缓冲写满之后再溢写到磁盘文件的。最后，同样会将所有临时磁盘文件都合并成一个磁盘文件，并创建一个单独的索引文件。

该过程的磁盘写机制其实跟未经优化的 HashShuffleManager 是一模一样的，因为都要创建数量惊人的磁盘文件，只是在最后会做一个磁盘文件的合并而已。因此少量的最终磁盘文件，也让该机制相对未经优化的 HashShuffleManager 来说，shuffle read 的性能会更好。

而该机制与普通 SortShuffleManager 运行机制的不同在于：第一，磁盘写机制不同；第二，不会进行排序。也就是说，**启用该机制的最大好处在于，shuffle write 过程中，不需要进行数据的排序操作，也就节省掉了这部分的性能开销**。

**bypass 运行机制的 SortShuffleManager 工作原理**如下图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9613857f3dc14cf03b454eff71a7b255.png)

### Tungsten Sort Shuffle 运行机制

基于 Tungsten Sort 的 Shuffle 实现机制主要是借助 Tungsten 项目所做的优化来高效处理 Shuffle。

Spark 提供了配置属性，用于选择具体的 Shuffle 实现机制，但需要说明的是，虽然默认情况下 Spark 默认开启的是基于 SortShuffle 实现机制，但实际上，参考 Shuffle 的框架内核部分可知基于 SortShuffle 的实现机制与基于 Tungsten Sort Shuffle 实现机制都是使用 SortShuffleManager，而内部使用的具体的实现机制，是通过提供的两个方法进行判断的：

**对应非基于 `Tungsten Sort` 时，通过 `SortShuffleWriter.shouldBypassMergeSort` 方法判断是否需要回退到 `Hash` 风格的 `Shuffle` 实现机制，当该方法返回的条件不满足时，则通过 `SortShuffleManager.canUseSerializedShuffle` 方法判断是否需要采用基于 `Tungsten Sort Shuffle` 实现机制，而当这两个方法返回都为 `false`，即都不满足对应的条件时，会自动采用普通运行机制**。

因此，当设置了 spark.shuffle.manager=tungsten-sort 时，也不能保证就一定采用基于 Tungsten Sort 的 Shuffle 实现机制。

要实现 Tungsten Sort Shuffle 机制需要满足以下条件：

Shuffle 依赖中不带聚合操作或没有对输出进行排序的要求。

Shuffle 的序列化器支持序列化值的重定位（当前仅支持 KryoSerializer Spark SQL 框架自定义的序列化器）。

Shuffle 过程中的输出分区个数少于 16777216 个。

实际上，使用过程中还有其他一些限制，如引入 Page 形式的内存管理模型后，内部单条记录的长度不能超过 128 MB （具体内存模型可以参考 PackedRecordPointer 类）。另外，分区个数的限制也是该内存模型导致的。

所以，目前使用基于 Tungsten Sort Shuffle 实现机制条件还是比较苛刻的。

### 优缺点

**优点：**

*   小文件的数量大量减少，Mapper 端的内存占用变少；
*   Spark 不仅可以处理小规模的数据，即使处理大规模的数据，也不会很容易达到性能瓶颈。

**缺点：**

*   如果 Mapper 中 Task 的数量过大，依旧会产生很多小文件，此时在 Shuffle 传数据的过程中到 Reducer 端， Reducer 会需要同时大量地记录进行反序列化，导致大量内存消耗和 GC 负担巨大，造成系统缓慢，甚至崩溃；
*   强制了在 Mapper 端必须要排序，即使数据本身并不需要排序；
*   它要基于记录本身进行排序，这就是 Sort-Based Shuffle 最致命的性能消耗。

Spark 底层执行原理
=============================================================================================================================================================================================================================================================================================================================

## Spark 运行流程

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/91fba69e08680b56fe728ec75a8cd561.png)  
具体运行流程如下：

1.  SparkContext 向资源管理器注册并向资源管理器申请运行 Executor
2.  资源管理器分配 Executor，然后资源管理器启动 Executor
3.  Executor 发送心跳至资源管理器
4.  SparkContext 构建 DAG 有向无环图
5.  将 DAG 分解成 Stage（TaskSet）
6.  把 Stage 发送给 TaskScheduler
7.  Executor 向 SparkContext 申请 Task
8.  TaskScheduler 将 Task 发送给 Executor 运行
9.  同时 SparkContext 将应用程序代码发放给 Executor
10.  Task 在 Executor 上运行，运行完毕释放所有资源

## 从代码角度看 DAG 图的构建

```
Val lines1 = sc.textFile(inputPath1).map(...).map(...)

Val lines2 = sc.textFile(inputPath2).map(...)

Val lines3 = sc.textFile(inputPath3)

Val dtinone1 = lines2.union(lines3)

Val dtinone = lines1.join(dtinone1)

dtinone.saveAsTextFile(...)

dtinone.filter(...).foreach(...)

```

上述代码的 DAG 图如下所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6e9e8df6880d3d594a092453ac94c782.png)  
Spark 内核会在需要计算发生的时刻绘制一张关于计算路径的有向无环图，也就是如上图所示的 DAG。

**Spark 的计算发生在 RDD 的 Action 操作，而对 Action 之前的所有 Transformation，Spark 只是记录下 RDD 生成的轨迹，而不会触发真正的计算。**

## 将 DAG 划分为 Stage 核心算法

一个 Application 可以有多个 job 多个 Stage：

Spark Application 中可以因为不同的 Action 触发众多的 job，一个 Application 中可以有很多的 job，每个 job 是由一个或者多个 Stage 构成的，后面的 Stage 依赖于前面的 Stage，也就是说只有前面依赖的 Stage 计算完毕后，后面的 Stage 才会运行。

划分依据：**Stage 划分的依据就是宽依赖，像 reduceByKey，groupByKey 等算子，会导致宽依赖的产生**。

> 回顾下宽窄依赖的划分原则：
> 
> *   窄依赖：父 RDD 的一个分区只会被子 RDD 的一个分区依赖。即一对一或者多对一的关系，可理解为独生子女。常见的窄依赖有：map、filter、union、mapPartitions、mapValues、join（父 RDD 是 hash-partitioned）等。
> *   宽依赖：父 RDD 的一个分区会被子 RDD 的多个分区依赖(涉及到 shuffle)。即一对多的关系，可理解为超生。常见的宽依赖有 groupByKey、partitionBy、reduceByKey、join（父 RDD 不是 hash-partitioned）等。

**核心算法：回溯算法**

**从后往前回溯/反向解析，遇到窄依赖加入本 Stage，遇见宽依赖进行 Stage 切分**。

Spark 内核会从触发 Action 操作的那个 RDD 开始从后往前推，首先会为最后一个 RDD 创建一个 Stage，然后继续倒推，如果发现对某个 RDD 是宽依赖，那么就会将宽依赖的那个 RDD 创建一个新的 Stage，那个 RDD 就是新的 Stage 的最后一个 RDD。然后依次类推，继续倒推，根据窄依赖或者宽依赖进行 Stage 的划分，直到所有的 RDD 全部遍历完成为止。

## 将 DAG 划分为 Stage 剖析

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8de2db1f0906a272d43cc18a9e6bb6fd.png)  
一个 Spark 程序可以有多个 DAG(有几个 Action，就有几个 DAG，上图最后只有一个 Action（图中未表现）,那么就是一个 DAG)。

一个 DAG 可以有多个 Stage(根据宽依赖/shuffle 进行划分)。

同一个 Stage 可以有多个 Task 并行执行(task 数=分区数，如上图，Stage1 中有三个分区 P1、P2、P3，对应的也有三个 Task)。

可以看到这个 DAG 中只 reduceByKey 操作是一个宽依赖，Spark 内核会以此为边界将其前后划分成不同的 Stage。

同时我们可以注意到，在图中 Stage1 中，**从 textFile 到 flatMap 到 map 都是窄依赖，这几步操作可以形成一个流水线操作，通过 flatMap 操作生成的 partition 可以不用等待整个 RDD 计算结束，而是继续进行 map 操作，这样大大提高了计算的效率**。

## 提交 Stages

调度阶段的提交，最终会被转换成一个任务集的提交，DAGScheduler 通过 TaskScheduler 接口提交任务集，这个任务集最终会触发 TaskScheduler 构建一个 TaskSetManager 的实例来管理这个任务集的生命周期，对于 DAGScheduler 来说，提交调度阶段的工作到此就完成了。

而 TaskScheduler 的具体实现则会在得到计算资源的时候，进一步通过 TaskSetManager 调度具体的任务到对应的 Executor 节点上进行运算。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9593128bfcd42ec38f94ff903668c216.png)

## 监控 Job、Task、Executor

DAGScheduler 监控 Job 与 Task：

*   要保证相互依赖的作业调度阶段能够得到顺利的调度执行，DAGScheduler 需要监控当前作业调度阶段乃至任务的完成情况。
*   这通过对外暴露一系列的回调函数来实现的，对于 TaskScheduler 来说，这些回调函数主要包括任务的开始结束失败、任务集的失败，DAGScheduler 根据这些任务的生命周期信息进一步维护作业和调度阶段的状态信息。

DAGScheduler 监控 Executor 的生命状态：

*   TaskScheduler 通过回调函数通知 DAGScheduler 具体的 Executor 的生命状态，如果某一个 Executor 崩溃了，则对应的调度阶段任务集的 ShuffleMapTask 的输出结果也将标志为不可用，这将导致对应任务集状态的变更，进而重新执行相关计算任务，以获取丢失的相关数据。

## 获取任务执行结果

结果 DAGScheduler：

*   一个具体的任务在 Executor 中执行完毕后，其结果需要以某种形式返回给 DAGScheduler，根据任务类型的不同，任务结果的返回方式也不同。

* * *

两种结果，中间结果与最终结果：

*   对于 FinalStage 所对应的任务，返回给 DAGScheduler 的是运算结果本身。
*   而对于中间调度阶段对应的任务 ShuffleMapTask，返回给 DAGScheduler 的是一个 MapStatus 里的相关存储信息，而非结果本身，这些存储位置信息将作为下一个调度阶段的任务获取输入数据的依据。

* * *

两种类型，DirectTaskResult 与 IndirectTaskResult：

根据任务结果大小的不同，ResultTask 返回的结果又分为两类：

*   如果结果足够小，则直接放在 DirectTaskResult 对象内中。
*   如果超过特定尺寸则在 Executor 端会将 DirectTaskResult 先序列化，再把序列化的结果作为一个数据块存放在 BlockManager 中，然后将 BlockManager 返回的 BlockID 放在 IndirectTaskResult 对象中返回给 TaskScheduler，TaskScheduler 进而调用 TaskResultGetter 将 IndirectTaskResult 中的 BlockID 取出并通过 BlockManager 最终取得对应的 DirectTaskResult。

## 任务调度总体诠释

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/51d1d837f7b6d9833f38998106965c0b.png)

### Executor 进程专属

**每个 Application 获取专属的 Executor 进程，该进程在 Application 期间一直驻留，并以多线程方式运行 Tasks。**

Spark Application 不能跨应用程序共享数据，除非将数据写入到外部存储系统。如图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a345b5964d8ec78a7d5d7bf4f11a5bbe.png)

### 支持多种资源管理器

Spark 与资源管理器无关，只要能够获取 Executor 进程，并能保持相互通信就可以了。

Spark 支持资源管理器包含：Standalone、On Mesos、On YARN、Or On EC2。如图所示:  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/501feb3b064d9f6bd58b810c684d267f.png)

### Job 提交就近原则

提交 SparkContext 的 Client 应该靠近 Worker 节点(运行 Executor 的节点)，最好是在同一个 Rack(机架)里，因为 Spark Application 运行过程中 SparkContext 和 Executor 之间有大量的信息交换;

如果想在远程集群中运行，最好使用 RPC 将 SparkContext 提交给集群，不要远离 Worker 运行 SparkContext。

如图所示:  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ee0092ed88477de71e9b3d5f7a87daf3.png)

### 移动程序而非移动数据的原则执行

移动程序而非移动数据的原则执行，Task 采用了数据本地性和推测执行的优化机制。

关键方法：taskIdToLocations、getPreferedLocations。

如图所示:  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0e65cf2182ffa63d994d41271621ebfc.png)  