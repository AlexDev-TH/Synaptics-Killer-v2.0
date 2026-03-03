<div align="center">

<img width="773" height="705" alt="image" src="https://github.com/user-attachments/assets/1439d7bf-6715-4bb5-985a-ec94fef0801a" />
  
### ⚔ XRed Backdoor Recovery Tool v2.0

**เครื่องมือกู้คืนไฟล์ที่ติดเชื้อมัลแวร์ Synaptics (XRed Backdoor) สำหรับไฟล์ EXE และ XLSX**

[![Python](https://img.shields.io/badge/Python-3.6%2B-red?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-GPL%20v3-darkred?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v2.0-crimson?style=for-the-badge)](../../releases)
[![Platform](https://img.shields.io/badge/Platform-Windows-red?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)

<br>

**Set By AlexDev** 🇹🇭

<br>

[📥 ดาวน์โหลด Release](../../releases) · [🐛 แจ้งปัญหา](../../issues) · [⭐ ให้ดาว](#)

</div>

---

## 📋 สารบัญ

- [🔍 เกี่ยวกับโปรเจค](#-เกี่ยวกับโปรเจค)
- [☠ XRed Backdoor คืออะไร?](#-xred-backdoor-คืออะไร)
- [⚡ ฟีเจอร์หลัก](#-ฟีเจอร์หลัก)
- [🚀 วิธีใช้งาน](#-วิธีใช้งาน)
- [🔧 หลักการทำงาน](#-หลักการทำงาน)
- [📊 ผลลัพธ์การกู้คืน](#-ผลลัพธ์การกู้คืน)
- [🛠 Build เป็น EXE](#-build-เป็น-exe)
- [⚠️ ข้อควรระวัง](#%EF%B8%8F-ข้อควรระวัง)
- [📜 License](#-license)

---

## 🔍 เกี่ยวกับโปรเจค

**Synaptics-Killer v2.0** เป็นเครื่องมือ CLI (Command Line Interface) ที่ออกแบบมาเพื่อ **ตรวจจับและกู้คืนไฟล์** ที่ถูกมัลแวร์ **Synaptics (XRed Backdoor)** แพร่เชื้อ

เครื่องมือนี้สามารถ:
- 🔥 กู้คืนไฟล์ `.exe` ที่ติดเชื้อกลับมาเป็นไฟล์ต้นฉบับ
- 📊 กู้คืนไฟล์ `.xlsm` ที่ถูกฝัง macro โดยแปลงกลับเป็น `.xlsx`
- ☠ หยุดโปรเซสมัลแวร์ ลบ Registry และไฟล์ไวรัสออกจากระบบ
- 📄 สร้างรายงานการกู้คืนอัตโนมัติ

> 💡 **ไม่ต้องติดตั้ง dependency ใดๆ** — ใช้ Python Standard Library ล้วน

---

## ☠ XRed Backdoor คืออะไร?

**XRed** (หรือ Synaptics Worm) เป็นมัลแวร์ประเภท **Backdoor** ที่พบครั้งแรกตั้งแต่ **ปี 2019** โดยแอบอ้างเป็นไดรเวอร์ `Synaptics Pointing Device Driver` (ไดรเวอร์ทัชแพดโน้ตบุ๊ก) เพื่อหลอกผู้ใช้

### 🚨 พฤติกรรมอันตรายของ XRed:

```
┌─────────────────────────────────────────────────────────────────┐
│  🔑  Keylogging         ดักจับทุกการกดแป้นพิมพ์ (รหัสผ่าน,       │
│                         ข้อมูลบัตรเครดิต, ฯลฯ)                   │
├─────────────────────────────────────────────────────────────────┤
│  📡  Data Exfiltration  ขโมยข้อมูลระบบ (ชื่อผู้ใช้, MAC Address, │
│                         Computer Name) ส่งผ่าน SMTP              │
├─────────────────────────────────────────────────────────────────┤
│  🔄  Self-Replication   แพร่กระจายผ่าน USB Drive ด้วย            │
│                         autorun.inf                              │
├─────────────────────────────────────────────────────────────────┤
│  📊  Excel Infection    ฝัง VBA Macro อันตรายลงในไฟล์ Excel      │
│                         (.xlsx → .xlsm)                          │
├─────────────────────────────────────────────────────────────────┤
│  🚪  Remote Backdoor    เปิดช่องให้แฮกเกอร์เข้าถึงระบบ,          │
│                         สั่งรันคำสั่ง, ถ่ายภาพหน้าจอ              │
├─────────────────────────────────────────────────────────────────┤
│  🦠  EXE Infection      ติดเชื้อไฟล์ .exe 32-bit ทุกไฟล์         │
│                         ที่อยู่ในเครื่อง                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📍 IOCs (Indicators of Compromise):

| Indicator | Value |
|-----------|-------|
| Mutex | `Synaptics2X` |
| Install Path | `C:\ProgramData\Synaptics\Synaptics.exe` |
| C2 Domain | `xred.mooo.com` |
| Registry Key | `HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run` |
| File Description | `Synaptics Pointing Device Driver` |

---

## ⚡ ฟีเจอร์หลัก

<table>
<tr>
<td width="50%">

### 🔥 Recovery Engine
- ดึงไฟล์ต้นฉบับจาก `EXERESX` resource ใน PE structure
- ลบ VBA Macro ที่เป็นอันตรายจากไฟล์ Excel
- รองรับทั้งไฟล์ `.exe` และ `.xlsm`
- สร้าง backup `.bak` ก่อนกู้คืน (เลือกได้)

</td>
<td width="50%">

### ☠ System Cleanup
- Kill โปรเซส `Synaptics.exe` และ `EXCEL.EXE`
- ลบ Registry Run Key ที่มัลแวร์สร้างไว้
- ลบโฟลเดอร์ `C:\ProgramData\Synaptics\`
- สร้างรายงานการกู้คืนอัตโนมัติ

</td>
</tr>
<tr>
<td width="50%">

### 🎨 CLI Interface
- ASCII 3D Art Banner โทนสีแดง
- Progress Bar แบบ Gradient
- Loading Animation พร้อม Spinner
- Status Icons แยกสีตามประเภท

</td>
<td width="50%">

### 🛡 Zero Dependencies
- ใช้ Python Standard Library ล้วน
- ไม่ต้อง `pip install` อะไรเพิ่ม
- PE Parser เขียนเอง (Lightweight)
- รองรับ Python 3.6+

</td>
</tr>
</table>

---

## 🚀 วิธีใช้งาน

### ความต้องการ
- **Python** 3.6 ขึ้นไป
- **Windows** 10/11 (สำหรับการใช้งานจริง)
- **สิทธิ์ Administrator** (สำหรับ System Cleanup)

### รันโปรแกรม

```bash
python Synaptics-AlexDev.py
```

### เมนูหลัก

```
╔══════════════════════════════════════════════════════════════╗
║  ◆  MAIN MENU                                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   [1] 🔥 Scan & Recover (without .bak backup)               ║
║       เขียนทับไฟล์ติดเชื้อด้วยไฟล์ที่กู้คืนโดยตรง            ║
║                                                              ║
║   [2] 💾 Scan & Recover (with .bak backup)                   ║
║       สร้างไฟล์สำรอง .bak ก่อนกู้คืน                         ║
║                                                              ║
║   [3] ☠  Kill Virus Processes & Clean System                 ║
║       หยุดโปรเซส, ลบ Registry และไฟล์มัลแวร์                 ║
║                                                              ║
║   [4] 🔍 Scan Only (detect without recovery)                 ║
║       ตรวจหาไฟล์ติดเชื้อโดยไม่แก้ไข                          ║
║                                                              ║
║   [5] 📂 Custom Directory Scan                               ║
║       ระบุโฟลเดอร์เองเพื่อสแกน                                ║
║                                                              ║
║   [0] Exit                                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

| ตัวเลือก | การทำงาน | คำอธิบาย |
|:---------:|----------|----------|
| `1` | Scan & Recover (No Backup) | กู้คืนเลย ไม่สร้าง .bak |
| `2` | Scan & Recover (Backup) | สร้าง .bak ก่อน แล้วกู้คืน |
| `3` | System Cleanup | Kill process + ลบ Registry + ลบไฟล์ไวรัส |
| `4` | Scan Only | ตรวจหาอย่างเดียว ไม่แก้ไข |
| `5` | Custom Scan | เลือกโฟลเดอร์สแกนเอง |
| `0` | Exit | ออกจากโปรแกรม |

---

## 🔧 หลักการทำงาน

### 🔹 การกู้คืนไฟล์ EXE

```
  ไฟล์ EXE ที่ติดเชื้อ
  ┌──────────────────────────────────────┐
  │  [Virus Code: Synaptics Backdoor]    │  ← มัลแวร์ฝังตัวเอง
  │  ┌────────────────────────────────┐  │
  │  │  EXERESX Resource              │  │  ← ไฟล์ต้นฉบับถูกเก็บไว้ที่นี่
  │  │  ┌──────────────────────────┐  │  │
  │  │  │  Original EXE (ของจริง)  │  │  │  ← ดึงออกมา = กู้คืน 100%
  │  │  └──────────────────────────┘  │  │
  │  └────────────────────────────────┘  │
  └──────────────────────────────────────┘
```

**ขั้นตอน:**
1. สแกนโฟลเดอร์ `Downloads`, `Documents`, `Desktop`
2. ตรวจ File Description → `"Synaptics Pointing Device Driver"`
3. ค้นหา resource ชื่อ `EXERESX` ใน PE structure
4. ดึงข้อมูลออกมาเขียนทับ → **ได้ไฟล์ต้นฉบับคืน 100%**

### 🔹 การกู้คืนไฟล์ XLSX

```
  ไฟล์ XLSM ที่ติดเชื้อ (ZIP archive)
  ┌──────────────────────────────────────┐
  │  [Content_Types].xml                 │
  │  xl/workbook.xml                     │
  │  xl/worksheets/sheet1.xml            │  ← ข้อมูล Excel ปกติ
  │  xl/vbaProject.bin  ← ⚠️ MACRO ไวรัส │  ← ลบตัวนี้ออก!
  │  xl/_rels/workbook.xml.rels          │
  └──────────────────────────────────────┘

          ↓ ลบ macro + แก้ Content Types ↓

  ไฟล์ XLSX ที่กู้คืนแล้ว
  ┌──────────────────────────────────────┐
  │  [Content_Types].xml  (แก้ไขแล้ว)    │
  │  xl/workbook.xml                     │
  │  xl/worksheets/sheet1.xml            │  ← ข้อมูลเดิมยังอยู่
  │  xl/_rels/workbook.xml.rels (แก้ไข)  │
  └──────────────────────────────────────┘  ← ✅ ปลอดภัย!
```

### 🔹 System Cleanup Flow

```
  Phase 1: Kill Processes
  ├── taskkill /F /IM Synaptics.exe
  └── taskkill /F /IM EXCEL.EXE
          ↓
  Phase 2: Clean Registry
  ├── HKLM\...\CurrentVersion\Run  →  ลบ "Synaptics Pointing Device Driver"
  ├── HKLM\WOW6432Node\...\Run    →  ลบ "Synaptics Pointing Device Driver"
  └── HKCU\...\CurrentVersion\Run  →  ลบ "Synaptics Pointing Device Driver"
          ↓
  Phase 3: Delete Virus Files
  ├── C:\ProgramData\Synaptics\    →  ลบทั้งโฟลเดอร์
  └── C:\Windows\System32\Synaptics\  →  ลบทั้งโฟลเดอร์
          ↓
  ✅ System Clean!
```

---

## 📊 ผลลัพธ์การกู้คืน

| ประเภทไฟล์ | อัตราสำเร็จ | หมายเหตุ |
|:----------:|:----------:|----------|
| **EXE** | ✅ **100%** | ไฟล์ต้นฉบับถูกเก็บครบใน EXERESX resource |
| **XLSX** | ⚠️ **~90-95%** | ข้อมูลอาจสูญหายบางส่วนจากการติดเชื้อ |

---

## 🛠 Build เป็น EXE

สามารถ build เป็นไฟล์ `.exe` เพื่อแจกจ่ายได้โดยไม่ต้องติดตั้ง Python:

```bash
# ติดตั้ง PyInstaller
pip install pyinstaller

# Build เป็นไฟล์เดียว
pyinstaller --onefile --name Synaptics-Killer Synaptics-AlexDev.py

# ไฟล์ EXE จะอยู่ที่ dist/Synaptics-Killer.exe
```

> ⚠️ **หมายเหตุ:** ให้รัน EXE ในฐานะ **Administrator** เพื่อใช้งาน System Cleanup ได้เต็มรูปแบบ

---

## ⚠️ ข้อควรระวัง

> [!WARNING]
> - ไฟล์ XLSX ที่กู้คืนอาจมีข้อมูลสูญหายบางส่วน
> - การเลือก **"without backup"** จะเขียนทับไฟล์เดิมโดยตรง — ไม่สามารถย้อนกลับได้
> - แนะนำให้เลือก **"with .bak backup"** เสมอเพื่อความปลอดภัย
> - ต้องรันด้วยสิทธิ์ **Administrator** สำหรับ Kill Process และ Registry Cleanup

> [!TIP]
> - หากสงสัยว่าติดเชื้อ ให้ใช้ตัวเลือก `[4] Scan Only` ก่อนเพื่อตรวจสอบ
> - ตัดการเชื่อมต่ออินเทอร์เน็ตก่อนทำการกู้คืนเพื่อป้องกันการส่งข้อมูลออก
> - สแกนด้วยโปรแกรม Antivirus หลังกู้คืนเสร็จเพื่อความมั่นใจ

---

## 🗂 โครงสร้างโปรเจค

```
Synaptics-Killer-v2.0/
├── 📄 Synaptics-AlexDev.py    # เครื่องมือหลัก
├── 📄 README.md               # เอกสารนี้
└── 📄 LICENSE                  # GPL-3.0
```

---

## 🤝 Contributing

พบบัค หรือมีไอเดียปรับปรุง? ยินดีรับทุกคน!

1. **Fork** โปรเจคนี้
2. สร้าง **Branch** ใหม่ (`git checkout -b feature/amazing-feature`)
3. **Commit** การเปลี่ยนแปลง (`git commit -m 'Add amazing feature'`)
4. **Push** ไปที่ Branch (`git push origin feature/amazing-feature`)
5. เปิด **Pull Request**

---

## 📜 License

โปรเจคนี้เผยแพร่ภายใต้ **GNU General Public License v3.0 (GPL-3.0)**

ดูรายละเอียดได้ที่ [LICENSE](LICENSE)

---

## 📚 แหล่งอ้างอิง

- [eSentire — XRed Backdoor Analysis](https://www.esentire.com/blog/xred-backdoor-the-hidden-threat-in-trojanized-programs)
- [ANY.RUN — XRed Malware Overview](https://any.run/malware-trends/xred/)
- [Malpedia — XRed / Synaptics Worm](https://malpedia.caad.fkie.fraunhofer.de/details/win.xred)

---

<div align="center">

### ⭐ หากเครื่องมือนี้ช่วยคุณได้ กดให้ดาว ⭐ เพื่อสนับสนุนครับ!

<br>

**Made with ❤️ by AlexDev 🇹🇭**

**v2.0 — 2025**

<br>

[![GitHub](https://img.shields.io/badge/GitHub-AlexDev--TH-red?style=for-the-badge&logo=github)](https://github.com/AlexDev-TH)

</div>
