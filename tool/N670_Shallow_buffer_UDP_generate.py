#!/usr/bin/env python3
from scapy.all import Ether, IP, UDP, Raw, wrpcap
import os
import sys
import subprocess
import time

# ================= [ 사용자 설정 섹션 ] =================
MY_IFACE = "eth0"  # 사용하시는 인터페이스 (예: eth1)

SRC_MAC = "00:00:22:33:44:55"
DST_MAC = "00:00:66:77:88:99" 
SRC_IP  = "111.1.1.152"
DST_IP  = "111.1.1.3"
SRC_PORT = 8192
DST_PORT = 5005

# 💡 UDP는 헤더가 8바이트(TCP는 20바이트)이므로, 
# 1518바이트 꽉 찬 프레임을 만들려면 Payload를 1472로 설정해야 합니다.
PAYLOAD_SIZE = 1472 
PACKET_COUNT = 70  # UDP는 시퀀스가 없으므로 대량으로 쏴보기 좋습니다.

TEMP_PCAP = "temp_udp_fast_stream.pcap"
# ========================================================

def send_udp_with_tcpreplay():
    if os.geteuid() != 0:
        print("❌ sudo 권한 필요")
        sys.exit(1)

    print(f"📦 {PACKET_COUNT}개 UDP 패킷 조립(IP ID 순차 증가) 및 Timestamp 조작 중...")
    packet_list = []
    
    current_ip_id = 100  # 시작 IP ID 설정
    payload_data = b"B" * PAYLOAD_SIZE  # TCP와 구분하기 위해 'B'로 채움
    
    # 기준 시간 설정 (현재 시간)
    base_time = time.time()

    for i in range(PACKET_COUNT):
        # 💡 TCP() 대신 UDP()를 사용하며, seq/ack/window/flags 옵션이 모두 빠집니다.
        pkt = Ether(src=SRC_MAC, dst=DST_MAC) / \
              IP(src=SRC_IP, dst=DST_IP, id=current_ip_id) / \
              UDP(sport=SRC_PORT, dport=DST_PORT) / \
              Raw(load=payload_data)
        
        # 패킷에 찍히는 시간을 0.000001초(1마이크로초) 간격으로 강제 주입
        pkt.time = base_time + (i * 0.000001)
        
        packet_list.append(pkt)
        
        # UDP는 시퀀스 번호(seq)가 없으므로 IP ID만 1씩 증가시킵니다.
        current_ip_id += 1 
        
        if current_ip_id > 65535:
            current_ip_id = 0

    print(f"💾 패킷을 임시 PCAP 파일({TEMP_PCAP})로 저장 중...")
    wrpcap(TEMP_PCAP, packet_list)

    try:
        print(f"🚀 tcpreplay 실행")
        
        # tcpreplay 실행 (--topspeed 옵션 유지)
        cmd = ["tcpreplay", "-i", MY_IFACE, "--topspeed", TEMP_PCAP]
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ tcpreplay 실행 중 에러 발생: {e}")
    except FileNotFoundError:
        print(f"\n❌ tcpreplay 명령어를 찾을 수 없습니다.")
    finally:
        # PCAP 파일 삭제
        if os.path.exists(TEMP_PCAP):
            os.remove(TEMP_PCAP)
            print(f"🧹 임시 파일({TEMP_PCAP}) 삭제 완료!")

if __name__ == "__main__":
    send_udp_with_tcpreplay()