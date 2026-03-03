import os
import json
import csv

BASE = os.path.join(os.path.dirname(__file__), 'data')
TXT_FILE = os.path.join(BASE, 'datos.txt')
JSON_FILE = os.path.join(BASE, 'datos.json')
CSV_FILE = os.path.join(BASE, 'datos.csv')


def save_txt(record: dict):
    os.makedirs(BASE, exist_ok=True)
    with open(TXT_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def read_txt():
    if not os.path.exists(TXT_FILE):
        return []
    with open(TXT_FILE, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def save_json(record: dict):
    os.makedirs(BASE, exist_ok=True)
    data = []
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
    data.append(record)
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []


def save_csv(record: dict):
    os.makedirs(BASE, exist_ok=True)
    exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['nombre','precio','cantidad'])
        if not exists:
            writer.writeheader()
        writer.writerow({
            'nombre': record.get('nombre',''),
            'precio': record.get('precio',''),
            'cantidad': record.get('cantidad','')
        })


def read_csv():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
