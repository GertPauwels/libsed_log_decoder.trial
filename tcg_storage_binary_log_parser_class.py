# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class TcgStorageBinaryLogParserClass(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.opal_command = []
        i = 0
        while not self._io.is_eof():
            self.opal_command.append(TcgStorageBinaryLogParserClass.OpalCommandType(self._io, self, self._root))
            i += 1


    class FeatureDescriptorBlockSidAuthenticationType(KaitaiStruct):
        """Feature Code = 0x0402."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.byte_1 = self._io.read_u1()
            self.byte_2 = self._io.read_u1()
            self.reserved = self._io.read_bytes(10)

        @property
        def sid_authentication_blocked_state(self):
            if hasattr(self, '_m_sid_authentication_blocked_state'):
                return self._m_sid_authentication_blocked_state

            self._m_sid_authentication_blocked_state = ((self.byte_1 & 2) >> 1)
            return getattr(self, '_m_sid_authentication_blocked_state', None)

        @property
        def hardware_reset(self):
            if hasattr(self, '_m_hardware_reset'):
                return self._m_hardware_reset

            self._m_hardware_reset = ((self.byte_2 & 1) >> 0)
            return getattr(self, '_m_hardware_reset', None)

        @property
        def locking_sp_freeze_lock_state(self):
            if hasattr(self, '_m_locking_sp_freeze_lock_state'):
                return self._m_locking_sp_freeze_lock_state

            self._m_locking_sp_freeze_lock_state = ((self.byte_1 & 8) >> 3)
            return getattr(self, '_m_locking_sp_freeze_lock_state', None)

        @property
        def locking_sp_freeze_lock_supported(self):
            if hasattr(self, '_m_locking_sp_freeze_lock_supported'):
                return self._m_locking_sp_freeze_lock_supported

            self._m_locking_sp_freeze_lock_supported = ((self.byte_1 & 4) >> 2)
            return getattr(self, '_m_locking_sp_freeze_lock_supported', None)

        @property
        def sid_value_state(self):
            if hasattr(self, '_m_sid_value_state'):
                return self._m_sid_value_state

            self._m_sid_value_state = ((self.byte_1 & 1) >> 0)
            return getattr(self, '_m_sid_value_state', None)


    class FeatureDescriptorOpalSscV1Type(KaitaiStruct):
        """Feature Code = 0x0200."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.base_comid = self._io.read_u2be()
            self.number_of_comids = self._io.read_u2be()
            self.byte_5 = self._io.read_u1()

        @property
        def range_crossing_behavior(self):
            if hasattr(self, '_m_range_crossing_behavior'):
                return self._m_range_crossing_behavior

            self._m_range_crossing_behavior = ((self.byte_5 & 1) >> 0)
            return getattr(self, '_m_range_crossing_behavior', None)


    class FeatureDescriptorOpalSscV2Type(KaitaiStruct):
        """Feature Code = 0x0203."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.base_comid = self._io.read_u2be()
            self.number_of_comids = self._io.read_u2be()
            self.byte_5 = self._io.read_u1()
            self.number_of_locking_sp_admin_authorities_supported = self._io.read_u2be()
            self.number_of_locking_sp_user_authorities_supported = self._io.read_u2be()
            self.initial_c_pin_sid_pin_indicator = self._io.read_u1()
            self.behavior_of_c_pin_sid_pin_upon_tper_revert = self._io.read_u1()
            self.reserved_for_future_common_ssc_parameters = self._io.read_bytes(5)

        @property
        def range_crossing_behavior(self):
            if hasattr(self, '_m_range_crossing_behavior'):
                return self._m_range_crossing_behavior

            self._m_range_crossing_behavior = ((self.byte_5 & 1) >> 0)
            return getattr(self, '_m_range_crossing_behavior', None)

        @property
        def minor_version(self):
            if hasattr(self, '_m_minor_version'):
                return self._m_minor_version

            self._m_minor_version = ((self._parent.byte_3 & 15) >> 0)
            return getattr(self, '_m_minor_version', None)


    class FeatureDescriptorListType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.feature_descriptor = []
            i = 0
            while not self._io.is_eof():
                self.feature_descriptor.append(TcgStorageBinaryLogParserClass.FeatureDescriptorType(self._io, self, self._root))
                i += 1



    class FeatureDescriptorDataRemovalMechanismType(KaitaiStruct):
        """Feature Code = 0x0404."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved_1 = self._io.read_u1()
            self.byte_2 = self._io.read_u1()
            self.supported_data_removal_mechanism = self._io.read_u1()
            self.byte_4 = self._io.read_u1()
            self.data_removal_time_for_supported_data_removal_mechanism_bit_0 = self._io.read_u2be()
            self.data_removal_time_for_supported_data_removal_mechanism_bit_1 = self._io.read_u2be()
            self.data_removal_time_for_supported_data_removal_mechanism_bit_2 = self._io.read_u2be()
            self.reserved_2 = self._io.read_u4be()
            self.data_removal_time_for_supported_data_removal_mechanism_bit_5 = self._io.read_u2be()
            self.reserved_for_future_supported_data_removal_mechanism_parameters = self._io.read_bytes(16)

        @property
        def data_removal_time_format_for_bit_1(self):
            if hasattr(self, '_m_data_removal_time_format_for_bit_1'):
                return self._m_data_removal_time_format_for_bit_1

            self._m_data_removal_time_format_for_bit_1 = ((self.byte_4 & 2) >> 1)
            return getattr(self, '_m_data_removal_time_format_for_bit_1', None)

        @property
        def data_removal_time_format_for_bit_0(self):
            if hasattr(self, '_m_data_removal_time_format_for_bit_0'):
                return self._m_data_removal_time_format_for_bit_0

            self._m_data_removal_time_format_for_bit_0 = ((self.byte_4 & 1) >> 0)
            return getattr(self, '_m_data_removal_time_format_for_bit_0', None)

        @property
        def data_removal_time_format_for_bit_2(self):
            if hasattr(self, '_m_data_removal_time_format_for_bit_2'):
                return self._m_data_removal_time_format_for_bit_2

            self._m_data_removal_time_format_for_bit_2 = ((self.byte_4 & 4) >> 2)
            return getattr(self, '_m_data_removal_time_format_for_bit_2', None)

        @property
        def data_removal_time_format_for_bit_5(self):
            if hasattr(self, '_m_data_removal_time_format_for_bit_5'):
                return self._m_data_removal_time_format_for_bit_5

            self._m_data_removal_time_format_for_bit_5 = ((self.byte_4 & 32) >> 5)
            return getattr(self, '_m_data_removal_time_format_for_bit_5', None)

        @property
        def data_removal_operation_interrupted(self):
            if hasattr(self, '_m_data_removal_operation_interrupted'):
                return self._m_data_removal_operation_interrupted

            self._m_data_removal_operation_interrupted = ((self.byte_2 & 2) >> 1)
            return getattr(self, '_m_data_removal_operation_interrupted', None)

        @property
        def data_removal_operation_processing(self):
            if hasattr(self, '_m_data_removal_operation_processing'):
                return self._m_data_removal_operation_processing

            self._m_data_removal_operation_processing = ((self.byte_2 & 1) >> 0)
            return getattr(self, '_m_data_removal_operation_processing', None)


    class FeatureDescriptorTperType(KaitaiStruct):
        """Feature Code = 0x0001
        page 52
        
        .. seealso::
           Source - https://trustedcomputinggroup.org/wp-content/uploads/TCG_Storage_Architecture_Core_Spec_v2.01_r1.00.pdf
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.byte_1 = self._io.read_u1()

        @property
        def ack_nak_supported(self):
            if hasattr(self, '_m_ack_nak_supported'):
                return self._m_ack_nak_supported

            self._m_ack_nak_supported = ((self.byte_1 & 4) >> 2)
            return getattr(self, '_m_ack_nak_supported', None)

        @property
        def streaming_supported(self):
            if hasattr(self, '_m_streaming_supported'):
                return self._m_streaming_supported

            self._m_streaming_supported = ((self.byte_1 & 16) >> 4)
            return getattr(self, '_m_streaming_supported', None)

        @property
        def comid_mgmt_supported(self):
            if hasattr(self, '_m_comid_mgmt_supported'):
                return self._m_comid_mgmt_supported

            self._m_comid_mgmt_supported = ((self.byte_1 & 64) >> 6)
            return getattr(self, '_m_comid_mgmt_supported', None)

        @property
        def async_supported(self):
            if hasattr(self, '_m_async_supported'):
                return self._m_async_supported

            self._m_async_supported = ((self.byte_1 & 2) >> 1)
            return getattr(self, '_m_async_supported', None)

        @property
        def buffer_mgmt_supported(self):
            if hasattr(self, '_m_buffer_mgmt_supported'):
                return self._m_buffer_mgmt_supported

            self._m_buffer_mgmt_supported = ((self.byte_1 & 8) >> 3)
            return getattr(self, '_m_buffer_mgmt_supported', None)

        @property
        def sync_supported(self):
            if hasattr(self, '_m_sync_supported'):
                return self._m_sync_supported

            self._m_sync_supported = ((self.byte_1 & 1) >> 0)
            return getattr(self, '_m_sync_supported', None)


    class FeatureDescriptorRubySscV1Type(KaitaiStruct):
        """Feature Code = 0x0304."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.base_comid = self._io.read_u2be()
            self.number_of_comids = self._io.read_u2be()
            self.byte_5 = self._io.read_u1()
            self.number_of_locking_sp_admin_authorities_supported = self._io.read_u2be()
            self.number_of_locking_sp_user_authorities_supported = self._io.read_u2be()
            self.initial_c_pin_sid_pin_indicator = self._io.read_u1()
            self.behavior_of_c_pin_sid_pin_upon_tper_revert = self._io.read_u1()
            self.reserved_for_future_common_ssc_parameters = self._io.read_bytes(5)

        @property
        def range_crossing_behavior(self):
            if hasattr(self, '_m_range_crossing_behavior'):
                return self._m_range_crossing_behavior

            self._m_range_crossing_behavior = ((self.byte_5 & 1) >> 0)
            return getattr(self, '_m_range_crossing_behavior', None)


    class PacketFormat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.session = self._io.read_u8be()
            self.seq_number = self._io.read_u4be()
            self.reserved = self._io.read_u2be()
            self.ack_type = self._io.read_u2be()
            self.acknowledgement = self._io.read_u4be()
            self.packet_format_length = self._io.read_u4be()
            self._raw_packet_format_payload = self._io.read_bytes(self.packet_format_length)
            _io__raw_packet_format_payload = KaitaiStream(BytesIO(self._raw_packet_format_payload))
            self.packet_format_payload = TcgStorageBinaryLogParserClass.DataSubPacketFormat(_io__raw_packet_format_payload, self, self._root)


    class OpalCommandType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.nvme_header = TcgStorageBinaryLogParserClass.NvmeHeaderType(self._io, self, self._root)
            _on = self.nvme_header.com_id
            if _on == 1:
                self.comid_packets = TcgStorageBinaryLogParserClass.Level0DiscoveryResponseData(self._io, self, self._root)
            elif _on == 2048:
                self.comid_packets = TcgStorageBinaryLogParserClass.ComPacketFormat(self._io, self, self._root)
            else:
                self.comid_packets = TcgStorageBinaryLogParserClass.ComPacketFormat(self._io, self, self._root)


    class CallTokenPayload(KaitaiStruct):

        class MethodUidEnum(Enum):
            properties = 65281
            start_session = 65282
            sync_session = 65283
            next = 25769803784
            getacl = 25769803789
            genkey = 25769803792
            revertsp = 25769803793
            get = 25769803798
            set = 25769803799
            authenticate = 25769803804
            revert = 25769804290
            activate = 25769804291
            random = 25769805313

        class InvokingUidEnum(Enum):
            session_manager_reserved = 255
            user1 = 38654902273
            user2 = 38654902274
            c_pin_admin1 = 47244705793
            c_pin_user1 = 47244836865
            c_pin_user2 = 47244836866
            locking_sp = 2220498092034
            locking_globalrange = 8804682956801
            locking_range1 = 8804683153409
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.token_header1 = self._io.read_u1()
            self.invoking_uid = KaitaiStream.resolve_enum(TcgStorageBinaryLogParserClass.CallTokenPayload.InvokingUidEnum, self._io.read_u8be())
            self.token_header2 = self._io.read_u1()
            self.method_uid = KaitaiStream.resolve_enum(TcgStorageBinaryLogParserClass.CallTokenPayload.MethodUidEnum, self._io.read_u8be())
            self.data = self._io.read_bytes((self._parent._parent.payload_length - 19))


    class NvmeHeaderType(KaitaiStruct):

        class NvmeCommandEnum(Enum):
            nvme_security_send = 129
            nvme_security_receive = 130
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.nvme_command = KaitaiStream.resolve_enum(TcgStorageBinaryLogParserClass.NvmeHeaderType.NvmeCommandEnum, self._io.read_u1())
            self.proto_id = self._io.read_u1()
            self.com_id = self._io.read_u2be()
            self.reserved = self._io.read_bytes(12)


    class FeatureDescriptorAdditionalDatastoreTablesType(KaitaiStruct):
        """Feature Code = 0x0202."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved = self._io.read_u2be()
            self.maximum_number_of_datastore_tables = self._io.read_u2be()
            self.maximum_total_size_of_datastore_tables = self._io.read_u4be()
            self.datastore_table_size_alignment = self._io.read_u4be()


    class FeatureDescriptorPyriteSscV1Type(KaitaiStruct):
        """Feature Code = 0x0302."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.base_comid = self._io.read_u2be()
            self.number_of_comids = self._io.read_u2be()
            self.reserved_1 = self._io.read_u1()
            self.reserved_2 = self._io.read_u2be()
            self.reserved_3 = self._io.read_u2be()
            self.initial_c_pin_sid_pin_indicator = self._io.read_u1()
            self.behavior_of_c_pin_sid_pin_upon_tper_revert = self._io.read_u1()
            self.reserved_for_future_common_ssc_parameters = self._io.read_bytes(5)


    class ComPacketFormat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved = self._io.read_u4be()
            self.com_id = self._io.read_u2be()
            self.com_id_extension = self._io.read_u2be()
            self.outstanding_data = self._io.read_u4be()
            self.min_transfer = self._io.read_u4be()
            self.payload_length = self._io.read_u4be()
            if self.payload_length > 0:
                self._raw_payload = self._io.read_bytes(self.payload_length)
                _io__raw_payload = KaitaiStream(BytesIO(self._raw_payload))
                self.payload = TcgStorageBinaryLogParserClass.PacketFormat(_io__raw_payload, self, self._root)



    class TokenPayload(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes((self._parent._parent.payload_length - 1))


    class FeatureDescriptorSingleUserModeType(KaitaiStruct):
        """Feature Code = 0x0201."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.number_of_locking_objects_supported = self._io.read_u4be()
            self.byte_5 = self._io.read_u1()

        @property
        def policy(self):
            if hasattr(self, '_m_policy'):
                return self._m_policy

            self._m_policy = ((self.byte_5 & 4) >> 2)
            return getattr(self, '_m_policy', None)

        @property
        def all(self):
            if hasattr(self, '_m_all'):
                return self._m_all

            self._m_all = ((self.byte_5 & 2) >> 1)
            return getattr(self, '_m_all', None)

        @property
        def any(self):
            if hasattr(self, '_m_any'):
                return self._m_any

            self._m_any = ((self.byte_5 & 1) >> 0)
            return getattr(self, '_m_any', None)


    class FeatureDescriptorGeometryReportingType(KaitaiStruct):
        """Feature Code = 0x0003
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved_1 = self._io.read_u1()
            self.reserved_2 = self._io.read_bytes(7)
            self.logical_block_size = self._io.read_u4be()
            self.alignment_granularity = self._io.read_u8be()
            self.lowest_aligned_lba = self._io.read_u8be()


    class FeatureDescriptorType(KaitaiStruct):

        class FeatureCodeEnum(Enum):
            tper_feature = 1
            locking_feature = 2
            geometry_reporting_feature = 3
            opal_ssc_v1_feature = 512
            single_user_mode_feature = 513
            additional_datastore_tables_feature = 514
            opal_ssc_v2_feature = 515
            opalite_ssc_feature = 769
            pyrite_ssc_v1_feature = 770
            pyrite_ssc_v2_feature = 771
            ruby_ssc_v1_feature = 772
            key_per_io_ssc_v1_feature = 773
            block_sid_authentication_feature = 1026
            configurable_namespace_locking_feature = 1027
            data_removal_mechanism_feature = 1028
            shadow_mbr_for_multiple_namespaces_feature_descriptor_feature = 1031
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.feature_code = KaitaiStream.resolve_enum(TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum, self._io.read_u2be())
            self.byte_3 = self._io.read_u1()
            self.feature_code_length = self._io.read_u1()
            _on = self.feature_code
            if _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.pyrite_ssc_v1_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorPyriteSscV1Type(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.block_sid_authentication_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorBlockSidAuthenticationType(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.pyrite_ssc_v2_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorPyriteSscV2Type(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.locking_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorLockingType(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.tper_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorTperType(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.ruby_ssc_v1_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorRubySscV1Type(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.data_removal_mechanism_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorDataRemovalMechanismType(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.opal_ssc_v2_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorOpalSscV2Type(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.single_user_mode_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorSingleUserModeType(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.opal_ssc_v1_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorOpalSscV1Type(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.opalite_ssc_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorOpaliteSscType(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.configurable_namespace_locking_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorConfigurableNamespaceLockingType(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.geometry_reporting_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorGeometryReportingType(_io__raw_descriptor_data, self, self._root)
            elif _on == TcgStorageBinaryLogParserClass.FeatureDescriptorType.FeatureCodeEnum.additional_datastore_tables_feature:
                self._raw_descriptor_data = self._io.read_bytes(self.feature_code_length)
                _io__raw_descriptor_data = KaitaiStream(BytesIO(self._raw_descriptor_data))
                self.descriptor_data = TcgStorageBinaryLogParserClass.FeatureDescriptorAdditionalDatastoreTablesType(_io__raw_descriptor_data, self, self._root)
            else:
                self.descriptor_data = self._io.read_bytes(self.feature_code_length)

        @property
        def version(self):
            if hasattr(self, '_m_version'):
                return self._m_version

            self._m_version = ((self.byte_3 & 240) >> 4)
            return getattr(self, '_m_version', None)

        @property
        def minor_version(self):
            if hasattr(self, '_m_minor_version'):
                return self._m_minor_version

            self._m_minor_version = ((self.byte_3 & 15) >> 0)
            return getattr(self, '_m_minor_version', None)


    class FeatureDescriptorOpaliteSscType(KaitaiStruct):
        """Feature Code = 0x0301."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.base_comid = self._io.read_u2be()
            self.number_of_comids = self._io.read_u2be()
            self.reserved_1 = self._io.read_u1()
            self.reserved_2 = self._io.read_u2be()
            self.reserved_3 = self._io.read_u2be()
            self.initial_c_pin_sid_pin_indicator = self._io.read_u1()
            self.behavior_of_c_pin_sid_pin_upon_tper_revert = self._io.read_u1()
            self.reserved_for_future_common_ssc_parameters = self._io.read_bytes(5)


    class FeatureDescriptorPyriteSscV2Type(KaitaiStruct):
        """Feature Code = 0x0303."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.base_comid = self._io.read_u2be()
            self.number_of_comids = self._io.read_u2be()
            self.reserved_1 = self._io.read_u1()
            self.reserved_2 = self._io.read_u2be()
            self.reserved_3 = self._io.read_u2be()
            self.initial_c_pin_sid_pin_indicator = self._io.read_u1()
            self.behavior_of_c_pin_sid_pin_upon_tper_revert = self._io.read_u1()
            self.reserved_for_future_common_ssc_parameters = self._io.read_bytes(5)


    class DataControlDataSubPacketFormat(KaitaiStruct):

        class TokenEnum(Enum):
            start_list_token = 240
            end_list_token = 241
            start_name_token = 242
            end_name_token = 243
            call_token = 248
            end_of_data_token = 249
            end_of_session_token = 250
            start_transaction_token = 251
            end_transaction_token = 252
            empty = 255
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.token = KaitaiStream.resolve_enum(TcgStorageBinaryLogParserClass.DataControlDataSubPacketFormat.TokenEnum, self._io.read_u1())
            _on = self.token
            if _on == TcgStorageBinaryLogParserClass.DataControlDataSubPacketFormat.TokenEnum.call_token:
                self.data_payload = TcgStorageBinaryLogParserClass.CallTokenPayload(self._io, self, self._root)
            else:
                self.data_payload = TcgStorageBinaryLogParserClass.TokenPayload(self._io, self, self._root)


    class FeatureDescriptorConfigurableNamespaceLockingType(KaitaiStruct):
        """Feature Code = 0x0403."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.byte_1 = self._io.read_u1()
            self.reserved = self._io.read_bytes(3)
            self.max_key_count = self._io.read_u4be()
            self.unused_key_count = self._io.read_u4be()
            self.max_ranges_per_namespace = self._io.read_u4be()

        @property
        def range_c(self):
            if hasattr(self, '_m_range_c'):
                return self._m_range_c

            self._m_range_c = ((self.byte_1 & 128) >> 7)
            return getattr(self, '_m_range_c', None)

        @property
        def range_p(self):
            if hasattr(self, '_m_range_p'):
                return self._m_range_p

            self._m_range_p = ((self.byte_1 & 64) >> 6)
            return getattr(self, '_m_range_p', None)

        @property
        def sum_c(self):
            if hasattr(self, '_m_sum_c'):
                return self._m_sum_c

            self._m_sum_c = ((self.byte_1 & 32) >> 5)
            return getattr(self, '_m_sum_c', None)


    class DataSubPacketFormat(KaitaiStruct):

        class SpfEnum(Enum):
            data_control = 0
            credit_control = 32768
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved_1 = self._io.read_u4be()
            self.reserved_2 = self._io.read_u2be()
            self.packet_kind = self._io.read_u2be()
            self.payload_length = self._io.read_u4be()
            if self.payload_length > 0:
                _on = self.packet_kind
                if _on == 0:
                    self._raw_data_sub_packet_payload = self._io.read_bytes(self.payload_length)
                    _io__raw_data_sub_packet_payload = KaitaiStream(BytesIO(self._raw_data_sub_packet_payload))
                    self.data_sub_packet_payload = TcgStorageBinaryLogParserClass.DataControlDataSubPacketFormat(_io__raw_data_sub_packet_payload, self, self._root)
                elif _on == 32768:
                    self._raw_data_sub_packet_payload = self._io.read_bytes(self.payload_length)
                    _io__raw_data_sub_packet_payload = KaitaiStream(BytesIO(self._raw_data_sub_packet_payload))
                    self.data_sub_packet_payload = TcgStorageBinaryLogParserClass.CreditControlDataSubPacketFormat(_io__raw_data_sub_packet_payload, self, self._root)
                else:
                    self.data_sub_packet_payload = self._io.read_bytes(self.payload_length)



    class CreditControlDataSubPacketFormat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.credit = self._io.read_u4be()


    class FeatureDescriptorLockingType(KaitaiStruct):
        """Feature Code = 0x0002
        page 53
        
        .. seealso::
           Source - https://trustedcomputinggroup.org/wp-content/uploads/TCG_Storage_Architecture_Core_Spec_v2.01_r1.00.pdf
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.byte_1 = self._io.read_u1()

        @property
        def mbr_done(self):
            if hasattr(self, '_m_mbr_done'):
                return self._m_mbr_done

            self._m_mbr_done = ((self.byte_1 & 64) >> 5)
            return getattr(self, '_m_mbr_done', None)

        @property
        def mbr_enable(self):
            if hasattr(self, '_m_mbr_enable'):
                return self._m_mbr_enable

            self._m_mbr_enable = ((self.byte_1 & 16) >> 4)
            return getattr(self, '_m_mbr_enable', None)

        @property
        def media_encryption(self):
            if hasattr(self, '_m_media_encryption'):
                return self._m_media_encryption

            self._m_media_encryption = ((self.byte_1 & 8) >> 3)
            return getattr(self, '_m_media_encryption', None)

        @property
        def locking_supported(self):
            if hasattr(self, '_m_locking_supported'):
                return self._m_locking_supported

            self._m_locking_supported = ((self.byte_1 & 1) >> 0)
            return getattr(self, '_m_locking_supported', None)

        @property
        def locking_enabled(self):
            if hasattr(self, '_m_locking_enabled'):
                return self._m_locking_enabled

            self._m_locking_enabled = ((self.byte_1 & 2) >> 1)
            return getattr(self, '_m_locking_enabled', None)

        @property
        def locked(self):
            if hasattr(self, '_m_locked'):
                return self._m_locked

            self._m_locked = ((self.byte_1 & 4) >> 2)
            return getattr(self, '_m_locked', None)


    class Level0DiscoveryResponseData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.length_of_parameter_data = self._io.read_u4be()
            self.data_structure_major_version = self._io.read_u2be()
            self.data_structure_minor_version = self._io.read_u2be()
            self.reserved = self._io.read_bytes(8)
            self.vendor_unique = self._io.read_bytes(32)
            self._raw_feature_descriptors = self._io.read_bytes((self.length_of_parameter_data - 44))
            _io__raw_feature_descriptors = KaitaiStream(BytesIO(self._raw_feature_descriptors))
            self.feature_descriptors = TcgStorageBinaryLogParserClass.FeatureDescriptorListType(_io__raw_feature_descriptors, self, self._root)



