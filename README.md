# 🚀 Media Transformatör - Dark-Pro v1.2.0

Bu uygulama, video ve fotoğraf dönüştürme işlemlerini (kırpma, sıkıştırma, format değiştirme) kullanıcı dostu, karanlık temalı bir arayüzle gerçekleştiren, **tek başına çalışan (standalone) bir Windows masaüstü aracıdır.**

## ✨ Temel Özellikler (v1.2.0)

### YENİ ÖZELLİK: Video Kırpma (Klip Üretimi)
* **Video Kırpma (Trim):** İçerik üreticileri için kritik! Yüklenen videonun sadece belirlenen **Başlangıç** ve **Bitiş saniyeleri** arasını kırparak yeni bir klip oluşturur. (saniye veya hh:mm:ss formatında giriş desteklenir.)

### Dönüştürme İşlevleri
* **Video'dan GIF'e Dönüştürme:** Saniyeler içinde yüksek kaliteli, döngülü GIF'ler üretir.
* **MP4 Boyut Küçültme:** Videolarınızı kaliteyi koruyarak sıkıştırır.
* **MP3'e Dönüştürme:** Videolardan sesi MP3 formatında ayırır.
* **Fotoğraf GIF Animasyonu:** Tek bir JPG/PNG'yi 5 saniyelik animasyonlu GIF'e çevirir.

### Teknik Mimarisi
* **Tek Dosya (OneFile) EXE:** Uygulama, FFmpeg motoru dahil tüm bağımlılıklarıyla birlikte tek bir 90+ MB'lık EXE dosyası olarak paketlenmiştir.
* **Modern Arayüz:** `customtkinter` kütüphanesi ile Dark-Pro temalı, şık ve sade bir kullanıcı deneyimi sunar.

## 🆕 Bu Sürümde (v1.2.0)

- **İlerleme çubuğunun %96'da takılması düzeltildi.** FFmpeg sürecinin `stdout/stderr` tamponlarının dolmasıyla oluşan kilitlenme, çıktılar `DEVNULL`'a yönlendirilerek giderildi. İşlem tamamlanınca bar artık beklemeden %100'e ilerliyor.
- **Hata yakalama iyileştirmesi.** FFmpeg başarısız olduğunda daha güvenli ve özet hata mesajı oluşturuluyor.

## ⚙️ Çözülen Kritik Sorunlar ve Teknik Detaylar

Bu projenin geliştirme aşamasında, Python'ın PyInstaller ve FFmpeg entegrasyonundan kaynaklanan ve uygulamanın stabilitesini doğrudan etkileyen zorlu hatalar aşılmıştır.

| Sorun Adı | Çözüm Yöntemi | Etkilenen Sürüm |
| :--- | :--- | :--- |
| **`Popen.__init__() creationflags` Hatası** | Python'ın 3.10+ sürümleriyle uyumluluk sorununu çözmek için, `subprocess` komutundaki uyumsuz **`creation_flags`** parametresi tamamen kaldırılmış, komutlar yeni sürüme uyumlu hale getirilmiştir. | v1.0.1 (Yeniden Oluşturuldu) |
| **FFprobe Süre Okuma Hatası** | Dosya yolundaki boşluklar ve Türkçe karakterler nedeniyle `ffprobe`'un süre okuyamaması sorunu, `subprocess` komutlarının doğru tırnaklama ve komut listesi yapısıyla yeniden düzenlenmesiyle çözülmüştür. | v1.1.0 |
| **CMD Penceresinin Görünmesi** | Arka planda anlık açılıp kapanan CMD/Terminal penceresi, **`--windowed`** PyInstaller bayrağı ve `creation_flags` yönetimi ile tamamen gizlenmiştir. | v1.0.1 |
| **Dosya Adı Taşması** | UX iyileştirmesi olarak, uzun dosya adlarının statü çubuğundan taşması `os.path.basename` metodu ile kısaltılarak engellenmiştir. | v1.1.0 |
| **İlerleme %96'da Takılı Kalıyor** | FFmpeg `stdout/stderr` akışları boru (PIPE) ile okunmadığında tamponlar dolup süreç kilitleniyordu. Çıktılar `DEVNULL`'a yönlendirilerek deadlock tamamen önlendi. | v1.2.0 |

---

## 🛠️ Kurulum ve Çalıştırma

### 📥 EXE İndirme (Tavsiye Edilen)

En güncel çalışan sürümü indirin. Kurulum gerektirmez.

➡️ **[Media-Transformatör-v1.2.0.exe'yi İndir](https://github.com/jasonbreakberk/Media-Transformator-Py/releases/latest)**

### 🐍 Geliştiriciler İçin

Projenin kaynak kodunu incelemek isterseniz:

1.  **Klonlayın:**
    ```bash
    git clone [https://github.com/jasonbreakberk/Media-Transformator-Py.git](https://github.com/jasonbreakberk/Media-Transformator-Py.git)
    ```
2.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install customtkinter ffmpeg-python pyinstaller
    ```
3.  **Çalıştırın:**
    ```bash
    python app.py
    ```

---

## 👨‍💻 Geliştirici

**[Harun Çelebi](https://github.com/jasonbreakberk)**

*Bu proje, geliştiricinin Python, Windows masaüstü uygulaması geliştirme ve zorlu üçüncü parti kütüphane (FFmpeg) entegrasyonu yeteneklerini gösteren bir portfolyo çalışmasıdır.*