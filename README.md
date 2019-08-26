# 这个工程下包含了适用于被ArcGIS GeoAnalytics Server Run Python Script接口调用的分析模型。

## 内容说明：
    - doc文件夹下包含了针对各个模型的使用文档，包括模型中工具的输入参数说明，以及代码调用样例
    - models文件夹下包含了具体的模型脚本


## 部署说明：
    这些模型是专为方便Run Python Script接口调用而设计的，在使用前需要预先将其部署到GA 依赖的python环境下
    1， 通过GA Server 的admin接口查询python库的位置
    以管理员身份登陆GA server admin：https://<full hostname>/gaserver/admin/system/properties
    查询'pysparkPython'属性- {"pysparkPython":"/usr/local/anaconda3/envs/arcgis/bin/python“}，

    2， 部署脚本
    拷贝models 目录下的脚本，部署到site-packages目录下，例如：/usr/local/anaconda3/envs/arcgis/lib/python3.6/site-packages/
    *注意授予arcgis用户拥有对脚本的执行和读权限。

## 模型清单：
    - landVarianceAnalysisModel: 地类差异分析模型。在国土资源土地利用大数据分析中，通过叠加分析多年数据，实现任意范围，任意多边形内地类变化识别、地类差异面积统计以及地类变化流向分析。
    - landClipStatisticModel：地类空间统计模型。按照指定范围或多边形，汇总统计范围内所有相关数据的面积、地类等信息，并输出裁切好的矢量图层和属性统计图表。
