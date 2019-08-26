地类空间统计模型调用案例及参数说明：

接口说明：

landClipStatistic(spark,geoanalytics,layers,extent="",group_field='DLMC', statistic_field = 'TBMJ', xzq_field = '',fs_layer_name='land_clip_statistics_result')

参数说明：
    - spark, geoanalytics,layers是run python script内部对象，不需改动，直接传入即可；
    - extent用于控制分析输入图层的范围，输入规则：
      extent = {"spatialReference": {"wkid": spatial_reference},"xmin": extent['xmin'], "ymin": extent['ymin'], "xmax": extent['xmax'],"ymax": extent['ymax']}

    - group_field: 用于分组字段，默认值是"DLMC"
    - statistic_field： 统计字段，默认值是"TBMJ"
    - xzq_field: 行政区划字段，如果该字段值为空字符串，默认不考虑行政区范围统计。如果给定该字段值，则纳入行政区维度统计。
    - fs_layer_name: 裁切输出的要素图层名。另外还会输出统计表名，在此基础上追加"_table"命名。    
   
===================================================================================
调用案例二：

Python Script:
--------------

import landClipStatisticModel

landClipStatisticModel.landClipStatistic(spark,geoanalytics,layers,extent="",group_field='DLMC', statistic_field = 'TBMJ', xzq_field = '',fs_layer_name='land_clip_statistics_result13')

landClipStatisticModel.landClipStatistic(spark,geoanalytics,layers,extent="",group_field='DLMC', statistic_field = 'TBMJ', xzq_field = 'QSDWDM',fs_layer_name='land_clip_statistics_result12')

Input Layers:
-------------

[{'url':'https://abi.arcgisonline.cn/abiserver/rest/services/DataStoreCatalogs/bigDataFileShares_dltb_for_shuhui/BigDataCatalogServer/二调'},{'url':'https://abi.arcgisonline.cn/server/rest/services/Hosted/polygon_for_sandiao/FeatureServer/0'}]



