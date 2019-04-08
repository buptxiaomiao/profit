# coding: utf-8

from utils.time_tool import TimeTool


class DfToModels(object):
    """
    DataFrame -> Model
    """

    @classmethod
    def df2models(cls, df, model_class, return_dict=False):
        """
        DataFrame -> Model
        :return:
        """
        trash_cols = []
        cols = df.columns
        for x in cols:
            if not hasattr(model_class, str(x)):
                trash_cols.append(x)

        l = []
        for _, row in df.iterrows():
            d = row.to_dict()
            for x in d.keys():
                # 处理None值 & 多余字段
                if not d[x] or x in trash_cols:
                    del d[x]
            if return_dict:
                l.append(d)
                continue

            o = model_class(**d)
            if hasattr(model_class, 'create_time'):
                o.create_time = TimeTool.now()
            if hasattr(model_class, 'update_time'):
                o.update_time = TimeTool.now()
            l.append(o)
        return l
