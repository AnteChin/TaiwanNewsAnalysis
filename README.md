# TaiwanNewsAnalysis
Finding keywords of each news; Generating word cloud; Creating histograms

`fen.py` and `toexcel.py` are old files

In `reports` directory you can find two python file. 

* `generator.py` can be used to devide whole passage into seperate Chinese words and count them. There is also a function that making a word cloud picture. Precision is set well.

* `painter.py` can generate histograms.

Before excute, make sure you have a excel file in the directory and it should contains column `title`, 'date` and 'context'.

* * *
统计台湾地区九合一大选中报道的数据, 并生成对应的词云图和直方图, 用于比对各候选人在不同媒体上的热度<br>
数据部分使用scrapy爬虫获得, 不列入此文件. 如欲了解请发邮件
