# fund_collect
./entry.py 将会读取fund.xlsx中的基金信息（第一列是基金名称，第二列是基金代码），每两分钟轮询一次当前估值；
输出结果会展示当前时间，并以今日估值涨幅降序展示结果。

get_fund_networth是实现的本体。

TODO:
后续加入接口获取其他日期的基金净值并进行分析
