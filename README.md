# 🌸 Anime DDoS Control Panel - F3MB0Y-AI Edition

<div align="center">
  <img src="https://img.shields.io/badge/Version-3.0-hotpink?style=for-the-badge&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3.13+-ff69b4?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-3.0.0-pink?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/License-Educational%20Only-red?style=for-the-badge">
</div>

<p align="center">
  <i>"Kawaii but Deadly ~ Senpai Notice Me!"</i><br>
  <b>✨ Web-based DDoS Control Panel dengan Tema Pink Anime ✨</b>
</p>

---

## 🎀 Features

| Feature | Description |
|---------|-------------|
| 🎨 **Pink Anime Theme** | UI aesthetic dengan warna pink + karakter anime |
| 🌐 **Web Based** | Control dari browser HP/PC/Laptop |
| ⚔️ **7 Attack Methods** | HTTP, Slowloris, TCP, UDP, SYN, ICMP, HADES MODE |
| 📊 **Real-time Stats** | Live monitoring packets, bytes, threads |
| 🎯 **IP/Domain Support** | Bisa pake IP atau domain langsung |
| 🔌 **Custom Port** | Bisa atur port target (default 12000) |
| 🚀 **150 Threads** | Attack power maksimal |
| 📱 **Responsive** | Bisa diakses dari HP |

---

## ⚔️ Attack Methods

| Method | Description | Power Level |
|--------|-------------|-------------|
| 🔥 **HTTP Flood** | Banjirin request HTTP ke web server | ⭐⭐⭐ |
| 🐌 **Slowloris** | Keep connections hanging, makan resource | ⭐⭐⭐⭐ |
| 💀 **TCP Flood** | Banjirin koneksi TCP | ⭐⭐⭐⭐ |
| 📦 **UDP Flood** | Banjirin packet UDP random | ⭐⭐⭐ |
| ⚡ **SYN Flood** | Half-open connections attack | ⭐⭐⭐⭐ |
| 📡 **ICMP Flood** | Ping flood attack | ⭐⭐ |
| 👑 **HADES MODE** | SEMUA METHOD SEKALIGUS! | ⭐⭐⭐⭐⭐ |

---

## 🚀 Installation (Termux)

```bash
# 1. Update packages
pkg update && pkg upgrade -y

# 2. Install Python & Git
pkg install python git -y

# 3. Clone repository
git clone https://github.com/Arxuoi/ddos_web
cd DDoS-Web-Control

# 4. Install Python packages
pip install flask requests

# 5. Run the server
python app.py
