# 🚀 Media Transformatör - Dark-Pro v1.0.1

Basit, hızlı ve şık bir arayüzle medya dönüştürme işlemlerini (Video'dan GIF'e, MP4 sıkıştırma vb.) tek tıkla yapmanızı sağlayan masaüstü uygulamasıdır. **%100 Python ve Tkinter** kullanılarak geliştirilmiştir.

Uygulama, tüm karmaşık işlemleri arkada popüler medya motoru **FFmpeg** ile gerçekleştirir, böylece en yüksek dönüştürme kalitesini sunar.

## ✨ Temel Özellikler

* **Video'dan GIF'e Dönüştürme:** Saniyeler içinde yüksek kaliteli GIF'ler oluşturun.
* **MP4 Boyut Küçültme:** Videolarınızı kaliteden ödün vermeden sıkıştırın.
* **MP3'e Dönüştürme:** Videolardan sesi hızla MP3 formatında çıkarın.
* **Fotoğraf GIF Animasyonu:** Birden fazla fotoğrafı 5 saniyelik GIF animasyonuna çevirin.
* **Tek Dosya (OneFile) Çalışma:** Uygulama, FFmpeg dahil tüm bağımlılıklarıyla birlikte **tek bir EXE** dosyası olarak paketlenmiştir. (90+ MB)
* **Modern Arayüz:** `customtkinter` kütüphanesi ile Dark-Pro temalı, şık ve modern bir kullanıcı deneyimi.

## ⚙️ Teknoloji Yığını

* **Python:** Projenin ana dili.
* **customtkinter:** Modern, karanlık tema destekli arayüz kütüphanesi.
* **FFmpeg:** Tüm medya işleme ve dönüştürme görevleri için kullanılan güçlü açık kaynak motor.
* **PyInstaller:** Uygulamayı tek başına çalışabilen (standalone) Windows EXE dosyasına paketlemek için kullanıldı.
* **Git / GitHub:** Sürüm kontrol ve yayınlama platformu.

## 🛠️ Kurulum ve Çalıştırma

### 📥 EXE İndirme (Tavsiye Edilen)

Uygulamayı kullanmak için herhangi bir kurulum gerekmez. En güncel sürümü indirin ve çalıştırmanız yeterlidir.

➡️ **[Media-Transformator-v1.0.1.exe'yi Buradan İndir](https://github.com/jasonbreakberk/Media-Transformator-Py/releases/latest)**

### 🐍 Geliştiriciler İçin

Eğer kodu incelemek isterseniz:

1.  **Klonlayın:**
    ```bash
    git clone [https://github.com/jasonbreakberk/Media-Transformator-Py.git](https://github.com/jasonbreakberk/Media-Transformator-Py.git)
    ```
2.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Çalıştırın:**
    ```bash
    python main.py
    ```

## 🐞 Çözülen Önemli Sorunlar (v1.0.1)

Bu sürüm, geliştirme aşamasında karşılaşılan ve uygulamanın stabilitesini artıran kritik bir hatayı içermektedir:

* **`Popen.__init__() got an unexpected keyword argument 'creationflags'` Hatası Çözümü:** Özellikle Python'ın 3.13 ve daha yeni sürümlerinde ortaya çıkan, Windows'a özgü bu uyumluluk sorunu, `subprocess.Popen` metodunda yapılan spesifik düzenlemelerle tamamen giderilmiştir.
* **CMD Penceresinin Görünmesi Engellendi:** Uygulama çalışırken arka planda anlık olarak açılıp kapanan CMD/Terminal penceresi, **`creationflags=subprocess.SW_HIDE`** (veya benzeri bir metod) kullanılarak tamamen gizlenmiştir. Bu sayede kullanıcıya pürüzsüz bir masaüstü deneyimi sunulmuştur.

---

## 👨‍💻 Geliştirici

**[Harun Çelebi](https://github.com/jasonbreakberk)**

*Bu proje, geliştiricinin Python ve masaüstü uygulama geliştirme yeteneklerini gösteren bir portfolyo çalışmasıdır.*