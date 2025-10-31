import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess 
import threading 
import sys 
import json 
import datetime
import re
import time

# Uygulamanın ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") 
CURRENT_LANGUAGE = "tr"

# =================================================================================
# LOKALİZASYON (DİL DESTEĞİ) SÖZLÜĞÜ - V1.5.0
# =================================================================================
LOCALE_DATA = {
    "tr": {
        "app_title": "Media Transformatör | Dark-Pro v1.5.0",
        "tab_convert": "Dönüştür",
        "tab_settings": "Ayarlar",
        "title_main": "🚀 MEDIA TRANSFORMATÖR",
        "input_placeholder": "Dönüştürülecek Dosyayı Seçin...",
        "button_select_file": "Dosya Seç",
        "label_trim_settings": "VİDEO KIRPMA (KLİP) AYARLARI (saniye/hh:mm:ss):",
        "placeholder_start": "0",
        "placeholder_end": "Son",
        "label_options": "İŞLEM SEÇENEKLERİ:",
        "radio_gif": "🎥 Video'dan GIF'e Dönüştür",
        "radio_mp4_kucult": "🎞️ MP4 Boyutunu Küçült (Sıkıştır)",
        "radio_mp3": "🎧 MP3'e Dönüştür (Sesi Çıkar)",
        "radio_photo_gif": "🖼️ Fotoğraftan GIF Yap (5s Animasyon)",
        "status_ready": "Hazır. Dosyanızı seçin.",
        "button_start": "DÖNÜŞTÜRMEYİ BAŞLAT",
        "status_processing_percent": "Dönüştürülüyor... {percent}%",
        "status_processing": "İşleniyor...",
        "status_successful": "✅ BAŞARILI! İşlem Tamamlandı.",
        "status_file_select_error": "❌ Lütfen Önce Geçerli Bir Dosya Seçin!",
        "status_file_cancel": "Dosya seçimi iptal edildi.",
        "status_theme_changed": "Tema '{theme}' olarak değiştirildi.",
        "status_lang_changed": "Dil {lang} olarak ayarlandı. Arayüz güncellendi.",
        "status_trim_ready": " hazır. (Manuel kırpma ayarlarını girin)",
        "status_ffmpeg_error": "FFMPEG HATA: {error}",
        "status_unknown_error": "BİLİNMEYEN HATA: {error}",
        "settings_theme": "Uygulama Teması:",
        "theme_dark": "Dark (Koyu)",
        "theme_light": "Light (Aydınlık)",
        "settings_lang": "Dil Seçeneği:",
        "lang_tr": "Türkçe",
        "lang_en": "English",
        "filedialog_img": "Dönüştürülecek Fotoğrafı Seçin",
        "filedialog_video": "Dönüştürülecek Dosyayı Seçin",
        "filetypes_img": "Görüntü Dosyaları",
        "filetypes_video": "Video Dosyaları",
        "filetypes_all": "Tüm Dosyalar",
        "progress_time": "⏱️ Süre: {time}",
        "progress_speed": "⚡ Hız: {speed}x",
        "progress_eta": "⏳ Kalan: {eta}"
    },
    "en": {
        "app_title": "Media Transformer | Dark-Pro v1.5.0",
        "tab_convert": "Convert",
        "tab_settings": "Settings",
        "title_main": "🚀 MEDIA TRANSFORMER",
        "input_placeholder": "Select File to Convert...",
        "button_select_file": "Select File",
        "label_trim_settings": "VIDEO TRIM (CLIP) SETTINGS (seconds/hh:mm:ss):",
        "placeholder_start": "0",
        "placeholder_end": "End",
        "label_options": "OPERATION OPTIONS:",
        "radio_gif": "🎥 Convert Video to GIF",
        "radio_mp4_kucult": "🎞️ Reduce MP4 Size (Compress)",
        "radio_mp3": "🎧 Convert to MP3 (Extract Audio)",
        "radio_photo_gif": "🖼️ Make GIF from Photo (5s Animation)",
        "status_ready": "Ready. Select your file.",
        "button_start": "START CONVERSION",
        "status_processing_percent": "Converting... {percent}%",
        "status_processing": "Processing...",
        "status_successful": "✅ SUCCESSFUL! Operation Completed.",
        "status_file_select_error": "❌ Please Select a Valid File First!",
        "status_file_cancel": "File selection cancelled.",
        "status_theme_changed": "Theme changed to '{theme}'.",
        "status_lang_changed": "Language set to {lang}. Interface updated.",
        "status_trim_ready": " ready. (Enter manual trim settings)",
        "status_ffmpeg_error": "FFMPEG ERROR: {error}",
        "status_unknown_error": "UNKNOWN ERROR: {error}",
        "settings_theme": "Application Theme:",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "settings_lang": "Language Option:",
        "lang_tr": "Turkish",
        "lang_en": "English",
        "filedialog_img": "Select Image to Convert",
        "filedialog_video": "Select File to Convert",
        "filetypes_img": "Image Files",
        "filetypes_video": "Video Files",
        "filetypes_all": "All Files",
        "progress_time": "⏱️ Time: {time}",
        "progress_speed": "⚡ Speed: {speed}x",
        "progress_eta": "⏳ Left: {eta}"
    }
}

# =================================================================================
# LOKALİZASYON YARDIMCI FONKSİYONLARI
# =================================================================================
def get_text(key):
    global CURRENT_LANGUAGE, LOCALE_DATA
    return LOCALE_DATA.get(CURRENT_LANGUAGE, LOCALE_DATA["tr"]).get(key, f"MISSING_TEXT_{key}")

def get_lang_code(lang_name):
    global LOCALE_DATA
    for code, data in LOCALE_DATA.items():
        if data["lang_" + code] == lang_name:
            return code
    return "tr" 

# =================================================================================
# FFMPEG YOLU
# =================================================================================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

FFMPEG_PATH = resource_path("ffmpeg.exe")
creation_flags_silent = 0x08000000 

# =================================================================================
# ZAMAN DÖNÜŞTÜRÜCÜ FONKSİYON
# =================================================================================
def format_time(seconds):
    """Saniyeyi HH:MM:SS formatına çevirir"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

# =================================================================================

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.ui_elements = {}
        self.selected_file_path = None 
        self.conversion_start_time = None
        self.is_converting = False
        
        # Değişkenleri başlat
        self.format_var = ctk.StringVar(value="gif")
        self.theme_var = ctk.StringVar(value=get_text("theme_dark"))
        self.lang_var = ctk.StringVar(value=get_text("lang_tr"))
        
        # İlk UI'ı oluştur
        self.rebuild_ui()

    def rebuild_ui(self):
        """Dil veya tema değiştiğinde tüm arayüzü yeniden çizer."""
        
        # Eski elementleri sil
        for widget in self.winfo_children():
            widget.destroy()

        self.title(get_text("app_title")) 
        self.geometry("720x720") 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- SEKME GÖRÜNÜMÜNÜ EKLEME ---
        self.tab_view = ctk.CTkTabview(self, width=680, height=680)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Sekme isimlerini dil dosyasından al
        tab_convert_name = get_text("tab_convert")
        tab_settings_name = get_text("tab_settings")

        self.tab_view.add(tab_convert_name)
        self.tab_view.add(tab_settings_name)
        
        tab_convert = self.tab_view.tab(tab_convert_name)
        tab_settings = self.tab_view.tab(tab_settings_name)
        
        tab_convert.grid_columnconfigure(0, weight=1)
        tab_settings.grid_columnconfigure(0, weight=1)
        
        self.setup_convert_tab(tab_convert)
        self.setup_settings_tab(tab_settings)

    def setup_convert_tab(self, tab_convert):
        """Dönüştür sekmesini kurar."""
        
        # BAŞLIK
        ctk.CTkLabel(
            tab_convert, 
            text=get_text("title_main"), 
            font=ctk.CTkFont(size=26, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n") 
        
        # INPUT FRAME
        input_frame = ctk.CTkFrame(tab_convert) 
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew") 
        input_frame.grid_columnconfigure(0, weight=1)

        self.ui_elements['file_path_entry'] = ctk.CTkEntry(
            input_frame, 
            placeholder_text=get_text("input_placeholder"), 
            height=35
        )
        self.ui_elements['file_path_entry'].grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.ui_elements['select_button'] = ctk.CTkButton(
            input_frame, 
            text=get_text("button_select_file"), 
            command=self.select_file, 
            fg_color="#3498DB", 
            hover_color="#2980B9",
            height=35,
            width=120
        )
        self.ui_elements['select_button'].grid(row=0, column=1, padx=10, pady=10)
        
        # KIRPMA ALANI
        trim_frame = ctk.CTkFrame(tab_convert) 
        trim_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew") 
        trim_frame.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(
            trim_frame, 
            text=get_text("label_trim_settings"), 
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=0, column=0, columnspan=4, padx=15, pady=(15, 10), sticky="w")
        
        ctk.CTkLabel(trim_frame, text="Başlangıç:").grid(row=1, column=0, padx=(15, 5), pady=10, sticky="e")
        self.ui_elements['start_entry'] = ctk.CTkEntry(
            trim_frame, 
            placeholder_text=get_text("placeholder_start"), 
            width=100
        )
        self.ui_elements['start_entry'].grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        
        ctk.CTkLabel(trim_frame, text="Bitiş:").grid(row=1, column=2, padx=(15, 5), pady=10, sticky="e")
        self.ui_elements['end_entry'] = ctk.CTkEntry(
            trim_frame, 
            placeholder_text=get_text("placeholder_end"), 
            width=100
        )
        self.ui_elements['end_entry'].grid(row=1, column=3, padx=(5, 15), pady=10, sticky="ew")
        
        # SEÇENEKLER BÖLÜMÜ
        options_frame = ctk.CTkFrame(tab_convert) 
        options_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew") 
        options_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            options_frame, 
            text=get_text("label_options"), 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")
        
        # Radyo Butonları
        ctk.CTkRadioButton(
            options_frame, 
            text=get_text("radio_gif"), 
            variable=self.format_var, 
            value="gif"
        ).grid(row=1, column=0, padx=15, pady=7, sticky="w")
        
        ctk.CTkRadioButton(
            options_frame, 
            text=get_text("radio_mp4_kucult"), 
            variable=self.format_var, 
            value="mp4_kucult"
        ).grid(row=2, column=0, padx=15, pady=7, sticky="w")
        
        ctk.CTkRadioButton(
            options_frame, 
            text=get_text("radio_mp3"), 
            variable=self.format_var, 
            value="mp3"
        ).grid(row=3, column=0, padx=15, pady=7, sticky="w")
        
        ctk.CTkRadioButton(
            options_frame, 
            text=get_text("radio_photo_gif"), 
            variable=self.format_var, 
            value="single_photo_to_gif"
        ).grid(row=4, column=0, padx=15, pady=(7, 15), sticky="w") 

        # İŞLEM BÖLÜMÜ - GELİŞMİŞ İLERLEME GÖSTERGESİ
        process_frame = ctk.CTkFrame(tab_convert)
        process_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew") 
        process_frame.grid_columnconfigure(0, weight=1)
        
        # Ana Progressbar
        self.progressbar = ctk.CTkProgressBar(
            process_frame, 
            orientation="horizontal", 
            mode="determinate", 
            progress_color="#2ECC71", 
            height=22
        )
        self.progressbar.grid(row=0, column=0, padx=15, pady=(15, 8), sticky="ew")
        self.progressbar.set(0)
        
        # Yüzde Göstergesi
        self.percent_label = ctk.CTkLabel(
            process_frame, 
            text="0%", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color="#2ECC71"
        )
        self.percent_label.grid(row=1, column=0, padx=15, pady=(0, 8), sticky="ew")

        # Detaylı İstatistikler Frame
        stats_frame = ctk.CTkFrame(process_frame, fg_color="transparent")
        stats_frame.grid(row=2, column=0, padx=15, pady=(0, 8), sticky="ew")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Geçen Süre
        self.time_label = ctk.CTkLabel(
            stats_frame, 
            text=get_text("progress_time").format(time="00:00"), 
            font=ctk.CTkFont(size=11), 
            text_color="#95A5A6"
        )
        self.time_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
        
        # İşlem Hızı
        self.speed_label = ctk.CTkLabel(
            stats_frame, 
            text=get_text("progress_speed").format(speed="0.0"), 
            font=ctk.CTkFont(size=11), 
            text_color="#95A5A6"
        )
        self.speed_label.grid(row=0, column=1, padx=5, pady=3)
        
        # Tahmini Kalan Süre
        self.eta_label = ctk.CTkLabel(
            stats_frame, 
            text=get_text("progress_eta").format(eta="--:--"), 
            font=ctk.CTkFont(size=11), 
            text_color="#95A5A6"
        )
        self.eta_label.grid(row=0, column=2, padx=5, pady=3, sticky="e")

        # Status Label
        self.status_label = ctk.CTkLabel(
            process_frame, 
            text=get_text("status_ready"), 
            text_color="#1ABC9C", 
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.status_label.grid(row=3, column=0, padx=15, pady=8, sticky="ew")

        # Start Button
        self.start_button = ctk.CTkButton(
            process_frame, 
            text=get_text("button_start"), 
            command=self.run_conversion_thread, 
            fg_color="#2ECC71", 
            hover_color="#27AE60", 
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.start_button.grid(row=4, column=0, padx=15, pady=(8, 15), sticky="ew")

        # Dosya yolu varsa, yeniden doldur
        if self.selected_file_path:
            self.ui_elements['file_path_entry'].insert(0, self.selected_file_path)

    def setup_settings_tab(self, tab_settings):
        """Ayarlar sekmesini kurar."""
        
        settings_container = ctk.CTkFrame(tab_settings)
        settings_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        settings_container.grid_columnconfigure(0, weight=1)
        
        # TEMA AYARLARI
        ctk.CTkLabel(
            settings_container, 
            text=get_text("settings_theme"), 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        theme_names = [get_text("theme_dark"), get_text("theme_light")]
        
        current_theme = ctk.get_appearance_mode()
        if current_theme == "Dark":
            self.theme_var.set(get_text("theme_dark"))
        else:
            self.theme_var.set(get_text("theme_light"))
            
        ctk.CTkOptionMenu(
            settings_container, 
            values=theme_names, 
            command=self.change_theme, 
            variable=self.theme_var,
            height=35
        ).grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # DİL AYARLARI
        ctk.CTkLabel(
            settings_container, 
            text=get_text("settings_lang"), 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=2, column=0, padx=20, pady=(30, 10), sticky="w")
        
        lang_names = [get_text("lang_tr"), get_text("lang_en")]
        self.lang_var.set(get_text("lang_" + CURRENT_LANGUAGE))
            
        ctk.CTkOptionMenu(
            settings_container, 
            values=lang_names, 
            command=self.change_language, 
            variable=self.lang_var,
            height=35
        ).grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    # ------------------- KONTROL FONKSİYONLARI -------------------
    
    def change_theme(self, new_theme):
        """Uygulama temasını değiştirir."""
        if "Dark" in new_theme or "Koyu" in new_theme:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        
        status_msg = get_text("status_theme_changed").format(theme=new_theme)
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=status_msg)

    def change_language(self, new_lang_name):
        """Uygulamanın dilini değiştirir ve arayüzü yeniden çizer."""
        global CURRENT_LANGUAGE
        
        new_lang_code = get_lang_code(new_lang_name)
        
        if CURRENT_LANGUAGE != new_lang_code:
            CURRENT_LANGUAGE = new_lang_code
            self.rebuild_ui()
            
            status_msg = get_text("status_lang_changed").format(lang=new_lang_name)
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=status_msg)

    def select_file(self):
        current_format = self.format_var.get()
        if current_format == "single_photo_to_gif":
            file_path = filedialog.askopenfilename(
                title=get_text("filedialog_img"),
                filetypes=((get_text("filetypes_img"), "*.jpg *.png *.jpeg"), (get_text("filetypes_all"), "*.*"))
            )
        else:
            file_path = filedialog.askopenfilename(
                title=get_text("filedialog_video"),
                filetypes=((get_text("filetypes_video"), "*.mp4 *.mov *.avi *.mkv"), (get_text("filetypes_all"), "*.*"))
            )
        
        if file_path:
            self.selected_file_path = file_path 
            
            file_name_short = os.path.basename(file_path)
            if len(file_name_short) > 30:
                file_name_short = file_name_short[:27] + '...'
            
            self.ui_elements['file_path_entry'].delete(0, 'end')
            self.ui_elements['file_path_entry'].insert(0, file_path) 
            
            self.ui_elements['end_entry'].delete(0, 'end') 
            
            status_msg = f"'{file_name_short}'{get_text('status_trim_ready')}"
            self.status_label.configure(text=status_msg, text_color="#1abc9c")
        else:
            self.status_label.configure(text=get_text("status_file_cancel"), text_color="orange")

    def update_progress(self, percent, elapsed_time, speed, eta):
        """İlerleme göstergesini günceller"""
        self.progressbar.set(percent / 100)
        self.percent_label.configure(text=f"{int(percent)}%")
        self.time_label.configure(text=get_text("progress_time").format(time=format_time(elapsed_time)))
        self.speed_label.configure(text=get_text("progress_speed").format(speed=f"{speed:.1f}"))
        self.eta_label.configure(text=get_text("progress_eta").format(eta=format_time(eta) if eta > 0 else "--:--"))
        
        if percent < 100:
            self.status_label.configure(
                text=get_text("status_processing_percent").format(percent=int(percent)), 
                text_color="yellow"
            )

    def run_conversion_thread(self):
        if not self.is_converting:
            conversion_thread = threading.Thread(target=self.start_conversion, daemon=True)
            conversion_thread.start()

    def start_conversion(self):
        if not self.selected_file_path or not os.path.exists(self.selected_file_path):
            self.status_label.configure(text=get_text("status_file_select_error"), text_color="red")
            return

        self.is_converting = True
        input_file = self.selected_file_path
        output_format = self.format_var.get()
        base, ext = os.path.splitext(input_file)
        
        start_time = self.ui_elements['start_entry'].get().strip()
        end_time = self.ui_elements['end_entry'].get().strip()
        
        self.conversion_start_time = datetime.datetime.now()
        self.start_button.configure(state="disabled", text=get_text("status_processing"))

        try:
            output_file = ""
            
            # FFMPEG Komut Ayarları
            trim_start_options = []
            trim_end_options = []
            
            if output_format in ["gif", "mp4_kucult"]:
                if start_time and start_time != '0':
                    trim_start_options += ['-ss', start_time]
                if end_time and end_time.lower() not in [get_text('placeholder_end').lower(), '']:
                    trim_end_options += ['-to', end_time]
            
            final_command = [FFMPEG_PATH] + trim_start_options + ['-i', input_file, '-y']
            
            if output_format == "gif":
                output_file = base + "_v1_5_klip.gif"
                final_command += trim_end_options + ['-filter:v', 'fps=15', '-loop', '0', output_file]
            elif output_format == "mp4_kucult":
                output_file = base + "_v1_5_kucuk.mp4"
                final_command += trim_end_options + ['-c:v', 'libx264', '-crf', '28', '-preset', 'medium', output_file]
            elif output_format == "mp3":
                output_file = base + "_v1_5_audio.mp3"
                final_command = [FFMPEG_PATH, '-i', input_file, '-y', '-vn', '-c:a', 'libmp3lame', '-q:a', '2', output_file]
            elif output_format == "single_photo_to_gif":
                output_file = base + "_v1_5_animasyon.gif"
                final_command = [FFMPEG_PATH, '-loop', '1', '-i', input_file, '-y', '-t', '5', '-vf', 'scale=500:-1,format=rgb24', output_file]

            # Video süresini al
            duration_cmd = [FFMPEG_PATH, '-i', input_file]
            duration_result = subprocess.run(duration_cmd, capture_output=True, text=True, creationflags=creation_flags_silent)
            duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})', duration_result.stderr)
            total_duration = 100
            if duration_match:
                h, m, s = map(int, duration_match.groups())
                total_duration = h * 3600 + m * 60 + s

            # subprocess ile çalıştırma
            process = subprocess.Popen(
                final_command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creation_flags_silent
            )
            
            # İlerleme simülasyonu
            progress_steps = 0
            last_percent = 0
            
            # Dosya boyutunu al (MB cinsinden)
            file_size_mb = os.path.getsize(input_file) / (1024 * 1024)
            
            while process.poll() is None:
                elapsed = (datetime.datetime.now() - self.conversion_start_time).total_seconds()
                
                # Format'a göre daha gerçekçi tahmini süre (dosya boyutu ve video süresine göre)
                if output_format == "single_photo_to_gif":
                    estimated_total = 5
                elif output_format == "mp3":
                    # MP3 çok hızlı - dosya boyutuna göre
                    estimated_total = max(file_size_mb * 0.05, 2)
                elif output_format == "mp4_kucult":
                    # MP4 sıkıştırma - hem dosya boyutu hem video süresine göre
                    estimated_total = max(file_size_mb * 0.8, total_duration * 0.15, 5)
                else:  # GIF
                    # GIF dönüşümü - dosya boyutuna göre
                    estimated_total = max(file_size_mb * 0.5, total_duration * 0.1, 3)
                
                # Logaritmik ilerleme - başta hızlı, sona doğru yavaş (%96'ya kadar)
                if elapsed < estimated_total * 0.5:
                    # İlk yarı: hızlı ilerleme
                    percent = (elapsed / estimated_total) * 70
                elif elapsed < estimated_total:
                    # İkinci yarı: yavaşlama
                    percent = 70 + ((elapsed - estimated_total * 0.5) / (estimated_total * 0.5)) * 26
                else:
                    # Tahmin aşıldı: %96'da bekle
                    percent = 96
                
                percent = min(percent, 96)
                
                if percent > last_percent:
                    last_percent = percent
                
                speed = (last_percent / 100) / max(elapsed, 0.1) * 10
                
                # ETA hesabı
                if last_percent < 96 and last_percent > 5:
                    eta = ((100 - last_percent) / last_percent) * elapsed
                else:
                    eta = max(estimated_total - elapsed, 0)
                
                self.after(0, self.update_progress, last_percent, elapsed, speed, eta)
                time.sleep(0.3)
                progress_steps += 1
                
                if progress_steps > 2000:
                    break
            
            # İşlem tamamlandı
            return_code = process.wait()
            
            if return_code == 0:
                # %100'e tamamla
                elapsed = (datetime.datetime.now() - self.conversion_start_time).total_seconds()
                self.after(0, self.update_progress, 100, elapsed, 1.0, 0)
                time.sleep(0.3)
                self.status_label.configure(text=get_text("status_successful"), text_color="green")
            else:
                raise subprocess.CalledProcessError(return_code, final_command, stderr="FFmpeg failed with non-zero exit code")
            
        except subprocess.CalledProcessError as e:
            self.progressbar.set(0)
            self.percent_label.configure(text="0%")
            error_msg = str(e)[:80]
            status_msg = get_text("status_ffmpeg_error").format(error=error_msg)
            self.status_label.configure(text=status_msg, text_color="red")
        except Exception as e:
            self.progressbar.set(0)
            self.percent_label.configure(text="0%")
            status_msg = get_text("status_unknown_error").format(error=str(e)[:50])
            self.status_label.configure(text=status_msg, text_color="red")
        finally:
            self.is_converting = False
            self.start_button.configure(state="normal", text=get_text("button_start"))
            
# Uygulamayı Çalıştır
if __name__ == "__main__":
    app = App()
    app.mainloop()