# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: arcgis_schema_descriptor
# Name: descriptor
# Author: mbegma
# Create data: 13.04.2020
# Description: 
# Copyright: (c) Дата+, 2020
# -----------------------------------------------------
import arcpy
import json
from datetime import datetime
from tool.const import OUTPUT_FORMAT, FC_INFO, FIELD_INFO, TABLE, FC, EXCLUSION_FIELDS_LIST, CSV_DELIMITER
from os import sep, path, makedirs
from io import open


def get_leveled_text_line(text, level=0):
    """
    Функция форматирует текст отступами в 2 пробела
    :param text:
    :param level:
    :return:
    """
    return u'{0}{1}'.format(u' ' * (level * 2), text)


def add_message(_text, _type=0, _level=0):
    is_process = True
    if is_process:
        type_msg = ['INFO', 'ERROR', 'WARNING']
        msg = u'{0} | {1} > {2}'.format(type_msg[_type],
                                        datetime.utcnow(),
                                        get_leveled_text_line(_text, _level))
        arcpy.AddMessage(msg)


def get_fields_data(fields_list, use_exclusion_fields_list=True):
    ret = {}
    for field in fields_list:
        fn = field.name
        f = {
            FIELD_INFO[0]: field.aliasName,
            FIELD_INFO[1]: field.type,
            FIELD_INFO[2]: field.length,
            FIELD_INFO[3]: field.domain
        }
        if use_exclusion_fields_list:
            if not fn.upper() in EXCLUSION_FIELDS_LIST:
                ret[fn] = f
        else:
            ret[fn] = f
    return ret


class Descriptor:
    def __init__(self, workspace, output_place, output_format='CSV', sort_fields=False):
        self.features_data_dict = {}
        self.workspace = workspace
        self.output_place = output_place
        self.output_format = output_format
        self.sort_fields = sort_fields
        self.output_file = None

    def create(self):
        arcpy.env.overwriteOutput = True
        if self.output_format not in OUTPUT_FORMAT:
            msg = u'Output format is not correct'
            # self.res_error_code = 2
            # self.res_error_message_list.append(msg)
            add_message(msg, _type=1)
            return

        if self.workspace is None or self.workspace == '':
            msg = u'Workspace is not define'
            # self.res_error_message_list.append(msg)
            # self.res_error_code = 3
            add_message(msg, _type=1)
            return

        if not arcpy.Exists(self.workspace):
            msg = u'Workspace is not present'
            # self.res_error_message_list.append(msg)
            # self.res_error_code = 4
            add_message(msg, _type=1)
            return
        else:
            arcpy.env.workspace = self.workspace

        if self.output_place is None or self.output_place == '':
            msg = u'Output place is not define'
            # self.res_error_message_list.append(msg)
            # self.res_error_code = 5
            add_message(msg, _type=1)
            return

        if not path.exists(self.output_place):
            makedirs(self.output_place)
            msg = u'Output place is not exist. Create it'
            # self.res_error_message_list.append(msg)
            add_message(msg, _type=2)

    def __get_data_about_feature_class__(self):
        fc_list = arcpy.ListFeatureClasses()
        for fc in fc_list:
            add_message(u'get info about: {0}'.format(fc))
            fc_name = u'{0}{1}{2}'.format(self.workspace, sep, fc)
            desc = arcpy.Describe(fc_name)
            if desc.dataType == FC:
                add_message(u'process Feature Classes')
                fields = arcpy.ListFields(fc_name)
                fields_names = get_fields_data(fields)
                d = {
                    FC_INFO[0]: desc.dataType,
                    FC_INFO[1]: desc.aliasName,
                    FC_INFO[2]: desc.shapeType,
                    FC_INFO[3]: fields_names
                }
                self.features_data_dict[desc.name] = d
            else:
                add_message(u'Unknown data type: {0}'.format(desc.dataType))

    def __get_data_about_table__(self):
        table_list = arcpy.ListTables()
        for table in table_list:
            add_message(u'get info about: {0}'.format(table))
            table_name = u'{0}{1}{2}'.format(self.workspace, sep, table)
            desc = arcpy.Describe(table_name)
            if desc.dataType == TABLE:
                fields = arcpy.ListFields(table_name)
                fields_names = get_fields_data(fields)
                d = {
                    FC_INFO[0]: desc.dataType,
                    FC_INFO[1]: desc.aliasName,
                    FC_INFO[2]: u'Table',
                    FC_INFO[3]: fields_names
                }
                self.features_data_dict[desc.name] = d
            else:
                add_message(u'Unknown data type: {0}'.format(desc.dataType))

    def write_to_csv(self):
        ret = None
        filename = u'{0}{1}{2}_csv.txt'.format(self.output_place, sep,
                                               self.workspace.rpartition(sep)[2])
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for item in self.features_data_dict:
                    current_item = self.features_data_dict[item]
                    caption = u'{0}: {1} (Alias: {2}; Type: {3})'.format(current_item[FC_INFO[0]],
                                                                         item,
                                                                         current_item[FC_INFO[1]],
                                                                         current_item[FC_INFO[2]])
                    current_fields_dict = current_item[FC_INFO[3]]
                    current_fields_keys = current_fields_dict.keys()

                    if self.sort_fields:
                        current_fields_keys = sorted(current_fields_keys)
                    f.write(u'{0}\n'.format(caption))
                    f.write(u'{0}\n'.format('Fields:'))
                    fields_caption = u'{0}{1}{2}{1}{3}{1}{4}{1}{5}'.format(u'field_name',
                                                                           CSV_DELIMITER,
                                                                           FIELD_INFO[0],
                                                                           FIELD_INFO[1],
                                                                           FIELD_INFO[2],
                                                                           FIELD_INFO[3])
                    f.write(u'{0}\n'.format(fields_caption))
                    for field in current_fields_keys:
                        fld = current_fields_dict[field]
                        line = u'{0}{1}{2}{1}{3}{1}{4}{1}{5}'.format(field,
                                                                     CSV_DELIMITER,
                                                                     fld[FIELD_INFO[0]],
                                                                     fld[FIELD_INFO[1]],
                                                                     fld[FIELD_INFO[2]],
                                                                     fld[FIELD_INFO[3]])
                        f.write(u'{0}\n'.format(line))
                    f.write(u'{0}\n'.format(''))
            ret = filename

        except Exception as err:
            ret = None
            raise err
        finally:
            return ret

    def write_to_json(self):
        ret = None
        filename = u'{0}{1}{2}_json.txt'.format(self.output_place, sep,
                                                self.workspace.rpartition(sep)[2])
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.features_data_dict, ensure_ascii=False, sort_keys=self.sort_fields, indent=1))
            ret = filename
        except Exception as err:
            ret = None
            raise err
        finally:
            return ret

    def execute(self):
        add_message(u'Executing ...')
        try:
            add_message(u'process with Feature Classes')
            self.__get_data_about_feature_class__()
            add_message(u'process finish')

            add_message(u'process with Tables')
            self.__get_data_about_table__()
            add_message(u'process finish')

            if len(self.features_data_dict) == 0:
                add_message(u'No data')
                return

            add_message(u'create output file ({0})'.format(self.output_format))

            if self.output_format == OUTPUT_FORMAT[0]:
                self.output_file = self.write_to_csv()
            elif self.output_format == OUTPUT_FORMAT[1]:
                self.output_file = self.write_to_json()
            else:
                add_message(u'Unknown format')

            add_message(u'output file created')

        except Exception as err:
            add_message(str(err.args), _type=1)
            raise err
        finally:
            return self.output_file
