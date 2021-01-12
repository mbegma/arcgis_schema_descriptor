# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: arcgis_schema_descriptor
# Name: model_descr_tool
# Filename: model_descr_tool.pyt
# Author: mbegma
# Create data: 12.01.2021
# Description: 
# Copyright: (c) Дата+, 2021
# -----------------------------------------------------
import arcpy
from tool.descriptor import Descriptor


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Model Describe Tool"
        self.alias = "Model Describe Tool"
        # List of tool classes associated with this toolbox        
        self.tools = [SchemaDescriptor]


class SchemaDescriptor(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "SchemaDescriptor"
        self.description = "Data model Schema Descriptor"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        workspace = arcpy.Parameter(
            displayName="Workspace",
            name="workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        output_place = arcpy.Parameter(
            displayName="Output folder",
            name="output_place",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        output_format = arcpy.Parameter(
            displayName="Output format",
            name="output_format",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        output_format.filter.type = "ValueList"
        output_format.filter.list = ['CSV', 'JSON']
        output_format.value = 'CSV'

        sort_fields = arcpy.Parameter(
            displayName="Sort fields",
            name="sort_fields",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")
        sort_fields.filter.type = "ValueList"
        sort_fields.filter.list = [True, False]
        sort_fields.value = False

        result_file = arcpy.Parameter(
            displayName="Result File",
            name="result_file",
            datatype="DEFile",
            parameterType="Derived",
            direction="Output")

        params = [workspace, output_place, output_format, sort_fields, result_file]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal        
        validation is performed.  This method is called whenever a parameter        
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool        
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        res_file = None
        arcpy.AddMessage(u'Start execute script')
        workspace = parameters[0].valueAsText
        # workspace = unicode(parameters[0].valueAsText, 'utf-8')
        arcpy.AddMessage(u'workspace: {0}({1})'.format(workspace, type(workspace)))

        output_place = parameters[1].valueAsText
        arcpy.AddMessage(u'output_place: {0}({1})'.format(output_place, type(output_place)))
        output_format = parameters[2].valueAsText
        arcpy.AddMessage(u'output_format: {0}({1})'.format(output_format, type(output_format)))
        sort_fields = parameters[3].value
        arcpy.AddMessage(u'sort_fields: {0}({1})'.format(sort_fields, type(sort_fields)))

        cl = Descriptor(workspace=workspace, output_place=output_place,
                        output_format=output_format, sort_fields=sort_fields)
        try:
            cl.create()
            cl.execute()
            res_file = cl.output_file
        except Exception as err:
            arcpy.AddMessage(str(err.args))
        finally:
            parameters[4].value = res_file
            arcpy.AddMessage(u'created file: {0}'.format(res_file))
            arcpy.AddMessage(u'Finish execute script')
        return
