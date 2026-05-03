import socket
import time
import threading
import json
import re
import os
import sys
import requests
from datetime import datetime

# ============= КОНФИГУРАЦИЯ FIREBASE =============
DATABASE_URL = "https://radminservers-default-rtdb.firebaseio.com"
API_KEY = "AIzaSyDVlmR7JsxP0yfR4EQYmecZ2qzigqVkzYY"

# ============= ОТПРАВКА В FIREBASE ЧЕРЕЗ REST API =============
def send_to_firebase_rest(servers_dict):
    """Отправка данных в Firebase через REST API"""
    try:
        servers_list = []
        for key, server in servers_dict.items():
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
        
        # Отправляем через REST API
        url = f"{DATABASE_URL}/servers.json"
        response = requests.put(url, json=data)
        
        if response.status_code == 200:
            print(f"[OK] Отправлено {len(servers_list)} серверов в Firebase")
            return True
        else:
            print(f"[ОШИБКА] HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ОШИБКА] Отправка: {e}")
        return False

# ============= ПОИСК СЕРВЕРОВ =============
MULTICAST_IP = "224.0.2.60"
PORT = 4445

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_servers():
    servers = {}
    running = True
    
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
    
    thread = threading.Thread(target=listener, daemon=True)
    thread.start()
    
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
            
            for key in list(servers.keys()):
                if current_time - servers[key]['last_seen'] > 10:
                    del servers[key]
            
            clear_screen()
            
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
            
            print("\n" + "=" * 50)
            print("Firebase: АКТИВЕН (REST API)")
            if servers:
                next_send = max(0, int(send_interval - (current_time - last_send)))
                print(f"Отправка каждые {send_interval} сек")
                print(f"Следующая отправка через: {next_send} сек")
            else:
                print("Ожидание серверов...")
            
            print("=" * 50)
            print("Нажмите Ctrl+C для выхода")
            print("=" * 50)
            
            if servers and (current_time - last_send >= send_interval):
                print("\nОтправка в Firebase...")
                send_to_firebase_rest(servers)
                last_send = current_time
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\nЗавершение работы...")
        running = False
        time.sleep(1)
        print("Программа остановлена")

# ============= ЗАПУСК =============
if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("\n" + "=" * 50)
        print("Установите requests:")
        print("  pip install requests")
        print("=" * 50)
        sys.exit(1)
    
    scan_servers()