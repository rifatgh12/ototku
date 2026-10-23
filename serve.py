import http.server
import socket
import socketserver
import sys
import webbrowser
import os

# Pastikan console Windows mendukung output UTF-8 untuk QR Code & emoji
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def get_local_ips():
    """Mendeteksi IP lokal komputer di jaringan Wi-Fi / LAN"""
    ips = []
    # Metode 1: Dummy socket connect ke router/internet
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        main_ip = s.getsockname()[0]
        s.close()
        if main_ip and not main_ip.startswith("127."):
            ips.append(main_ip)
    except Exception:
        pass

    # Metode 2: Cek semua interface lokal
    try:
        hostname = socket.gethostname()
        for addr in socket.gethostbyname_ex(hostname)[2]:
            if not addr.startswith("127.") and addr not in ips:
                ips.append(addr)
    except Exception:
        pass

    return ips if ips else ["127.0.0.1"]

class OtotKuHandler(http.server.SimpleHTTPRequestHandler):
    """Handler HTTP dengan MIME types lengkap untuk PWA & Web modern"""
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.webmanifest': 'application/manifest+json',
        '.json': 'application/json',
        '.svg': 'image/svg+xml',
        '.js': 'application/javascript',
        '.mjs': 'application/javascript',
        '.png': 'image/png',
        '.webp': 'image/webp',
        '.ico': 'image/x-icon',
        '.css': 'text/css',
        '.html': 'text/html; charset=utf-8',
    }

    def end_headers(self):
        # Header agar PWA dan caching berjalan optimal
        self.send_header('Cache-Control', 'no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        # Buat log request terminal tetap rapi dan tidak bising
        if any(args[0].startswith(x) for x in ['GET /favicon', 'GET /icon']):
            return
        sys.stdout.write(f"  [Akses] {self.address_string()} -> {args[0]}\n")

def find_available_port(start_port=8000, max_tries=20):
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    return start_port

def print_qr_code(url):
    """Mencetak QR Code scannable di terminal"""
    try:
        import qrcode
        qr = qrcode.QRCode(box_size=1, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        print("\n  📱 SCAN QR CODE INI MENGGUNAKAN KAMERA HP ANDA:\n")
        qr.print_ascii(invert=True)
        print("")
        return True
    except Exception as e:
        return False

def main():
    # Pastikan direktori kerja adalah lokasi file ini
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    port = find_available_port(8000)
    ips = get_local_ips()
    primary_ip = ips[0]
    device_url = f"http://{primary_ip}:{port}"
    local_url = f"http://localhost:{port}"

    print("=" * 66)
    print("      🚀 OTOTKU - SERVER LOKAL UNTUK PERANGKAT LAIN 📱")
    print("=" * 66)
    print("  Server web lokal aktif dan siap diakses!")
    print(f"\n  👉 Buka di Komputer ini:   {local_url}")
    print(f"  👉 Buka di HP/Tablet/Device lain: \033[1;32m{device_url}\033[0m")
    
    if len(ips) > 1:
        print("  (IP alternatif jika Wi-Fi berbeda: " + ", ".join([f"http://{ip}:{port}" for ip in ips[1:]]) + ")")

    # Cetak QR Code di terminal
    qr_shown = print_qr_code(device_url)

    print("-" * 66)
    print("  📋 CARA MEMBUKA DI HP / PERANGKAT LAIN:")
    print("  1. Pastikan HP dan Komputer terhubung ke Wi-Fi / Hotspot yang SAMA.")
    if qr_shown:
        print("  2. Arahkan Kamera HP ke QR Code di atas (atau buka link di browser HP).")
    else:
        print(f"  2. Buka browser di HP (Chrome / Safari), lalu ketik: {device_url}")
    print("  3. Di browser HP, ketuk menu lalu pilih 'Tambahkan ke Layar Utama'")
    print("     atau 'Instal Aplikasi' untuk menjadikannya seperti aplikasi native!")
    print("-" * 66)
    print("  Tekan Ctrl + C di jendela ini untuk mematikan server.")
    print("=" * 66 + "\n")

    # Buka browser lokal di PC otomatis
    try:
        webbrowser.open(local_url)
    except Exception:
        pass

    try:
        with socketserver.TCPServer(("0.0.0.0", port), OtotKuHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server dihentikan. Sampai jumpa lagi di latihan berikutnya!\n")
    except Exception as e:
        print(f"\n❌ Error menjalankan server: {e}\n")

if __name__ == '__main__':
    main()
