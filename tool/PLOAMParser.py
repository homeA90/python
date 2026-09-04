import tkinter as tk
from tkinter import messagebox
import re

def dump_payload(payload_hex):
    """지정되지 않은 페이로드를 8바이트 단위 Hex 및 ASCII로 덤프"""
    lines = []
    for i in range(0, len(payload_hex), 16):
        chunk_hex = payload_hex[i:i+16]
        formatted_hex = " ".join([chunk_hex[j:j+2] for j in range(0, len(chunk_hex), 2)])
        chunk_ascii = ''.join([chr(int(chunk_hex[j:j+2], 16)) if 32 <= int(chunk_hex[j:j+2], 16) <= 126 else '.' for j in range(0, len(chunk_hex), 2)])
        lines.append(f"  ▶ {formatted_hex:<23} | {chunk_ascii}")
    return lines

# ==================================================================================================================================================
# 1. G-PON 파서 (틀 구성)
# ==================================================================================================================================================
def parse_gpon(hex_str, direction):
    if len(hex_str) != 26:
        return f"오류: G-PON PLOAM은 13바이트(26자리)여야 합니다.\n(현재 {len(hex_str)//2}바이트)\n\n입력 데이터:\n{hex_str}"

    result = []
    result.append("=" * 65)
    result.append(" PON PLOAM Message Parser (G-PON 13-byte Format)")
    result.append("=" * 65)
    result.append(f"Direction      : {direction if direction != 'Unknown' else 'Not Specified'}")
    result.append("-" * 65)
    result.append(" [ G-PON 세부 파싱 로직 추후 구현 예정 ]")
    result.append(f" Raw Hex       : {hex_str.upper()}")
    result.append("=" * 65)
    return "\n".join(result)

# ==================================================================================================================================================
# 2. XG-PON 파서 (틀 구성)
# ==================================================================================================================================================
def parse_xgpon(hex_str, direction):
    if len(hex_str) != 96:
        return f"오류: XG-PON PLOAM은 48바이트(96자리)여야 합니다.\n(현재 {len(hex_str)//2}바이트)\n\n입력 데이터:\n{hex_str}"

    result = []
    result.append("=" * 65)
    result.append(" PON PLOAM Message Parser (XG-PON 48-byte Format)")
    result.append("=" * 65)
    result.append(f"Direction      : {direction if direction != 'Unknown' else 'Not Specified'}")
    result.append("-" * 65)
    result.append(" [ XG-PON 세부 파싱 로직 추후 구현 예정 ]")
    result.append(f" Raw Hex       : {hex_str.upper()}")
    result.append("=" * 65)
    return "\n".join(result)




# ==================================================================================================================================================
# 3. XGS-PON 파서 (전체 구현) G.9807.1_C.11.2.6
# ==================================================================================================================================================
def parse_xgspon(hex_str, direction):
    if len(hex_str) != 96:
        return f"오류: XGS-PON PLOAM은 48바이트(96자리)여야 합니다.\n(현재 {len(hex_str)//2}바이트)\n\n입력 데이터:\n{hex_str}"

    # 공통 헤더 파싱 (4 bytes)
    onu_id = int(hex_str[0:4], 16)
    msg_id = int(hex_str[4:6], 16)
    seq_no = int(hex_str[6:8], 16)

    # Message ID 매핑
    ds_msg_type_map = {
        0x01: "Burst_Profile", 
        0x03: "Assign_ONU-ID",
        0x04: "Ranging_Time", 
        0x05: "Deactivate_ONU-ID", 
        0x06: "Disable_Serial_Number",
        0x09: "Request_Registration", 
        0x0A: "Assign_Alloc-ID", 
        0x0D: "Key_Control",
        0x12: "Sleep_Allow",
        0x13: "Calibration_Request",
        0x14: "Adjust_Tx_Wavelength",
        0x15: "Tuning_Control",
        0x17: "System_Profile",
        0x18: "Channel_Profile",
        0x19: "Protectoin_Control",
        0x1A: "Change_Power",
        0X1B: "Power_Consumption_Inquire",
        0x1C: "Rate_Control",
        0x1D: "Reboot_ONU",
        0x1E: "Collision_Feedback"
    }
    
    us_msg_type_map = {
        0x01: "Serial_Number_ONU", 
        0x02: "Registration", 
        0x05: "Key_Report",
        0x09: "Acknowledgement", 
        0x10: "Sleep_Request",
        0x1A: "Tuning_Response",
        0x1B: "Power_Consumption_Report",
        0x1c: "Rate_Response"
    }

    if direction == "US":
        msg_name = us_msg_type_map.get(msg_id, f"Unknown_US_{msg_id:02X}")
    elif direction == "DS":
        msg_name = ds_msg_type_map.get(msg_id, f"Unknown_DS_{msg_id:02X}")
    else:
        msg_name = f"DS: {ds_msg_type_map.get(msg_id, '?')} / US: {us_msg_type_map.get(msg_id, '?')}"

    result = []
    result.append("=" * 65)
    result.append(" PON PLOAM Message Parser (XGS-PON 48-byte Format)")
    result.append("=" * 65)
    result.append(f"Direction      : {direction if direction != 'Unknown' else 'Not Specified'}")
    result.append(f"ONU-ID         : 0x{onu_id:04X} ({'Broadcast' if onu_id == 0x3FF else onu_id})")
    result.append(f"Message ID     : 0x{msg_id:02X} ({msg_name})")
    result.append(f"Sequence No    : 0x{seq_no:02X} ({seq_no})")
    result.append("-" * 65)

    # 페이로드 추출 (36 bytes)
    payload = hex_str[8:80]
    formatted_payload = " ".join([payload[i:i+8] for i in range(0, len(payload), 8)])
    result.append(f"Payload (Raw)  : {formatted_payload.upper()}")
    result.append("-" * 65)

    # 세부 페이로드 분석
    result.append(f" [ 세부 페이로드 분석: {msg_name} ]")

    ################################################################################################################
    ############################################# DownStream 페이로드 ################################################
    ################################################################################################################
    if direction == "DS" and msg_id == 0x01:  # Burst_Profile
        # 1. 대상 ONU 식별 (Octet 1-2 적용)
        if onu_id == 0x03FF:
            target_onu = "0x03FF (Broadcast: All 2.5G & 10G US ONUs)"
        elif onu_id == 0x03FE:
            target_onu = "0x03FE (Broadcast: 10G US ONUs only)"
        else:
            target_onu = f"0x{onu_id:04X} (Directed to specific ONU)"

        # 2. 페이로드 파싱 (Octet 5 ~ 40)
        # Octet 5: Burst profile control (VVVV 0RPP)
        profile_ctrl = int(payload[0:2], 16)
        version = (profile_ctrl >> 4) & 0x0F
        r_bit = (profile_ctrl >> 2) & 0x01
        profile_index = profile_ctrl & 0x03
        r_str = "9.95328 Gbit/s" if r_bit == 1 else "2.48832 Gbit/s"

        # Octet 6: Upstream FEC indication (0000 000F)
        fec_ind = int(payload[2:4], 16) & 0x0F
        fec_str = "FEC on" if fec_ind == 1 else "FEC off"

        # Octet 7: Delimiter length (0000 DDDD)
        delimiter_len = int(payload[4:6], 16) & 0x0F

        # Octets 8-15: Delimiter (8 bytes)
        delimiter_pat = payload[6:22]

        # Octet 16: Preamble length (0000 LLLL)
        preamble_len = int(payload[22:24], 16) & 0x0F

        # Octet 17: Preamble repeat count        
        preamble_rep_raw = int(payload[24:26], 16)
        if r_bit == 0:
            preamble_rep = preamble_rep_raw & 0x1F  # 000P PPPP
        else:
            preamble_rep = preamble_rep_raw & 0xFF  # PPPP PPPP

        # Octets 18-25: Preamble pattern (8 bytes)
        preamble_pat = payload[26:42]

        # Octets 26-33: PON-TAG (8 bytes)
        pon_tag = payload[42:58]

        # Octets 34-40: Padding (7 bytes)
        padding = payload[58:72]
        
        result.append(f"  ▶ Target ONU       : {target_onu}")
        result.append(f"  ▶ Profile Control  : 0x{profile_ctrl:02X} (Version: {version}, Rate: {r_str}, Index: {profile_index})")
        result.append(f"  ▶ Upstream FEC     : 0x{fec_ind:02X} ({fec_str})")
        result.append(f"  ▶ Delimiter Length : {delimiter_len} octets")
        result.append(f"  ▶ Delimiter        : 0x{delimiter_pat.upper()}")
        result.append(f"  ▶ Preamble Length  : {preamble_len} octets")
        result.append(f"  ▶ Preamble Repeat  : {preamble_rep} times")
        result.append(f"  ▶ Preamble Pattern : 0x{preamble_pat.upper()}")
        result.append(f"  ▶ PON-TAG          : 0x{pon_tag.upper()}")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x03:  # Assign_ONU-ID
        # Octets 5-6: Assigned ONU-ID (10-bit value)
        assigned_id = int(payload[0:4], 16) & 0x03FF

        # Octets 7-10: Vendor_ID
        vendor_id_hex = payload[4:12]
        vendor_id_ascii = bytes.fromhex(vendor_id_hex).decode('ascii', errors='ignore')

        # Octets 11-14: VSSN
        vssn = payload[12:20]

        # Octet 15: Upstream nominal line rate indicator (0000 000U)
        us_rate_ind = int(payload[20:22], 16) & 0x01
        us_rate_str = "10 Gbit/s" if us_rate_ind == 1 else "2.5 Gbit/s"

        # Octets 16-40: Padding
        padding = payload[22:72]

        result.append(f"  ▶ Assigned ONU-ID  : 0x{assigned_id:04X} ({assigned_id})")
        result.append(f"  ▶ Vendor ID        : 0x{vendor_id_hex.upper()} (ASCII: '{vendor_id_ascii}')")
        result.append(f"  ▶ VSSN             : 0x{vssn.upper()}")
        result.append(f"  ▶ US Nominal Rate  : 0x{us_rate_ind:02X} ({us_rate_str})")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x04:  # Ranging_Time
        # Octet 5: Control octet (0000 0XSP)
        control_octet = int(payload[0:2], 16)
        p_bit = control_octet & 0x01
        s_bit = (control_octet >> 1) & 0x01
        
        if p_bit == 1:
            delay_type_str = "Absolute (Ignore S)"
        else:
            sign_str = "Negative (Decrease EqD)" if s_bit == 1 else "Positive (Increase EqD)"
            delay_type_str = f"Relative, {sign_str}"

        # Octets 6-9: Equalization-Delay
        eqd = int(payload[2:10], 16)
        eqd_us = eqd / 2488.32
        
        # Octets 10-13: Downstream PON-ID (Not used for XGS-PON)
        ds_pon_id = payload[10:18]
        
        # Octets 14-17: Upstream PON-ID (Not used for XGS-PON)
        us_pon_id = payload[18:26]
        
        # Octets 18-40: Padding
        padding = payload[26:72]

        result.append(f"  ▶ Control Octet    : 0x{control_octet:02X} ({delay_type_str})")
        result.append(f"  ▶ Equalization Delay: 0x{eqd:08X} ({eqd} bit periods @ 2.48832 Gbit/s), {eqd_us:.3f} us)")
        result.append(f"  ▶ DS PON-ID (N/A)  : 0x{ds_pon_id.upper()}")
        result.append(f"  ▶ US PON-ID (N/A)  : 0x{us_pon_id.upper()}")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x05:  # Deactivate_ONU-ID
        # Octets 5-40: Padding (Set to 0x00 by the transmitter; treated as "don't care" by the receiver)
        padding = payload[0:72]

        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x06:  # Disable_Serial_Number
        # Octet 5: Disable/enable
        option = int(payload[0:2], 16)
        if option == 0xFF:
            opt_str = "Deny upstream access to this ONU"
        elif option == 0x00:
            opt_str = "Allow upstream access to this ONU"
        elif option == 0x0F:
            opt_str = "Deny upstream access to all ONUs"
        elif option == 0xF0:
            opt_str = "Allow upstream access to all ONUs"
        elif option == 0x3F:
            opt_str = "Not used for XGS-PON"
        else:
            opt_str = "Unknown/Reserved"
            
        # Octets 6-9: Vendor_ID
        vendor_id_hex = payload[2:10]
        vendor_id_ascii = bytes.fromhex(vendor_id_hex).decode('ascii', errors='ignore')
        
        # Octets 10-13: VSSN
        vssn = payload[10:18]
        
        # Octets 14-40: Padding
        padding = payload[18:72]

        result.append(f"  ▶ Disable/Enable   : 0x{option:02X} ({opt_str})")
        result.append(f"  ▶ Vendor ID        : 0x{vendor_id_hex.upper()} (ASCII: '{vendor_id_ascii}')")
        result.append(f"  ▶ VSSN             : 0x{vssn.upper()}")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x09:  # Request_Registration
        # Octets 5-40: Padding (Set to 0x00 by the transmitter; treated as "don't care" by the receiver)
        padding = payload[0:72]

        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x0A:  # Assign_Alloc-ID
        # Octets 5-6: Alloc-ID-value (14 bits, aligned to LSB)
        alloc_id = int(payload[0:4], 16) & 0x3FFF
        
        # Octet 7: Alloc-ID-type
        alloc_type = int(payload[4:6], 16)
        if alloc_type == 0x01:
            type_str = "XGEM-encapsulated payload"
        elif alloc_type == 0xFF:
            type_str = "Deallocate this Alloc-ID"
        else:
            type_str = "Reserved"
            
        # Octets 8-9: Alloc-ID scope (Not used for XGS-PON)
        alloc_scope = payload[6:10]
        
        # Octets 10-40: Padding
        padding = payload[10:72]

        result.append(f"  ▶ Alloc-ID Value   : 0x{alloc_id:04X} ({alloc_id})")
        result.append(f"  ▶ Alloc-ID Type    : 0x{alloc_type:02X} ({type_str})")
        result.append(f"  ▶ Alloc-ID Scope   : 0x{alloc_scope.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x0D:  # Key_Control
        # Octet 5: Reserved
        reserved = payload[0:2]
        
        # Octet 6: Control flag (0000 000C)
        ctrl_flag = int(payload[2:4], 16) & 0x01
        ctrl_str = "Confirm the existing key" if ctrl_flag == 1 else "Generate and send a new key"
        
        # Octet 7: Key index (0000 00BB)
        key_index = int(payload[4:6], 16) & 0x03
        if key_index == 1:
            key_idx_str = "First key of a key pair"
        elif key_index == 2:
            key_idx_str = "Second key of a key pair"
        else:
            key_idx_str = "Unknown/Reserved"
            
        # Octet 8: Key_Length
        key_len_val = int(payload[6:8], 16)
        key_len_str = "256 bytes" if key_len_val == 0 else f"{key_len_val} bytes"
        
        # Octets 9-40: Padding
        padding = payload[8:72]

        result.append(f"  ▶ Reserved         : 0x{reserved.upper()}")
        result.append(f"  ▶ Control Flag     : 0x{ctrl_flag:02X} ({ctrl_str})")
        result.append(f"  ▶ Key Index        : 0x{key_index:02X} ({key_idx_str})")
        result.append(f"  ▶ Key Length       : 0x{key_len_val:02X} ({key_len_str})")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x12:  # Sleep_Allow
        # Octet 5: Control flag (0000 000A)
        ctrl_flag = int(payload[0:2], 16)
        a_bit = ctrl_flag & 0x01
        
        if a_bit == 1:
            ctrl_str = "Sleep allowed ON"
        elif a_bit == 0:
            ctrl_str = "Sleep allowed OFF"
        else:
            ctrl_str = "Reserved"
            
        # Octets 6-40: Padding
        padding = payload[2:72]

        result.append(f"  ▶ Control Flag     : 0x{ctrl_flag:02X} ({ctrl_str})")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id == 0x1D:  # Reboot_ONU
        # Octets 5-8: Vendor_ID
        vendor_id_hex = payload[0:8]
        vendor_id_ascii = bytes.fromhex(vendor_id_hex).decode('ascii', errors='ignore')
        
        # Octets 9-12: VSSN
        vssn = payload[8:16]
        
        # Octet 13: Reboot depth
        reboot_depth = int(payload[16:18], 16)
        if reboot_depth == 0x0:
            depth_str = "MIB Reset"
        elif reboot_depth == 0x1:
            depth_str = "Perform equivalent of OMCI reboot"
        elif reboot_depth == 0x2:
            depth_str = "Perform equivalent of power cycle reboot"
        elif reboot_depth == 0x3:
            depth_str = "Configuration reset, then perform MIB reset and reboot"
        else:
            depth_str = "Reserved"

        # Octet 14: Reboot image
        reboot_image = int(payload[18:20], 16)
        if reboot_image == 0x0:
            image_str = "Load and execute the image that is currently committed"
        elif reboot_image == 0x1:
            image_str = "Load and execute the image that is not currently committed"
        else:
            image_str = "Unknown/Reserved"
            
        # Octet 15: ONU state
        onu_state = int(payload[20:22], 16)
        if onu_state == 0x0:
            state_str = "Reboot if ONU is in any state"
        elif onu_state == 0x1:
            state_str = "Reboot only if ONU in states O1, O2-3"
        else:
            state_str = "Unknown/Reserved"
            
        # Octet 16: Flags
        flags = int(payload[22:24], 16)
        call_state_flag = flags & 0x03  # Bits 2-1
        if call_state_flag == 0x00:
            flag_str = "Reboot regardless of POTS/VoIP call state"
        elif call_state_flag == 0x01:
            flag_str = "Reboot only if no POTS/VoIP calls are in progress"
        elif call_state_flag == 0x02:
            flag_str = "Reboot only if no emergency call is in progress"
        else:
            flag_str = "Reserved"
            
        # Octets 17-40: Padding
        padding = payload[24:72]

        result.append(f"  ▶ Vendor ID        : 0x{vendor_id_hex.upper()} (ASCII: '{vendor_id_ascii}')")
        result.append(f"  ▶ VSSN             : 0x{vssn.upper()}")
        result.append(f"  ▶ Reboot Depth     : 0x{reboot_depth:02X} ({depth_str})")
        result.append(f"  ▶ Reboot Image     : 0x{reboot_image:02X} ({image_str})")
        result.append(f"  ▶ ONU State        : 0x{onu_state:02X} ({state_str})")
        result.append(f"  ▶ Flags            : 0x{flags:02X} ({flag_str})")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "DS" and msg_id in (0x13, 0x14, 0x15, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C): # 사용하지 않는 메시지 타입
        # 0x13: Calibration_Request
        # 0x14: Adjust_Tx_Wavelength
        # 0x15: Tuning_Control
        # 0x17: System_Profile
        # 0x18: Channel_Profile
        # 0x19: Protection_Control
        # 0x1A: Change_Power_Level
        # 0x1B: Power_Consumption_Inquire
        # 0x1C: Rate_Control
        
        # Octets 5-40: Raw payload (Not applicable to XGS-PON)
        raw_payload = payload[0:72]

        result.append(f"  ▶ 참고 사항    : XGS-PON 규격에 해당하지 않음")
        result.append(f"  ▶ 상세 설명    : [ITU-T G.989.3] 규격에 정의된 메시지이나, XGS-PON 시스템에서는 사용되지 않습니다.")
        result.append(f"  ▶ 원본 페이로드: 0x{raw_payload.upper()}")
    
    ###############################################################################################################
    ############################################# UpStream 페이로드 ################################################
    ###############################################################################################################
    elif direction == "US" and msg_id == 0x01:  # Serial_Number_ONU
        # Octets 5-8: Vendor_ID
        vendor_id_hex = payload[0:8]
        vendor_id_ascii = bytes.fromhex(vendor_id_hex).decode('ascii', errors='ignore')
        
        # Octets 9-12: VSSN
        vssn = payload[8:16]
        
        # Octets 13-16: Random_delay
        rand_delay_hex = payload[16:24]
        rand_delay_val = int(rand_delay_hex, 16)
        
        # Octets 17-18: Correlation tag (Not used for XGS-PON)
        correlation_tag = payload[24:28]
        
        # Octets 19-22: Current downstream PON-ID (Not used for XGS-PON)
        current_ds_pon_id = payload[28:36]
        
        # Octets 23-26: Current upstream PON-ID (Not used for XGS-PON)
        current_us_pon_id = payload[36:44]
        
        # Octets 27-34: Calibration record status (Not used for XGS-PON)
        cal_record_status = payload[44:60]
        
        # Octet 35: Tuning granularity (Not used for XGS-PON)
        tuning_granularity = payload[60:62]
        
        # Octet 36: Step tuning time (Not used for XGS-PON)
        step_tuning_time = payload[62:64]
        
        # Octet 37: Upstream line rate capability (0000 00HL)
        us_rate_cap = int(payload[64:66], 16)
        h_bit = (us_rate_cap >> 1) & 0x01
        l_bit = us_rate_cap & 0x01
        
        h_str = "Supported" if h_bit == 1 else "Not supported"
        l_str = "Supported" if l_bit == 0 else "Not supported"  # L=0 means supported
        
        # Octet 38: Attenuation (Not used for XGS-PON)
        attenuation = payload[66:68]
        
        # Octet 39: Power levelling capability (Not used for XGS-PON)
        power_levelling = payload[68:70]
        
        # Octet 40: Padding
        padding = payload[70:72]

        result.append(f"  ▶ Vendor ID        : 0x{vendor_id_hex.upper()} (ASCII: '{vendor_id_ascii}')")
        result.append(f"  ▶ VSSN             : 0x{vssn.upper()}")
        result.append(f"  ▶ Random Delay     : 0x{rand_delay_hex.upper()} ({rand_delay_val} bit periods @ 2.48832 Gbit/s)")
        result.append(f"  ▶ Correlation Tag  : 0x{correlation_tag.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Current DS PON-ID: 0x{current_ds_pon_id.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Current US PON-ID: 0x{current_us_pon_id.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Cal Record Status: 0x{cal_record_status.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Tuning Granularity: 0x{tuning_granularity.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Step Tuning Time : 0x{step_tuning_time.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ US Line Rate Cap : 0x{us_rate_cap:02X}")
        result.append(f"     - 9.95328 Gbit/s: {h_str}")
        result.append(f"     - 2.48832 Gbit/s: {l_str}")
        result.append(f"  ▶ Attenuation      : 0x{attenuation.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Power Levelling  : 0x{power_levelling.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "US" and msg_id == 0x02:  # Registration
        # Octets 5-40: Registration_ID (36 bytes)
        reg_id_hex = payload[0:72]
        reg_id_ascii = bytes.fromhex(reg_id_hex).decode('ascii', errors='ignore').strip('\x00')

        result.append(f"  ▶ Registration ID  : 0x{reg_id_hex.upper()}")
        result.append(f"  ▶ Registration ASCII: '{reg_id_ascii}'")

    elif direction == "US" and msg_id == 0x05:  # Key_Report
        # Octet 5: Report type (0000 000R)
        report_type = int(payload[0:2], 16) & 0x01
        report_str = "Report on existing key" if report_type == 1 else "New key"
        
        # Octet 6: Key index (0000 00BB)
        key_index = int(payload[2:4], 16) & 0x03
        if key_index == 1:
            key_idx_str = "First key of a key pair"
        elif key_index == 2:
            key_idx_str = "Second key of a key pair"
        else:
            key_idx_str = "Unknown/Reserved"
            
        # Octet 7: Fragment number (0000 0FFF)
        fragment_num = int(payload[4:6], 16) & 0x07
        
        # Octet 8: Reserved
        reserved = payload[6:8]
        
        # Octets 9-40: Key_Fragment (32 bytes)
        key_fragment = payload[8:72]

        result.append(f"  ▶ Report Type      : 0x{report_type:02X} ({report_str})")
        result.append(f"  ▶ Key Index        : 0x{key_index:02X} ({key_idx_str})")
        result.append(f"  ▶ Fragment Number  : 0x{fragment_num:02X} ({fragment_num})")
        result.append(f"  ▶ Reserved         : 0x{reserved.upper()}")
        result.append(f"  ▶ Key Fragment     : 0x{key_fragment.upper()}")

    elif direction == "US" and msg_id == 0x09:  # Acknowledgement
        # Octet 5: Completion_code
        comp_code = int(payload[0:2], 16)
        if comp_code == 0x00:
            comp_str = "OK"
        elif comp_code == 0x01:
            comp_str = "No message to send"
        elif comp_code == 0x02:
            comp_str = "Busy, preparing a response"
        elif comp_code == 0x03:
            comp_str = "Unknown message type"
        elif comp_code == 0x04:
            comp_str = "Parameter error"
        elif comp_code == 0x05:
            comp_str = "Processing error"
        else:
            comp_str = "Reserved"
            
        # Octet 6: Attenuation (Not used for XGS-PON)
        attenuation = payload[2:4]
        
        # Octet 7: Power levelling capability (Not used for XGS-PON)
        power_levelling = payload[4:6]
        
        # Octets 8-40: Padding
        padding = payload[6:72]

        result.append(f"  ▶ Completion Code  : 0x{comp_code:02X} ({comp_str})")
        result.append(f"  ▶ Attenuation      : 0x{attenuation.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Power Levelling  : 0x{power_levelling.upper()} (N/A for XGS-PON)")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "US" and msg_id == 0x10:  # Sleep_Request
        # Octet 5: Activity_level
        activity_level = int(payload[0:2], 16)
        if activity_level == 0x00:
            act_str = "Sleep_Request (Awake)"
        elif activity_level == 0x03:
            act_str = "Sleep_Request (WSleep) - Watchful sleep mode request"
        else:
            act_str = "Reserved"
            
        # Octets 6-40: Padding
        padding = payload[2:72]

        result.append(f"  ▶ Activity Level   : 0x{activity_level:02X} ({act_str})")
        result.append(f"  ▶ Padding          : 0x{padding.upper()}")

    elif direction == "US" and msg_id in (0x1A, 0x1B, 0x1C): # 사용하지 않는 메시지 타입
        # 0x1A: Tuning_Response
        # 0x1B: Power_Consumption_Report
        # 0x1C: Rate_Response
        
        # Octets 5-40: Raw payload (Not applicable to XGS-PON)
        raw_payload = payload[0:72]

        result.append(f"  ▶ 참고 사항    : XGS-PON 규격에 해당하지 않음")
        result.append(f"  ▶ 상세 설명    : [ITU-T G.989.3]의 표 11-31과 동일하며, XGS-PON과는 무관함")
        result.append(f"  ▶ 원본 페이로드: 0x{raw_payload.upper()}")

    else:
        # 지정되지 않은 메시지의 경우 Hex Dump 출력
        result.extend(dump_payload(payload))

    result.append("-" * 65)
    
    # 7. MIC 파싱 (8 bytes)
    mic = hex_str[80:96]
    result.append(f"MIC (8 bytes)  : 0x{mic.upper()}")
    result.append("=" * 65)

    return "\n".join(result)

# ==========================================
# 통합 파싱 라우터
# ==========================================
def process_parsing():
    input_text = txt_input.get("1.0", tk.END).strip()
    pon_type = pon_type_var.get()
    
    if not input_text:
        messagebox.showwarning("경고", "변환할 로그를 입력하십시오.")
        return
    
    # 1. 방향 추출 및 정제 (이후 하위 함수에 전달됨)
    direction = "Unknown"
    dir_match = re.search(r'(US|DS)\s+PLOAM', input_text, re.IGNORECASE)
    if dir_match:
        direction = dir_match.group(1).upper()
        
    match = re.search(r'\{\s*(.*?)\s*\}', input_text)
    if match:
        hex_str = match.group(1).replace(' ', '').strip()
    else:
        hex_str = input_text.replace(' ', '').strip()

    # 2. PON 타입에 따른 라우팅
    if pon_type == "G-PON":
        parsed_result = parse_gpon(hex_str, direction)
    elif pon_type == "XG-PON":
        parsed_result = parse_xgpon(hex_str, direction)
    elif pon_type == "XGS-PON":
        parsed_result = parse_xgspon(hex_str, direction)  # 수정: 함수명과 인자 일치시킴
    else:
        parsed_result = "지원하지 않는 PON 타입입니다."

    txt_output.delete("1.0", tk.END)
    txt_output.insert(tk.END, parsed_result)

def clear_text():
    txt_input.delete("1.0", tk.END)
    txt_output.delete("1.0", tk.END)

# ==========================================
# GUI 인터페이스 구성
# ==========================================
root = tk.Tk()
root.title("Multi-PON PLOAM Hex Parser")
root.geometry("720x760")

# PON 타입 선택 라디오 버튼 영역
frame_radio = tk.Frame(root)
frame_radio.pack(pady=(15, 5))

tk.Label(frame_radio, text="[ PON 타입 선택 ]", font=("Arial", 10, "bold")).pack(side="left", padx=10)
pon_type_var = tk.StringVar(value="XGS-PON")
tk.Radiobutton(frame_radio, text="G-PON", variable=pon_type_var, value="G-PON").pack(side="left", padx=10)
tk.Radiobutton(frame_radio, text="XG-PON", variable=pon_type_var, value="XG-PON").pack(side="left", padx=10)
tk.Radiobutton(frame_radio, text="XGS-PON", variable=pon_type_var, value="XGS-PON").pack(side="left", padx=10)

# 로그 입력 영역
tk.Label(root, text="[ 원본 PLOAM 로그 입력 ]").pack(anchor="w", padx=10, pady=5)
txt_input = tk.Text(root, height=5, width=95, font=("Consolas", 10))
txt_input.pack(padx=10)
txt_input.insert(tk.END, "[0x4869d96f] DS PLOAM { 03fe0144 040008ce 99ce5e50 28b41f08 7faaaaaa aaaaaaaa aa000000 00000000 00000000 00000000 c473dde3 b922ea10 }")

# 실행 버튼 영역
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_convert = tk.Button(frame_buttons, text="변환 (Convert)", command=process_parsing, width=15, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_convert.pack(side="left", padx=5)

btn_clear = tk.Button(frame_buttons, text="초기화 (Clear)", command=clear_text, width=15)
btn_clear.pack(side="left", padx=5)

# 파싱 결과 출력 영역
tk.Label(root, text="[ 파싱 결과 ]").pack(anchor="w", padx=10, pady=5)
txt_output = tk.Text(root, height=28, width=100, font=("Consolas", 10), bg="#1E1E1E", fg="#00FF00")
txt_output.pack(padx=10, pady=5)

root.mainloop()