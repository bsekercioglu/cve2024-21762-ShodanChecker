# Shodan API ile Fortinet SSL VPN Zafiyeti Kontrolü

Bu Python programı, Shodan.io API'sini kullanarak belirli bir şehirdeki (örneğin, "Samsun" gibi) belirli bir portta (örneğin, 10443) çalışan Fortinet SSL VPN sunucularının zafiyetlerini kontrol eder. Program, her sunucu için SSL sertifikası bilgilerini alır ve Fortinet SSL VPN sunucusu olup olmadığını belirlemek için kontrol isteği gönderir. Sonuçlar, her sunucu için bir rapor oluşturularak ekrana yazdırılır.

## Kullanım

1. Shodan.io API anahtarınızı `SHODAN_API_KEY` değişkenine yerleştirin.
2. Gerekirse, arama sorgusunu (`api.search` fonksiyonu içindeki sorgu) düzenleyin. Varsayılan olarak "port:10443 city:samsun" olarak ayarlanmıştır.
3. Programı çalıştırın.

## Gereksinimler

- Python 3.x
- `shodan`, `requests`, `pyopenssl` ve `OpenSSL` kütüphaneleri

## Kurulum

1. Python 3.x yükleyin.
2. Gerekli Python kütüphanelerini yüklemek için terminal veya komut istemcisinde aşağıdaki komutu çalıştırın:

pip install shodan requests pyopenssl

3. `main.py` dosyasını çalıştırın.

## Notlar

- Bu program, belirli bir şehirde belirli bir portta çalışan Fortinet SSL VPN sunucularının zafiyetlerini kontrol etmek için Shodan.io API'sini kullanır.
- Program, her sunucunun SSL sertifikası bilgilerini almak için OpenSSL ve pyOpenSSL kütüphanelerini kullanır.
- `check` fonksiyonu, Fortinet SSL VPN sunucusunun zafiyetini kontrol eder. `get_ssl_cert_cn` fonksiyonu ise sunucunun SSL sertifikası bilgilerini alır.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.
