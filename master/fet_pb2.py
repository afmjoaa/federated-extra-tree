# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fet.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tfet.proto\x12\x12\x63om.groupseven.fet\"<\n BroadcastRandomFeatureSetRequest\x12\x18\n\x10selectedFeatures\x18\x01 \x03(\x05\"$\n\x10ReceivedResponse\x12\x10\n\x08response\x18\x01 \x01(\x08\"I\n$GetRandomSplitValueFromClientRequest\x12\x0f\n\x07\x66\x65\x61ture\x18\x01 \x01(\x05\x12\x10\n\x08\x63lientId\x18\x02 \x01(\x05\"M\n%GetRandomSplitValueFromClientResponse\x12\x10\n\x08\x63lientId\x18\x01 \x01(\x05\x12\x12\n\nsplitValue\x18\x02 \x01(\x01\"]\n$GetAggregatedValuesFromClientRequest\x12\x0f\n\x07\x66\x65\x61ture\x18\x01 \x01(\x05\x12\x10\n\x08\x63lientId\x18\x02 \x01(\x05\x12\x12\n\nsplitValue\x18\x03 \x01(\x01\"\xac\x01\n%GetAggregatedValuesFromClientResponse\x12@\n\x13\x61ggregatedValueLeft\x18\x01 \x01(\x0b\x32#.com.groupseven.fet.AggregatedValue\x12\x41\n\x14\x61ggregatedValueRight\x18\x02 \x01(\x0b\x32#.com.groupseven.fet.AggregatedValue\"=\n\x0f\x41ggregatedValue\x12\x14\n\x0c\x61pprovedLoan\x18\x01 \x01(\x05\x12\x14\n\x0c\x64\x65\x63linedLoan\x18\x02 \x01(\x05\"P\n)BroadcastTreeNodesBasedOnBestSplitRequest\x12\x0f\n\x07\x66\x65\x61ture\x18\x01 \x01(\x05\x12\x12\n\nsplitValue\x18\x02 \x01(\x01\x32\xd9\x04\n MasterClientCommunicationService\x12w\n\x19\x42roadcastRandomFeatureSet\x12\x34.com.groupseven.fet.BroadcastRandomFeatureSetRequest\x1a$.com.groupseven.fet.ReceivedResponse\x12\x96\x01\n\x1dGetRandomSplitValueFromClient\x12\x38.com.groupseven.fet.GetRandomSplitValueFromClientRequest\x1a\x39.com.groupseven.fet.GetRandomSplitValueFromClientResponse(\x01\x12\x96\x01\n\x1dGetAggregatedValuesFromClient\x12\x38.com.groupseven.fet.GetAggregatedValuesFromClientRequest\x1a\x39.com.groupseven.fet.GetAggregatedValuesFromClientResponse(\x01\x12\x89\x01\n\"BroadcastTreeNodesBasedOnBestSplit\x12=.com.groupseven.fet.BroadcastTreeNodesBasedOnBestSplitRequest\x1a$.com.groupseven.fet.ReceivedResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fet_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BROADCASTRANDOMFEATURESETREQUEST._serialized_start=33
  _BROADCASTRANDOMFEATURESETREQUEST._serialized_end=93
  _RECEIVEDRESPONSE._serialized_start=95
  _RECEIVEDRESPONSE._serialized_end=131
  _GETRANDOMSPLITVALUEFROMCLIENTREQUEST._serialized_start=133
  _GETRANDOMSPLITVALUEFROMCLIENTREQUEST._serialized_end=206
  _GETRANDOMSPLITVALUEFROMCLIENTRESPONSE._serialized_start=208
  _GETRANDOMSPLITVALUEFROMCLIENTRESPONSE._serialized_end=285
  _GETAGGREGATEDVALUESFROMCLIENTREQUEST._serialized_start=287
  _GETAGGREGATEDVALUESFROMCLIENTREQUEST._serialized_end=380
  _GETAGGREGATEDVALUESFROMCLIENTRESPONSE._serialized_start=383
  _GETAGGREGATEDVALUESFROMCLIENTRESPONSE._serialized_end=555
  _AGGREGATEDVALUE._serialized_start=557
  _AGGREGATEDVALUE._serialized_end=618
  _BROADCASTTREENODESBASEDONBESTSPLITREQUEST._serialized_start=620
  _BROADCASTTREENODESBASEDONBESTSPLITREQUEST._serialized_end=700
  _MASTERCLIENTCOMMUNICATIONSERVICE._serialized_start=703
  _MASTERCLIENTCOMMUNICATIONSERVICE._serialized_end=1304
# @@protoc_insertion_point(module_scope)
