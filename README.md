# fund_collect
cd instant_net_worth
python .\get_fund_networth.py 
将会读取fund.xlsx中的基金信息（第一列是基金名称，第二列是基金代码），每分钟轮询一次当前估值；
输出结果会展示当前时间，并以今日估值涨幅降序展示结果。

cd tool
python .\calc.py 可以计算定投的预期收入
参数为：
年限, 收益率, 定投金额, 定投增长率, 通货膨胀率
example:
python.exe .\calc.py 10 0.2 10000 0.1 0.08
current value considered inflation 2210503

TODO:
daily_net_worth下的每日净值分析，待完善
