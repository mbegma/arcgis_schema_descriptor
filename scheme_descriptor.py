# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: arcgis_schema_descriptor
# Name: scheme_descriptor
# Author: mbegma
# Create data: 13.04.2020
# Description: 
# Copyright:
# -----------------------------------------------------
import arcpy
from tool.descriptor import Descriptor


def main():
    arcpy.AddMessage(u'Starting main method')
    # DEBUG
    workspace = ur'C:\Work\2020\ПКК\CS\RAYON_CS.gdb'
    output_place = ur'C:\Work\2020\ПКК'
    output_format = u'CSV'  # 'CSV'
    # output_format = 'JSON'
    sort_fields = False
    cl = Descriptor(workspace=workspace, output_place=output_place,
                    output_format=output_format, sort_fields=sort_fields)
    try:
        cl.create()
        cl.execute()
        arcpy.AddMessage(u'created file: {0}'.format(cl.output_file))
    except Exception as err:
        arcpy.AddMessage(str(err.args))
    finally:
        arcpy.AddMessage(u'finish')


if __name__ == "__main__":
    main()
