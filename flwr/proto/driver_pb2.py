# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/driver.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flwr.proto import node_pb2 as flwr_dot_proto_dot_node__pb2
from flwr.proto import task_pb2 as flwr_dot_proto_dot_task__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x66lwr/proto/driver.proto\x12\nflwr.proto\x1a\x15\x66lwr/proto/node.proto\x1a\x15\x66lwr/proto/task.proto\"\x11\n\x0fGetNodesRequest\"$\n\x10GetNodesResponse\x12\x10\n\x08node_ids\x18\x01 \x03(\x04\"@\n\x12PushTaskInsRequest\x12*\n\rtask_ins_list\x18\x01 \x03(\x0b\x32\x13.flwr.proto.TaskIns\"\'\n\x13PushTaskInsResponse\x12\x10\n\x08task_ids\x18\x02 \x03(\t\"F\n\x12PullTaskResRequest\x12\x1e\n\x04node\x18\x01 \x01(\x0b\x32\x10.flwr.proto.Node\x12\x10\n\x08task_ids\x18\x02 \x03(\t\"A\n\x13PullTaskResResponse\x12*\n\rtask_res_list\x18\x01 \x03(\x0b\x32\x13.flwr.proto.TaskRes2\xf5\x01\n\x06\x44river\x12G\n\x08GetNodes\x12\x1b.flwr.proto.GetNodesRequest\x1a\x1c.flwr.proto.GetNodesResponse\"\x00\x12P\n\x0bPushTaskIns\x12\x1e.flwr.proto.PushTaskInsRequest\x1a\x1f.flwr.proto.PushTaskInsResponse\"\x00\x12P\n\x0bPullTaskRes\x12\x1e.flwr.proto.PullTaskResRequest\x1a\x1f.flwr.proto.PullTaskResResponse\"\x00\x62\x06proto3')



_GETNODESREQUEST = DESCRIPTOR.message_types_by_name['GetNodesRequest']
_GETNODESRESPONSE = DESCRIPTOR.message_types_by_name['GetNodesResponse']
_PUSHTASKINSREQUEST = DESCRIPTOR.message_types_by_name['PushTaskInsRequest']
_PUSHTASKINSRESPONSE = DESCRIPTOR.message_types_by_name['PushTaskInsResponse']
_PULLTASKRESREQUEST = DESCRIPTOR.message_types_by_name['PullTaskResRequest']
_PULLTASKRESRESPONSE = DESCRIPTOR.message_types_by_name['PullTaskResResponse']
GetNodesRequest = _reflection.GeneratedProtocolMessageType('GetNodesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETNODESREQUEST,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.GetNodesRequest)
  })
_sym_db.RegisterMessage(GetNodesRequest)

GetNodesResponse = _reflection.GeneratedProtocolMessageType('GetNodesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETNODESRESPONSE,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.GetNodesResponse)
  })
_sym_db.RegisterMessage(GetNodesResponse)

PushTaskInsRequest = _reflection.GeneratedProtocolMessageType('PushTaskInsRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUSHTASKINSREQUEST,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.PushTaskInsRequest)
  })
_sym_db.RegisterMessage(PushTaskInsRequest)

PushTaskInsResponse = _reflection.GeneratedProtocolMessageType('PushTaskInsResponse', (_message.Message,), {
  'DESCRIPTOR' : _PUSHTASKINSRESPONSE,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.PushTaskInsResponse)
  })
_sym_db.RegisterMessage(PushTaskInsResponse)

PullTaskResRequest = _reflection.GeneratedProtocolMessageType('PullTaskResRequest', (_message.Message,), {
  'DESCRIPTOR' : _PULLTASKRESREQUEST,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.PullTaskResRequest)
  })
_sym_db.RegisterMessage(PullTaskResRequest)

PullTaskResResponse = _reflection.GeneratedProtocolMessageType('PullTaskResResponse', (_message.Message,), {
  'DESCRIPTOR' : _PULLTASKRESRESPONSE,
  '__module__' : 'flwr.proto.driver_pb2'
  # @@protoc_insertion_point(class_scope:flwr.proto.PullTaskResResponse)
  })
_sym_db.RegisterMessage(PullTaskResResponse)

_DRIVER = DESCRIPTOR.services_by_name['Driver']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETNODESREQUEST._serialized_start=85
  _GETNODESREQUEST._serialized_end=102
  _GETNODESRESPONSE._serialized_start=104
  _GETNODESRESPONSE._serialized_end=140
  _PUSHTASKINSREQUEST._serialized_start=142
  _PUSHTASKINSREQUEST._serialized_end=206
  _PUSHTASKINSRESPONSE._serialized_start=208
  _PUSHTASKINSRESPONSE._serialized_end=247
  _PULLTASKRESREQUEST._serialized_start=249
  _PULLTASKRESREQUEST._serialized_end=319
  _PULLTASKRESRESPONSE._serialized_start=321
  _PULLTASKRESRESPONSE._serialized_end=386
  _DRIVER._serialized_start=389
  _DRIVER._serialized_end=634
# @@protoc_insertion_point(module_scope)