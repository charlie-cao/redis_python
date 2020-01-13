#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import redis
#  redis-py使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。默认，每个Redis实例都会维护一个自己的连接池。可以直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池。
pool = redis.ConnectionPool(host='localhost', port=6379)
 
r = redis.Redis(connection_pool=pool)
r.set('foo', 'Bar')
print(r.get('foo'))


r.zadd('zz', n1=11, n2=22)
print(r.zcard('zz'))