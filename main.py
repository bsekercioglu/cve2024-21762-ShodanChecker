import socket
import ssl
import sys
import shodan
import requests
import OpenSSL.crypto
from requests.exceptions import RequestException
from requests.exceptions import Timeout


context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname=False
context.verify_mode=ssl.CERT_NONE

TIMEOUT=30
SHODAN_API_KEY='<SHODAN API KEY BURAYA YAZILACAK>'
api = shodan.Shodan(SHODAN_API_KEY)



def send_req(host, req):
    try:
        s=socket.create_connection(host, timeout=5)
    except: return -1
    ss=context.wrap_socket(s)
    ss.send(req)
    try:
        return ss.read(2048)
    except socket.timeout:
        return 0
        
control_req="""POST /remote/VULNCHECK HTTP/1.1\r
Host: {}\r
Transfer-Encoding: chunked\r
\r
0\r
\r
\r
"""

check_req="""POST /remote/VULNCHECK HTTP/1.1\r
Host: {}\r
Transfer-Encoding: chunked\r
\r
0000000000000000FF\r
\r
"""
def check(host):
    baseurl="https://{}:{}".format(*host)
    r1=send_req(host, control_req.format(baseurl).encode())
    
    if r1==-1:
        return "Bağlantı Hatası"
    if r1==0:
        return "İstek hatası oluştu"
        return
    if b"HTTP/1.1 403 Forbidden" not in r1:
        print("[UYARI] Bu sistem Fortigate SSL VPN yapısını kullanmıyor.")
    r2=send_req(host, check_req.format(baseurl).encode())
    if r2==0: return "SSL VPN Açığı var. Firmware güncellenmesi gerekli"
    else: return "Güvenlik yaması yapılmış."

def get_ssl_cert_cn(ip):
    url = f'https://{ip}:10443/'  # IP adresine ve 10443 portuna HTTPS isteği gönderme
    try:
        response = requests.get(url, verify=False,timeout=60)  # HTTPS sertifikasını doğrulamamak için verify=False kullanılıyor
        if response.status_code == 200:
            # SSL sertifikasını al
            cert = ssl.get_server_certificate((ip, 10443))
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            # Subject içinden CN (Common Name) bilgisini al
            cn = dict(x509.get_subject().get_components()).get(b'CN').decode()
            return (f'IP: {ip}, Model: {cn}')
    except RequestException as e:
        print(f'{ip} adresinden bilgi alınamadı: {e}')
    except Timeout as e:
        print(f'{ip} adresinde TimeOut durumu oluştu')
    except Exception as e:
        print(f'{ip} adresinden bilgi alınamadı: {e}')


def get_fortinet_device_info(ip):
    url = f'https://{ip}:10443/'  # IP adresine ve 10443 portuna HTTPS isteği gönderme
    try:
        response = requests.get(url, verify=False)  # HTTPS sertifikasını doğrulamamak için verify=False kullanılıyor
        if response.status_code == 200:
            # Yanıt başlıklarından Fortinet: Device: kısmını alarak ekrana yazdırma
            fortinet_device_info = response.headers.get('Fortinet: Device:')
            
            print(f'IP: {ip}, Fortinet Device Info: {fortinet_device_info}')
    except Exception as e:
        print(f'Error fetching data from {ip}: {e}')

        
def main():
    # Shodan API'ye bağlanma
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        # Shodan API'ye sorguyu gönderme
        result = api.search('port:10443 city:samsun')

        # IP adreslerini listeye alma
        ip_list = [entry['ip_str'] for entry in result['matches']]

        # IP adreslerini ekrana yazdırma
        for ip in ip_list:
            HOST=(ip,10443)
            print(get_ssl_cert_cn(ip),check(HOST))
            

    except shodan.APIError as e:
        print('Error: %s' % e)

if __name__ == '__main__':
    main()
