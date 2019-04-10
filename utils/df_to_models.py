# coding: utf-8

import numpy as np

from utils.time_tool import TimeTool
from utils.log_tools import logger


class DfToModels(object):
    """
    DataFrame -> Model
    """

    @classmethod
    def df2models(cls, df, model_class, to_dict=False):
        """
        DataFrame -> Model
        :return:
        """
        l = []
        fields = model_class._meta.fields.keys()
        for _, row in df.iterrows():
            d = row.to_dict()
            d = {k: d[k] for k in fields if d.get(k, None) and d.get(k, None) is not np.nan}
            if to_dict:
                l.append(d)
            else:
                o = model_class(**d)
                o.create_time = TimeTool.now()
                o.update_time = TimeTool.now()
                l.append(o)
        return l
