from helpers import *
import pickle

# 具象实现类-过滤器模板 (空过滤器)
class FilterHmm(BaseFilter):
    filter_type = "Director"
    # 可调参数
    parameters = [
    ]
    # 状态变量
    variables = [
    ]

    def __init__(self, strategy_inst):
        # 继承父类
        super().__init__(strategy_inst=strategy_inst)
        self.flag = 1 # 默认为1, 表示"未过滤,允许开仓"
        # 需要画中间过程的变量值 (存在该字典中, 若draw_all为True, 则会在分钟结束后画出这些变量值)
        self.chart_vars = {}
        # 加载模型
        with open("hmm.pkl", "rb") as file:
            self.hmm_model = pickle.load(file)

    def get_filter_flag(self, bars):
        """
        输入: bars
        功能: 计算过滤器指标
        输出: self.flag (0:过滤, 1:不过滤)
        """
        features = None
        state = self.hmm_model.predict(features)
        if state == 0:
            self.flag = 1
        else:
            self.flag = 0


    def draw(self, bars, draw_all=True):
        self.chart.fmz_chart.add(
            self.chart.get_series_index(self.chart.chart_config, "filter_template_flag"),
            [self.bar.time, self.flag]
        )
