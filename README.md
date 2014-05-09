
一个bug 遍体的 爬虫框架（这也能算框架吗）
很好玩。

<code>spider.py</code> 使用 gevent ，没有更新。。
<code>crawler.py</code> 使用 threading。所有的改动都集中在这个文件了。
url 抓取列表在 redis DB 1 里面
倒排索引在 redis DB 2 内