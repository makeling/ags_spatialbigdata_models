# -*- coding: utf-8 -*-
# !/usr/bin/python
__author__ = 'ma_keling'
# Version     : 1.0.0
# Start Time  : 2019-8-15
# Update Log :
    # 2019-8-19: change statistics method
    # 2019-8-26: Add statistics in a polygon


# create GA polygon layer by polygon array
def build_polygon_layer(sc,spark,polygon,wkid):
    from pyspark.sql.types import DoubleType, ArrayType, StructType, StructField,IntegerType
    from pyspark.sql import Row

    # two fields:
    row = Row(1, [polygon])
    rows = [row]
    rdd = sc.parallelize(rows)
    fschema = StructType()
    fschema.add("ID", data_type=IntegerType())
    rings_Type = StructType(
    [StructField("rings", ArrayType(elementType=ArrayType(elementType=ArrayType(elementType=DoubleType()))))])
    meta = {'geometry': {'type': 'polygon', 'spatialReference': {'latestWkid': wkid, 'wkid': wkid}}}

    fschema.add("$geometry", data_type=rings_Type, metadata=meta)

    df = spark.createDataFrame(rdd, fschema)

    return df


# extent = {"spatialReference": {"wkid": spatial_reference},"xmin": extent['xmin'], "ymin": extent['ymin'], "xmax": extent['xmax'],"ymax": extent['ymax']}
# polygon = "[[[107.3245410960689,22.206513426341015],[109.61817976466745,22.206513426341015],[109.61817976466745,24.0349678791908],[107.3245410960689,22.206513426341015]]]"
# temp_path : server share directory
def landVarianceAnalysis(sc,spark,geoanalytics,layers,extent="",polygon="",poly_wkid=4527,contrast_field_name='DLMC',wkid = 0,fs_layer_name='land_variance_layer',temp_path='/gis/gis3054/directories/temp'):
    import pandas as pd
    import os
    import json

    if polygon == "":
        if extent == "":
            # 1 input data
            data_pre = layers[0]
            data_next = layers[1]
        else:
            # 1 input data
            pre_url = layers[0]['url']
            next_url = layers[1]['url']

            data_pre = spark.read.format('webgis').option('extent', extent).load(pre_url)
            data_next = spark.read.format('webgis').option('extent', extent).load(next_url)
    else:
        input_polygon = json.loads(polygon)
        polygon_df = build_polygon_layer(sc,spark,input_polygon,poly_wkid)
        if extent == "":
            # 1 input data
            i_data_pre = layers[0]
            i_data_next = layers[1]

            data_pre = geoanalytics.clip_layer(polygon_df, i_data_pre)
            data_next = geoanalytics.clip_layer(polygon_df, i_data_next)
        else:
            # 1 input data
            pre_url = layers[0]['url']
            next_url = layers[1]['url']

            i_data_pre = spark.read.format('webgis').option('extent', extent).load(pre_url)
            i_data_next = spark.read.format('webgis').option('extent', extent).load(next_url)
            data_pre = geoanalytics.clip_layer(polygon_df, i_data_pre)
            data_next = geoanalytics.clip_layer(polygon_df, i_data_next)


    # 2 union for calculate difference
    difference_layer = geoanalytics.overlay_layers(data_pre, data_next, overlay_type='Union', include_overlaps=False)

    # 3 calculate change field
    if wkid != 0:
        difference_layer_proj = geoanalytics.project(difference_layer, wkid)

    else:
        difference_layer_proj = difference_layer

    overlay_field_name = contrast_field_name + "_overlay"

    exp = "var dl = $feature[\"" + contrast_field_name + "\"]; var dl_overlay = $feature[\"" + overlay_field_name + "\"]; if(dl == dl_overlay) return 0; else return 1"

    difference_layer_change = geoanalytics.calculate_field(difference_layer_proj, field_name="change",
                                                           data_type="Integer",
                                                           expression=exp)

    difference_layer_change.write.format('webgis').option('dataStore', 'spatiotemporal').save(
        fs_layer_name)

    # 4 calculate area for difference area
    difference_layer_area = geoanalytics.calculate_field(difference_layer_proj, field_name="diff_area",
                                                         data_type="Double",
                                                         expression="Area($feature)")

    # 5 Aggreate level 1
    aggr_table = geoanalytics.summarize_attributes(difference_layer_area, [contrast_field_name, overlay_field_name],
                                                   summary_fields=[
                                                       {'onStatisticField': 'diff_area', 'statisticType': 'SUM'}])

    # 6 generate pivot table
    pre_area = aggr_table.groupBy(contrast_field_name).sum('SUM_diff_area').collect()

    current_area = aggr_table.groupBy(overlay_field_name).sum('SUM_diff_area').collect()

    diff_area = {}

    for srow in current_area:
        sd_dlmc = srow[overlay_field_name]
        sd_area = srow['sum(SUM_diff_area)']
        for erow in pre_area:
            ed_dlmc = erow[contrast_field_name]
            if ed_dlmc == sd_dlmc:
                diff_area[sd_dlmc] = sd_area - erow["sum(SUM_diff_area)"]

    fs_table_name = fs_layer_name + "_vartable"
    pd_table = aggr_table.toPandas()

    df_pivot = pd.pivot_table(pd_table, index=contrast_field_name, columns=overlay_field_name, values='SUM_diff_area')

    for key in diff_area.keys():
        for i in range(len(df_pivot) - 1):
            if key == df_pivot.index[i]:
                df_pivot[key][i] = diff_area[key]

    # 7 export result
    export_path = os.path.join(temp_path, fs_table_name + '.csv')

    print("Table export path:", export_path)
    df_pivot.to_csv(export_path, encoding='utf-8')

    # 8 publish service
    statistic_result = spark.read.csv(export_path, header='true', encoding='utf-8')

    statistic_result.write.format('webgis').option('dataStore', 'spatiotemporal').save(fs_table_name)