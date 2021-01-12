## arcgis_schema_descriptor
#### A tool for obtaining the data structure of the ArcGIS format (sde, *.gdb) in a simple readable form (csv, json)  
input parameters:  
workspace - ArcGIS data, like gdb or sde  
output_place - directory in which the result is formed  
output_format - string value: 'CSV' or 'JSON'  
sort_fields - flag indicating whether to sort the output: True | False  
   
**model_descr_tool.pyt** - ArcGIS python toolbox with **SchemaDescriptor** tools