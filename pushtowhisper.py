import keyboard
import sounddevice as sd
import soundfile as sf
import tempfile
import os
import pyperclip
import time
import numpy as np
import queue
import time
import os
import site

# Ekran kartı (CUDA) DLL dosyalarının yüklenebilmesi için sistem yollarını (PATH) koda tanıtıyoruz
try:
    for sp in site.getsitepackages():
        cublas_path = os.path.join(sp, "nvidia", "cublas", "bin")
        cudnn_path = os.path.join(sp, "nvidia", "cudnn", "bin")
        if os.path.exists(cublas_path):
            os.add_dll_directory(cublas_path)
            os.environ["PATH"] = cublas_path + os.pathsep + os.environ["PATH"]
        if os.path.exists(cudnn_path):
            os.add_dll_directory(cudnn_path)
            os.environ["PATH"] = cudnn_path + os.pathsep + os.environ["PATH"]
except Exception:
    pass

from faster_whisper import WhisperModel

# RTX 4050 için en uygun model (large-v3-turbo ile kusursuz Türkçe doğruluğu elde edilir, ilk açılışta ~3GB indirir)
MODEL_SIZE = "large-v3-turbo"

print("Yapay zeka modeli VRAM'e (Ekran Kartına) yükleniyor, lütfen bekleyin...")
# device="cuda" ve compute_type="float16" ile ekran kartınızın tüm gücünü kullanır (RTX'in hakkını verir)
model = WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16")
print("Model başarıyla yüklendi! F9 tuşuna BASILI TUTARAK konuşun.")

# Ses kayıt ayarları
CHANNELS = 1
RATE = 16000

# Global Değişkenler
is_recording = False
audio_q = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Mikrofon her zaman açıktır ancak sadece F9'a basılıyken (is_recording=True) kasaya veri atar."""
    if is_recording:
        audio_q.put(indata.copy())

def main():
    global is_recording
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, "whisper_temp.wav")
    
    print("\n✅ Sistem Tamamen Hazır! Mikrofon arka planda aktif...")
    print("👉 İstediğiniz zaman F9'a basılı tutup konuşabilirsiniz (Gecikme süresi 0 ms).")
    
    # Mikrofonu bir kez açıp sonsuz döngü boyunca açık bırakıyoruz. Böylece "telsizin açılmasını bekleme" gecikmesi yaşanmıyor.
    with sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=audio_callback):
        while True:
            # F9 tuşuna basılmasını bekle
            keyboard.wait('f9')
            
            print("\n🔴 Kayıt başladı! Konuşun... (Tuşu bıraktığınızda çevrilir)")
            
            # İçerideki eski ses kırıntılarını temizle
            while not audio_q.empty():
                audio_q.get_nowait()
                
            # Mikrofondan gelen seli "kaydet" moduna geçir
            is_recording = True
            
            # Basılı tutulduğu sürece bekle
            while keyboard.is_pressed('f9'):
                time.sleep(0.01)
                
            # Tuş bırakıldığında, insanın son kelimesinin (yankı, nefes vb.) kesilmemesi için 
            # kaydı durdurmadan önce ekstra yarım saniye (0.4 sn) daha kaydet
            time.sleep(0.4)
                
            # Kaydı tamamen durdur
            is_recording = False
            
            # Biriktirilen blokları çıkar
            audio_data = []
            while not audio_q.empty():
                audio_data.append(audio_q.get())
                
            if not audio_data:
                continue
                
            audio_concat = np.concatenate(audio_data, axis=0)
            
            # Eğer 0.5 saniyeden kısa basıldıysa görmezden gel (yanlışlıkla basmalara karşı)
            if len(audio_concat) < (RATE * 0.5):
                print("⚠️ Tuşa çok kısa bastınız, dikkate alınmadı.")
                continue
                
            sf.write(audio_path, audio_concat, RATE)
            
            print("⏳ Çevriliyor...")
            
            # Kullanıcının koda girmeden kelime ekleyebilmesi için dışarıdan .txt dosyası okuyoruz
            kelime_dosyasi = "kelimeler.txt"
            
            if not os.path.exists(kelime_dosyasi):
                # Eğer dosya henüz yoksa, varsayılan bir tane oluştur
                with open(kelime_dosyasi, "w", encoding="utf-8") as f:
                    f.write("Merhaba adım Burak. Ulaştırma Bakanlığı, n8n, Fine Tuning, LLM, RAG, yapay zeka gibi yazılım jargonları üzerine konuşuyorum düzgün dökebilmek için.")
            
            # Dosyayı oku (Böylece kullanıcı not defterini güncelleyip kaydettiğinde programı kapatıp açmasa bile anında etki eder)
            with open(kelime_dosyasi, "r", encoding="utf-8") as f:
                custom_dictionary = f.read().strip()
            
            # VAD filtresi baştaki/aradaki sessizlikleri kırparak yapay zekanın cümleyi unutmasını/atlamasını engeller
            segments, info = model.transcribe(audio_path, beam_size=5, language="tr", condition_on_previous_text=False, vad_filter=True, initial_prompt=custom_dictionary)
            
            # Segmentleri birleştir
            text = " ".join([segment.text for segment in segments]).strip()
            
            if text:
                print(f"✅ Yazdırılan metin: {text}")
                # Olası Türkçe karakter bozulmalarına karşı panoya kopyala
                pyperclip.copy(text)
                time.sleep(0.1) # Panonun işletim sistemi tarafından algılanması için çok kısa bir an bekle
                
                # Aktif pencereye yapıştır
                keyboard.press_and_release('ctrl+v')
            else:
                print("❌ Ses algılanmadı veya anlaşılamadı.")

if __name__ == "__main__":
    # Scriptin klavye komutlarını okuyabilmesi için Yönetici haklarıyla çalıştırılması gerekebilir
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram kapatıldı.")