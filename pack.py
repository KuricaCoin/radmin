import socket
import time
import threading
import json
import re
import os
import sys
from datetime import datetime

# ============= ВСТРОЕННАЯ КОНФИГУРАЦИЯ FIREBASE =============
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDVlmR7JsxP0yfR4EQYmecZ2qzigqVkzYY",
    "authDomain": "radminservers.firebaseapp.com",
    "databaseURL": "https://radminservers-default-rtdb.firebaseio.com",
    "projectId": "radminservers",
    "storageBucket": "radminservers.firebasestorage.app",
    "messagingSenderId": "12810811697",
    "appId": "1:12810811697:web:a17080d449c77cad921810",
    "measurementId": "G-MJC1SW954W"
}

# ============= ВСТРОЕННЫЙ SERVICE ACCOUNT КЛЮЧ =============
SERVICE_ACCOUNT_KEY = {
    "type": "service_account",
    "project_id": "radminservers",
    "private_key_id": "9720f73e08dcb8210a069e8e1be1694ecc3468ea",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDjF2dDLOWW0VM0\noTxrFxEE3LXovMIgaBkkbiJ8S/Em5va2GDB/F2iFJ63tJiEcoPquAQmacBtqgKls\n3hc8/cPw79CCFr/vyhEYOIfl+lj1VPC/nVnl+g0iGi3Ft8jA2l34I8LpNaxsjFUL\ndSkJIdG1/Rt02wQu7AFp8k7ZKNaJjpE+g/Szj+z5xg3v3emm0GxQdjrQq7NFrvRQ\nEuL8r2l4HAEOY6mAYAbQDVdq4rdGuOjKt3b5Ow7K1kkM1BKjX+LfokxjN8ua9LPI\n0hYOb99F4VFWRVmNjxH175i0ykvtMjHRQQLig8pW4GWMmNm/teXLDqIOoiNDLbJy\noqJxuzbRAgMBAAECggEAcRIslNqMgHE+jDSCCFJmY3Tf0H/36rnaVvTNj/UiIDwc\n+GMH9qf5n1837x4um3oeBzi2BuMuC3P/qBjXGkPCZbuKptNcAzGqHFS9ecmStKjz\n7HyVD/jWxDWjt9BAEaJI6q4ntQXIEg43pCpUYdsod4SMwLzykshpFc8T6nW2iKt3\nGy+7i2w8M2IBlH3N8eC89D8lLiKixp/+VCYdGX8T7NFfqGiczbWsyn0nGJ4GBNJn\nj+u1jTPKDAz69SjQlD9xdL8c9FZsoyU4BbiYsyjY0+WPU1ymfn+eMkQs+rUAXqpM\nAxjKwLKcKl7cd9BlvkR5s2Foc1GevFXOeh4wo7/URwKBgQD7qkDGspviqaT311YA\nYBP+MNZBYmxE/w+6Z6m0rXalnHU6nVnkBoA1Y45I2r2Nnvgs6LUD/uolOakl91MB\nMjaLo8x7PH4kgEhy6YrWZ4hqAzQLkAQb8/IEL3UpV0BqM8nOozVY9j3U8uykM20Q\ngGDyFjTFpjgaTaaQjKiJGsx1owKBgQDnAMo8kSxHCaaDdSjsG2PW/HtMdzxiNDoS\nILRT8yQ3GcFn46Rx/zUMT/e/GNy4IP8utc/F/gUuTs1M3cgZttue8e3dZOEtTaTl\nsSnVcSEEqx7gemNiTHOLHmBtI2XrODNELTImQ+Sr6qNU6C2PBelH8vnk6AX6JdKM\nswVs5yqg+wKBgFsHPQDh7+Kvi/0dhX0DQ5gI4CasTA801uKMxmSU7bp/eiOmcLI6\n67rj9L5DaJbGLmxIC9mTJewrDBSwffSLzhD6QWc9/T6ErC/sa4ybzErUN8oK4IGf\n3iVHaTB339PKQa+ddxljj//rkk7eTw/N78MA5zuqoNZayem1Buz4pYXTAoGAKkh+\nvC9mh2pAzHc5kl5BHC0C9LAuoVsl9gN+fo9W5a8VM8r7YtJwB1zr4FLQs/N2QjqN\nWZRxplROR++gnPRXpvRpscixXvWDZXfUTHl0rcIU2MoOPwP3clORGukL0s5qs+QB\n9fcfeEhutS/6ht9yH/VdwISn823Q6Ggsag62QtkCgYEAwUx6WQpLu/w5cuJsVvxQ\njqntjquNZ7YXnUCM9FOYJNyidAcoXV3/d806TJeKoV2Ure55Hls2Wf5dmyqjj/WG\ngHW1PD+pF9et+U28kDcOXgACRwRwxPHSiJErId/c75FIDeSPwYFfem+Bhu0tCS7C\nJ0sZ/AvA467rvsZ6edkhVv8=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fbsvc@radminservers.iam.gserviceaccount.com",
    "client_id": "100286210170451665711",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40radminservers.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# ============= ПОДКЛЮЧЕНИЕ FIREBASE (без файлов) =============
firebase_initialized = False
firebase_ref = None

def init_firebase():
    """Инициализация Firebase со встроенным ключом"""
    global firebase_initialized, firebase_ref
    
    try:
        import firebase_admin
        from firebase_admin import credentials, db
        
        # Используем встроенный словарь как ключ
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
        
        # Инициализируем (если еще не инициализировано)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_CONFIG['databaseURL']
            })
            print("[OK] Firebase подключен успешно!")
        
        firebase_ref = db.reference('/servers')
        firebase_initialized = True
        return True
        
    except Exception as e:
        print(f"[ОШИБКА] Firebase: {e}")
        return False

# ============= ОТПРАВКА В FIREBASE =============
def send_to_firebase(servers_dict):
    """Отправка данных в Firebase"""
    global firebase_ref
    
    if not firebase_initialized or not firebase_ref:
        return False
    
    try:
        servers_list = []
        for key, server in servers_dict.items():
            # Очищаем MOTD от цветовых кодов
            clean_motd = re.sub(r'§[0-9a-fklmnor]', '', server['motd'])[:100]
            
            servers_list.append({
                'ip': server['ip'],
                'motd': clean_motd,
                'ad': server['ad'],
                'last_seen': server['last_seen']
            })
        
        data = {
            'timestamp': time.time(),
            'count': len(servers_list),
            'servers': servers_list,
            'last_update': datetime.now().isoformat()
        }
        
        # Отправляем данные
        firebase_ref.set(data)
        print(f"[OK] Отправлено {len(servers_list)} серверов в Firebase")
        return True
        
    except Exception as e:
        print(f"[ОШИБКА] Отправка: {e}")
        return False

# ============= ПОИСК СЕРВЕРОВ =============
MULTICAST_IP = "224.0.2.60"
PORT = 4445

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_servers():
    """Основная функция сканирования"""
    servers = {}
    running = True
    
    # Слушатель мультикаста
    def listener():
        nonlocal running
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', PORT))
            
            mreq = socket.inet_aton(MULTICAST_IP) + socket.inet_aton('0.0.0.0')
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            
            while running:
                sock.settimeout(1)
                try:
                    data, addr = sock.recvfrom(65535)
                    msg = data.decode(errors='ignore')
                    
                    if '[MOTD]' in msg and '[/MOTD]' in msg and '[AD]' in msg and '[/AD]' in msg:
                        motd = msg.split('[MOTD]')[1].split('[/MOTD]')[0]
                        ad = msg.split('[AD]')[1].split('[/AD]')[0]
                        key = f"{addr[0]}:{ad}"
                        
                        servers[key] = {
                            'ip': addr[0],
                            'motd': motd,
                            'ad': ad,
                            'last_seen': time.time()
                        }
                except socket.timeout:
                    pass
                except:
                    pass
        except Exception as e:
            print(f"Ошибка слушателя: {e}")
    
    # Запускаем слушатель
    thread = threading.Thread(target=listener, daemon=True)
    thread.start()
    
    # Инициализируем Firebase
    print("Инициализация Firebase...")
    init_firebase()
    
    last_send = 0
    send_interval = 15
    
    print("=" * 50)
    print("Radmin Server Scanner")
    print("=" * 50)
    print(f"Мультикаст: {MULTICAST_IP}:{PORT}")
    print("=" * 50)
    print("\nСканирование запущено. Нажмите Ctrl+C для выхода\n")
    
    try:
        while running:
            current_time = time.time()
            
            # Очистка старых серверов (нет пакетов > 10 сек)
            for key in list(servers.keys()):
                if current_time - servers[key]['last_seen'] > 10:
                    del servers[key]
            
            clear_screen()
            
            # Вывод информации
            print("=" * 50)
            print("Radmin Server Scanner")
            print("=" * 50)
            
            if servers:
                print(f"\nНайдено серверов: {len(servers)}\n")
                print("-" * 50)
                
                for i, (key, srv) in enumerate(servers.items(), 1):
                    clean_motd = re.sub(r'§[0-9a-fklmnor]', '', srv['motd'])[:50]
                    print(f"{i:2}. IP: {srv['ip']}")
                    print(f"    MOTD: {clean_motd}")
                    print(f"    AD: {srv['ad']}")
                    print()
                    
                    if i >= 20:
                        remaining = len(servers) - 20
                        if remaining > 0:
                            print(f"... и еще {remaining} серверов\n")
                        break
                
                print("-" * 50)
            else:
                print("\nПоиск серверов...\n")
                print("   Ожидание multicast пакетов от Radmin VPN")
                print("   Убедитесь что вы подключены к Radmin VPN\n")
            
            # Статус Firebase
            print("\n" + "=" * 50)
            if firebase_initialized:
                print("Firebase: ПОДКЛЮЧЕН")
                if servers:
                    next_send = max(0, int(send_interval - (current_time - last_send)))
                    print(f"Отправка каждые {send_interval} сек")
                    print(f"Следующая отправка через: {next_send} сек")
                else:
                    print("Ожидание серверов...")
            else:
                print("Firebase: НЕ ПОДКЛЮЧЕН")
                print("Проверьте интернет соединение")
            
            print("=" * 50)
            print("Нажмите Ctrl+C для выхода")
            print("=" * 50)
            
            # Отправка в Firebase
            if firebase_initialized and servers and (current_time - last_send >= send_interval):
                print("\nОтправка в Firebase...")
                send_to_firebase(servers)
                last_send = current_time
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\nЗавершение работы...")
        running = False
        time.sleep(1)
        print("Программа остановлена")

# ============= ЗАПУСК =============
if __name__ == "__main__":
    # Проверяем наличие firebase-admin
    try:
        import firebase_admin
    except ImportError:
        print("\n" + "=" * 50)
        print("Firebase не установлен!")
        print("=" * 50)
        print("\nУстановите Firebase:")
        print("  pip install firebase-admin")
        print("\nИли продолжайте без Firebase (только локальное отображение)")
        print("=" * 50)
        
        choice = input("\nПродолжить без Firebase? (y/n): ").lower()
        if choice != 'y':
            sys.exit(0)
    
    scan_servers()