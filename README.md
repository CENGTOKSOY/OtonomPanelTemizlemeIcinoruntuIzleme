Gereksinimler

- Raspberry Pi
- L298N Motor Sürücü
- DC Motorlar (motor sürücüye bağlı)
- Su pompası
- Raspberry Pi ile uyumlu bir kamera
- OpenCV
- NumPy
- RPi.GPIO kütüphanesi

Kurulum

OpenCV ve NumPy Kurulumu:

bash
Kodu kopyala
sudo apt-get update
sudo apt-get install python3-opencv
pip3 install numpy

Kamera arayüzünü etkinleştirin:

bash
Kodu kopyala
sudo raspi-config
Interfacing Options > Camera yolunu izleyerek etkinleştirin.

Bu depoyu Raspberry Pi'nize klonlayın veya indirin.

Kullanım

Robotu Hazırlayın:

DC motorları L298N motor sürücüye bağlayın.
Motor sürücüyü, kodda belirtilen GPIO pinlerine Raspberry Pi'ye bağlayın.
Kamerayı robotun üstüne yerleştirin.
Su pompasının belirtilen GPIO pinine bağlı olduğundan emin olun.

Robotu güneş paneli üzerine yerleştirin:
Öncelikle panelin temiz olduğundan emin olun ve clean_panel_image.png isimli bir referans görüntüsü alın.

Kodu Çalıştırın:

bash
Kodu kopyala
python3 SolarPanelCleanRobot.py

Kod Açıklaması

Ana kod birkaç bölüme ayrılmıştır:

Başlangıç
Gerekli kütüphanelerin (cv2, numpy, time, RPi.GPIO) import edilmesi.
Motorlar ve su pompası kontrolü için bir Robot sınıfının tanımlanması.
GPIO pinlerinin motorlar ve su pompası için ayarlanması.

Robot Sınıfı
__init__: Motor pinlerini başlatır ve GPIO ayarlarını yapar.
setup_gpio: GPIO ayarlarını yapılandırır.
move_robot: Robotun hareket yönünü ve süresini kontrol eder.
set_motor_direction: Motor pinlerini ileri ve geri hareket için ayarlar.
activate_motors: Belirtilen motorları aktif hale getirir.
stop_all_motors: Tüm motorları durdurur.
start_cleaning: Temizlik işlemini başlatır.
stop_cleaning: Temizlik işlemini durdurur.

Yüzey Taraması
scan_surface: Robotun üzerindeki kameradan alınan görüntü ile referans görüntüyü karşılaştırarak kir tespit eder.

Ana Döngü
Güneş panelinin temiz referans görüntüsünü yakalar.
Sürekli olarak yüzeyi tarar ve kir olup olmadığını kontrol eder.
Kir tespit edilmezse robotu ileri hareket ettirir, kir tespit edilirse robotu durdurur ve temizlik işlemini başlatır.
Temizlik işlemi tamamlandığında yeniden taramaya başlar.

İstisna Yönetimi
KeyboardInterrupt (Ctrl+C) ile program sonlandırıldığında kamera kaynaklarını serbest bırakır, OpenCV pencerelerini kapatır ve GPIO ayarlarını temizler.

Kodun Açıklaması
Bu kod, Raspberry Pi, bir kamera ve birkaç DC motor kullanarak güneş panellerini temizlemek üzere tasarlanmış bir robotu kontrol eder. Robot, güneş paneli yüzeyinde kir tespit etmek için sürekli tarama yapar ve tespit edilen kir noktalarını temizlemek üzere hareket eder.

Ana Bileşenler:

Robot Sınıfı:
GPIO pinlerine bağlı motorlar ve su pompasının başlangıç ve ayarlarını yapar.
Robotun ileri ve geri hareketini, temizleme mekanizmasının başlatılması ve durdurulmasını sağlar.

Yüzey Taraması:
Kameradan alınan görüntüleri OpenCV kullanarak işler.
Mevcut görüntüyü temiz güneş paneli referans görüntüsü ile karşılaştırarak farklılıkları tespit eder.
scan_surface fonksiyonu, görüntüyü işleyerek kir tespiti yapar ve sonuç döner.

Ana Döngü:
Sürekli olarak güneş panelini kir için tarar.
Kir tespit edilmezse robotu ileri hareket ettirir.
Kir tespit edildiğinde robotu durdurur ve temizleme işlemini başlatır.
Temizlik tamamlandığında tarama işlemine devam eder.

GPIO Yapılandırması:
GPIO pinleri, motorları L298N motor sürücü kullanarak kontrol etmek için yapılandırılmıştır. Her motorun yön kontrolü için iki kontrol pini (IN1 ve IN2) bulunur.
Su pompası, tek bir GPIO pinine bağlıdır.

Motor Kontrolü:
set_motor_direction metodu, motor pinlerini ileri veya geri hareket için ayarlar.
activate_motors metodu, gerekli pinleri HIGH yaparak motorları başlatır.
stop_all_motors metodu, tüm motor pinlerini LOW yaparak motorları durdurur.

Temizlik Mekanizması:
start_cleaning metodu, temizleme silindiri motorunu ve su pompasını çalıştırır.
stop_cleaning metodu, temizleme motorunu ve su pompasını durdurur.

Bu yapı, robotun otonom bir şekilde güneş paneli temizleme işlemini gerçekleştirmesini sağlar; kir tespiti yapar, kirli noktaya hareket eder, temizler ve sonra taramaya devam eder.
