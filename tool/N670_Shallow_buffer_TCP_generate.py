#!/usr/bin/env python3
from scapy.all import Ether, IP, TCP, Raw, wrpcap
import os
import sys
import subprocess
import time

# ================= [ 사용자 설정 섹션 ] =================
MY_IFACE = "eth0"  # 사용하시는 인터페이스

SRC_MAC = "00:00:22:33:44:55"
DST_MAC = "00:00:66:77:88:99" 
SRC_IP  = "111.1.1.152"
DST_IP  = "111.1.1.3"
SRC_PORT = 8192
DST_PORT = 5005

PAYLOAD_SIZE = 1460 
PACKET_COUNT = 48  # LRO 병합 확인을 위해 나중에 10~100 정도로 늘려보세요!

TEMP_PCAP = "temp_fast_stream.pcap"
# ========================================================

def send_with_tcpreplay():
    if os.geteuid() != 0:
        print("❌ sudo 권한 필요")
        sys.exit(1)

    print(f"📦 {PACKET_COUNT}개 패킷 조립(IP ID 순차 증가) 및 Timestamp 조작 중...")
    packet_list = []
    
    current_seq = 0
    current_ip_id = 100  # 💡 시작 IP ID 설정 (임의의 숫자 100부터 시작)
    
    payload_data = b"A" * PAYLOAD_SIZE
    
    # 기준 시간 설정 (현재 시간)
    base_time = time.time()

    for i in range(PACKET_COUNT):
        # 💡 [핵심 포인트] IP 헤더에 id=current_ip_id 를 명시적으로 추가!
        pkt = Ether(src=SRC_MAC, dst=DST_MAC) / \
              IP(src=SRC_IP, dst=DST_IP, id=current_ip_id) / \
              TCP(sport=SRC_PORT, dport=DST_PORT, flags="A", 
                  seq=current_seq, ack=1, window=8192) / \
              Raw(load=payload_data)
        
        # 패킷에 찍히는 시간을 0.000001초(1마이크로초) 간격으로 강제 주입
        pkt.time = base_time + (i * 0.000001)
        
        packet_list.append(pkt)
        
        # 다음 패킷을 위해 값들 증가
        current_seq += PAYLOAD_SIZE
        current_ip_id += 1  # 💡 IP ID도 1씩 증가 (하드웨어 LRO 엔진 조건 만족)
        
        # IP ID는 16비트(0~65535)이므로 한 바퀴 돌면 0으로 초기화 처리 (대량 패킷 쏠 때 에러 방지)
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
    send_with_tcpreplay()