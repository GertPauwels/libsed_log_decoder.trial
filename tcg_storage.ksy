meta:
  id: tcg_storage_binary_log_parser
  endian: be
  file-extension: bin

seq:
  - id: opal_command
    type: opal_command_type
    repeat: eos

types:
  opal_command_type:
    seq:
      - id: nvme_header
        type: nvme_header_type
      - id: comid_packets
        type:
          switch-on: nvme_header.com_id
          cases:
            1: level_0_discovery_response_data
            2048: com_packet_format
            _: com_packet_format

  nvme_header_type:
    seq:
      - id: nvme_command
        type: u1
        enum: nvme_command_enum
      - id: proto_id
        type: u1
      - id: com_id
        type: u2
      - id: reserved
        size: 12
    enums:
      nvme_command_enum:
        129: nvme_security_send
        130: nvme_security_receive

# level_0_discovery_response_data
##################################
  level_0_discovery_response_data:  # Table 39 p51
    seq:
      - id: length_of_parameter_data
        type: u4
      - id: data_structure_major_version
        type: u2
      - id: data_structure_minor_version
        type: u2
      - id: reserved
        size: 8
      - id: vendor_unique
        size: 32
      - id: feature_descriptors
        type: feature_descriptor_list_type
        size: length_of_parameter_data - 44

  feature_descriptor_list_type:
    seq:
      - id: feature_descriptor
        type: feature_descriptor_type
        repeat: eos
        
  feature_descriptor_type:
    seq:
      - id: feature_code
        type: u2
        enum: feature_code_enum
      - id: byte_3
        type: u1
      - id: feature_code_length
        type: u1
      - id: descriptor_data
        size: feature_code_length
        type:
          switch-on: feature_code
          cases: 
            feature_code_enum::tper_feature: feature_descriptor_tper_type
            feature_code_enum::locking_feature: feature_descriptor_locking_type
            feature_code_enum::geometry_reporting_feature: feature_descriptor_geometry_reporting_type
            feature_code_enum::opal_ssc_v1_feature: feature_descriptor_opal_ssc_v1_type
            feature_code_enum::single_user_mode_feature: feature_descriptor_single_user_mode_type
            feature_code_enum::additional_datastore_tables_feature: feature_descriptor_additional_datastore_tables_type
            feature_code_enum::opal_ssc_v2_feature: feature_descriptor_opal_ssc_v2_type
            feature_code_enum::opalite_ssc_feature: feature_descriptor_opalite_ssc_type
            feature_code_enum::pyrite_ssc_v1_feature: feature_descriptor_pyrite_ssc_v1_type
            feature_code_enum::pyrite_ssc_v2_feature: feature_descriptor_pyrite_ssc_v2_type
            feature_code_enum::ruby_ssc_v1_feature: feature_descriptor_ruby_ssc_v1_type
            feature_code_enum::block_sid_authentication_feature: feature_descriptor_block_sid_authentication_type
            feature_code_enum::configurable_namespace_locking_feature: feature_descriptor_configurable_namespace_locking_type
            feature_code_enum::data_removal_mechanism_feature: feature_descriptor_data_removal_mechanism_type

    instances:
      version:
        value: (byte_3 & 0b11110000) >> 4
      minor_version:
        value: (byte_3 & 0b00001111) >> 0

    enums:
      feature_code_enum:
        0x0001: tper_feature
        0x0002: locking_feature
        0x0003: geometry_reporting_feature
        0x0200: opal_ssc_v1_feature
        0x0201: single_user_mode_feature
        0x0202: additional_datastore_tables_feature
        0x0203: opal_ssc_v2_feature
        0x0301: opalite_ssc_feature
        0x0302: pyrite_ssc_v1_feature
        0x0303: pyrite_ssc_v2_feature
        0x0304: ruby_ssc_v1_feature
        0x0305: key_per_io_ssc_v1_feature  # type not defined in this ksy file
        0x0402: block_sid_authentication_feature
        0x0403: configurable_namespace_locking_feature
        0x0404: data_removal_mechanism_feature
        0x0407: shadow_mbr_for_multiple_namespaces_feature_descriptor_feature  # type not defined in this ksy file

  feature_descriptor_tper_type:
    doc: |
      Feature Code = 0x0001
      page 52
    doc-ref: https://trustedcomputinggroup.org/wp-content/uploads/TCG_Storage_Architecture_Core_Spec_v2.01_r1.00.pdf
    seq:
      - id: byte_1
        type: u1
    instances:
      comid_mgmt_supported:
        value: (byte_1 & 0b01000000) >> 6
      streaming_supported:
        value: (byte_1 & 0b00010000) >> 4
      buffer_mgmt_supported:
        value: (byte_1 & 0b00001000) >> 3
      ack_nak_supported:
        value: (byte_1 & 0b00000100) >> 2
      async_supported:
        value: (byte_1 & 0b00000010) >> 1
      sync_supported:
        value: (byte_1 & 0b00000001) >> 0
   
  feature_descriptor_locking_type:
    doc: |
      Feature Code = 0x0002
      page 53
    doc-ref: https://trustedcomputinggroup.org/wp-content/uploads/TCG_Storage_Architecture_Core_Spec_v2.01_r1.00.pdf
    seq:
      - id: byte_1
        type: u1
    instances:
      mbr_done:
        value: (byte_1 & 0b01000000) >> 5
      mbr_enable:
        value: (byte_1 & 0b00010000) >> 4
      media_encryption:
        value: (byte_1 & 0b00001000) >> 3
      locked:
        value: (byte_1 & 0b00000100) >> 2
      locking_enabled:
        value: (byte_1 & 0b00000010) >> 1
      locking_supported:
        value: (byte_1 & 0b00000001) >> 0
  
  feature_descriptor_geometry_reporting_type:
    doc: |
      Feature Code = 0x0003
    seq:
      - id: reserved_1
        type: u1
      - id: reserved_2
        size: 7
      - id: logical_block_size
        type: u4
      - id: alignment_granularity
        type: u8
      - id: lowest_aligned_lba
        type: u8

  feature_descriptor_opal_ssc_v1_type:
    doc: Feature Code = 0x0200
    seq:
      - id: base_comid
        type: u2
      - id: number_of_comids
        type: u2
      - id: byte_5
        type: u1
    instances:
      range_crossing_behavior:
        value: (byte_5 & 0b00000001) >> 0

  feature_descriptor_single_user_mode_type:
    doc: Feature Code = 0x0201
    seq:
      - id: number_of_locking_objects_supported
        type: u4
      - id: byte_5
        type: u1
    instances:
      policy:
        value: (byte_5 & 0b00000100) >> 2
      all:
        value: (byte_5 & 0b00000010) >> 1
      any:
        value: (byte_5 & 0b00000001) >> 0

  feature_descriptor_additional_datastore_tables_type:
    doc: Feature Code = 0x0202
    seq:
      - id: reserved
        type: u2
      - id: maximum_number_of_datastore_tables
        type: u2
      - id: maximum_total_size_of_datastore_tables
        type: u4
      - id: datastore_table_size_alignment
        type: u4

  feature_descriptor_opal_ssc_v2_type:
    doc: Feature Code = 0x0203
    seq:
      - id: base_comid
        type: u2
      - id: number_of_comids
        type: u2
      - id: byte_5
        type: u1
      - id: number_of_locking_sp_admin_authorities_supported
        type: u2
      - id: number_of_locking_sp_user_authorities_supported
        type: u2
      - id: initial_c_pin_sid_pin_indicator
        type: u1
      - id: behavior_of_c_pin_sid_pin_upon_tper_revert
        type: u1
      - id: reserved_for_future_common_ssc_parameters
        size: 5
    instances:
      range_crossing_behavior:
        value: (byte_5 & 0b00000001) >> 0
      minor_version: 
        value: (_parent.byte_3 & 0b00001111) >> 0

  feature_descriptor_opalite_ssc_type:
    doc: Feature Code = 0x0301
    seq:
      - id: base_comid
        type: u2
      - id: number_of_comids
        type: u2
      - id: reserved_1
        type: u1
      - id: reserved_2
        type: u2
      - id: reserved_3
        type: u2
      - id: initial_c_pin_sid_pin_indicator
        type: u1
      - id: behavior_of_c_pin_sid_pin_upon_tper_revert
        type: u1
      - id: reserved_for_future_common_ssc_parameters
        size: 5

  feature_descriptor_pyrite_ssc_v1_type:
    doc: Feature Code = 0x0302
    seq:
      - id: base_comid
        type: u2
      - id: number_of_comids
        type: u2
      - id: reserved_1
        type: u1
      - id: reserved_2
        type: u2
      - id: reserved_3
        type: u2
      - id: initial_c_pin_sid_pin_indicator
        type: u1
      - id: behavior_of_c_pin_sid_pin_upon_tper_revert
        type: u1
      - id: reserved_for_future_common_ssc_parameters
        size: 5

  feature_descriptor_pyrite_ssc_v2_type:
    doc: Feature Code = 0x0303
    seq:
      - id: base_comid
        type: u2
      - id: number_of_comids
        type: u2
      - id: reserved_1
        type: u1
      - id: reserved_2
        type: u2
      - id: reserved_3
        type: u2
      - id: initial_c_pin_sid_pin_indicator
        type: u1
      - id: behavior_of_c_pin_sid_pin_upon_tper_revert
        type: u1
      - id: reserved_for_future_common_ssc_parameters
        size: 5

  feature_descriptor_ruby_ssc_v1_type:
    doc: Feature Code = 0x0304
    seq:
      - id: base_comid
        type: u2
      - id: number_of_comids
        type: u2
      - id: byte_5
        type: u1
      - id: number_of_locking_sp_admin_authorities_supported
        type: u2
      - id: number_of_locking_sp_user_authorities_supported
        type: u2
      - id: initial_c_pin_sid_pin_indicator
        type: u1
      - id: behavior_of_c_pin_sid_pin_upon_tper_revert
        type: u1
      - id: reserved_for_future_common_ssc_parameters
        size: 5
    instances:
      range_crossing_behavior:
        value: (byte_5 & 0b00000001) >> 0

  feature_descriptor_block_sid_authentication_type:
    doc: Feature Code = 0x0402
    seq:
      - id: byte_1
        type: u1
      - id: byte_2
        type: u1
      - id: reserved
        size: 10
    instances:
      locking_sp_freeze_lock_state:
        value: (byte_1 & 0b00001000) >> 3
      locking_sp_freeze_lock_supported:
        value: (byte_1 & 0b00000100) >> 2
      sid_authentication_blocked_state:
        value: (byte_1 & 0b00000010) >> 1
      sid_value_state:
        value: (byte_1 & 0b00000001) >> 0
      hardware_reset:
        value: (byte_2 & 0b00000001) >> 0

  feature_descriptor_configurable_namespace_locking_type:
    doc: Feature Code = 0x0403
    seq:
      - id: byte_1
        type: u1
      - id: reserved
        size: 3
      - id: max_key_count
        type: u4
      - id: unused_key_count
        type: u4
      - id: max_ranges_per_namespace
        type: u4

  feature_descriptor_data_removal_mechanism_type:
    doc: Feature Code = 0x0404
    seq:
      - id: reserved_1
        type: u1
      - id: byte_2
        type: u1
      - id: supported_data_removal_mechanism
        type: u1
      - id: byte_4
        type: u1
      - id: data_removal_time_for_supported_data_removal_mechanism_bit_0
        type: u2
      - id: data_removal_time_for_supported_data_removal_mechanism_bit_1
        type: u2
      - id: data_removal_time_for_supported_data_removal_mechanism_bit_2
        type: u2
      - id: reserved_2
        type: u4
      - id: data_removal_time_for_supported_data_removal_mechanism_bit_5
        type: u2
      - id: reserved_for_future_supported_data_removal_mechanism_parameters
        size: 16
    instances:
      data_removal_operation_interrupted:
        value: (byte_2 & 0b00000010) >> 1
      data_removal_operation_processing:
        value: (byte_2 & 0b00000001) >> 0
      data_removal_time_format_for_it_5:
        value: (byte_4 & 0b00100000) >> 5
      data_removal_time_format_for_it_2:
        value: (byte_4 & 0b00000100) >> 2
      data_removal_time_format_for_it_1:
        value: (byte_4 & 0b00000010) >> 1
      data_removal_time_format_for_it_0:
        value: (byte_4 & 0b00000001) >> 0

  # com_packet_format
  #########################################################

  com_packet_format:  # Table 17 p23
    seq:
      - id: reserved
        type: u4
      - id: com_id
        type: u2
      - id: com_id_extension
        type: u2
      - id: outstanding_data
        type: u4
      - id: min_transfer
        type: u4
      - id: payload_length
        type: u4
      - id: payload
        type: packet_format
        size: payload_length
        if: payload_length > 0

  packet_format:  # Table 18 p24
    seq:
      - id: session
        type: u8
      - id: seq_number
        type: u4
      - id: reserved
        type: u2
      - id: ack_type
        type: u2
      - id: acknowledgement
        type: u4
      - id: packet_format_length
        type: u4
      - id: packet_format_payload
        size: packet_format_length
        type: data_sub_packet_format
        
  data_sub_packet_format:  # Table 20 p27
    seq:
      - id: reserved_1
        type: u4
      - id: reserved_2
        type: u2
      - id: packet_kind
        type: u2
      - id: payload_length
        type: u4
      - id: data_sub_packet_payload
        size: payload_length
        type:
          switch-on: packet_kind
          cases:
            0x0000: data_control_data_sub_packet_format
            0x8000: credit_control_data_sub_packet_format
        if: payload_length > 0
    enums:
      spf_enum:
        0x0000: data_control
        0x8000: credit_control


  data_control_data_sub_packet_format:
    seq:
      - id: token
        type: u1
        enum: token_enum
      - id: data_payload
        type:
          switch-on: token
          cases:
            token_enum::call_token: call_token_payload
            _: token_payload
    enums:
      token_enum:
        0xf0: start_list_token
        0xf1: end_list_token
        0xf2: start_name_token
        0xf3: end_name_token
        0xf8: call_token
        0xf9: end_of_data_token
        0xfa: end_of_session_token
        0xfb: start_transaction_token
        0xfc: end_transaction_token
        0xff: empty

  token_payload:
    seq:
      - id: data
        size: _parent._parent.payload_length - 1 

  call_token_payload:
    seq:
      - id: token_header1
        type: u1
      - id: invoking_uid
        type: u8
        enum: invoking_uid_enum
      - id: token_header2
        type: u1
      - id: method_uid
        type: u8
        enum: method_uid_enum
      - id: data
        size: _parent._parent.payload_length - 19
    enums:
      method_uid_enum:
        0x000000000000FF01: properties
        0x000000000000FF02: start_session
        0x000000000000FF03: sync_session
        0x0000000600000008: next
        0x000000060000000D: getacl
        0x0000000600000010: genkey
        0x0000000600000011: revertsp
        0x0000000600000016: get
        0x0000000600000017: set
        0x000000060000001C: authenticate
        0x0000000600000202: revert
        0x0000000600000203: activate
        0x0000000600000601: random
      invoking_uid_enum:
        0x00000000000000FF: session_manager_reserved
        0x0000020500000002: locking_sp
        0x0000000B00010001: c_pin_admin1
        0x0000000B00030001: c_pin_user1
        0x0000000B00030002: c_pin_user2
        0x0000000900030001: user1
        0x0000000900030002: user2
        0x0000080200000001: locking_globalrange
        0x0000080200030001: locking_range1

  credit_control_data_sub_packet_format:
    seq:
      - id: credit
        type: u4
