import argparse
import os
import sys
import logging
from io import BytesIO
from tcg_storage_binary_log_parser_class import TcgStorageBinaryLogParserClass as LogParser, KaitaiStream
from tcg_storage_custom_printer_class import CustomPrinter
from colorama import Fore, Style
from typing import Optional

# Define the Unicode code point for the left top character
left_top_code_point = 0x250C        # Unicode code point for 'BOX DRAWINGS LIGHT DOWN AND RIGHT'
vertical_line_code_point = 0x2502   # Unicode code point for 'BOX DRAWINGS LIGHT VERTICAL'
left_bottom_code_point = 0x2514     # Unicode code point for 'BOX DRAWINGS LIGHT UP AND RIGHT'
# Convert the code point to a Unicode character
vertical_line_chr = chr(vertical_line_code_point)
left_top_chr = chr(left_top_code_point)
left_bottom_chr = chr(left_bottom_code_point)

class SedcliMessageViewer:
    """Class for viewing SEDCLI messages from a binary file."""
    status_codes = {
        0x00: f"{Fore.GREEN}SUCCESS{Style.RESET_ALL}",
        0x01: f"{Fore.RED}NOT_AUTHORIZED{Style.RESET_ALL}",
        0x02: f"{Fore.RED}OBSOLETE{Style.RESET_ALL}",
        0x03: f"{Fore.RED}SP_BUSY{Style.RESET_ALL}",
        0x04: f"{Fore.RED}SP_FAILED{Style.RESET_ALL}",
        0x05: f"{Fore.RED}SP_DISABLED{Style.RESET_ALL}",
        0x06: f"{Fore.RED}SP_FROZEN{Style.RESET_ALL}",
        0x07: f"{Fore.RED}NO_SESSIONS_AVAILABLE{Style.RESET_ALL}",
        0x08: f"{Fore.RED}UNIQUENESS_CONFLICT{Style.RESET_ALL}",
        0x09: f"{Fore.RED}INSUFFICIENT_SPACE{Style.RESET_ALL}",
        0x0A: f"{Fore.RED}INSUFFICIENT_ROWS{Style.RESET_ALL}",
        0x0C: f"{Fore.RED}INVALID_PARAMETER{Style.RESET_ALL}",
        0x0D: f"{Fore.RED}OBSOLETE{Style.RESET_ALL}",
        0x0E: f"{Fore.RED}OBSOLETE{Style.RESET_ALL}",
        0x0F: f"{Fore.RED}TPER_MALFUNCTION{Style.RESET_ALL}",
        0x10: f"{Fore.RED}TRANSACTION_FAILURE{Style.RESET_ALL}",
        0x11: f"{Fore.RED}RESPONSE_OVERFLOW{Style.RESET_ALL}",
        0x12: f"{Fore.RED}AUTHORITY_LOCKED_OUT{Style.RESET_ALL}",
        0x3F: f"{Fore.RED}FAIL{Style.RESET_ALL}"
    }
    nvme_security_send = 0x81
    nvme_security_receive = 0x82

# Lines below in remark as they are not used and can be removed after further testing
#
#    # Define the Unicode code point for the left top character
#    left_top_code_point = 0x250C        # Unicode code point for 'BOX DRAWINGS LIGHT DOWN AND RIGHT'
#    vertical_line_code_point = 0x2502   # Unicode code point for 'BOX DRAWINGS LIGHT VERTICAL'
#    left_bottom_code_point = 0x2514     # Unicode code point for 'BOX DRAWINGS LIGHT UP AND RIGHT'
#    # Convert the code point to a Unicode character
#    vertical_line_chr = chr(vertical_line_code_point)
#    left_top_chr = chr(left_top_code_point)
#    left_bottom_chr = chr(left_bottom_code_point)

    def __init__(self, args, custom_printer):
        """Initialize SedcliMessageViewer with command line arguments."""
        self.file_path = args.file
        self.verbose = args.verbose
        self.messages = []
        self.custom_printer = custom_printer
        self.start_message = args.start_message
        self.end_message = args.end_message
        self.html_output = args.html_output
        self.no_colors = args.no_colors

    def load_messages_from_binary_log(self, file_path: Optional[str] = None, start_message: int = 1, end_message: int = -1):
        """Load messages from a binary log file or stdin.

        Args:
            file_path (str, optional): Path to the binary log file. If not provided, reads from stdin.
            start_message (int): Index of the first message to include.
            end_message (int): Index of the last message to include. Defaults to -1, indicating all messages after start_message.

        This method reads binary data from the specified file or stdin, parses it using the LogParser,
        and populates the 'messages' attribute with the parsed messages.
        """
        try:
            if file_path:
                with open(file_path, 'rb') as f:
                    data = f.read()
            else:
                data = sys.stdin.buffer.read()

            kaitai_stream = KaitaiStream(BytesIO(data))
            sedcli_instance = LogParser(kaitai_stream)

            self.messages = sedcli_instance.opal_command[start_message - 1:end_message]
        except FileNotFoundError as e:
            logging.error(f"Error: File '{file_path}' not found. {e}")
            sys.exit(1)            
        except Exception as e:
            logging.error(f"Error: An unexpected error occurred - {e}")
            sys.exit(1)

    def format_hex(data, leading_spaces=0, ASCII=True):
        """
        Format binary data as hexadecimal and ASCII representation.

        Args:
            data (bytes): The binary data to be formatted.
            leading_spaces (int): Number of spaces to add at the beginning of each line.
            ASCII (bool): Flag indicating whether to include ASCII representation.

        Returns:
            list of str: Formatted hexadecimal and ASCII representation of the data.

        """
        HEX_CHARACTERS_PER_BYTE = 2
        HEX_BYTES_PER_LINE = 16
        HEX_CHARACTERS_PER_LINE = (HEX_CHARACTERS_PER_BYTE + 1) * HEX_BYTES_PER_LINE
        ASCII_START = ord(' ')
        ASCII_END = ord('~')
        ASCII_DOT = '.'

        # Convert binary data to hexadecimal string
        hex_string = data.hex()

        # Format hexadecimal string with space separation every two characters
        formatted_hex = ' '.join(hex_string[i:i+HEX_CHARACTERS_PER_BYTE] for i in range(0, len(hex_string), HEX_CHARACTERS_PER_BYTE))

        # Split the formatted hexadecimal string into lines of 47 characters each
        lines = [formatted_hex[i:i + HEX_CHARACTERS_PER_LINE -1] for i in range(0, len(formatted_hex), HEX_CHARACTERS_PER_LINE)]

        # Convert hexadecimal to ASCII, showing only printable characters
        ascii_chars = ''.join([chr(int(hex_char, 16)) if ASCII_START <= int(hex_char, 16) <= ASCII_END else ASCII_DOT for hex_char in formatted_hex.split(' ')])

        # Add leading spaces to lines except the first one
        result_lines = [' ' * leading_spaces + line if index > 0 else line for index, line in enumerate(lines)]

        # Build the final lines by combining hexadecimal and ASCII representations
        final_lines = []
        # Iterate over each line of the hexadecimal representation
        for index, line in enumerate(result_lines):
            # Calculate the starting index for the ASCII representation of the current line
            start_index = index * HEX_BYTES_PER_LINE
            # Calculate the ending index for the ASCII representation of the current line
            # Ensure that the ending index does not exceed the length of the ASCII characters
            end_index = min((index + 1) * HEX_BYTES_PER_LINE, len(ascii_chars))
            # Calculate the number of trailing spaces to add after the hexadecimal part
            # If the line doesn't contain a full line of bytes, calculate the number of missing bytes and spaces
            if end_index - start_index < HEX_BYTES_PER_LINE:
                # Calculate the number of missing bytes
                missing_bytes = HEX_BYTES_PER_LINE - (end_index - start_index)
                # Each byte is represented by two hexadecimal characters, plus one space
                # Multiply by the number of missing bytes to get the total number of spaces needed
                trailing_spaces = missing_bytes * (HEX_CHARACTERS_PER_BYTE + 1)
            else:
                # If the line contains a full line of bytes, no trailing spaces are needed
                trailing_spaces = 0
            # Build the final line with appropriate spacing
            if ASCII:
                # Concatenate the line of hexadecimal characters, trailing spaces, and the corresponding ASCII representation
                final_lines.append(line + ' ' * trailing_spaces + '  ' + ascii_chars[start_index:end_index])
            else:
                # Concatenate the line of hexadecimal characters with trailing spaces
                final_lines.append(line + ' ' * trailing_spaces)
        return final_lines

    def print_nvme_command(self, message, i):
        """Print NVME command based on verbosity level."""
        _NVMe_Command_value = message.nvme_header.nvme_command.value
        _NVMe_Command_name = message.nvme_header.nvme_command.name
        _Proto_ID = message.nvme_header.proto_id
        _Com_ID = message.nvme_header.com_id
        _Proto_ID_hex = '0x{:02X}'.format(_Proto_ID)
        _Com_ID_hex = '0x{:04X}'.format(_Com_ID)
        _Opcode_hex = '0x{:02X}'.format(message.nvme_header.nvme_command.value)

        if _NVMe_Command_value == self.nvme_security_receive and _Com_ID == 1:
            block_type = 'start'
        elif _NVMe_Command_value == self.nvme_security_send:
            block_type = 'start'
        else:
            block_type = 'mid'

        if self.verbose == 1:
            self.custom_printer.print(f"{Fore.YELLOW}{i+1}{Style.RESET_ALL}: {Fore.GREEN}{_NVMe_Command_name}{Style.RESET_ALL} ({_Proto_ID_hex}, {_Com_ID_hex})", block_type=block_type)
        elif self.verbose == 2:
            self.custom_printer.print(f"{Fore.YELLOW}Message {i+1}{Style.RESET_ALL}: NVME Command (Opcode={Fore.GREEN}{_NVMe_Command_name}{Style.RESET_ALL}, ProtoID={_Proto_ID_hex}, ComID={_Com_ID_hex})", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"{Fore.YELLOW}Message {i+1}{Style.RESET_ALL}: NVME Command: {Fore.GREEN}{_NVMe_Command_name}{Style.RESET_ALL}", block_type=block_type)
            self.custom_printer.print(f"  Opcode: {Fore.GREEN}{_Opcode_hex}{Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"  ProtocolID: {_Proto_ID_hex}", block_type='mid')
            self.custom_printer.print(f"  CommunicationID: {_Com_ID_hex}", block_type='mid')
        else:
            self.custom_printer.print(f"Invalid verbosity level: {self.verbose}")

    def print_ComPacketFormat(self, message):
        """Print COM Packet Format based on verbosity level."""
        _Reserved = message.comid_packets.reserved
        _Com_ID_hex = '0x{:04X}'.format(message.comid_packets.com_id)
        _Com_ID_Extension_hex = '0x{:04X}'.format(message.comid_packets.com_id_extension)
        _Outstanding_Data = message.comid_packets.outstanding_data
        _Min_Transfer = message.comid_packets.min_transfer
        _Payload_Length = message.comid_packets.payload_length

        if self.verbose == 1:
            self.custom_printer.print(f"  COM Packet Format ({_Com_ID_hex}, {_Com_ID_Extension_hex}, {_Outstanding_Data}, {_Min_Transfer}, {_Payload_Length})", block_type='mid')
        elif self.verbose == 2:
            self.custom_printer.print(f"  COM Packet Format (ComID={_Com_ID_hex}, ComIDExt={_Com_ID_Extension_hex}, OutstData={_Outstanding_Data}, MinTransf={_Min_Transfer}, PaylLen={_Payload_Length})", block_type='mid')
        elif self.verbose == 3:
            self.custom_printer.print(f"  COM Packet Format:", block_type='mid')
            self.custom_printer.print(f"    Reserved: {_Reserved}", block_type='mid')
            self.custom_printer.print(f"    Com ID: {_Com_ID_hex}", block_type='mid')
            self.custom_printer.print(f"    Com ID Extension: {_Com_ID_Extension_hex}", block_type='mid')
            self.custom_printer.print(f"    Outstanding Data: {_Outstanding_Data}", block_type='mid')
            self.custom_printer.print(f"    Min Transfer: {_Min_Transfer}", block_type='mid')
            self.custom_printer.print(f"    Payload Length: {_Payload_Length}", block_type='mid')
        else:
            self.custom_printer.print(f"Invalid verbosity level: {self.verbose}")

    def print_ComPacketFormat_Payload(self, message):
        _comid_packets_payload_session = message.comid_packets.payload.session
        _comid_packets_payload_seq_number = message.comid_packets.payload.seq_number
        _comid_packets_payload_reserved = message.comid_packets.payload.reserved
        _comid_packets_payload_ack_type = message.comid_packets.payload.ack_type
        _comid_packets_payload_acknowledgement = message.comid_packets.payload.acknowledgement
        _comid_packets_payload_packet_format_length = message.comid_packets.payload.packet_format_length

        if self.verbose == 1:
            self.custom_printer.print(f"    Payload ({_comid_packets_payload_session}, {_comid_packets_payload_seq_number}, {_comid_packets_payload_ack_type}, {_comid_packets_payload_acknowledgement}, {_comid_packets_payload_packet_format_length})", block_type='mid')
        elif self.verbose == 2:
            self.custom_printer.print(f"    Payload (Ses={_comid_packets_payload_session}, SeqNbr={_comid_packets_payload_seq_number}, AckType={_comid_packets_payload_ack_type}, Ack={_comid_packets_payload_acknowledgement}, PackForLen={_comid_packets_payload_packet_format_length})", block_type='mid')
        elif self.verbose == 3:
            self.custom_printer.print(f"    Payload:", block_type='mid')
            self.custom_printer.print(f"      Session: {_comid_packets_payload_session}", block_type='mid')
            self.custom_printer.print(f"      Seq Number: {_comid_packets_payload_seq_number}", block_type='mid')
            self.custom_printer.print(f"      Reserved: {_comid_packets_payload_reserved}", block_type='mid')
            self.custom_printer.print(f"      Ack Type: {_comid_packets_payload_ack_type}", block_type='mid')
            self.custom_printer.print(f"      Acknowledgement: {_comid_packets_payload_acknowledgement}", block_type='mid')
            self.custom_printer.print(f"      Packet Format Length: {_comid_packets_payload_packet_format_length}", block_type='mid')

    def print_ComPacketFormat_Payload_PacketFormatPayload(self, message):
        _payload_reserved_1 = message.comid_packets.payload.packet_format_payload.reserved_1
        _payload_reserved_2 = message.comid_packets.payload.packet_format_payload.reserved_2
        _payload_packet_kind = message.comid_packets.payload.packet_format_payload.packet_kind
        _payload_payload_length = message.comid_packets.payload.packet_format_payload.payload_length

        if self.verbose == 1:
            self.custom_printer.print(f"     Packet Format Payload ({_payload_reserved_1}, {_payload_reserved_2}, {_payload_packet_kind}, {_payload_payload_length})", block_type='mid')
        elif self.verbose == 2:
            self.custom_printer.print(f"      Packet Format Payload (Rsvd1={_payload_reserved_1}, Rsvd2={_payload_reserved_2}, PcktKind={_payload_packet_kind}, PaylLen={_payload_payload_length})", block_type='mid')
        elif self.verbose == 3:
            self.custom_printer.print(f"      Packet Format Payload:", block_type='mid')
            self.custom_printer.print(f"        Reserved 1:, {_payload_reserved_1}", block_type='mid')
            self.custom_printer.print(f"        Reserved 2:, {_payload_reserved_2}", block_type='mid')
            self.custom_printer.print(f"        Packet kind, {_payload_packet_kind}", block_type='mid')
            self.custom_printer.print(f"        Payload Length: {_payload_payload_length}", block_type='mid')

    def print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayload(self, message):
        if message.comid_packets.payload.packet_format_payload.packet_kind == 0:
            self.print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayload(message)
        elif message.comid_packets.payload.packet_format_payload.packet_kind == 0x8000:
            self.print_ComPacketFormat_Payload_PacketFormatPayload_CreditControlDataSubPacketPayload(message)

    def print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayload(self, message):
        _token = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.token

        if _token == LogParser.DataControlDataSubPacketFormat.TokenEnum.call_token:
            self.print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayloadCallToken(message)
        elif _token == LogParser.DataControlDataSubPacketFormat.TokenEnum.start_list_token:
            self.print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayloadStartListToken(message)
        else:
            self.print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayloadToken(message)

    def print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayloadCallToken(self, message):
        _NVMe_Command_value = message.nvme_header.nvme_command.value
        _data_part, _statusCode_part = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.data_payload.data.split(b'\xf9', 1)
        _data_hex = SedcliMessageViewer.format_hex(_data_part, 20)
        _statusCodeByte = int(_statusCode_part[1])
        _statusCodeStr = self.status_codes.get(_statusCodeByte, f"{Fore.RED}Unknown Error Code{Style.RESET_ALL}")
        _token_name = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.token.name
        _invoking_uid_value = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.data_payload.invoking_uid

        if isinstance(_invoking_uid_value, int):
            _invoking_uid_name = ' '.join(f'{byte:02X}' for byte in _invoking_uid_value.to_bytes(8, 'big'))
        else:
            _invoking_uid_name = _invoking_uid_value.name

        _method_uid_value = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.data_payload.method_uid
        if isinstance(_method_uid_value, int):
            _method_uid_name = ' '.join(f'{byte:02X}' for byte in _method_uid_value.to_bytes(8, 'big'))
        else:
            _method_uid_name = _method_uid_value.name

        block_type = 'end' if _NVMe_Command_value == self.nvme_security_receive else 'mid'

        if self.verbose == 1:
            self.custom_printer.print(f"          Data Control Data Sub Packet Format ({Fore.GREEN}{_token_name}{Style.RESET_ALL})", block_type='mid')
            self.custom_printer.print(f"            Data Payload ({Fore.GREEN}{_invoking_uid_name}{Style.RESET_ALL}, {Fore.GREEN}{_method_uid_name}{Style.RESET_ALL})", block_type='mid')
            self.custom_printer.print(f"              Data: ", block_type='mid', end_line=False)
            self.print_multilines(_data_hex, Fore.CYAN)
            self.custom_printer.print(f"              Status Code: {_statusCodeStr}", block_type=block_type)
        elif self.verbose == 2:
            self.custom_printer.print(f"          Data Control Data Sub Packet Format (Tkn={Fore.GREEN}{_token_name}{Style.RESET_ALL})", block_type='mid')
            self.custom_printer.print(f"            Data Payload:", block_type='mid')
            self.custom_printer.print(f"              Invoking UID: {Fore.GREEN}{_invoking_uid_name}{Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"              Method UID:   {Fore.GREEN}{_method_uid_name}{Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"              Data: ", block_type='mid',end_line=False)
            self.print_multilines(_data_hex, Fore.CYAN)
            self.custom_printer.print(f"              Status Code: {_statusCodeStr}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"          Data Control Data Sub Packet Format:")
            self.custom_printer.print(f"            Token: {Fore.GREEN}{_token_name}{Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"            Data Payload:", block_type='mid')
            self.custom_printer.print(f"              Invoking UID: {Fore.GREEN}{_invoking_uid_name}{Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"              Method UID:   {Fore.GREEN}{_method_uid_name}{Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"              Data: ", block_type='mid',end_line=False)
            self.print_multilines(_data_hex, Fore.CYAN)
            self.custom_printer.print(f"              Status Code: {_statusCodeStr}", block_type=block_type)

    def print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayloadStartListToken(self, message):
        _NVMe_Command_value = message.nvme_header.nvme_command.value
        _data_part, _statusCode_part = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.data_payload.data.split(b'\xf9', 1)
        _statusCodeByte = int(_statusCode_part[1])
        _data_hex = SedcliMessageViewer.format_hex(b'\xF0' + _data_part, 20)
        _statusCodeStr = self.status_codes.get(_statusCodeByte, F"{Fore.RED}Unknown Error Code{Style.RESET_ALL}")
        block_type = 'end' if _NVMe_Command_value == self.nvme_security_receive else 'mid'

        if self.verbose == 1:
            self.custom_printer.print(f"              Data: {Fore.CYAN}{_data_hex}{Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"              Status Code: {_statusCodeStr}", block_type=block_type)
        elif self.verbose == 2:
            self.custom_printer.print(f"          Data Control Data Sub Packet Format:", block_type='mid')
            self.custom_printer.print(f"              Data: ", block_type='mid', end_line=False)
            self.print_multilines(_data_hex, Fore.CYAN)
            self.custom_printer.print(f"              Status Code: {_statusCodeStr}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"          Data Control Data Sub Packet Format:", block_type='mid')
            self.custom_printer.print(f"              Data: ", block_type='mid', end_line=False)
            self.print_multilines(_data_hex, Fore.CYAN)
            self.custom_printer.print(f"              Status Code: {_statusCodeStr}", block_type=block_type)

    def print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayloadToken(self, message):
        _NVMe_Command_value = message.nvme_header.nvme_command.value
        _token_value = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.token
        _data = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.data_payload.data

        if isinstance(_token_value, int):
            _token_name = ' '.join(f'0x{byte:02X}' for byte in _token_value.to_bytes(1, 'big'))
        else:
            _token_name = _token_value.name

        if _NVMe_Command_value == self.nvme_security_receive :
            block_type = 'mid'
            if _data:
                block_type = 'mid'
            else:
                block_type = 'end'
        else:
            block_type = 'mid'

        if self.verbose == 1:
            self.custom_printer.print(f"          Data Control Data Sub Packet Format ({Fore.GREEN}{_token_name}{Style.RESET_ALL})", block_type=block_type)
            if _data:
                _data_part, _statusCode_part = _data.split(b'\xf9', 1)
                _statusCodeByte = int(_statusCode_part[1])
                _data_hex = SedcliMessageViewer.format_hex(_data_part, 20)
                _statusCodeStr = self.status_codes.get(_statusCodeByte, F"{Fore.RED}Unknown Error Code{Style.RESET_ALL}")
                self.custom_printer.print(f"          Data: ", block_type='mid', end_line=False)
                self.print_multilines(_data_hex, Fore.CYAN)
                self.custom_printer.print(f"          Status Code: {_statusCodeStr}", block_type='end')
        elif self.verbose == 2:
            self.custom_printer.print(f"          Data Control Data Sub Packet Format (Tkn={Fore.GREEN}{_token_name}{Style.RESET_ALL})", block_type=block_type)
            if _data:
                _data_part, _statusCode_part = _data.split(b'\xf9', 1)
                _statusCodeByte = int(_statusCode_part[1])
                _data_hex = SedcliMessageViewer.format_hex(_data_part, 20)
                _statusCodeStr = self.status_codes.get(_statusCodeByte, F"{Fore.RED}Unknown Error Code{Style.RESET_ALL}")
                self.custom_printer.print(f"          Data: ", block_type='mid', end_line=False)
                self.print_multilines(_data_hex, Fore.CYAN)
                self.custom_printer.print(f"          Status Code: {_statusCodeStr}", block_type='end')
        elif self.verbose == 3:
            self.custom_printer.print(f"          Data Control Data Sub Packet Format:", block_type='mid')
            self.custom_printer.print(f"            Token: {Fore.GREEN}{_token_name}{Style.RESET_ALL}", block_type=block_type)
            if _data:
                _data_part, _statusCode_part = _data.split(b'\xf9', 1)
                _statusCodeByte = int(_statusCode_part[1])
                _data_hex = SedcliMessageViewer.format_hex(_data_part, 20)
                _statusCodeStr = self.status_codes.get(_statusCodeByte, F"{Fore.RED}Unknown Error Code{Style.RESET_ALL}")
                self.custom_printer.print(f"          Data: ", block_type='mid', end_line=False)
                self.print_multilines(_data_hex, Fore.CYAN)
                self.custom_printer.print(f"          Status Code: {_statusCodeStr}", block_type='end')

    def print_ComPacketFormat_Payload_PacketFormatPayload_CreditControlDataSubPacketPayload(self, message):
        _NVMe_Command_value = message.nvme_header.nvme_command.value
        _credit = message.comid_packets.payload.packet_format_payload.data_sub_packet_payload.credit

        block_type = 'end' if _NVMe_Command_value == self.nvme_security_receive else 'mid'

        if self.verbose == 1:
            self.custom_printer.print(f"          Credit Control Data Sub Packet Format: ({_credit})", block_type=block_type)
        elif self.verbose == 2:
            self.custom_printer.print(f"          Credit Control Data Sub Packet Format: (Crdt={_credit})", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"          Credit Control Data Sub Packet Format:", block_type='mid')
            self.custom_printer.print(f"            Credit: {_credit}", block_type=block_type)

    ########################################
    #   Discovery Response decoding:
    ########################################
    def print_multilines(self, lines, color=Fore.CYAN, first_line_block_type='none_second_part', next_line_block_type='mid'):
        num_lines = len(lines)
        for index, line in enumerate(lines):
            # Determine the block type based on the index
            if index == 0:
                block_type = first_line_block_type
            elif index == num_lines - 1:
                block_type = 'end' if next_line_block_type == 'end' else 'mid'
            else:
                block_type = next_line_block_type
            # Print the line with the specified color and block type
            self.custom_printer.print(f"{color}{line}{Style.RESET_ALL}", block_type=block_type)

    def print_Discovery_Response_Data_generic(self, feature_descriptor, is_last_descriptor=False):
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} ({feature_descriptor.version}, {feature_descriptor.feature_code_length})", block_type='mid')
            if feature_descriptor.feature_code_length <= 16:
                self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
                self.print_multilines(_descriptor_data_hex, Fore.CYAN, 'none_second_part', 'end')
            else:
                self.custom_printer.print(f"      Descriptor Data: ", 'mid', end_line=False)
                self.print_multilines(_descriptor_data_hex, Fore.CYAN, 'none_second_part', block_type)
        elif self.verbose == 2:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            if feature_descriptor.feature_code_length <= 16:
                self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
                self.print_multilines(_descriptor_data_hex, Fore.CYAN, 'none_second_part', 'end')
            else:
                self.custom_printer.print(f"      Descriptor Data: ", 'mid', end_line=False)
                self.print_multilines(_descriptor_data_hex, Fore.CYAN, 'none_second_part', block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: {feature_descriptor.descriptor_data}", block_type=block_type)

    def print_Discovery_Response_Data_tper_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG-Storage-Opal-SSC-v2p02-r1p0_pub24jan2022.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        Sync={feature_descriptor.descriptor_data.sync_supported}, Async={feature_descriptor.descriptor_data.async_supported}, ACK/NAK={feature_descriptor.descriptor_data.ack_nak_supported}, BufMgmt={feature_descriptor.descriptor_data.buffer_mgmt_supported}, Strmng={feature_descriptor.descriptor_data.streaming_supported}, ComIDMgmt={feature_descriptor.descriptor_data.comid_mgmt_supported}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Sync Supported        : {feature_descriptor.descriptor_data.sync_supported}", block_type='mid')
            self.custom_printer.print(f"        Async Supported       : {feature_descriptor.descriptor_data.async_supported}", block_type='mid')
            self.custom_printer.print(f"        ACK/NAK Supported     : {feature_descriptor.descriptor_data.ack_nak_supported}", block_type='mid')
            self.custom_printer.print(f"        Buffer Mgmt Supported : {feature_descriptor.descriptor_data.buffer_mgmt_supported}", block_type='mid')
            self.custom_printer.print(f"        Streaming Supported   : {feature_descriptor.descriptor_data.streaming_supported}", block_type='mid')
            self.custom_printer.print(f"        ComID Mgmt Supported  : {feature_descriptor.descriptor_data.comid_mgmt_supported}", block_type=block_type)

    def print_Discovery_Response_Data_locking_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG-Storage-Opal-SSC-v2p02-r1p0_pub24jan2022.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        LckSup={feature_descriptor.descriptor_data.locking_supported}, LckEnbld={feature_descriptor.descriptor_data.locking_enabled}, Lckd={feature_descriptor.descriptor_data.locked}, MdEncr={feature_descriptor.descriptor_data.media_encryption}, MBREnbld={feature_descriptor.descriptor_data.mbr_enable}, MBRDn={feature_descriptor.descriptor_data.mbr_done}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Locking Supported     : {feature_descriptor.descriptor_data.locking_supported}", block_type='mid')
            self.custom_printer.print(f"        Locking Enabled       : {feature_descriptor.descriptor_data.locking_enabled}", block_type='mid')
            self.custom_printer.print(f"        Locked                : {feature_descriptor.descriptor_data.locked}", block_type='mid')
            self.custom_printer.print(f"        MediaEncryption       : {feature_descriptor.descriptor_data.media_encryption}", block_type='mid')
            self.custom_printer.print(f"        MBREnabled            : {feature_descriptor.descriptor_data.mbr_enable}", block_type='mid')
            self.custom_printer.print(f"        MBRDone               : {feature_descriptor.descriptor_data.mbr_done}", block_type=block_type)

    def print_Discovery_Response_Data_geometry_reporting_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG-Storage-Opal-SSC-v2p02-r1p0_pub24jan2022.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        LgclBS={feature_descriptor.descriptor_data.logical_block_size}, AlgnGrn={feature_descriptor.descriptor_data.alignment_granularity}, LwstAlgnLBA={feature_descriptor.descriptor_data.lowest_aligned_lba}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Logical block size    : {feature_descriptor.descriptor_data.logical_block_size}", block_type='mid')
            self.custom_printer.print(f"        Alignment granularity : {feature_descriptor.descriptor_data.alignment_granularity}", block_type='mid')
            self.custom_printer.print(f"        Lowest aligned LBA    : {feature_descriptor.descriptor_data.lowest_aligned_lba}", block_type=block_type)

    def print_Discovery_Response_Data_single_user_mode_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG_Storage-Opal_Feature_Set_Single_User_Mode_v1.00_r2.00.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        NmbrLckObjSup={feature_descriptor.descriptor_data.number_of_locking_objects_supported}, Plc={feature_descriptor.descriptor_data.policy}, All={feature_descriptor.descriptor_data.all}, Any={feature_descriptor.descriptor_data.any}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Number of Locking Objects Supported    : {feature_descriptor.descriptor_data.number_of_locking_objects_supported}", block_type='mid')
            self.custom_printer.print(f"        Policy : {feature_descriptor.descriptor_data.policy}", block_type='mid')
            self.custom_printer.print(f"        All :    {feature_descriptor.descriptor_data.all}", block_type='mid')
            self.custom_printer.print(f"        Any :    {feature_descriptor.descriptor_data.any}", block_type=block_type)

    def print_Discovery_Response_Data_additional_datastore_tables_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG-Storage-Opal-Family-Feature-Set-Additional-Data-Store-Tables-Version-1.01-Revision-1.18.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        MxNmbrDSTbls={feature_descriptor.descriptor_data.maximum_number_of_datastore_tables}, MxTtlSzDSTbls={feature_descriptor.descriptor_data.maximum_total_size_of_datastore_tables}, SzAlgnm={feature_descriptor.descriptor_data.datastore_table_size_alignment}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Maximum number of DataStore tables     : {feature_descriptor.descriptor_data.maximum_number_of_datastore_tables}", block_type='mid')
            self.custom_printer.print(f"        Maximum total size of DataStore tables : {feature_descriptor.descriptor_data.maximum_total_size_of_datastore_tables}", block_type='mid')
            self.custom_printer.print(f"        DataStore table size alignment         : {feature_descriptor.descriptor_data.datastore_table_size_alignment}", block_type=block_type)

    def print_Discovery_Response_Data_opal_ssc_v2_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG-Storage-Opal-SSC-v2p02-r1p0_pub24jan2022.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        BsComID={feature_descriptor.descriptor_data.base_comid}, NmbrComIDs={feature_descriptor.descriptor_data.number_of_comids}, RngCrssBhvr={feature_descriptor.descriptor_data.range_crossing_behavior}, NmbrLckSPAdmin={feature_descriptor.descriptor_data.number_of_locking_sp_admin_authorities_supported}, NmbrLckSPUser={feature_descriptor.descriptor_data.number_of_locking_sp_user_authorities_supported}, IntSIDIndctr={feature_descriptor.descriptor_data.initial_c_pin_sid_pin_indicator}, BhvrSIDTPerRvrt={feature_descriptor.descriptor_data.behavior_of_c_pin_sid_pin_upon_tper_revert}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Base ComID                                 : {feature_descriptor.descriptor_data.base_comid}", block_type='mid')
            self.custom_printer.print(f"        Number of ComIDs                           : {feature_descriptor.descriptor_data.number_of_comids}", block_type='mid')
            self.custom_printer.print(f"        Range Crossing Behavior                    : {feature_descriptor.descriptor_data.range_crossing_behavior}", block_type='mid')
            self.custom_printer.print(f"        Number of Locking SP Admin Authorities     : {feature_descriptor.descriptor_data.number_of_locking_sp_admin_authorities_supported}", block_type='mid')
            self.custom_printer.print(f"        Number of Locking SP User Authorities      : {feature_descriptor.descriptor_data.number_of_locking_sp_user_authorities_supported}", block_type='mid')
            self.custom_printer.print(f"        Initial C_PIN_SID PIN Indicator            : {feature_descriptor.descriptor_data.initial_c_pin_sid_pin_indicator}", block_type='mid')
            self.custom_printer.print(f"        Behavior of C_PIN_SID PIN upon TPer Revert : {feature_descriptor.descriptor_data.behavior_of_c_pin_sid_pin_upon_tper_revert}", block_type=block_type)

    def print_Discovery_Response_Data_block_sid_authentication_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG_Storage-Feature_Set_Block_SID_Authentication_v1.01_r1.00.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        LckSPFrLckSt={feature_descriptor.descriptor_data.locking_sp_freeze_lock_state}, LckSPFrLckSp={feature_descriptor.descriptor_data.locking_sp_freeze_lock_supported}, SIDAthBlckSt={feature_descriptor.descriptor_data.sid_authentication_blocked_state}, SIDVlSt={feature_descriptor.descriptor_data.sid_value_state}, HrdwRst={feature_descriptor.descriptor_data.hardware_reset}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Locking SP Freeze Lock State     : {feature_descriptor.descriptor_data.locking_sp_freeze_lock_state}", block_type='mid')
            self.custom_printer.print(f"        Locking SP Freeze Lock supported : {feature_descriptor.descriptor_data.locking_sp_freeze_lock_supported}", block_type='mid')
            self.custom_printer.print(f"        SID Authentication Blocked State : {feature_descriptor.descriptor_data.sid_authentication_blocked_state}", block_type='mid')
            self.custom_printer.print(f"        SID Value State                  : {feature_descriptor.descriptor_data.sid_value_state}", block_type='mid')
            self.custom_printer.print(f"        Hardware reset                   : {feature_descriptor.descriptor_data.hardware_reset}", block_type=block_type)

    def print_Discovery_Response_Data_configurable_namespace_locking_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG-Storage-Feature-Set-Configurable-Locking-for-NVMe-Namespaces-and-SCSI-LUNs-Version-1.02-Revision-1.16_pub-1.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        RngC={feature_descriptor.descriptor_data.range_c}, RngP={feature_descriptor.descriptor_data.range_p}, SumC={feature_descriptor.descriptor_data.sum_c}, Unsd={feature_descriptor.descriptor_data.unused_key_count}, MxRngPrNS={feature_descriptor.descriptor_data.max_ranges_per_namespace}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Range_C                      : {feature_descriptor.descriptor_data.range_c}", block_type='mid')
            self.custom_printer.print(f"        Range_P                      : {feature_descriptor.descriptor_data.range_p}", block_type='mid')
            self.custom_printer.print(f"        Sum_C                        : {feature_descriptor.descriptor_data.sum_c}", block_type='mid')
            self.custom_printer.print(f"        Unused Key Count             : {feature_descriptor.descriptor_data.unused_key_count}", block_type='mid')
            self.custom_printer.print(f"        Maximum Ranges Per Namespace : {feature_descriptor.descriptor_data.max_ranges_per_namespace}", block_type=block_type)

    def print_Discovery_Response_Data_data_removal_mechanism_feature(self, feature_descriptor, is_last_descriptor=False):
        # https://trustedcomputinggroup.org/wp-content/uploads/TCG-Storage-Feature-Set-Configurable-Locking-for-NVMe-Namespaces-and-SCSI-LUNs-Version-1.02-Revision-1.16_pub-1.pdf
        block_type = 'end' if is_last_descriptor else 'mid'

        if self.verbose == 1:
            _descriptor_data_hex = SedcliMessageViewer.format_hex(feature_descriptor._raw_descriptor_data, 23)
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data: ", block_type=block_type, end_line=False)
            self.print_multilines(_descriptor_data_hex, Fore.CYAN)
        elif self.verbose == 2:
            self.custom_printer.print(f"      {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL} (Ver={feature_descriptor.version}, Len={feature_descriptor.feature_code_length})", block_type='mid')
            self.custom_printer.print(f"        DataRmvlPrc={feature_descriptor.descriptor_data.data_removal_operation_processing}, DataRmvlIntr={feature_descriptor.descriptor_data.data_removal_operation_interrupted}, SpprtdMchnsm={bin(feature_descriptor.descriptor_data.supported_data_removal_mechanism)}, FrmtBt0={feature_descriptor.descriptor_data.data_removal_time_format_for_bit_0}, FrmtBt1={feature_descriptor.descriptor_data.data_removal_time_format_for_bit_1}, FrmtBt2={feature_descriptor.descriptor_data.data_removal_time_format_for_bit_2}, FrmtBt5={feature_descriptor.descriptor_data.data_removal_time_format_for_bit_5}, TmBt0={feature_descriptor.descriptor_data.data_removal_time_for_supported_data_removal_mechanism_bit_0}, TmBt1={feature_descriptor.descriptor_data.data_removal_time_for_supported_data_removal_mechanism_bit_1}, TmBt2={feature_descriptor.descriptor_data.data_removal_time_for_supported_data_removal_mechanism_bit_2}, TmBt5={feature_descriptor.descriptor_data.data_removal_time_for_supported_data_removal_mechanism_bit_5}", block_type=block_type)
        elif self.verbose == 3:
            self.custom_printer.print(f"      Feature Code: {Fore.GREEN}{feature_descriptor.feature_code.name} ({hex(feature_descriptor.feature_code.value)}){Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"      Version: {feature_descriptor.version}", block_type='mid')
            self.custom_printer.print(f"      Feature Code Length: {feature_descriptor.feature_code_length}", block_type='mid')
            self.custom_printer.print(f"      Descriptor Data:", block_type='mid')
            self.custom_printer.print(f"        Data Removal Operation Processing : {feature_descriptor.descriptor_data.data_removal_operation_processing}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Operation Interrupted : {feature_descriptor.descriptor_data.data_removal_operation_interrupted}", block_type='mid')
            self.custom_printer.print(f"        Supported Data Removal Mechanism : {bin(feature_descriptor.descriptor_data.supported_data_removal_mechanism)}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Time Format for bit 0 : {feature_descriptor.descriptor_data.data_removal_time_format_for_bit_0}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Time Format for bit 1 : {feature_descriptor.descriptor_data.data_removal_time_format_for_bit_1}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Time Format for bit 2 : {feature_descriptor.descriptor_data.data_removal_time_format_for_bit_2}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Time Format for bit 5 : {feature_descriptor.descriptor_data.data_removal_time_format_for_bit_5}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Time for supported data removal mechanism bit 0 : {feature_descriptor.descriptor_data.data_removal_time_for_supported_data_removal_mechanism_bit_0}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Time for supported data removal mechanism bit 1 : {feature_descriptor.descriptor_data.data_removal_time_for_supported_data_removal_mechanism_bit_1}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Time for supported data removal mechanism bit 2 : {feature_descriptor.descriptor_data.data_removal_time_for_supported_data_removal_mechanism_bit_2}", block_type='mid')
            self.custom_printer.print(f"        Data Removal Time for supported data removal mechanism bit 5 : {feature_descriptor.descriptor_data.data_removal_time_for_supported_data_removal_mechanism_bit_5}", block_type=block_type)

    def print_Discovery_Response_Data(self, message):
        featureDescriptorFunctionMap= {
            LogParser.FeatureDescriptorType.FeatureCodeEnum.tper_feature:               self.print_Discovery_Response_Data_tper_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.locking_feature:            self.print_Discovery_Response_Data_locking_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.geometry_reporting_feature: self.print_Discovery_Response_Data_geometry_reporting_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.opal_ssc_v1_feature:        self.print_Discovery_Response_Data_generic,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.single_user_mode_feature:   self.print_Discovery_Response_Data_single_user_mode_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.additional_datastore_tables_feature: self.print_Discovery_Response_Data_additional_datastore_tables_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.opal_ssc_v2_feature:        self.print_Discovery_Response_Data_opal_ssc_v2_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.opalite_ssc_feature:        self.print_Discovery_Response_Data_generic,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.pyrite_ssc_v1_feature:      self.print_Discovery_Response_Data_generic,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.pyrite_ssc_v2_feature:      self.print_Discovery_Response_Data_generic,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.ruby_ssc_v1_feature:        self.print_Discovery_Response_Data_generic,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.key_per_io_ssc_v1_feature:  self.print_Discovery_Response_Data_generic,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.block_sid_authentication_feature:       self.print_Discovery_Response_Data_block_sid_authentication_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.configurable_namespace_locking_feature: self.print_Discovery_Response_Data_configurable_namespace_locking_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.data_removal_mechanism_feature:         self.print_Discovery_Response_Data_data_removal_mechanism_feature,
            LogParser.FeatureDescriptorType.FeatureCodeEnum.shadow_mbr_for_multiple_namespaces_feature_descriptor_feature: self.print_Discovery_Response_Data_generic,
        }
        _length_of_parameter_data = message.comid_packets.length_of_parameter_data
        _major_version = message.comid_packets.data_structure_major_version
        _minor_version = message.comid_packets.data_structure_minor_version
        if self.verbose == 1:
            self.custom_printer.print(f"  {Fore.MAGENTA}Level 0 Discovery Response Data{Style.RESET_ALL} ({_length_of_parameter_data}, {_major_version}, {_minor_version})", block_type='mid')
        elif self.verbose == 2:
            _comid_packets_vendor_unique_hex = SedcliMessageViewer.format_hex(message.comid_packets.vendor_unique, 20)
            self.custom_printer.print(f"  {Fore.MAGENTA}Level 0 Discovery Response Data{Style.RESET_ALL} (len={_length_of_parameter_data}, Maj={_major_version}, Min={_minor_version})", block_type='mid')
            self.custom_printer.print(f"    Vendor Unique:  ", block_type='mid', end_line=False)
            self.print_multilines(_comid_packets_vendor_unique_hex, Fore.CYAN)
            self.custom_printer.print(f"    Feature Descriptors: ", block_type='mid')
        elif self.verbose == 3:
            _comid_packets_reserved_hex = SedcliMessageViewer.format_hex(message.comid_packets.reserved, 20)
            _comid_packets_vendor_unique_hex = SedcliMessageViewer.format_hex(message.comid_packets.vendor_unique, 20)
            self.custom_printer.print(f"  {Fore.MAGENTA}Level 0 Discovery Response Data:{Style.RESET_ALL}", block_type='mid')
            self.custom_printer.print(f"    Length of Parameter Data: {_length_of_parameter_data}", block_type='mid')
            self.custom_printer.print(f"    Data Structure Major Version: {_major_version}", block_type='mid')
            self.custom_printer.print(f"    Data Structure Minor Version: {_minor_version}", block_type='mid')
            self.custom_printer.print(f"    Reserved:       ", block_type='mid', end_line=False)
            self.print_multilines(_comid_packets_reserved_hex, Fore.CYAN)
            self.custom_printer.print(f"    Vendor Unique:  ", block_type='mid', end_line=False)
            self.print_multilines(_comid_packets_vendor_unique_hex, Fore.CYAN)
            self.custom_printer.print(f"    Feature Descriptors: ")

        num_descriptors = len(message.comid_packets.feature_descriptors.feature_descriptor)
        for index, feature_descriptor in enumerate(message.comid_packets.feature_descriptors.feature_descriptor):
            featureDescriptorFunction = featureDescriptorFunctionMap.get(feature_descriptor.feature_code)
            # Pass True to indicate it's the last descriptor if it's the last one, else False
            _is_last_descriptor = index == num_descriptors - 1
            if featureDescriptorFunction:
                # Call the appropriate function with the message as argument
                featureDescriptorFunction(feature_descriptor, _is_last_descriptor)
            else:
                # Handle the case where feature code is not recognized
                self.custom_printer.print(f"      {Fore.MAGENTA}Unsupported feature code:{Style.RESET_ALL}", feature_descriptor.feature_code, block_type='mid')
                self.print_Discovery_Response_Data_generic(feature_descriptor, _is_last_descriptor)

    def print_messages(self):
        """Print messages based on verbosity level."""
        for i, message in enumerate(self.messages):
            self.print_nvme_command(message, self.start_message + i - 1)
            if message.nvme_header.com_id == 1:
                self.print_Discovery_Response_Data(message)
            else:
                self.print_ComPacketFormat(message)
                if message.comid_packets.payload_length > 0:
                    self.print_ComPacketFormat_Payload(message)
                    if message.comid_packets.payload.packet_format_length > 0:
                        self.print_ComPacketFormat_Payload_PacketFormatPayload(message)
                        if message.comid_packets.payload.packet_format_payload.payload_length > 0:
                            self.print_ComPacketFormat_Payload_PacketFormatPayload_DataSubPacketPayload(message)

def start():
    """Start the SEDCLI Binary File Viewer."""
    output_file = "libsed.html"

    custom_printer = CustomPrinter(color=not args.no_colors, write_to_html=args.html_output, html_file_name=output_file)
    custom_printer.set_use_block(True)

    custom_printer.set_block_characters(f"{Fore.YELLOW}{left_top_chr} {Style.RESET_ALL}",f"{Fore.YELLOW}{vertical_line_chr} {Style.RESET_ALL}", f"{Fore.YELLOW}{left_bottom_chr} {Style.RESET_ALL}")

    message_viewer = SedcliMessageViewer(args, custom_printer)
    message_viewer.load_messages_from_binary_log(args.file, args.start_message, args.end_message)
    message_viewer.print_messages()
    
    custom_printer.print(f"{Fore.GREEN}Number of messages in {args.file}: {len(message_viewer.messages)}", block_type='none')
    if args.html_output:
        custom_printer.print(f"{Fore.GREEN}html output written: {output_file}", block_type='none')

if __name__ == "__main__":
    # Use os.path.basename to get the script name without directory and extension
    script_name = os.path.basename(__file__)
    script_name_no_extension, _ = os.path.splitext(script_name)

    parser = argparse.ArgumentParser(
        description="SEDCLI Binary File Viewer"
    )
    parser.add_argument("-f", "--file",
        help="Path to the binary file containing TCG Storage messages",
        #default="binary_log_file.bin_0x79c-0x7f3.bin"
        default="libsed_2550.bin"
        #default="libsed.bin"
        #default=None
    )
    parser.add_argument("-v", "--verbose",
        type=int,
        choices=[1, 2, 3],
        default=2,
        help="Increase output verbosity (1: minimal, 2: moderate, 3: high)"
    )
    parser.add_argument("-s", "--start-message",
        type=int,
        default=1,
        help="Index of the first message to parse (starting from 1)"
    )
    parser.add_argument("-e", "--end-message",
        type=int,
        default=1,#None,
        help="Index of the last message to parse"
        )
    parser.add_argument("-o", "--html-output",
        default=True,
        action="store_true",
        help="Write output to HTML file"
    )    
    parser.add_argument("-b", "--no-colors",
        default=False,
        action="store_true",
        help="Disable colors"
    )
    parser.add_argument("-V", "--version",
        action="store_true",
        help="Show the version"
    )
    args = parser.parse_args()

    # Add the script_name to the args structure
    args.script_name = script_name
    args.script_name_no_extension = script_name_no_extension

    start()

# Complete Discovery response parsing
# There is no status code in print_ComPacketFormat_Payload_PacketFormatPayload_CreditControlDataSubPacketPayload