地类差异分析模型使用文档

模型调用案例及参数说明：

接口说明：
1，地类差异分析

landVarianceAnalysis(sc,spark,geoanalytics,layers,extent="",polygon="",poly_wkid=4527,contrast_field_name='DLMC',wkid = 0,fs_layer_name='land_variance_layer',temp_path='/gis/gis3054/directories/temp')

参数说明：
    - sc,spark,geoanalytics, layers是run python script内部对象，不需改动，直接传入即可；
    - extent用于控制分析输入图层的范围，输入规则：
      extent = {"spatialReference": {"wkid": spatial_reference},"xmin": extent['xmin'], "ymin": extent['ymin'], "xmax": extent['xmax'],"ymax": extent['ymax']}
    - polygon 输入多边形，按多边形范围裁切地类进行差异分析，输入规则：
      polygon = "[[[118.26266908499997,27.34870321300002],[118.44655755300005,27.34870321300002],[118.26266908499997,27.421048263999978],[118.26266908499997,27.34870321300002]]]"
    - poly_wkid: 输入多边形的空间参考，这个参数用于构造polygon layer， 值应该和传入的polygon空间参考匹配

    - contrast_field_name: 用于对比分析的字段名，默认值是"DLMC"
    - wkid：用于空间投影的wkid值，默认值是0，表示不投影
    - fs_layer_name: 差异分析后用于标识地类变化的要素图层名，变化字段名为"change"；
    - temp_path : 共享临时目录，用于差异分析的表会输出到这个目录下，因此需要所有GA节点都能访问到，建议使用server集群的directories目录

=====================================================================================================================================================================================================
调用案例1：

Python Script:
--------------

import landVarianceAnalysisModel

polygon = "[[[118.26266908499997,27.34870321300002],[118.44655755300005,27.34870321300002],[118.26266908499997,27.421048263999978],[118.26266908499997,27.34870321300002]]]"

p_wkid = 4610

landVarianceAnalysisModel.landVarianceAnalysis(sc,spark,geoanalytics,layers,polygon = polygon,poly_wkid=p_wkid,contrast_field_name='dlmc', fs_layer_name='makl_land_variance_layer04',temp_path='/gis/gis3054/directories/temp')


Input Layers:
--------------

[{"url":"https://abi.arcgisonline.cn/server/rest/services/Hosted/ED/FeatureServer/1"},{"url":"https://abi.arcgisonline.cn/server/rest/services/Hosted/SD/FeatureServer/0"}]


