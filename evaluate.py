# -*- coding:utf-8 -*-

import pandas as pd

"""评价标准请查看 ./notebook/evaluate.ipynb"""

def evaluate(result_path, standard_path):
    """结果评价函数。
    @input:
        result_path: 结果 csv 文件。包括三列 [SentenceId,View,Opinion]
        standard_path: 答案 csv 文件。形式与result_path 相同。
    @return:
        P: precision
        R: recall rate
        F1: F1 value
    """
    df_result = pd.read_csv(result_path, sep='\t')
    df_standard = pd.read_csv(standard_path, sep='\t')
    df_result['id'] = df_result.SentenceId.apply(lambda num_id: str(num_id))
    df_result['key'] = df_result.id + df_result.View  # 将id和视角拼起来作为唯一标识
    df_standard['id'] = df_standard.SentenceId.apply(lambda num_id: str(num_id))
    df_standard['key'] = df_standard.id + df_standard.View  # 将id和视角拼起来作为唯一标识
    # 漏判 fn1, 多判 fn2
    r_key = set(df_result.key.values)
    s_key = set(df_standard.key.values)
    tn = len(r_key & s_key)  # 视角判断正确,取两者交集
    fn1 = len(s_key) - tn
    fn2 = len(r_key) - tn
    p_view = float(tn) / len(r_key)  # 视角提取正确率
    r_view = float(tn) / len(s_key)  # 视角提取召回率
    f1_view = 2 * p_view * r_view / (p_view + r_view) # 视角提取 F1 值
    print 'p_view=%g, r_view=%g, f1_view=%g' % (p_view, r_view, f1_view)
    # 情感判断正确 tp, 判断错误 fp
    df_result['view_opinion'] = df_result.key + df_result.Opinion  # id_view_opinion
    df_standard['view_opinion'] = df_standard.key + df_standard.Opinion  # id_view_opinion
    r_vo = set(df_result.view_opinion.values)
    s_vo = set(df_standard.view_opinion.values)
    tp = len(r_vo & s_vo)
    fp = tn - tp
    P = float(tp) / (tn + fn2)  # 准确率
    R = float(tp) / (tp + fn1)  # 召回率
    F1 = 2*P*R / (P+R)
    # print 'tn=%d, fn1=%d, fn2=%d, tp=%d, fp=%d' % (tn, fn1, fn2, tp, fp)
    print 'P=%g, R=%g, F1=%g' % (P, R, F1)