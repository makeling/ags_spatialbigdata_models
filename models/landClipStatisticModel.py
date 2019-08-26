# -*- coding: utf-8 -*-
# !/usr/bin/python
__author__ = 'ma_keling'
# Version     : 1.0.0
# Start Time  : 2019-8-15
# Update Time :
# Change Log  :

# extent = {"spatialReference": {"wkid": spatial_reference},"xmin": extent['xmin'], "ymin": extent['ymin'], "xmax": extent['xmax'],"ymax": extent['ymax']}
def landClipStatistic(spark,geoanalytics,layers,extent="",group_field='DLMC', statistic_field = 'TBMJ', xzq_field = '',fs_layer_name='land_clip_statistics_result'):
    # 1 input data
    if extent == "":
        input_layer = layers[0]
        clip_layer = layers[1]
    else:
        input_layer_url = layers[0]['url']
        clip_layer_url = layers[1]['url']

        input_layer = spark.read.format('webgis').option('extent', extent).load(input_layer_url)
        clip_layer = spark.read.format('webgis').option('extent', extent).load(clip_layer_url)

    # 2: clip input_layer
    clip_result_layer = geoanalytics.clip_layer(input_layer, clip_layer)

    clip_result_layer.write.format('webgis').option('dataStore', 'spatiotemporal').save(
        fs_layer_name)

    # 3 Aggregate clip result area based on groupby field

    if xzq_field == "":
        aggr_table = geoanalytics.summarize_attributes(clip_result_layer, [group_field],
                                                       summary_fields=[{'onStatisticField': statistic_field,
                                                                'statisticType': 'SUM'}])
    else:
        aggr_table = geoanalytics.summarize_attributes(clip_result_layer, [xzq_field, group_field],
                                                       summary_fields=[{'onStatisticField': statistic_field,
                                                                        'statisticType': 'SUM'}])

    aggr_table.write.format('webgis').option('dataStore', 'spatiotemporal').save(
        fs_layer_name + '_table')


