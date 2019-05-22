# coding: utf-8

from datetime import datetime, timedelta
import tushare as ts

# 首次使用，需要设置token
# ts.set_token("******")


def daily_classifier(ts_code, trade_date):
    """ A 股每日走势的分类

    使用该方法前，请仔细阅读：http://blog.sina.com.cn/s/blog_486e105c010009uy.html

    每个交易日产生 8 根 30 分钟 K 线，分别在前三根和最后三根中计算中枢，其结果分以下情况：
    1）没有中枢；
    2）仅有一个中枢，或计算得到的两个中枢区间有重叠；
    3）有两个中枢，且没有重叠。
    """
    start_date = datetime.strptime(trade_date, '%Y%m%d')
    end_date = start_date + timedelta(days=1)
    end_date = end_date.date().__str__().replace("-", "")

    df = ts.pro_bar(ts_code=ts_code, freq='30min', start_date=trade_date, end_date=end_date)
    df.sort_values('trade_time', inplace=True)
    data = df[['ts_code', 'trade_time', 'high', 'low']].iloc[1:, :]
    data = data.reset_index(drop=True)
    assert len(data) == 8, "每个交易日，A股有且只有8跟30分钟K线"

    def _central(tri):
        c_low = max(tri['low'])
        c_high = min(tri['high'])
        if c_low >= c_high:
            # None means no central found
            central = None
        else:
            central = {
                "time_span": "%s - %s" % (tri.iloc[0, 1], tri.iloc[2, 1]),
                "price_span": (c_low, c_high)
            }
        return central

    first_central = _central(data.iloc[:3, :])
    last_central = _central(data.iloc[-3:, :])
    return first_central, last_central


if __name__ == '__main__':
    fc, lc = daily_classifier('600122.SH', "20190521")
    print(fc, lc)
