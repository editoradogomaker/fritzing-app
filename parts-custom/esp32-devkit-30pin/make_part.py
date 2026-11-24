#!/usr/bin/env python3
"""Generates ESP32_DevKit_30pin_USB-C.fzpz (import in Fritzing: File > Import > Part...)."""
import os, zipfile

MODULE_ID = "ESP32_DevKit_30pin_USBC_01"
NAME = "ESP32_DevKit_30pin_USB-C"
LEFT = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"]
RIGHT = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"]
PINS = LEFT + RIGHT  # connector0..14 = left top->bottom, connector15..29 = right top->bottom
GPIO = {"VP": "GPIO36 (input only)", "VN": "GPIO39 (input only)", "D34": "GPIO34 (input only)", "D35": "GPIO35 (input only)",
        "TX0": "GPIO1 / UART0 TX", "RX0": "GPIO3 / UART0 RX", "TX2": "GPIO17 / UART2 TX", "RX2": "GPIO16 / UART2 RX",
        "EN": "Enable / reset", "VIN": "5V in/out (USB)", "3V3": "3.3V output"}
def desc(n):
    return GPIO.get(n, f"GPIO{n[1:]}" if n[0] == "D" else n)

# ---- breadboard: 1 unit = 0.01in. Rows 1.0in apart, 0.1in pitch, board 1.1 x 2.0in (USB-C sticks out below)
BW, BH = 110, 212
LX, RX, Y0 = 5, 105, 24
def pin_xy(i):
    return (LX, Y0 + 10 * i) if i < 15 else (RX, Y0 + 10 * (i - 15))

def breadboard():
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{BW/100}in" height="{BH/100}in" viewBox="0 0 {BW} {BH}">',
         '<g id="breadboard">',
         # black PCB
         '<rect x="0" y="0" width="110" height="200" rx="3" fill="#111111" stroke="#000000" stroke-width="0.6"/>',
         # PCB antenna area
         '<rect x="19" y="1" width="70" height="26" fill="#1c1c1c"/>',
         '<path d="M24 24 V6 H34 V20 H44 V6 H54 V20 H64 V6 H74 V20 H84 V6" fill="none" stroke="#c9a227" stroke-width="1.6"/>',
         # ESP-WROOM-32 metal shield
         '<rect x="22" y="27" width="64" height="70" rx="1" fill="#c9b062" stroke="#8a7634" stroke-width="0.6"/>',
         '<rect x="22" y="27" width="64" height="70" rx="1" fill="url(#g)" opacity="0.35"/>',
         '<text x="54" y="46" font-family="Droid Sans, Arial, sans-serif" font-size="10" fill="#5a4c1c" text-anchor="middle">ESP-32</text>',
         '<text x="54" y="56" font-family="Droid Sans, Arial, sans-serif" font-size="4" fill="#5a4c1c" text-anchor="middle">Wi-Fi + Bluetooth</text>',
         '<rect x="62" y="68" width="18" height="18" fill="#e8dfae" stroke="#5a4c1c" stroke-width="0.4"/>',
         '<circle cx="31" cy="90" r="1.6" fill="#5a4c1c"/>',
         # regulator, USB-UART chip, small SMD parts
         '<rect x="28" y="143" width="14" height="19" fill="#222" stroke="#444" stroke-width="0.4"/>',
         '<rect x="67" y="144" width="15" height="15" fill="#222" stroke="#555" stroke-width="0.4"/>',
         '<text x="44" y="150" font-family="Droid Sans, Arial, sans-serif" font-size="4" fill="#ddd">U2</text>',
         '<rect x="26" y="106" width="58" height="14" fill="#1a1a1a" stroke="#3a3a3a" stroke-width="0.4"/>',
         '<rect x="30" y="124" width="22" height="8" fill="#1a1a1a" stroke="#3a3a3a" stroke-width="0.4"/>',
         # EN / BOOT buttons
         '<rect x="18" y="180" width="11" height="11" fill="#c8c8c8" stroke="#777" stroke-width="0.5"/><circle cx="23.5" cy="185.5" r="3" fill="#333"/>',
         '<rect x="80" y="180" width="11" height="11" fill="#c8c8c8" stroke="#777" stroke-width="0.5"/><circle cx="85.5" cy="185.5" r="3" fill="#333"/>',
         '<text x="25" y="177" font-family="Droid Sans, Arial, sans-serif" font-size="4" fill="#eee" text-anchor="middle">EN</text>',
         '<text x="86" y="177" font-family="Droid Sans, Arial, sans-serif" font-size="4" fill="#eee" text-anchor="middle">BOOT</text>',
         # USB-C connector
         '<rect x="36" y="172" width="38" height="40" rx="2" fill="#b9bcc0" stroke="#6c7075" stroke-width="0.6"/>',
         '<rect x="40" y="195" width="30" height="8" rx="4" fill="#1a1a1a"/>',
         # mounting holes
         ''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#f2f2f2" stroke="#999" stroke-width="0.5"/>' for x, y in ((6, 9), (104, 9), (6, 190), (104, 190))),
         ]
    # pin labels (white), gold pin heads and connector hit areas
    for i, n in enumerate(PINS):
        x, y = pin_xy(i)
        if i < 15:
            s.append(f'<text x="11" y="{y+1.6}" font-family="Droid Sans, Arial, sans-serif" font-size="4.4" fill="#f4f4f4">{n}</text>')
        else:
            s.append(f'<text x="99" y="{y+1.6}" font-family="Droid Sans, Arial, sans-serif" font-size="4.4" fill="#f4f4f4" text-anchor="end">{n}</text>')
    for i in range(30):
        x, y = pin_xy(i)
        s.append(f'<circle cx="{x}" cy="{y}" r="2.7" fill="#d4af37" stroke="#8a6d12" stroke-width="0.5"/><circle cx="{x}" cy="{y}" r="1" fill="#222"/>')
    for i in range(30):
        x, y = pin_xy(i)
        s.append(f'<rect id="connector{i}pin" x="{x-2.5}" y="{y-2.5}" width="5" height="5" fill="none" stroke="none"/>')
    s.append('</g>')
    s.insert(1, '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient></defs>')
    s.append('</svg>')
    return "\n".join(s)

# ---- schematic: 1 unit = 0.01in, pin pitch 0.1in, pins 0.2in long
def schematic():
    W, H = 170, 190
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W/100}in" height="{H/100}in" viewBox="0 0 {W} {H}">',
         '<g id="schematic">',
         '<rect x="30" y="5" width="110" height="180" fill="#ffffff" stroke="#000000" stroke-width="1"/>',
         '<text x="85" y="17" font-family="Droid Sans, Arial, sans-serif" font-size="7" text-anchor="middle" fill="#000">ESP32 DevKit</text>']
    for i, n in enumerate(PINS):
        side_left = i < 15
        y = 30 + 10 * (i if side_left else i - 15)
        if side_left:
            x1, x2, tx, anchor = 10, 30, 34, "start"
        else:
            x1, x2, tx, anchor = 160, 140, 136, "end"
        s.append(f'<text x="{tx}" y="{y+2.3}" font-family="Droid Sans, Arial, sans-serif" font-size="6.5" text-anchor="{anchor}" fill="#000">{n}</text>')
        s.append(f'<line id="connector{i}pin" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#000000" stroke-width="1"/>')
        s.append(f'<rect id="connector{i}terminal" x="{x1-0.5 if side_left else x1-0.5}" y="{y-0.5}" width="1" height="1" fill="none" stroke="none"/>')
    s += ['</g>', '</svg>']
    return "\n".join(s)

# ---- pcb: 1 unit = 0.001in
def pcb():
    W, H = 1200, 2100
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W/1000}in" height="{H/1000}in" viewBox="0 0 {W} {H}">',
         '<g id="silkscreen">',
         '<rect x="50" y="60" width="1100" height="2000" fill="none" stroke="#ffffff" stroke-width="10"/>',
         '<text x="600" y="190" font-family="Droid Sans, Arial, sans-serif" font-size="70" text-anchor="middle" fill="#ffffff">ESP32 DevKit</text>',
         '<rect x="440" y="1830" width="320" height="230" fill="none" stroke="#ffffff" stroke-width="10"/>',
         '<text x="600" y="1960" font-family="Droid Sans, Arial, sans-serif" font-size="60" text-anchor="middle" fill="#ffffff">USB-C</text>',
         '</g>',
         '<g id="copper1"><g id="copper0">']
    for i in range(30):
        x = 100 if i < 15 else 1100
        y = 300 + 100 * (i if i < 15 else i - 15)
        s.append(f'<circle id="connector{i}pad" cx="{x}" cy="{y}" r="27.5" fill="none" stroke="#F7BD13" stroke-width="20"/>')
    s += ['</g></g>', '</svg>']
    return "\n".join(s)

def fzp():
    views = f"""<views>
<breadboardView><layers image='breadboard/{NAME}_breadboard.svg'><layer layerId='breadboard'/></layers></breadboardView>
<schematicView><layers image='schematic/{NAME}_schematic.svg'><layer layerId='schematic'/></layers></schematicView>
<pcbView><layers image='pcb/{NAME}_pcb.svg'><layer layerId='copper1'/><layer layerId='silkscreen'/><layer layerId='copper0'/></layers></pcbView>
<iconView><layers image='breadboard/{NAME}_breadboard.svg'><layer layerId='icon'/></layers></iconView>
</views>"""
    conns = []
    for i, n in enumerate(PINS):
        conns.append(f"""<connector id='connector{i}' type='male' name='{n}'>
<description>{desc(n)}</description>
<views>
<breadboardView><p layer='breadboard' svgId='connector{i}pin'/></breadboardView>
<schematicView><p layer='schematic' svgId='connector{i}pin' terminalId='connector{i}terminal'/></schematicView>
<pcbView><p layer='copper0' svgId='connector{i}pad'/><p layer='copper1' svgId='connector{i}pad'/></pcbView>
</views>
</connector>""")
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<module fritzingVersion='1.0.8' moduleId='{MODULE_ID}'>
<version>1</version>
<author>custom</author>
<title>ESP32 DevKit (30 pins, USB-C)</title>
<label>ESP32</label>
<date>2026-11-24</date>
<tags><tag>ESP32</tag><tag>WiFi</tag><tag>Bluetooth</tag><tag>DevKit</tag><tag>Espressif</tag></tags>
<properties>
<property name='family'>ESP32</property>
<property name='type'>ESP32 DevKit 30 pins USB-C</property>
<property name='variant'>variant 1</property>
<property name='part number'>ESP32 DevKit V1 (30 pin)</property>
</properties>
<description>ESP32 development board (ESP-WROOM-32), 30 pins, USB-C, 3.3V logic. Row spacing 1.0in (25.4mm), pitch 0.1in.</description>
{views}
<connectors>
{chr(10).join(conns)}
</connectors>
<buses>
<bus id='gnd'><nodeMember connectorId='connector13'/><nodeMember connectorId='connector28'/></bus>
</buses>
</module>
"""

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), NAME + ".fzpz")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"part.{NAME}.fzp", fzp())
        z.writestr(f"svg.breadboard.{NAME}_breadboard.svg", breadboard())
        z.writestr(f"svg.schematic.{NAME}_schematic.svg", schematic())
        z.writestr(f"svg.pcb.{NAME}_pcb.svg", pcb())
    print("wrote", out)
