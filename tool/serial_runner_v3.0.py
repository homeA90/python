# 실행파일(exe) 만드는법
# cd c:\hub4com-2.1.0.0-386 로 이동
# 이동한 경로해서 pyinstaller -w -F --add-data "hub4com-2.1.0.0-386.zip;." "serial runner_old.py"  입력
# hub4com과 합치려면 저 압축파일이 같이 있어야함.
# 만약 hub4com 버전이 바뀌었거나 파일명을 다르게 하고싶으면 아래 코드 485줄에서  zip_name 변수를 .exe로 만들때 지정한 이름으로 변경하고, pyinstaller 시 add-data를 zip_name 변수값과 동일하게 지정하면 됨 


import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import subprocess
import threading
import time
import queue
import traceback
import zipfile

# 파이썬 버전 차이로 인한 에러를 막기 위해 윈도우 고유 상수값 직접 지정
CREATE_NO_WINDOW = 0x08000000

# --- 둥근 모서리 버튼을 위한 커스텀 클래스 ---
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, width, height, corner_radius, bg_color, fg_color, font, command=None, hover_color=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color or bg_color
        self.text_val = text
        
        self.rect = self._create_round_rect(0, 0, width, height, corner_radius, fill=bg_color)
        self.text_item = self.create_text(width/2, height/2, text=text, font=font, fill=fg_color)
        
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def _create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.create_polygon(points, **kwargs, smooth=True)

    def config(self, text=None, bg=None, fg=None, **kwargs):
        if text is not None:
            self.itemconfigure(self.text_item, text=text)
            self.text_val = text
        if bg is not None:
            self.itemconfigure(self.rect, fill=bg)
            self.bg_color = bg
        if fg is not None:
            self.itemconfigure(self.text_item, fill=fg)
            self.fg_color = fg
        if kwargs:
            super().config(**kwargs)

    def cget(self, prop):
        if prop == "text": return self.text_val
        return super().cget(prop)

    def on_press(self, event):
        self.itemconfigure(self.rect, fill=self.bg_color) 
    def on_release(self, event):
        self.itemconfigure(self.rect, fill=self.hover_color)
        if self.command: self.command()
    def on_enter(self, event):
        self.config(cursor="hand2")
        self.itemconfigure(self.rect, fill=self.hover_color)
    def on_leave(self, event):
        self.config(cursor="")
        self.itemconfigure(self.rect, fill=self.bg_color)


class Hub4comManager:
    def __init__(self, root, working_dir):
        self.root = root
        self.root.title("시리얼 원격 접속 관리자")
        self.root.geometry("560x800") 
        
        self.working_dir = working_dir
        self.running_flags = {}
        self.running_procs = {}
        
        self.monitor_states = {} 
        self.active_monitors = [] 
        
        # --- [Toss Style Color Palette] ---
        self.BG_COLOR = "#F2F4F6"
        self.CARD_COLOR = "#FFFFFF"
        self.TEXT_MAIN = "#191F28"
        self.TEXT_SUB = "#8B95A1"
        self.BTN_BLUE = "#3182F6"
        self.BTN_RED = "#F04452"
        self.BTN_LIGHT = "#E8F3FF"
        self.INPUT_BG = "#F9FAFB"
        self.BORDER_COLOR = "#E5E8EB"
        self.CONSOLE_BG = "#191F28" 
        
        self.DISABLED_BG = "#E5E8EB"
        self.DISABLED_FG = "#A0AAB5"
        
        self.SCROLL_THUMB_COLOR = "#3B4859"
        self.SCROLL_TRACK_COLOR = "#10141A"
        
        self.FONT_MAIN = ("Malgun Gothic", 10)
        self.FONT_BOLD = ("Malgun Gothic", 10, "bold")
        self.FONT_BTN = ("Malgun Gothic", 12, "bold")
        
        self.root.configure(bg=self.BG_COLOR)
        self.rows = []

        self._setup_ui()

    def _setup_ui(self):
        control_frame = tk.Frame(self.root, bg=self.BG_COLOR, pady=15, padx=15)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        RoundedButton(control_frame, text="전체 실행 ▶", width=110, height=38, corner_radius=10, 
                      bg_color=self.BTN_BLUE, fg_color="white", hover_color="#1B64DA", font=self.FONT_BOLD, 
                      command=self.start_all).pack(side=tk.LEFT, padx=5)
        
        RoundedButton(control_frame, text="전체 정지 ■", width=110, height=38, corner_radius=10, 
                      bg_color=self.BTN_RED, fg_color="white", hover_color="#D92F3E", font=self.FONT_BOLD, 
                      command=self.stop_all).pack(side=tk.LEFT, padx=5)
        
        RoundedButton(control_frame, text="포트 추가 ＋", width=100, height=38, corner_radius=10, 
                      bg_color=self.BTN_LIGHT, fg_color=self.BTN_BLUE, hover_color="#D0E4FF", font=self.FONT_BOLD, 
                      command=self.add_row).pack(side=tk.RIGHT, padx=5)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar", gripcount=0, background=self.BORDER_COLOR, darkcolor=self.BG_COLOR, lightcolor=self.BG_COLOR, troughcolor=self.BG_COLOR, bordercolor=self.BG_COLOR, arrowcolor=self.TEXT_SUB)
        style.configure("Toss.TCombobox", fieldbackground=self.INPUT_BG, background=self.INPUT_BG, bordercolor=self.BORDER_COLOR, lightcolor=self.INPUT_BG, darkcolor=self.INPUT_BG, borderwidth=1, arrowcolor=self.TEXT_SUB, foreground=self.TEXT_MAIN, focuscolor=self.INPUT_BG)
        style.map("Toss.TCombobox", fieldbackground=[("disabled", self.DISABLED_BG), ("readonly", self.INPUT_BG)], selectbackground=[("disabled", self.DISABLED_BG), ("readonly", self.INPUT_BG)], foreground=[("disabled", self.DISABLED_FG)], selectforeground=[("disabled", self.DISABLED_FG), ("readonly", self.TEXT_MAIN)], background=[("disabled", self.DISABLED_BG), ("readonly", self.INPUT_BG)], arrowcolor=[("disabled", self.DISABLED_BG)], bordercolor=[("focus", self.BORDER_COLOR)])
        style.configure("Dark.Vertical.TScrollbar", gripcount=0, background=self.SCROLL_THUMB_COLOR, troughcolor=self.SCROLL_TRACK_COLOR, bordercolor=self.SCROLL_TRACK_COLOR, darkcolor=self.SCROLL_TRACK_COLOR, lightcolor=self.SCROLL_TRACK_COLOR, arrowcolor="#8B95A1")
        style.map("Dark.Vertical.TScrollbar", background=[("active", self.SCROLL_THUMB_COLOR), ("!active", self.SCROLL_THUMB_COLOR)], darkcolor=[("active", self.SCROLL_TRACK_COLOR), ("!active", self.SCROLL_TRACK_COLOR)], lightcolor=[("active", self.SCROLL_TRACK_COLOR), ("!active", self.SCROLL_TRACK_COLOR)])

        bottom_container = tk.Frame(self.root, bg=self.BG_COLOR)
        bottom_container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, padx=15, pady=(0, 15))

        mon_frame = tk.Frame(bottom_container, bg=self.CONSOLE_BG, bd=0)
        mon_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))
        mon_title = tk.Label(mon_frame, text="통합 모니터링 (Running Status)", bg="#202A36", fg="#FFFFFF", font=("Malgun Gothic", 9, "bold"), pady=5)
        mon_title.pack(fill=tk.X)
        self.mon_txt = tk.Text(mon_frame, bg=self.CONSOLE_BG, fg="#E5E8EB", font=("Consolas", 10), state="disabled", relief="flat", padx=10, pady=10, height=6)
        mon_scroll = ttk.Scrollbar(mon_frame, orient="vertical", command=self.mon_txt.yview, style="Dark.Vertical.TScrollbar")
        self.mon_txt.configure(yscrollcommand=mon_scroll.set)
        mon_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.mon_txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.mon_txt.tag_config("run", foreground="#8B95A1")    
        self.mon_txt.tag_config("error", foreground="#F04452")  

        log_frame = tk.Frame(bottom_container, bg=self.CONSOLE_BG, bd=0)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))
        log_title = tk.Label(log_frame, text="통합 로그 (Event History)", bg="#202A36", fg="#FFFFFF", font=("Malgun Gothic", 9, "bold"), pady=5)
        log_title.pack(fill=tk.X)
        self.log_txt = tk.Text(log_frame, bg=self.CONSOLE_BG, fg="#E5E8EB", font=("Consolas", 10), state="disabled", relief="flat", padx=10, pady=10, height=8)
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_txt.yview, style="Dark.Vertical.TScrollbar")
        self.log_txt.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_txt.tag_config("info", foreground="#3182F6")   
        self.log_txt.tag_config("success", foreground="#28A745")
        self.log_txt.tag_config("error", foreground="#F04452")  
        self.log_txt.tag_config("warning", foreground="#F5A623")

        self.canvas_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(15, 0), pady=(0, 15))
        
        header_frame = tk.Frame(self.canvas_frame, bg=self.BG_COLOR)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(0, 5))
        tk.Label(header_frame, text="시리얼 포트", bg=self.BG_COLOR, fg=self.TEXT_SUB, font=self.FONT_BOLD, width=12).pack(side=tk.LEFT, padx=4)
        tk.Label(header_frame, text="TCP 포트", bg=self.BG_COLOR, fg=self.TEXT_SUB, font=self.FONT_BOLD, width=12).pack(side=tk.LEFT, padx=4)
        tk.Label(header_frame, text="Baudrate", bg=self.BG_COLOR, fg=self.TEXT_SUB, font=self.FONT_BOLD, width=10).pack(side=tk.LEFT, padx=4)
        tk.Label(header_frame, text="제어", bg=self.BG_COLOR, fg=self.TEXT_SUB, font=self.FONT_BOLD, width=8).pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg=self.BG_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview, style="Vertical.TScrollbar")
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.BG_COLOR)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        def _on_mousewheel(event):
            widget = self.root.winfo_containing(event.x_root, event.y_root)
            if not widget: return
            if widget == self.log_txt:
                self.log_txt.yview_scroll(int(-1*(event.delta/120)), "units")
            elif widget == self.mon_txt:
                self.mon_txt.yview_scroll(int(-1*(event.delta/120)), "units")
            else:
                if self.scrollable_frame.winfo_reqheight() > self.canvas.winfo_height():
                    self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.root.bind_all("<MouseWheel>", _on_mousewheel)

        self.add_row(is_init=True)
        self.print_log(f"시스템 준비 완료 (경로: {self.working_dir})", "info")
        self.print_log("원하시는 포트를 실행해주세요.", "info")

    def print_log(self, message, tag="info"):
        def _write():
            try:
                self.log_txt.config(state="normal")
                self.log_txt.insert(tk.END, message + "\n", tag)
                self.log_txt.see(tk.END) 
                self.log_txt.config(state="disabled")
            except: pass
        self.root.after(0, _write)

    def update_monitor(self, com, message, tag="run"):
        if com not in self.active_monitors:
            self.active_monitors.append(com)
        self.monitor_states[com] = (message, tag)
        self._render_monitor()

    def remove_monitor(self, com):
        if com in self.monitor_states:
            del self.monitor_states[com]
        if com in self.active_monitors:
            self.active_monitors.remove(com)
        self._render_monitor()

    def _render_monitor(self):
        def _write():
            try:
                self.mon_txt.config(state="normal")
                self.mon_txt.delete(1.0, tk.END)
                for com in self.active_monitors:
                    msg, tag = self.monitor_states[com]
                    self.mon_txt.insert(tk.END, msg + "\n", tag)
                self.mon_txt.config(state="disabled")
            except: pass
        self.root.after(0, _write)

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._toggle_scrollbar()

    def _on_canvas_configure(self, event=None):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self._toggle_scrollbar()

    def _toggle_scrollbar(self):
        if self.scrollable_frame.winfo_reqheight() > self.canvas.winfo_height():
            self.scrollbar.pack(side="right", fill="y", padx=(0, 15))
        else:
            self.scrollbar.pack_forget()

    def _create_entry(self, parent, width, default_text):
        entry = tk.Entry(parent, width=width, justify="center", font=self.FONT_MAIN, 
                         bg=self.INPUT_BG, fg=self.TEXT_MAIN, relief="flat", 
                         disabledbackground=self.DISABLED_BG, disabledforeground=self.DISABLED_FG,
                         highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_COLOR)
        entry.insert(0, default_text)
        return entry

    def add_row(self, is_init=False):
        row_frame = tk.Frame(self.scrollable_frame, bg=self.CARD_COLOR, pady=10, padx=10, highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_COLOR)
        row_frame.pack(fill=tk.X, pady=4, padx=2)

        com_val = f"COM{len(self.rows) + 9}"
        tcp_val = str(10009 + len(self.rows)) 

        com_entry = self._create_entry(row_frame, 12, com_val)
        com_entry.pack(side=tk.LEFT, padx=4)

        tcp_entry = self._create_entry(row_frame, 15, tcp_val)
        tcp_entry.pack(side=tk.LEFT, padx=4)

        baud_combo = ttk.Combobox(row_frame, values=["115200", "38400", "9600"], width=10, justify="center", font=self.FONT_MAIN, state="readonly", style="Toss.TCombobox")
        baud_combo.current(0)
        baud_combo.pack(side=tk.LEFT, padx=4)

        def _prevent_combo_scroll(event):
            if self.scrollable_frame.winfo_reqheight() > self.canvas.winfo_height():
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"
        baud_combo.bind("<MouseWheel>", _prevent_combo_scroll)

        toggle_btn = RoundedButton(row_frame, text="▶", width=34, height=34, corner_radius=8, 
                                   bg_color="#E8F8EE", fg_color="#28A745", hover_color="#D4EDDA", font=("", 14, "bold"))
        toggle_btn.command = lambda btn=toggle_btn, c=com_entry, t=tcp_entry, b=baud_combo: self.toggle_single(btn, c, t, b)
        toggle_btn.pack(side=tk.LEFT, padx=(10, 4))

        row_data = (com_entry, tcp_entry, baud_combo, toggle_btn)
        
        del_btn = RoundedButton(row_frame, text="✕", width=34, height=34, corner_radius=8, 
                                bg_color=self.BG_COLOR, fg_color=self.TEXT_SUB, hover_color="#D1D6DB", font=("Malgun Gothic", 12, "bold"))
        del_btn.command = lambda f=row_frame, e=row_data: self.delete_row(f, e)
        del_btn.pack(side=tk.LEFT, padx=4)

        self.rows.append(row_data)

        if not is_init and hasattr(self, 'log_txt'):
            self.print_log(f"[{com_val}] 추가되었습니다.", "info")

    def delete_row(self, frame, entries):
        com_entry = entries[0]
        self.stop_single(com_entry, is_delete=True)
        frame.destroy()
        if entries in self.rows:
            self.rows.remove(entries)

    def toggle_single(self, btn, com_entry, tcp_entry, baud_combo):
        if btn.cget("text") == "▶":
            self.start_single(com_entry, tcp_entry, baud_combo)
            btn.config(text="■", bg="#FCE8E8", fg=self.BTN_RED) 
            btn.hover_color = "#FAD1D1"
            com_entry.config(state="disabled")
            tcp_entry.config(state="disabled")
            baud_combo.config(state="disabled")
        else:
            self.stop_single(com_entry)
            btn.config(text="▶", bg="#E8F8EE", fg="#28A745") 
            btn.hover_color = "#D4EDDA"
            com_entry.config(state="normal")
            tcp_entry.config(state="normal")
            baud_combo.config(state="readonly")

    def start_single(self, com_entry, tcp_entry, baud_combo):
        com = com_entry.get().strip().upper()
        tcp = tcp_entry.get().strip()
        baud = baud_combo.get().strip()

        if not (com and tcp and baud): return
        if self.running_flags.get(com, False): return

        self.running_flags[com] = True
        
        t = threading.Thread(target=self._monitor_loop, args=(com, tcp, baud), daemon=True)
        t.start()

    # ★ 수정: 정지 시 os.system 대신 subprocess를 투명하게 사용하여 까만 창 튀어나옴 방지
    def _kill_process(self, pid):
        try:
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)
        except:
            pass

    def stop_single(self, com_entry, is_delete=False):
        com = com_entry.get().strip().upper()
        if com:
            self.running_flags[com] = False 
            proc = self.running_procs.get(com)
            if proc:
                self._kill_process(proc.pid)
            
            if is_delete:
                self.print_log(f"[{com}] 삭제되었습니다.", "warning")
            else:
                self.print_log(f"[{com}] 정지되었습니다.", "info")
                
            self.remove_monitor(com)

    def _monitor_loop(self, com, tcp, baud):
        exe_path = os.path.join(self.working_dir, "hub4com.exe")
        cmd = [
            exe_path,
            "--route=0:1", "--route=1:0",
            "--use-driver=serial", f"--baud={baud}", "--data=8", "--parity=n", "--stop=1",
            "--ox=on", "--ix=on", "--octs=off", "--odsr=off",
            f"\\\\.\\{com}",
            "--use-driver=tcp", f"*{tcp}", f"*{tcp}"
        ]
        
        while self.running_flags.get(com, False):
            self.print_log(f"[{com}] 실행되었습니다.", "success")
            self.update_monitor(com, f"{com} starting...", "run")
            
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE,
                                        text=True, cwd=self.working_dir, creationflags=CREATE_NO_WINDOW)
                self.running_procs[com] = proc

                q = queue.Queue()
                def reader():
                    try:
                        for line in iter(proc.stdout.readline, ''):
                            q.put(line)
                    except: pass
                threading.Thread(target=reader, daemon=True).start()

                error_found = False
                dot_count = 1
                
                while self.running_flags.get(com, False) and proc.poll() is None:
                    try:
                        line = q.get(timeout=1.0) 
                        if "ERROR" in line.upper():
                            error_found = True
                            break
                    except queue.Empty:
                        dots = "." * dot_count
                        self.update_monitor(com, f"{com} running {dots:<3}", "run")
                        dot_count = (dot_count % 3) + 1 

                if error_found and self.running_flags.get(com, False):
                    self.print_log(f"[{com}] 에러 발생!", "error")
                    self.print_log(f"[{com}] 3초 뒤 재시작합니다...", "warning")
                    
                    self._kill_process(proc.pid)
                    
                    for i in range(3, 0, -1):
                        if not self.running_flags.get(com, False): break
                        self.update_monitor(com, f"{com} ERROR! {i}초 뒤 재시작...", "error")
                        time.sleep(1)
                else:
                    self._kill_process(proc.pid)
                    break

            except Exception as e:
                self.print_log(f"[!] {com} 에러: hub4com.exe 파일을 실행할 수 없습니다.", "error")
                self.update_monitor(com, f"{com} 시스템 오류!", "error")
                time.sleep(5)

        self.remove_monitor(com)

    def start_all(self):
        for com_entry, tcp_entry, baud_combo, toggle_btn in self.rows:
            if toggle_btn.cget("text") == "▶":
                self.toggle_single(toggle_btn, com_entry, tcp_entry, baud_combo)

    def stop_all(self):
        for com_entry, tcp_entry, baud_combo, toggle_btn in self.rows:
            if toggle_btn.cget("text") == "■":
                self.toggle_single(toggle_btn, com_entry, tcp_entry, baud_combo)


# ==============================================================================
# ★★★ ZIP 압축 해제 & 경로 자동 기억 시스템 ★★★
# ==============================================================================

def fast_scan_for_hub4com():
    local_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(local_dir, "hub4com.exe")):
        return local_dir

    search_dirs = [
        r"C:\hub4com-2.1.0.0-386",
        r"C:\hub4com",
        r"C:\com0com",
        os.environ.get('ProgramFiles', r'C:\Program Files'),
        os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)')
    ]
    
    for base_dir in search_dirs:
        if not base_dir or not os.path.exists(base_dir): continue
        try:
            for root, dirs, files in os.walk(base_dir):
                depth = root[len(base_dir):].count(os.sep)
                if depth > 2: del dirs[:] 
                if "hub4com.exe" in (f.lower() for f in files):
                    return root
        except: pass
    
    return None

def setup_environment():
    config_file = os.path.join(os.path.expanduser("~"), ".hub4com_manager_config.txt")
    
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            saved_dir = f.read().strip()
            if os.path.exists(os.path.join(saved_dir, "hub4com.exe")):
                return saved_dir 

    found_dir = fast_scan_for_hub4com()
    if found_dir:
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(found_dir)
        return found_dir

    setup_root = tk.Tk()
    setup_root.withdraw() 
    
    msg = ("PC에서 'hub4com' 모듈을 찾을 수 없습니다.\n\n"
           "▶ 내장된 파일을 압축 해제(설치) 하시겠습니까?\n\n"
           "(이미 수동으로 압축을 푸셨다면 '아니요'를 눌러 파일을 직접 선택해주세요)")
           
    if messagebox.askyesno("초기 셋업 안내", msg):
        zip_name = "hub4com-2.1.0.0-386.zip" # 이름 원복
        zip_path = os.path.join(sys._MEIPASS, zip_name) if hasattr(sys, '_MEIPASS') else os.path.join(os.path.dirname(os.path.abspath(__file__)), zip_name)
        
        if os.path.exists(zip_path):
            messagebox.showinfo("폴더 선택", "어느 폴더에 설치(압축 해제) 하시겠습니까?\n\nC드라이브나 문서 등 원하시는 폴더를 선택해주세요.")
            
            extract_dir = filedialog.askdirectory(title="hub4com 설치 폴더 선택")
            
            if extract_dir:
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    
                    exact_exe_dir = None
                    for root, dirs, files in os.walk(extract_dir):
                        if "hub4com.exe" in (f.lower() for f in files):
                            exact_exe_dir = root
                            break
                            
                    if exact_exe_dir:
                        with open(config_file, "w", encoding="utf-8") as f:
                            f.write(exact_exe_dir)
                        messagebox.showinfo("설치 완료", "성공적으로 설치되었습니다!\n프로그램을 시작합니다.")
                        setup_root.destroy()
                        return exact_exe_dir
                    else:
                        messagebox.showerror("에러", "압축을 풀었으나 'hub4com.exe'를 찾을 수 없습니다.")
                except Exception as e:
                    messagebox.showerror("압축 해제 오류", f"파일을 푸는 중 오류가 발생했습니다:\n{e}")
        else:
            messagebox.showwarning("경고", f"내장된 압축 파일({zip_name})이 존재하지 않습니다.\n수동으로 파일을 선택해주세요.")
            
    messagebox.showinfo("수동 경로 지정", "압축을 푸신 폴더로 이동하여 'hub4com.exe' 파일을 직접 선택해주세요.")
    
    selected_file = filedialog.askopenfilename(
        title="hub4com.exe 파일 찾기",
        filetypes=[("실행 파일", "hub4com.exe")]
    )
    
    if selected_file and os.path.basename(selected_file).lower() == "hub4com.exe":
        target_dir = os.path.dirname(selected_file)
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(target_dir)
        setup_root.destroy()
        return target_dir
    else:
        messagebox.showerror("종료", "'hub4com.exe' 파일이 올바르게 선택되지 않아 프로그램을 종료합니다.")
        setup_root.destroy()
        sys.exit(0)


if __name__ == "__main__":
    try:
        working_dir = setup_environment()
        
        root = tk.Tk()
        app = Hub4comManager(root, working_dir)
        root.mainloop()
        
    except Exception as e:
        print("==========================================")
        print("프로그램 실행 중 치명적인 에러가 발생했습니다!")
        print("==========================================")
        traceback.print_exc()
        print("==========================================")
        os.system("pause")