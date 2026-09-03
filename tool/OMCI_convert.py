import customtkinter as ctk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import re
import subprocess
import os
import tempfile

class OMCIToPcapApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("OMCI to PCAP Converter")
        self.geometry("1000x750")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        
        self.wireshark_path = r"C:\Program Files\Wireshark\text2pcap.exe"
        
        self.setup_ui()
        
    def setup_ui(self):
        # 상단 공통 버튼 영역
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(fill="x", padx=20, pady=(10, 5))
        
        self.btn_lua_guide = ctk.CTkButton(self.frame_top, text="omci.lua 설치 방법", width=120, fg_color="#17a2b8", hover_color="#138496", command=self.show_lua_guide)
        self.btn_lua_guide.pack(side="left")

        self.btn_settings = ctk.CTkButton(self.frame_top, text="Wireshark 경로 설정", width=120, command=self.open_settings)
        self.btn_settings.pack(side="right")
        
        # 탭 뷰 영역
        self.tabview = ctk.CTkTabview(self, height=450)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.tab_text = self.tabview.add("텍스트 직접 붙여넣기")
        self.tab_file = self.tabview.add("TXT 파일 불러오기")
        
        self.setup_tab_text()
        self.setup_tab_file()
        
        # 하단 Pcap 변환 실행 영역
        self.lbl_output = ctk.CTkLabel(self, text="Pcap 저장 위치 설정", font=("Arial", 14, "bold"))
        self.lbl_output.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.frame_output = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_output.pack(fill="x", padx=20, pady=(5, 10))
        
        self.entry_output = ctk.CTkEntry(self.frame_output, placeholder_text="저장할 Pcap 파일 경로를 지정하세요", fg_color="#ffcc00", text_color="black")
        self.entry_output.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_browse = ctk.CTkButton(self.frame_output, text="경로 찾기", width=100, command=self.browse_output)
        self.btn_browse.pack(side="right")
        
        self.btn_convert = ctk.CTkButton(self, text="PCAP 변환 실행", height=45, font=("Arial", 15, "bold"), command=self.process_and_convert)
        self.btn_convert.pack(fill="x", padx=20, pady=(0, 15))

    def setup_tab_text(self):
        frame_label = ctk.CTkFrame(self.tab_text, fg_color="transparent")
        frame_label.pack(fill="x", pady=(5, 0))
        
        lbl_input = ctk.CTkLabel(frame_label, text="OMCI 원본 로그 입력", font=("Arial", 14, "bold"))
        lbl_input.pack(side="left")
        
        btn_help = ctk.CTkButton(frame_label, text="OMCI 로그 입력 형태", width=100, height=24, fg_color="#555555", hover_color="#333333", command=self.show_log_example)
        btn_help.pack(side="left", padx=10)
        
        btn_validate = ctk.CTkButton(frame_label, text="로그 검증", width=100, height=24, fg_color="#28a745", hover_color="#218838", command=self.validate_text_input)
        btn_validate.pack(side="right")
        
        self.text_input = ctk.CTkTextbox(self.tab_text, height=200, fg_color="#ffcc00", text_color="black", wrap="none")
        self.text_input.pack(fill="both", expand=True, pady=(5, 5))
        
        self.lbl_summary_title = ctk.CTkLabel(self.tab_text, text="검증 결과:", font=("Arial", 12, "bold"))
        self.lbl_summary_title.pack(anchor="w")
        
        self.text_summary = ctk.CTkTextbox(self.tab_text, height=80, fg_color="#f4f4f4", text_color="black")
        self.text_summary.pack(fill="x", pady=(0, 5))
        self.text_summary.configure(state="disabled")

    def setup_tab_file(self):
        lbl_file = ctk.CTkLabel(self.tab_file, text="OMCI 로그가 저장된 TXT 파일을 선택하세요", font=("Arial", 14, "bold"))
        lbl_file.pack(anchor="w", pady=(20, 10))
        
        frame_file_input = ctk.CTkFrame(self.tab_file, fg_color="transparent")
        frame_file_input.pack(fill="x")
        
        self.entry_input_file = ctk.CTkEntry(frame_file_input, placeholder_text="로그 파일 경로", fg_color="#e0e0e0", text_color="black")
        self.entry_input_file.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_file_browse = ctk.CTkButton(frame_file_input, text="파일 찾기", width=100, command=self.browse_input_file)
        btn_file_browse.pack(side="right")

    def show_log_example(self):
        example_win = ctk.CTkToplevel(self)
        example_win.title("입력 로그 형태 예시")
        example_win.geometry("1000x200")
        example_win.transient(self)
        
        lbl = ctk.CTkLabel(example_win, text="아래와 같은 형태의 원본 로그를 공백 여부에 관계없이 그대로 붙여넣으세요.", font=("Arial", 13, "bold"))
        lbl.pack(anchor="w", padx=20, pady=(15, 5))
        
        example_text = (
            "[   891]    31.821343 US 2de6240a 002fa10b: 11750.Create: MAC bridge port configuration data(002f).a10b: result 00\n"
            "   00000000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................\n"
            "   00000010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................"

            "[   892]    31.836664 DS 2de7440a 0054a10b: 11751.Create: VLAN tagging filter data(0054).a10b\n"
            "   00000000  0b af 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................\n"
            "   00000010  00 00 00 00 00 00 00 00 10 01 00 00 00 00 00 00   ................"
        )
        
        textbox = ctk.CTkTextbox(example_win, height=100, fg_color="#333333", text_color="white", font=("Consolas", 12), wrap="none")
        textbox.insert("1.0", example_text)
        textbox.configure(state="disabled") 
        textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def show_lua_guide(self):
        guide_win = ctk.CTkToplevel(self)
        guide_win.title("Wireshark omci.lua 플러그인 설치 및 사용 방법")
        guide_win.geometry("750x350")
        guide_win.transient(self)
        
        lbl = ctk.CTkLabel(guide_win, text="[ omci.lua 플러그인 셋업 가이드 ]", font=("Arial", 14, "bold"))
        lbl.pack(anchor="w", padx=20, pady=(15, 10))
        
        guide_text = (
            "1. 플러그인 다운로드\n"
            "   - 아래 GitHub 주소로 접속하여 'omci.lua' 파일을 다운로드합니다.\n"
            "   - https://github.com/0liv1er/omci-wireshark-dissector\n\n"
            "2. 플러그인 폴더에 복사\n"
            "   - Wireshark 실행 후 상단 메뉴에서 [도움말(Help)] -> [Wireshark 정보(About Wireshark)] -> [폴더(Folders)] 탭으로 이동합니다.\n"
            "   - 'Personal Lua Plugins' 또는 'Global Lua Plugins' 경로를 확인하고 해당 폴더를 열어 omci.lua 파일을 넣습니다.\n\n"
            "3. Wireshark 재실행 및 적용\n"
            "   - Wireshark를 완전히 종료한 후 다시 실행하거나, 단축키 [Ctrl + Shift + L]을 눌러 스크립트를 리로드합니다.\n"
            "   - 본 툴은 변환 시 0x88b5 이더넷 헤더를 씌우도록 설계되었으므로, 해당 플러그인이 적용되어 있다면\n"
            "     PCAP 파일 열기 시 별도의 설정 없이 자동으로 OMCI 패킷이 완벽하게 디코딩됩니다."
        )
        
        textbox = ctk.CTkTextbox(guide_win, fg_color="#333333", text_color="white", font=("Arial", 13), wrap="word")
        textbox.insert("1.0", guide_text)
        # 사용자가 링크를 드래그해서 복사할 수 있도록 disabled 대신 readonly 형태의 바인딩을 추가하거나 단순 disabled로 설정
        textbox.configure(state="disabled")
        textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def open_settings(self):
        setting_win = ctk.CTkToplevel(self)
        setting_win.title("설정")
        setting_win.geometry("500x150")
        setting_win.transient(self)
        
        lbl = ctk.CTkLabel(setting_win, text="text2pcap.exe 경로:")
        lbl.pack(anchor="w", padx=20, pady=(20, 5))
        
        entry_path = ctk.CTkEntry(setting_win, width=400)
        entry_path.insert(0, self.wireshark_path)
        entry_path.pack(padx=20)
        
        def save_path():
            self.wireshark_path = entry_path.get()
            setting_win.destroy()
            
        btn_save = ctk.CTkButton(setting_win, text="저장", command=save_path)
        btn_save.pack(pady=15)

    def browse_input_file(self):
        filename = fd.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            self.entry_input_file.delete(0, "end")
            self.entry_input_file.insert(0, filename)
            
    def browse_output(self):
        filename = fd.asksaveasfilename(defaultextension=".pcap", filetypes=[("PCAP files", "*.pcap")])
        if filename:
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, filename)

    def analyze_logs(self, raw_text):
        valid_packets = []
        invalid_seqs = []
        error_details = []
        total = 0

        blocks = re.split(r'(?=\[\s*\d+\s*\])', raw_text)
        
        for block in blocks:
            if not block.strip():
                continue
                
            seq_match = re.search(r'\[\s*(\d+)\s*\]', block)
            if not seq_match:
                continue
            
            total += 1
            seq_num = seq_match.group(1)
            
            header_match = re.search(r'(?:DS|US)\s+([0-9a-fA-F]{8})\s+([0-9a-fA-F]{8})', block)
            payload_matches = re.findall(r'\s*[0-9a-fA-F]{8}\s+((?:[0-9a-fA-F]{2}\s){1,16})', block)
            
            payload_hex = "".join([m.replace(' ', '') for m in payload_matches])
            
            if header_match and len(payload_hex) >= 64:
                header_hex = header_match.group(1) + header_match.group(2)
                payload_hex = payload_hex[:64]
                valid_packets.append((header_hex, payload_hex))
            else:
                invalid_seqs.append(seq_num)
                error_details.append(f"[{seq_num}] 형태 오류")

        valid = len(valid_packets)
        invalid = len(invalid_seqs)
        
        return valid_packets, invalid_seqs, total, valid, invalid, error_details

    def validate_text_input(self):
        raw_text = self.text_input.get("1.0", "end-1c")
        if not raw_text.strip():
            self.update_summary("원본 로그를 입력하세요.")
            return None
            
        _, invalid_seqs, total, valid, invalid, error_details = self.analyze_logs(raw_text)
        
        summary_text = f"총 갯수: {total} 개 | 정상: {valid} 개 | 인식실패: {invalid} 개\n"
        summary_text += "-" * 50 + "\n"
        
        if invalid > 0:
            summary_text += " | ".join(error_details)
        else:
            summary_text += "모든 로그가 정상적인 형태입니다."
            
        self.update_summary(summary_text)
        
        if invalid > 0:
            error_msg = f"형태가 손상된 로그가 {invalid}개 발견되었습니다.\n수정 후 다시 시도하십시오.\n\n[오류 발생 시퀀스 번호]\n" + ", ".join(invalid_seqs)
            mb.showerror("로그 형태 오류", error_msg)
            return False
        return True

    def update_summary(self, text):
        self.text_summary.configure(state="normal")
        self.text_summary.delete("1.0", "end")
        self.text_summary.insert("1.0", text)
        self.text_summary.configure(state="disabled")

    def generate_hex_text(self, packets):
        result_lines = []
        for header, payload in packets:
            full_hex = (header + payload)
            row1, row2, row3 = full_hex[0:32], full_hex[32:64], full_hex[64:96]
            
            def format_row(offset, data):
                return f"{offset} " + " ".join(data[i:i+2] for i in range(0, len(data), 2))
                
            result_lines.append(format_row("000000", row1))
            result_lines.append(format_row("000010", row2))
            result_lines.append(format_row("000020", row3))
            result_lines.append("")
            
        return "\n".join(result_lines)

    def process_and_convert(self):
        raw_text = ""
        current_tab = self.tabview.get()
        
        if current_tab == "텍스트 직접 붙여넣기":
            raw_text = self.text_input.get("1.0", "end-1c")
            if not self.validate_text_input():
                return
        elif current_tab == "TXT 파일 불러오기":
            input_file = self.entry_input_file.get()
            if not input_file or not os.path.exists(input_file):
                mb.showerror("오류", "유효한 텍스트 파일을 선택하세요.")
                return
            try:
                with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
                    raw_text = f.read()
            except Exception as e:
                mb.showerror("파일 읽기 오류", f"파일을 읽는 중 오류가 발생했습니다.\n{str(e)}")
                return

        output_file = self.entry_output.get()
        if not output_file:
            mb.showerror("오류", "저장할 PCAP 파일 경로를 지정하세요.")
            return
            
        if not os.path.exists(self.wireshark_path):
            mb.showerror("오류", f"text2pcap.exe를 찾을 수 없습니다.\n현재 경로: {self.wireshark_path}")
            return

        valid_packets, invalid_seqs, total, valid, invalid, _ = self.analyze_logs(raw_text)
        
        if invalid > 0:
            error_msg = f"변환이 차단되었습니다. 파일 내에 형태가 손상된 로그가 {invalid}개 있습니다.\n\n[오류 발생 시퀀스 번호]\n" + ", ".join(invalid_seqs)
            mb.showerror("로그 형태 오류", error_msg)
            return
            
        if valid == 0:
            mb.showerror("오류", "유효한 OMCI 패킷을 찾을 수 없습니다.")
            return
            
        formatted_text = self.generate_hex_text(valid_packets)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_txt:
            temp_txt.write(formatted_text)
            temp_txt_path = temp_txt.name
            
        try:
            cmd = [self.wireshark_path, "-e", "0x88b5", temp_txt_path, output_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                mb.showinfo("성공", f"PCAP 변환이 완료되었습니다.\n총 패킷 수: {valid}개\n저장 경로: {output_file}")
            else:
                mb.showerror("Wireshark 오류", f"변환 중 오류가 발생했습니다.\n{result.stderr}")
        except Exception as e:
            mb.showerror("실행 오류", f"명령어 실행 중 예외가 발생했습니다.\n{str(e)}")
        finally:
            os.remove(temp_txt_path)

if __name__ == "__main__":
    app = OMCIToPcapApp()
    app.mainloop()