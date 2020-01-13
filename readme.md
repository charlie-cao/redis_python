# 使用Python 客户端测试 redis 

mac 安装
brew install redis

启动
redis-server

客户端
redis-cli

常用命令
set key value	设置 key 的值
get key	获取 key 的值
exists key	查看此 key 是否存在
keys *	查看所有的 key
flushall	消除所有的 key

https://www.cnblogs.com/zhaohuhu/p/9140673.html
1 (1) 速度快，因为数据存在内存中，类似于HashMap，HashMap的优势就是查找和操作的时间复杂度都是O(1)
2  
3 (2) 支持丰富数据类型，支持string，list，set，sorted set，hash
4  
5 (3) 支持事务，操作都是原子性，所谓的原子性就是对数据的更改要么全部执行，要么全部不执行
6  
7 (4) 丰富的特性：可用于缓存，消息，按key设置过期时间，过期后将会自动删除
redis相比memcached有哪些优势？
1 (1) memcached所有的值均是简单的字符串，redis作为其替代者，支持更为丰富的数据类型
2  
3 (2) redis的速度比memcached快很多
4  
5 (3) redis可以持久化其数据

redis常见性能问题和解决方案：
复制代码
 1 (1) Master最好不要做任何持久化工作，如RDB内存快照和AOF日志文件
 2 
 3 (2) 如果数据比较重要，某个Slave开启AOF备份数据，策略设置为每秒同步一次
 4 
 5 (3) 为了主从复制的速度和连接的稳定性，Master和Slave最好在同一个局域网内
 6 
 7 (4) 尽量避免在压力很大的主库上增加从库
 8 
 9 (5) 主从复制不要用图状结构，用单向链表结构更为稳定，即：Master <- Slave1 <- Slave2 <- Slave3...
10 
11 这样的结构方便解决单点故障问题，实现Slave对Master的替换。如果Master挂了，可以立刻启用Slave1做Master，其他不变。

MySQL里有2000w数据，redis中只存20w的数据，如何保证redis中的数据都是热点数据
复制代码
 1  相关知识：redis 内存数据集大小上升到一定大小的时候，就会施行数据淘汰策略。redis 提供 6种数据淘汰策略：
 2 
 3 voltile-lru：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰
 4 
 5 volatile-ttl：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
 6 
 7 volatile-random：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰
 8 
 9 allkeys-lru：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰
10 
11 allkeys-random：从数据集（server.db[i].dict）中任意选择数据淘汰
12 
13 no-enviction（驱逐）：禁止驱逐数据
Memcache与Redis的区别都有哪些？
复制代码
 1 1)、存储方式
 2 
 3 Memecache把数据全部存在内存之中，断电后会挂掉，数据不能超过内存大小。
 4 
 5 Redis有部份存在硬盘上，这样能保证数据的持久性。
 6 
 7 2)、数据支持类型
 8 
 9 Memcache对数据类型支持相对简单。
10 
11 Redis有复杂的数据类型。
12 
13 
14 3），value大小
15 
16 redis最大可以达到1GB，而memcache只有1MB
Redis 常见的性能问题都有哪些？如何解决？
复制代码
1 1).Master写内存快照，save命令调度rdbSave函数，会阻塞主线程的工作，当快照比较大时对性能影响是非常大的，会间断性暂停服务，所以Master最好不要写内存快照。
2 
3 
4 2).Master AOF持久化，如果不重写AOF文件，这个持久化方式对性能的影响是最小的，但是AOF文件会不断增大，AOF文件过大会影响Master重启的恢复速度。Master最好不要做任何持久化工作，包括内存快照和AOF日志文件，特别是不要启用内存快照做持久化,如果数据比较关键，某个Slave开启AOF备份数据，策略为每秒同步一次。
5 
6  
7 3).Master调用BGREWRITEAOF重写AOF文件，AOF在重写的时候会占大量的CPU和内存资源，导致服务load过高，出现短暂服务暂停现象。
8 
9 4). Redis主从复制的性能问题，为了主从复制的速度和连接的稳定性，Slave和Master最好在同一个局域网内


redis 最适合的场景
复制代码
 1 Redis最适合所有数据in-momory的场景，虽然Redis也提供持久化功能，但实际更多的是一个disk-backed的功能，跟传统意义上的持久化有比较大的差别，那么可能大家就会有疑问，似乎Redis更像一个加强版的Memcached，那么何时使用Memcached,何时使用Redis呢?
 2 
 3        如果简单地比较Redis与Memcached的区别，大多数都会得到以下观点：
 4 
 5      1 、Redis不仅仅支持简单的k/v类型的数据，同时还提供list，set，zset，hash等数据结构的存储。
 6      2 、Redis支持数据的备份，即master-slave模式的数据备份。
 7      3 、Redis支持数据的持久化，可以将内存中的数据保持在磁盘中，重启的时候可以再次加载进行使用。
 8 
 9 （1）、会话缓存（Session Cache）
10 
11 最常用的一种使用Redis的情景是会话缓存（session cache）。用Redis缓存会话比其他存储（如Memcached）的优势在于：Redis提供持久化。当维护一个不是严格要求一致性的缓存时，如果用户的购物车信息全部丢失，大部分人都会不高兴的，现在，他们还会这样吗？
12 
13 幸运的是，随着 Redis 这些年的改进，很容易找到怎么恰当的使用Redis来缓存会话的文档。甚至广为人知的商业平台Magento也提供Redis的插件。
14 
15 （2）、全页缓存（FPC）
16 
17 除基本的会话token之外，Redis还提供很简便的FPC平台。回到一致性问题，即使重启了Redis实例，因为有磁盘的持久化，用户也不会看到页面加载速度的下降，这是一个极大改进，类似PHP本地FPC。
18 
19 再次以Magento为例，Magento提供一个插件来使用Redis作为全页缓存后端。
20 
21 此外，对WordPress的用户来说，Pantheon有一个非常好的插件  wp-redis，这个插件能帮助你以最快速度加载你曾浏览过的页面。
22 
23 （3）、队列
24 
25 Reids在内存存储引擎领域的一大优点是提供 list 和 set 操作，这使得Redis能作为一个很好的消息队列平台来使用。Redis作为队列使用的操作，就类似于本地程序语言（如Python）对 list 的 push/pop 操作。
26 
27 如果你快速的在Google中搜索“Redis queues”，你马上就能找到大量的开源项目，这些项目的目的就是利用Redis创建非常好的后端工具，以满足各种队列需求。例如，Celery有一个后台就是使用Redis作为broker，你可以从这里去查看。
28 
29 （4），排行榜/计数器
30 
31 Redis在内存中对数字进行递增或递减的操作实现的非常好。集合（Set）和有序集合（Sorted Set）也使得我们在执行这些操作的时候变的非常简单，Redis只是正好提供了这两种数据结构。所以，我们要从排序集合中获取到排名最靠前的10个用户–我们称之为“user_scores”，我们只需要像下面一样执行即可：
32 
33 当然，这是假定你是根据你用户的分数做递增的排序。如果你想返回用户及用户的分数，你需要这样执行：
34 
35 ZRANGE user_scores 0 10 WITHSCORES
36 
37 Agora Games就是一个很好的例子，用Ruby实现的，它的排行榜就是使用Redis来存储数据的，你可以在这里看到。
38 
39 （5）、发布/订阅
40 
41 最后（但肯定不是最不重要的）是Redis的发布/订阅功能。发布/订阅的使用场景确实非常多。我已看见人们在社交网络连接中使用，还可作为基于发布/订阅的脚本触发器，甚至用Redis的发布/订阅功能来建立聊天系统！（不，这是真的，你可以去核实）。
42 
43 Redis提供的所有特性中，我感觉这个是喜欢的人最少的一个，虽然它为用户提供如果此多功能。




 Python操作Redis
1、安装方法
复制代码
1 sudo pip install redis
2 or
3 sudo easy_install redis
4 or
5 源码安装
6  
7 详见：https://github.com/WoLpH/redis-py

