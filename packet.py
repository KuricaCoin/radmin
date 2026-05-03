import socket
import time
import threading
import json
import re
import os
import sys

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
    "private_key_id": "3f979279ebc00ba5c583d777fda63cf1de210e65",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDUE4fkIujwsAEz\nxa9tfN8Rs/WI6Baj3d29PqedxLrodJYiF8KS3M5NgBMMOe5xYI0VO9dJzovT2LBY\ncW7/y4uY/vzgLh18JsHLbVh71diZ/sjHpgUV1tlxJjFhNsLSbcaZ1OJzM10pMI0W\no/6e6k+5zMJPDDifPEFvvSFfnonNLy2bIqVsJiztZC+R7LfCTaBIGjnRN0C6QpGU\nfQHEjlmVO+deAA110b3bkZmx8YG9o41T3XhgatwFdhGQnrroUCaatjNOEl/ztyYx\niQOEtsk2G9PXI/BV5DUTP5VA93tHpiI0o6iwK5tSeb89OIq2tGoAet5zjzK7bdXj\nGvo/Cr55AgMBAAECggEACK1h5oY9JLf23KDujBrLX8SOu9LPNlY6H+ej4RMvGJrI\nl82EExFAya//V4U5Sd9K9n7z0JvIYdsgYAYIJiQ0aoaoXx3T7AQD8uhe8fYufiKM\nIYsb8yhOzk/jPliIwSZntVyeBVupKKnJZA9CuErbBz2nB6f22yEShlllN63bco80\nAn/+KvpFA0iKvcGLQzsbrg4dQqecdF9I1gsEVUh+aI+VWyw7H6O3HVxdnOQnfJX3\niYiOz2nywzamWwsWp4r+QIEFB+shJXBXzFsXho1aIBi5mZzsErPmirNIUdewt1yu\nDW8AbKIdyLnt2JsmrJ0ry4fE+2wEivu7OCCSUc7lwQKBgQD3xgvGW3SXMc+YyLzh\n5pM8BuNSsusXe+kjkDvBG3Ie+m2OXFK/BtJPu8oTMWwjw3y5sI/fUq55VNnq/Ef8\nAiqkrDJSn8mSBYntx8k3L+Ygj8nGYe3sikk1f4md3pwU2zXa5DkpGAAWVCa3yNbn\n4F5XSgeTuzriB8PYYwGNTQRg6QKBgQDbHhM6Papgvg6xAusYkJs6wgWQHtW4r+8/\nlmJYKj+hLk5tXV3ZER6TlqPeyUphAl3OGcVg660waPgIcMgxETyVN3move0NdVyZ\nGqnmPMTBhjWhvJJpOBvDOyHkX7sN6zs0vA1Vkz/cvpQVlKZxQ3jVHbGhxPqgIcLj\nZzOvQpR3EQKBgQDd937e8VluhYIbtmF34o8uLGGD2aNAQ5JleLX/Vi4TUHfLHCxI\n07yfD3WFYjYlh+B5nZIWF8UUDw62M9HtEqfPJDBk0p7KgMnCycMZ/IAl1YqGfX6e\n9HeHRL0tP5sGGCeT8/a9OLIDTtnstTDJQ7hgbIKDNy0WBqzNckyWoFN22QKBgC+X\nFqH9prWgUdyMP7d0IOLgJQkqSUz1mUb8SJvRgURmpE4Ii0uL9lIj06+dlHQBaZJL\n8pycU19CTSy4IiLWFYxrIhdOOOBFbzkpm2EQLcPCfH+GT15e+1ipzTCmwh/ByXgo\np9TASIyPL+aIBKZw+xt+eYgjGjQRYRy223jjQw+hAoGBALUTtEKYIpUeH3bKz/Pj\nRl0kD+W2KF2I27b4Tb84axzYe4udN6P71n8bPqmphTTWPAEWts/6uHqOPDlUhEHy\nhQFeeErxdfcxyg4PIKaqbL1bSGPZDqiMcSop/OFgeVByte4+0kZ263DUheHHH8X8\n/QjsXvY86G4ctxvXEGeLBxDE\n-----END PRIVATE KEY-----\n",
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
    """Инициализация Firebase со встроенной конфигурацией"""
    global firebase_initialized, firebase_ref
    
    try:
        import firebase_admin
        from firebase_admin import credentials, db
        
        # Используем встроенный ключ
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
        
        # Инициализируем (если еще не инициализировано)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_CONFIG['databaseURL']
            })
        
        firebase_ref = db.reference('/servers')
        firebase_initialized = True
        print("[OK] Firebase connected")
        return True
        
    except Exception as e:
        print(f"[ERROR] Firebase: {e}")
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
            'last_update': {'.sv': 'timestamp'}
        }
        
        firebase_ref.set(data)
        print(f"[OK] Sent {len(servers_list)} servers to Firebase")
        return True
        
    except Exception as e:
        print(f"[ERROR] Send failed: {e}")
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
            print(f"Listener error: {e}")
    
    # Запускаем слушатель
    thread = threading.Thread(target=listener, daemon=True)
    thread.start()
    
    # Инициализируем Firebase
    print("Initializing Firebase...")
    init_firebase()
    
    last_send = 0
    send_interval = 15
    
    print("=" * 60)
    print("Radmin Server Scanner")
    print("=" * 60)
    print(f"Multicast: {MULTICAST_IP}:{PORT}")
    print("=" * 60)
    print("\nScanning started. Press Ctrl+C to exit\n")
    
    try:
        while running:
            current_time = time.time()
            
            # Очистка старых серверов (нет пакетов > 10 сек)
            for key in list(servers.keys()):
                if current_time - servers[key]['last_seen'] > 10:
                    del servers[key]
            
            clear_screen()
            
            # Вывод информации
            print("=" * 60)
            print("Radmin Server Scanner")
            print("=" * 60)
            
            if servers:
                print(f"\nFound servers: {len(servers)}\n")
                print("-" * 60)
                
                # Показываем все сервера
                for i, (key, srv) in enumerate(servers.items(), 1):
                    clean_motd = re.sub(r'§[0-9a-fklmnor]', '', srv['motd'])[:50]
                    print(f"{i:2}. IP: {srv['ip']}")
                    print(f"    MOTD: {clean_motd}")
                    print(f"    AD: {srv['ad']}")
                    print()
                    
                    if i >= 20:
                        remaining = len(servers) - 20
                        if remaining > 0:
                            print(f"... and {remaining} more servers\n")
                        break
                
                print("-" * 60)
            else:
                print("\nSearching for servers...\n")
                print("   Waiting for multicast packets from Radmin VPN")
                print("   Make sure you are connected to Radmin VPN\n")
            
            # Статус Firebase
            print("\n" + "=" * 60)
            if firebase_initialized:
                print("Firebase: CONNECTED")
                if servers:
                    next_send = max(0, int(send_interval - (current_time - last_send)))
                    print(f"Send interval: every {send_interval} sec")
                    print(f"Next send in: {next_send} sec")
                else:
                    print("Waiting for servers...")
            else:
                print("Firebase: NOT CONNECTED")
                print("Check: pip install firebase-admin")
            
            print("=" * 60)
            print("Press Ctrl+C to exit")
            print("=" * 60)
            
            # Отправка в Firebase
            if firebase_initialized and servers and (current_time - last_send >= send_interval):
                print("\nSending to Firebase...")
                send_to_firebase(servers)
                last_send = current_time
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        running = False
        time.sleep(1)
        print("Program stopped")

# ============= ЗАПУСК =============
if __name__ == "__main__":
    # Проверяем наличие firebase-admin
    try:
        import firebase_admin
    except ImportError:
        print("\n" + "=" * 60)
        print("Firebase not installed!")
        print("=" * 60)
        print("\nInstall Firebase:")
        print("  pip install firebase-admin")
        print("\nOr continue without Firebase (local display only)")
        print("=" * 60)
        
        choice = input("\nContinue without Firebase? (y/n): ").lower()
        if choice != 'y':
            sys.exit(0)
    
    scan_servers()