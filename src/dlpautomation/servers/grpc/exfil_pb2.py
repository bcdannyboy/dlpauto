# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: exfil.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x65xfil.proto\"\x1c\n\x0c\x45xfilRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1d\n\nExfilReply\x12\x0f\n\x07message\x18\x01 \x01(\t2=\n\x0c\x45xfilService\x12-\n\rSendExfilData\x12\r.ExfilRequest\x1a\x0b.ExfilReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exfil_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_EXFILREQUEST']._serialized_start=15
  _globals['_EXFILREQUEST']._serialized_end=43
  _globals['_EXFILREPLY']._serialized_start=45
  _globals['_EXFILREPLY']._serialized_end=74
  _globals['_EXFILSERVICE']._serialized_start=76
  _globals['_EXFILSERVICE']._serialized_end=137
# @@protoc_insertion_point(module_scope)