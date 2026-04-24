# 🎤 Bas-Konuş Yapay Zeka Dikte Asistanı (Windows)

Bu proje, klavyenizdeki F9 tuşunu bir telsiz (bas-konuş) mandalı gibi kullanarak arka planda OpenAI'ın devasa hızlı ve zeki `large-v3-turbo` Whisper yapay zeka modelini çalıştıran sesli bir asistan projesidir. Siz tuşa basıp konuşursunuz, tuşu bıraktığınız an algıladığı metni kusursuz bir Türkçe (ve tam imla kuralları) ile anında aktif olan klasöre/pencereye yansıtıp yapıştırır.

## 🚀 Özellikler

- **0 ms Kayıt Ertelemesi:** Mikrofon kayıt motoru uyutulmadığı için F9 tuşuna bastığınız an "İlk harf yutulması" yaşatmadan kayda geçer.
- **Tail Padding (Kuyruk Koruması):** Cümle bittikten sonra tuşu bıraksanız bile program sesin mikrofon yolundaki yankısını kaçırmamak için siz fark etmeden 0.4 sn arka planda kaydetmeye devam eder, son harfleri es geçmez.
- **Kişisel Sözlük İle Tam Doğruluk (`kelimeler.txt`):** Yabancı terimleri, sektörel argoları (RAG, LoRA, n8n, Python) koda girmeden dışarıdan müdahaleyle kusursuz bir şekilde yazdırabilirsiniz. 
- **Derin VAD (Ses Duyarlılık) Filtresi:** Aralardaki nefes seslerini, dudak şapırdatmalarını veya uzun es boşluklarını tıraşlayarak yapay zekanın cümlenizi "yarıda kesilmiş" zannedip unutmasını engeller.
- **Ghost Paste (Oto-Yapıştır):** Elde ettiği mükemmel metni klavye-clipboard arayüzü ile doğrudan tarayıcınıza veya herhangi bir yazılımdaki input (metin) kutusuna sihir gibi yapıştırır.

---

## 🛠 Kurulum ve Sistem Gereksinimleri

Program `Python 3.8` veya üzeri bir sürüm ve **Windows işletim sistemi** üzerinde test edilerek yayınlanmıştır. Diğer projelerle çakışmaması adına Sanal Ortam (venv) kullanılarak indirilmesi tavsiye edilir.

### 1. Kütüphaneleri Yükleyin
Proje klasörünüze terminal ile girerek gereksinim kütüphanelerini kurun:
```powershell
pip install -r requirements.txt
```

*(Not: Proje performansı zirvede tutmak ve sesinizi saniyeler içinde anlayabilmek için ekran kartınızın Tensor çekirdeklerini (GPU/CUDA) kullanır. `ctranslate2` motorunun Windows'ta DLL dosyalarını bulabilmesi için projeye 1.5GB ağırlığındaki `nvidia-cublas-cu12` dosyaları paket ile entegre indirilmektedir. Siz bu gereksinimleri kurduğunuzda 3GB'lık NVIDIA CUDA Toolkit programını kurmanıza gerek kalmadan ekran kartınızla tam uyumlu çalışır).*

---

## 📖 Kullanım Kılavuzu

1. Projeyi bir komut satırında veya IDE üzerinde çalıştırın:
```powershell
python bas_konus.py
```
2. Terminal üstünde "Sistem Tamamen Hazır!" mesajını gördüğünüz an işlem tamamlanmıştır. (Not: Programı yürüttüğünüzde `large-v3-turbo` modelini henüz yüklemediyseniz ilk çalıştırmaya mahsus **3.1 GB** ebatında dosyaları internetten indirecek, sonraki kullanımlarda direkt çalışacaktır).
3. Parmağınızla **F9 tuşuna basılı tutun** ve konuşmaya başlayın (Bas-Çek yapmayın, mandal mantığı).
4. Cümleniz bittiğinde konuşmayı bırakın ve ardından son heceniz çıktıktan sonra **F9 tuşunu bırakın**.
5. Bir saniyeden kısa bir süre içinde terminalde "⏳ Çevriliyor..." ibaresini göreceksiniz. Elleriniz klavyeden uzaktayken arka plandaki o metin Chrome aramasına, not defterinize veya farenin aktif bıraktığı yer neresiyse anında kendiliğinden yapışacaktır.

---

### 🧠 Kelime Dağarcığını Eğitmek (Önemli!)
Uygulamayı çalıştırdığınız an klasörün kök dizinine otomatik olarak `kelimeler.txt` dosyası fırlatılır. İçine iş ve meslek alanınızda çok kullandığınız ancak sistemin yanlış anladığı terimleri (örneğin "LLM", "RAG", "Machine Learning", "Eksel" yerine Excel) virgülle ayırarak yazıp Not Defteri'ne **Kaydet(Ctrl+S)** deyin. 
Yapay zeka bunu bir kopya kağıdı belleği olarak beyninde tutacak, siz konuştuğunuz o saniyede kelime listesinde arayıp eşleştirecek ve o anki metni harika çıkartacaktır. (Bunun için programı kapatıp açmanıza gerek yoktur).

---

## ⚠️ Uyarılar ve Olası Hatalar

- Programın donanım tuşu `F9` hamlelerini işletim sistemi seviyesinde rahat yakalayabilmesi için kullandığınız IDE'nin ya da CMD/PowerShell pencerelerinin **Yönetici Olarak Çalıştırılması (Run As Administrator)** gerekebilir. 
- Yüksek boyutlu ses kartı hafızasına (VRAM) sahip bir donanımınız olmaması durumunda cihaz "Out-Of-Memory (OOM)" yani yetersiz bellek çökmesine maruz kalabilir. Bu problemi kod içerisindeki 27. Satırda yer alan `MODEL_SIZE` değerini `"large-v3-turbo"` yerine `"medium"` veya çok güçlü bir işlemciniz varsa `"small"` seçeneğiyle değiştirerek çözebilirsiniz.
