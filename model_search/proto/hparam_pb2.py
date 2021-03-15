# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: model_search/proto/hparam.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='model_search/proto/hparam.proto',
  package='model_search',
  syntax='proto3',
  serialized_options=b'\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1fmodel_search/proto/hparam.proto\x12\x0cmodel_search\"\xe2\x04\n\tHParamDef\x12\x33\n\x06hparam\x18\x01 \x03(\x0b\x32#.model_search.HParamDef.HparamEntry\x1a\x1a\n\tBytesList\x12\r\n\x05value\x18\x01 \x03(\x0c\x1a\x1e\n\tFloatList\x12\x11\n\x05value\x18\x01 \x03(\x02\x42\x02\x10\x01\x1a\x1e\n\tInt64List\x12\x11\n\x05value\x18\x01 \x03(\x03\x42\x02\x10\x01\x1a\x1d\n\x08\x42oolList\x12\x11\n\x05value\x18\x01 \x03(\x08\x42\x02\x10\x01\x1a\xd1\x02\n\nHParamType\x12\x15\n\x0bint64_value\x18\x01 \x01(\x03H\x00\x12\x15\n\x0b\x66loat_value\x18\x02 \x01(\x02H\x00\x12\x15\n\x0b\x62ytes_value\x18\x03 \x01(\x0cH\x00\x12\x14\n\nbool_value\x18\x07 \x01(\x08H\x00\x12\x37\n\nint64_list\x18\x04 \x01(\x0b\x32!.model_search.HParamDef.Int64ListH\x00\x12\x37\n\nfloat_list\x18\x05 \x01(\x0b\x32!.model_search.HParamDef.FloatListH\x00\x12\x37\n\nbytes_list\x18\x06 \x01(\x0b\x32!.model_search.HParamDef.BytesListH\x00\x12\x35\n\tbool_list\x18\x08 \x01(\x0b\x32 .model_search.HParamDef.BoolListH\x00\x42\x06\n\x04kind\x1aQ\n\x0bHparamEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".model_search.HParamDef.HParamType:\x02\x38\x01\x42\x03\xf8\x01\x01\x62\x06proto3'
)




_HPARAMDEF_BYTESLIST = _descriptor.Descriptor(
  name='BytesList',
  full_name='model_search.HParamDef.BytesList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='model_search.HParamDef.BytesList.value', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=116,
  serialized_end=142,
)

_HPARAMDEF_FLOATLIST = _descriptor.Descriptor(
  name='FloatList',
  full_name='model_search.HParamDef.FloatList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='model_search.HParamDef.FloatList.value', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=144,
  serialized_end=174,
)

_HPARAMDEF_INT64LIST = _descriptor.Descriptor(
  name='Int64List',
  full_name='model_search.HParamDef.Int64List',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='model_search.HParamDef.Int64List.value', index=0,
      number=1, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=176,
  serialized_end=206,
)

_HPARAMDEF_BOOLLIST = _descriptor.Descriptor(
  name='BoolList',
  full_name='model_search.HParamDef.BoolList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='model_search.HParamDef.BoolList.value', index=0,
      number=1, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=208,
  serialized_end=237,
)

_HPARAMDEF_HPARAMTYPE = _descriptor.Descriptor(
  name='HParamType',
  full_name='model_search.HParamDef.HParamType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='int64_value', full_name='model_search.HParamDef.HParamType.int64_value', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='float_value', full_name='model_search.HParamDef.HParamType.float_value', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bytes_value', full_name='model_search.HParamDef.HParamType.bytes_value', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='model_search.HParamDef.HParamType.bool_value', index=3,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='int64_list', full_name='model_search.HParamDef.HParamType.int64_list', index=4,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='float_list', full_name='model_search.HParamDef.HParamType.float_list', index=5,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bytes_list', full_name='model_search.HParamDef.HParamType.bytes_list', index=6,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bool_list', full_name='model_search.HParamDef.HParamType.bool_list', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='kind', full_name='model_search.HParamDef.HParamType.kind',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=240,
  serialized_end=577,
)

_HPARAMDEF_HPARAMENTRY = _descriptor.Descriptor(
  name='HparamEntry',
  full_name='model_search.HParamDef.HparamEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='model_search.HParamDef.HparamEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='model_search.HParamDef.HparamEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=579,
  serialized_end=660,
)

_HPARAMDEF = _descriptor.Descriptor(
  name='HParamDef',
  full_name='model_search.HParamDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hparam', full_name='model_search.HParamDef.hparam', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_HPARAMDEF_BYTESLIST, _HPARAMDEF_FLOATLIST, _HPARAMDEF_INT64LIST, _HPARAMDEF_BOOLLIST, _HPARAMDEF_HPARAMTYPE, _HPARAMDEF_HPARAMENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=660,
)

_HPARAMDEF_BYTESLIST.containing_type = _HPARAMDEF
_HPARAMDEF_FLOATLIST.containing_type = _HPARAMDEF
_HPARAMDEF_INT64LIST.containing_type = _HPARAMDEF
_HPARAMDEF_BOOLLIST.containing_type = _HPARAMDEF
_HPARAMDEF_HPARAMTYPE.fields_by_name['int64_list'].message_type = _HPARAMDEF_INT64LIST
_HPARAMDEF_HPARAMTYPE.fields_by_name['float_list'].message_type = _HPARAMDEF_FLOATLIST
_HPARAMDEF_HPARAMTYPE.fields_by_name['bytes_list'].message_type = _HPARAMDEF_BYTESLIST
_HPARAMDEF_HPARAMTYPE.fields_by_name['bool_list'].message_type = _HPARAMDEF_BOOLLIST
_HPARAMDEF_HPARAMTYPE.containing_type = _HPARAMDEF
_HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind'].fields.append(
  _HPARAMDEF_HPARAMTYPE.fields_by_name['int64_value'])
_HPARAMDEF_HPARAMTYPE.fields_by_name['int64_value'].containing_oneof = _HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind']
_HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind'].fields.append(
  _HPARAMDEF_HPARAMTYPE.fields_by_name['float_value'])
_HPARAMDEF_HPARAMTYPE.fields_by_name['float_value'].containing_oneof = _HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind']
_HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind'].fields.append(
  _HPARAMDEF_HPARAMTYPE.fields_by_name['bytes_value'])
_HPARAMDEF_HPARAMTYPE.fields_by_name['bytes_value'].containing_oneof = _HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind']
_HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind'].fields.append(
  _HPARAMDEF_HPARAMTYPE.fields_by_name['bool_value'])
_HPARAMDEF_HPARAMTYPE.fields_by_name['bool_value'].containing_oneof = _HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind']
_HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind'].fields.append(
  _HPARAMDEF_HPARAMTYPE.fields_by_name['int64_list'])
_HPARAMDEF_HPARAMTYPE.fields_by_name['int64_list'].containing_oneof = _HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind']
_HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind'].fields.append(
  _HPARAMDEF_HPARAMTYPE.fields_by_name['float_list'])
_HPARAMDEF_HPARAMTYPE.fields_by_name['float_list'].containing_oneof = _HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind']
_HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind'].fields.append(
  _HPARAMDEF_HPARAMTYPE.fields_by_name['bytes_list'])
_HPARAMDEF_HPARAMTYPE.fields_by_name['bytes_list'].containing_oneof = _HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind']
_HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind'].fields.append(
  _HPARAMDEF_HPARAMTYPE.fields_by_name['bool_list'])
_HPARAMDEF_HPARAMTYPE.fields_by_name['bool_list'].containing_oneof = _HPARAMDEF_HPARAMTYPE.oneofs_by_name['kind']
_HPARAMDEF_HPARAMENTRY.fields_by_name['value'].message_type = _HPARAMDEF_HPARAMTYPE
_HPARAMDEF_HPARAMENTRY.containing_type = _HPARAMDEF
_HPARAMDEF.fields_by_name['hparam'].message_type = _HPARAMDEF_HPARAMENTRY
DESCRIPTOR.message_types_by_name['HParamDef'] = _HPARAMDEF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HParamDef = _reflection.GeneratedProtocolMessageType('HParamDef', (_message.Message,), {

  'BytesList' : _reflection.GeneratedProtocolMessageType('BytesList', (_message.Message,), {
    'DESCRIPTOR' : _HPARAMDEF_BYTESLIST,
    '__module__' : 'model_search.proto.hparam_pb2'
    # @@protoc_insertion_point(class_scope:model_search.HParamDef.BytesList)
    })
  ,

  'FloatList' : _reflection.GeneratedProtocolMessageType('FloatList', (_message.Message,), {
    'DESCRIPTOR' : _HPARAMDEF_FLOATLIST,
    '__module__' : 'model_search.proto.hparam_pb2'
    # @@protoc_insertion_point(class_scope:model_search.HParamDef.FloatList)
    })
  ,

  'Int64List' : _reflection.GeneratedProtocolMessageType('Int64List', (_message.Message,), {
    'DESCRIPTOR' : _HPARAMDEF_INT64LIST,
    '__module__' : 'model_search.proto.hparam_pb2'
    # @@protoc_insertion_point(class_scope:model_search.HParamDef.Int64List)
    })
  ,

  'BoolList' : _reflection.GeneratedProtocolMessageType('BoolList', (_message.Message,), {
    'DESCRIPTOR' : _HPARAMDEF_BOOLLIST,
    '__module__' : 'model_search.proto.hparam_pb2'
    # @@protoc_insertion_point(class_scope:model_search.HParamDef.BoolList)
    })
  ,

  'HParamType' : _reflection.GeneratedProtocolMessageType('HParamType', (_message.Message,), {
    'DESCRIPTOR' : _HPARAMDEF_HPARAMTYPE,
    '__module__' : 'model_search.proto.hparam_pb2'
    # @@protoc_insertion_point(class_scope:model_search.HParamDef.HParamType)
    })
  ,

  'HparamEntry' : _reflection.GeneratedProtocolMessageType('HparamEntry', (_message.Message,), {
    'DESCRIPTOR' : _HPARAMDEF_HPARAMENTRY,
    '__module__' : 'model_search.proto.hparam_pb2'
    # @@protoc_insertion_point(class_scope:model_search.HParamDef.HparamEntry)
    })
  ,
  'DESCRIPTOR' : _HPARAMDEF,
  '__module__' : 'model_search.proto.hparam_pb2'
  # @@protoc_insertion_point(class_scope:model_search.HParamDef)
  })
_sym_db.RegisterMessage(HParamDef)
_sym_db.RegisterMessage(HParamDef.BytesList)
_sym_db.RegisterMessage(HParamDef.FloatList)
_sym_db.RegisterMessage(HParamDef.Int64List)
_sym_db.RegisterMessage(HParamDef.BoolList)
_sym_db.RegisterMessage(HParamDef.HParamType)
_sym_db.RegisterMessage(HParamDef.HparamEntry)


DESCRIPTOR._options = None
_HPARAMDEF_FLOATLIST.fields_by_name['value']._options = None
_HPARAMDEF_INT64LIST.fields_by_name['value']._options = None
_HPARAMDEF_BOOLLIST.fields_by_name['value']._options = None
_HPARAMDEF_HPARAMENTRY._options = None
# @@protoc_insertion_point(module_scope)