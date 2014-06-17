
一个微型爬虫框架

<code>spider.py</code> 使用 gevent ，没有更新。。
<code>crawler.py</code> 使用 threading。所有的改动都集中在这个文件了。


url 抓取列表在 redis DB 1 里面


倒排索引在 redis DB 2 内，unicode 编码