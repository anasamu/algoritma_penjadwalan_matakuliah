# utils.py

import json
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import random
import datetime # Import datetime for timestamp

def sks_to_minutes(sks):
    """Mengubah SKS menjadi durasi menit."""
    if sks == 2:
        return 90
    elif sks == 3:
        return 135
    return 0

def time_to_minutes(time_str):
    """Mengubah string waktu 'HH:MM' menjadi menit sejak 00:00."""
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

def minutes_to_time(total_minutes):
    """Mengubah total menit menjadi string waktu 'HH:MM'."""
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h:02d}:{m:02d}"

def load_dataset(filename):
    """Memuat dataset dari file JSON."""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def get_dosen_name(dosen_id, dosen_list):
    """Mendapatkan nama dosen dari ID."""
    for dosen in dosen_list:
        if dosen["id"] == dosen_id:
            return dosen["nama"]
    return "Unknown Dosen"

def get_usage_counts(schedule, key_name_or_func):
    """Helper to count usage of items based on a key name or function."""
    usage_counts = defaultdict(int)
    for item in schedule:
        if callable(key_name_or_func):
            key = key_name_or_func(item)
        else:
            key = item[key_name_or_func]
        usage_counts[key] += 1
    return dict(usage_counts)

# <hr/> Global Order for Days <hr/>
HARI_ORDER = {"Senin": 1, "Selasa": 2, "Rabu": 3, "Kamis": 4, "Jumat": 5, "Sabtu": 6, "Minggu": 7}
UNIQUE_ID = random.randint(100000, 999999)  # Unique ID for each report

# <hr/> Konflik Checker <hr/>
def check_conflicts(schedule):
    """Memeriksa konflik dalam jadwal."""
    konflik = []
    
    ruangan_slots = defaultdict(list)
    dosen_slots = defaultdict(list)

    for item in schedule:
        hari = item["hari"]
        jam_mulai = time_to_minutes(item["jam_mulai"])
        jam_selesai = time_to_minutes(item["jam_selesai"])
        ruangan = item["ruangan"]
        dosen = item["dosen"]
        
        ruangan_slots[hari].append((ruangan, jam_mulai, jam_selesai, item["matakuliah"]))
        dosen_slots[hari].append((dosen, jam_mulai, jam_selesai, item["matakuliah"]))

    for hari, sessions in ruangan_slots.items():
        for i, (ruang1, mulai1, selesai1, mk1) in enumerate(sessions):
            for j, (ruang2, mulai2, selesai2, mk2) in enumerate(sessions):
                if i != j and ruang1 == ruang2:
                    if not (selesai1 <= mulai2 or mulai1 >= selesai2):
                        konflik.append(f"[KONFLIK RUANGAN] {ruang1} - {hari} {minutes_to_time(mulai1)}-{minutes_to_time(selesai1)} ({mk1}) vs {minutes_to_time(mulai2)}-{minutes_to_time(selesai2)} ({mk2})")

    for hari, sessions in dosen_slots.items():
        for i, (dosen1, mulai1, selesai1, mk1) in enumerate(sessions):
            for j, (dosen2, mulai2, selesai2, mk2) in enumerate(sessions):
                if i != j and dosen1 == dosen2:
                    if not (selesai1 <= mulai2 or mulai1 >= selesai2):
                        konflik.append(f"[KONFLIK DOSEN] {dosen1} - {hari} {minutes_to_time(mulai1)}-{minutes_to_time(selesai1)} ({mk1}) vs {minutes_to_time(mulai2)}-{minutes_to_time(selesai2)} ({mk2})")

    return list(set(konflik))


# <hr/> Visualization Functions (Updated for 3 algorithms) <hr/>
def performance_comparison(backtracking_time, greedy_time, ilp_time, report_dir, filename="performance_comparison.png"):
    algorithms = ['Backtracking', 'Greedy', 'ILP']
    times = [backtracking_time, greedy_time, ilp_time]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, times, color=['skyblue', 'salmon', 'lightgreen'])
    plt.ylabel('Execution Time (seconds)')
    plt.title('Performa Eksekusi Algoritma Penjadwalan')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar, time_val in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f'{time_val:.4f}', ha='center', va='bottom')

    plt.tight_layout()
    os.makedirs(report_dir, exist_ok=True) # Ensure the specific report directory exists
    plt.savefig(os.path.join(report_dir, filename))
    plt.close()

def schedule_comparison(backtracking_schedule, greedy_schedule, ilp_schedule, report_dir, filename="schedule_comparison.png"):
    ordered_days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    
    backtracking_counts = [sum(1 for item in backtracking_schedule if item["hari"] == day) for day in ordered_days]
    greedy_counts = [sum(1 for item in greedy_schedule if item["hari"] == day) for day in ordered_days]
    ilp_counts = [sum(1 for item in ilp_schedule if item["hari"] == day) for day in ordered_days]

    x = range(len(ordered_days))
    width = 0.25

    plt.figure(figsize=(12, 7))
    plt.bar([i - width for i in x], backtracking_counts, width, label='Backtracking', color='skyblue')
    plt.bar(x, greedy_counts, width, label='Greedy', color='salmon')
    plt.bar([i + width for i in x], ilp_counts, width, label='ILP', color='lightgreen')

    plt.ylabel('Number of Scheduled Sessions')
    plt.title('Perbandingan Jumlah Sesi Terjadwal per Hari')
    plt.xticks(x, ordered_days)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    os.makedirs(report_dir, exist_ok=True) # Ensure the specific report directory exists
    plt.savefig(os.path.join(report_dir, filename))
    plt.close()

def compare_matakuliah_usage(backtracking_schedule, greedy_schedule, ilp_schedule, report_dir, filename="matakuliah_usage_comparison.png"):
    backtracking_mk_usage = get_usage_counts(backtracking_schedule, "matakuliah")
    greedy_mk_usage = get_usage_counts(greedy_schedule, "matakuliah")
    ilp_mk_usage = get_usage_counts(ilp_schedule, "matakuliah")

    all_matakuliah = sorted(list(set(list(backtracking_mk_usage.keys()) + list(greedy_mk_usage.keys()) + list(ilp_mk_usage.keys()))))
    
    backtracking_values = [backtracking_mk_usage.get(mk, 0) for mk in all_matakuliah]
    greedy_values = [greedy_mk_usage.get(mk, 0) for mk in all_matakuliah]
    ilp_values = [ilp_mk_usage.get(mk, 0) for mk in all_matakuliah]

    x = range(len(all_matakuliah))
    width = 0.25

    plt.figure(figsize=(15, 8))
    plt.bar([i - width for i in x], backtracking_values, width, label='Backtracking', color='skyblue')
    plt.bar(x, greedy_values, width, label='Greedy', color='salmon')
    plt.bar([i + width for i in x], ilp_values, width, label='ILP', color='lightgreen')

    plt.ylabel('Number of Sessions Scheduled')
    plt.title('Perbandingan Penggunaan Mata Kuliah')
    plt.xticks(x, all_matakuliah, rotation=90, fontsize=8)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    os.makedirs(report_dir, exist_ok=True) # Ensure the specific report directory exists
    plt.savefig(os.path.join(report_dir, filename))
    plt.close()

def compare_ruangan_usage(backtracking_schedule, greedy_schedule, ilp_schedule, report_dir, filename="ruangan_usage_comparison.png"):
    backtracking_room_usage = get_usage_counts(backtracking_schedule, "ruangan")
    greedy_room_usage = get_usage_counts(greedy_schedule, "ruangan")
    ilp_room_usage = get_usage_counts(ilp_schedule, "ruangan")

    all_ruangan = sorted(list(set(list(backtracking_room_usage.keys()) + list(greedy_room_usage.keys()) + list(ilp_room_usage.keys()))))

    backtracking_values = [backtracking_room_usage.get(room, 0) for room in all_ruangan]
    greedy_values = [greedy_room_usage.get(room, 0) for room in all_ruangan]
    ilp_values = [ilp_room_usage.get(room, 0) for room in all_ruangan]

    x = range(len(all_ruangan))
    width = 0.25

    plt.figure(figsize=(10, 6))
    plt.bar([i - width for i in x], backtracking_values, width, label='Backtracking', color='skyblue')
    plt.bar(x, greedy_values, width, label='Greedy', color='salmon')
    plt.bar([i + width for i in x], ilp_values, width, label='ILP', color='lightgreen')

    plt.ylabel('Number of Sessions Scheduled')
    plt.title('Perbandingan Penggunaan Ruangan')
    plt.xticks(x, all_ruangan, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    os.makedirs(report_dir, exist_ok=True) # Ensure the specific report directory exists
    plt.savefig(os.path.join(report_dir, filename))
    plt.close()

def compare_slot_waktu_usage(backtracking_schedule, greedy_schedule, ilp_schedule, report_dir, filename="slot_waktu_usage_comparison.png"):
    def get_slot_key(item):
        return f"{item['hari']} {item['jam_mulai']}"

    backtracking_slot_usage = get_usage_counts(backtracking_schedule, get_slot_key)
    greedy_slot_usage = get_usage_counts(greedy_schedule, get_slot_key)
    ilp_slot_usage = get_usage_counts(ilp_schedule, get_slot_key)

    all_slots = list(set(list(backtracking_slot_usage.keys()) + list(greedy_slot_usage.keys()) + list(ilp_slot_usage.keys())))

    def sort_key_for_slots(slot_str):
        parts = slot_str.split(' ')
        hari = parts[0]
        jam_mulai = parts[1]
        return (HARI_ORDER.get(hari, 99), time_to_minutes(jam_mulai))

    all_slots = sorted(all_slots, key=sort_key_for_slots)

    backtracking_values = [backtracking_slot_usage.get(slot, 0) for slot in all_slots]
    greedy_values = [greedy_slot_usage.get(slot, 0) for slot in all_slots]
    ilp_values = [ilp_slot_usage.get(slot, 0) for slot in all_slots]

    x = range(len(all_slots))
    width = 0.25

    plt.figure(figsize=(18, 7))
    plt.bar([i - width for i in x], backtracking_values, width, label='Backtracking', color='skyblue')
    plt.bar(x, greedy_values, width, label='Greedy', color='salmon')
    plt.bar([i + width for i in x], ilp_values, width, label='ILP', color='lightgreen')

    plt.ylabel('Number of Sessions Scheduled')
    plt.title('Perbandingan Penggunaan Slot Waktu')
    plt.xticks(x, all_slots, rotation=90, fontsize=7)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    os.makedirs(report_dir, exist_ok=True) # Ensure the specific report directory exists
    plt.savefig(os.path.join(report_dir, filename))
    plt.close()


def generate_html_schedule_content(schedule, algorithm_prefix, ordered_days=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]):
    """
    Menghasilkan konten HTML (tabel jadwal per hari) untuk dimasukkan ke dalam accordion.
    Menerima 'algorithm_prefix' untuk ID unik accordion.
    """
    html_content = ""
    if not schedule:
        html_content += "<p>Tidak ada jadwal yang berhasil dibuat.</p>"
    else:
        # Sort schedule by day and then by start time for consistent display
        sorted_schedule = sorted(schedule, key=lambda x: (HARI_ORDER.get(x["hari"], 99), time_to_minutes(x["jam_mulai"])))
        
        schedule_per_day = defaultdict(list)
        for entry in sorted_schedule:
            schedule_per_day[entry["hari"]].append(entry)

        for day in ordered_days:
            entries = schedule_per_day.get(day, [])
            if entries:
                # Accordion button
                html_content += f"""
                <button class="accordion">{day} ({len(entries)} Sesi)</button>
                <div class="panel">
                """
                
                # Table inside accordion panel
                html_content += "<table>\n"
                html_content += "    <thead>\n"
                html_content += "        <tr>\n"
                html_content += "            <th>Waktu</th>\n"
                html_content += "            <th>Ruangan</th>\n"
                html_content += "            <th>Mata Kuliah</th>\n"
                html_content += "            <th>Dosen</th>\n"
                html_content += "            <th>Sesi Ke</th>\n"
                html_content += "            <th>Jml. Mahasiswa</th>\n"
                html_content += "        </tr>\n"
                html_content += "    </thead>\n"
                html_content += "    <tbody>\n"
                for item in entries:
                    html_content += f"""
                    <tr>
                        <td>{item.get('jam_mulai', '')} - {item.get('jam_selesai', '')}</td>
                        <td>{item.get('ruangan', '')}</td>
                        <td>{item.get('matakuliah', '')}</td>
                        <td>{item.get('dosen', '')}</td>
                        <td>{item.get('sesi', '')}</td>
                        <td>{item.get('jumlah_mahasiswa', '')}</td>
                    </tr>
                    """
                html_content += "    </tbody>\n"
                html_content += "</table>\n"
                html_content += "</div>\n" # Close panel div

    return html_content

def generate_html_failed_sessions_content(failed_sessions):
    """
    Menghasilkan konten HTML untuk daftar sesi yang gagal dijadwalkan (konflik).
    Menerima list dictionaries dari failed_sessions.
    """
    html_content = ""
    if not failed_sessions:
        html_content += "<p>Tidak ada sesi yang gagal dijadwalkan (bebas konflik).</p>"
    else:
        html_content += "<table>\n"
        html_content += "    <thead>\n"
        html_content += "        <tr>\n"
        html_content += "            <th>Mata Kuliah</th>\n"
        html_content += "            <th>Dosen</th>\n"
        html_content += "            <th>Sesi Ke</th>\n"
        html_content += "            <th>Jumlah Mahasiswa</th>\n"
        html_content += "            <th>Alasan</th>\n"
        html_content += "        </tr>\n"
        html_content += "    </thead>\n"
        html_content += "    <tbody>\n"
        for item in failed_sessions:
            # Asumsi item di failed_sessions memiliki 'matakuliah', 'dosen', dan 'reason'
            # Anda mungkin perlu menyesuaikan key 'reason' jika struktur data Anda berbeda
            mk_name = item.get('matakuliah', 'N/A')
            dosen_name = item.get('dosen', 'N/A')
            sesi_ke = item.get('sesi', 'N/A')
            jumlah_mahasiswa = item.get('jumlah_mahasiswa', 'N/A')
            reason = item.get('reason', 'Tidak ada alasan spesifik disebutkan.')
            html_content += f"""
            <tr class="conflict-row">
                <td>{mk_name}</td>
                <td>{dosen_name}</td>
                <td>{sesi_ke}</td>
                <td>{jumlah_mahasiswa}</td>
                <td><span class="conflict-reason">{reason}</span></td>
            </tr>
            """
        html_content += "    </tbody>\n"
        html_content += "</table>\n"
    return html_content

# <hr/> FUNGSI UTAMA UNTUK GENERATE LAPORAN LENGKAP <hr/>
def generate_full_report_html(dataset, backtracking_result, greedy_result, ilp_result, output_filename="laporan_penjadwalan.html"):
    
    # Generate a unique directory name based on timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.join('report', timestamp)
    os.makedirs(report_dir, exist_ok=True) # Create the timestamped directory

    # 1. Persiapkan data mata kuliah agar menampilkan nama dosen
    matakuliah_data_for_table = []
    for mk in dataset['matakuliah']:
        mk_copy = mk.copy() # Buat salinan agar tidak memodifikasi dataset asli
        mk_copy['dosen_name'] = get_dosen_name(mk['dosen_id'], dataset['dosen'])
        matakuliah_data_for_table.append(mk_copy)

    # 2. Hitung jumlah mata kuliah yang diampu setiap dosen
    dosen_mk_counts = defaultdict(int)
    for mk in dataset['matakuliah']:
        dosen_mk_counts[mk['dosen_id']] += 1
    
    # 3. Gabungkan data dosen dengan jumlah mata kuliah
    dosen_data_for_table = []
    for dosen in dataset['dosen']:
        dosen_id = dosen['id']
        dosen_name = dosen['nama']
        mk_count = dosen_mk_counts[dosen_id]
        dosen_data_for_table.append({
            "id": dosen_id,
            "nama": dosen_name,
            "jumlah_matakuliah_diampu": mk_count
        })

    # 4. Ekstrak jadwal dan statistik
    backtracking_schedule = backtracking_result['schedule']
    greedy_schedule = greedy_result['schedule']
    ilp_schedule = ilp_result['schedule']

    backtracking_stats = backtracking_result['stats']
    greedy_stats = greedy_result['stats']
    ilp_stats = ilp_result['stats']

    # 5. Generate semua grafik visualisasi, passing report_dir
    perf_img = "performance_comparison.png"
    schedule_day_img = "schedule_comparison.png"
    mk_usage_img = "matakuliah_usage_comparison.png"
    room_usage_img = "ruangan_usage_comparison.png"
    slot_usage_img = "slot_waktu_usage_comparison.png"

    performance_comparison(
        backtracking_stats['execution_time'],
        greedy_stats['execution_time'],
        ilp_stats['execution_time'],
        report_dir, # Pass report_dir
        filename=perf_img
    )
    schedule_comparison(backtracking_schedule, greedy_schedule, ilp_schedule, report_dir, filename=schedule_day_img) # Pass report_dir
    compare_matakuliah_usage(backtracking_schedule, greedy_schedule, ilp_schedule, report_dir, filename=mk_usage_img) # Pass report_dir
    compare_ruangan_usage(backtracking_schedule, greedy_schedule, ilp_schedule, report_dir, filename=room_usage_img) # Pass report_dir
    compare_slot_waktu_usage(backtracking_schedule, greedy_schedule, ilp_schedule, report_dir, filename=slot_usage_img) # Pass report_dir

    # Fungsi bantu untuk membuat tabel HTML dari list dictionaries
    def create_html_table(data_list, headers_map):
        """
        data_list: list of dictionaries [{key: value}, ...]
        headers_map: dictionary mapping {Header Display Name: data_key_in_dict}
                     e.g., {"Mata Kuliah ID": "id"}
        """
        if not data_list:
            return "<p>Tidak ada data.</p>"
        
        table_html = "<table>\n<thead>\n<tr>"
        for header_display_name in headers_map.keys():
            table_html += f"<th>{header_display_name}</th>"
        table_html += "</tr>\n</thead>\n<tbody>\n"
        
        for item in data_list:
            table_html += "<tr>"
            for data_key in headers_map.values():
                table_html += f"<td>{item.get(data_key, '')}</td>"
            table_html += "</tr>\n"
        table_html += "</tbody>\n</table>"
        return table_html

    # Membuat tabel untuk setiap bagian dataset
    # Perbarui mk_headers untuk menggunakan 'dosen_name'
    mk_headers = {"ID": "id", "Nama": "nama", "SKS": "sks", "Dosen": "dosen_name", "Jumlah Mahasiswa": "jumlah_mahasiswa"}
    dosen_headers = {"ID": "id", "Nama": "nama", "Jumlah Mata Kuliah Diampu": "jumlah_matakuliah_diampu"}
    slot_headers = {"Hari": "hari", "Jam Mulai": "jam_mulai", "Jam Selesai": "jam_selesai"}
    ruangan_headers = {"ID": "id", "Nama": "nama", "Kapasitas": "kapasitas"}

    # Gunakan matakuliah_data_for_table yang sudah diperkaya dengan nama dosen
    mk_table_html = create_html_table(matakuliah_data_for_table, mk_headers)
    dosen_table_html = create_html_table(dosen_data_for_table, dosen_headers) # Gunakan data dosen yang sudah diperkaya
    slot_table_html = create_html_table(dataset['slot_waktu'], slot_headers)
    ruangan_table_html = create_html_table(dataset['ruangan'], ruangan_headers)

    # Dapatkan konten jadwal untuk setiap algoritma (sekarang menggunakan Accordion)
    backtracking_schedule_content = generate_html_schedule_content(backtracking_schedule, "backtracking")
    greedy_schedule_content = generate_html_schedule_content(greedy_schedule, "greedy")
    ilp_schedule_content = generate_html_schedule_content(ilp_schedule, "ilp")

    # Dapatkan konten failed sessions/konflik untuk setiap algoritma
    # Menggunakan 'failed_details' sebagai sumber data konflik
    backtracking_failed_content = generate_html_failed_sessions_content(backtracking_stats.get('failed_details', []))
    greedy_failed_content = generate_html_failed_sessions_content(greedy_stats.get('failed_details', []))
    ilp_failed_content = generate_html_failed_sessions_content(ilp_stats.get('failed_details', []))

    # 6. Bangun konten HTML final - Update image paths to include report_dir
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Laporan Lengkap Penjadwalan Kuliah</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #eef1f5; color: #333; }}
            .container {{ max-width: 1200px; margin: 30px auto; padding: 25px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h1, h2, h3 {{ color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-top: 40px; }}
            h1 {{ text-align: center; font-size: 2.5em; color: #003366; }}
            h2 {{ font-size: 1.8em; }}
            h3 {{ font-size: 1.4em; border-bottom: 1px solid #ccc; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; background-color: #fff; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }}
            th {{ background-color: #e2e6ea; color: #333; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f1f1f1; }}
            .image-container {{ text-align: center; margin: 30px 0; }}
            .image-container img {{ max-width: 90%; height: auto; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .highlight-error {{ color: red; font-weight: bold; }}

            /* <hr/> Styles for Tabs <hr/> */
            .tab-container {{ overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1; margin-bottom: 20px; border-radius: 8px; }}
            .tab-button {{ background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s; font-size: 17px; }}
            .tab-button:hover {{ background-color: #ddd; }}
            .tab-button.active {{ background-color: #ccc; }}
            .tab-content {{ display: none; padding: 20px; border-top: none; animation: fadeEffect 0.5s; }}
            @keyframes fadeEffect {{
                from {{opacity: 0;}}
                to {{opacity: 1;}}
            }}
            /* <hr/> End Styles for Tabs <hr/> */

            /* <hr/> Styles for Accordion <hr/> */
            .accordion {{
                background-color: #eee;
                color: #444;
                cursor: pointer;
                padding: 18px;
                width: 100%;
                border: none;
                text-align: left;
                outline: none;
                font-size: 15px;
                transition: 0.4s;
                border-bottom: 1px solid #ddd;
                font-weight: bold;
            }}
            .accordion.active, .accordion:hover {{
                background-color: #ccc;
            }}
            .accordion:last-of-type {{
                border-bottom: none;
            }}
            .panel {{
                padding: 0 18px;
                background-color: white;
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.2s ease-out;
            }}
            .panel table {{
                margin-top: 15px;
                margin-bottom: 15px;
            }}
            /* <hr/> End Styles for Accordion <hr/> */
            .conflict-row td {{
                background-color: #ffe0e0; /* Light red background for conflict rows */
            }}
            .conflict-item {{
                color: #c00;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Laporan Lengkap Penjadwalan Kuliah</h1>
            <p>Laporan ini menyajikan hasil penjadwalan kuliah menggunakan tiga algoritma berbeda: <strong>Backtracking</strong>, <strong>Greedy</strong>, dan <strong>Integer Linear Programming (ILP)</strong>. Tujuannya adalah membandingkan performa dan efektivitas masing-masing algoritma dalam menghasilkan jadwal yang optimal dan bebas konflik berdasarkan dataset yang diberikan.</p>

            <hr/>

            <h2>Dataset yang Digunakan</h2>
            <p>Berikut adalah detail komponen dataset yang digunakan untuk proses penjadwalan:</p>

            <h3>Data Mata Kuliah</h3>
            {mk_table_html}

            <h3>Data Dosen</h3>
            {dosen_table_html}

            <h3>Data Slot Waktu</h3>
            {slot_table_html}

            <h3>Data Ruangan</h3>
            {ruangan_table_html}

            <hr/>

            <h2>Ringkasan Hasil Penjadwalan</h2>
            <h3>Perbandingan Waktu Eksekusi</h3>
            <table>
                <thead>
                    <tr>
                        <th>Algoritma</th>
                        <th>Waktu Eksekusi (detik)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Backtracking</td><td>{backtracking_stats['execution_time']:.4f}</td></tr>
                    <tr><td>Greedy</td><td>{greedy_stats['execution_time']:.4f}</td></tr>
                    <tr><td>ILP</td><td>{ilp_stats['execution_time']:.4f}</td></tr>
                </tbody>
            </table>

            <h3>Perbandingan Statistik Penjadwalan</h3>
            <table>
                <thead>
                    <tr>
                        <th>Algoritma</th>
                        <th>Total Sesi Dicoba Dijadwalkan</th>
                        <th>Sesi Berhasil Dijadwalkan</th>
                        <th>Sesi Konflik (Gagal)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Backtracking</td>
                        <td>{backtracking_stats['total_slots_attempted']}</td>
                        <td>{backtracking_stats['scheduled_slots']}</td>
                        <td class="{'' if backtracking_stats['conflicts'] == 0 else 'highlight-error'}">{backtracking_stats['conflicts']}</td>
                    </tr>
                    <tr>
                        <td>Greedy</td>
                        <td>{greedy_stats['total_slots_attempted']}</td>
                        <td>{greedy_stats['scheduled_slots']}</td>
                        <td class="{'' if greedy_stats['conflicts'] == 0 else 'highlight-error'}">{greedy_stats['conflicts']}</td>
                    </tr>
                    <tr>
                        <td>ILP</td>
                        <td>{ilp_stats['total_slots_attempted']}</td>
                        <td class="{'' if ilp_stats['scheduled_slots'] <= ilp_stats['total_slots_attempted'] else 'highlight-error'}">{ilp_stats['scheduled_slots']}</td>
                        <td class="{'' if ilp_stats['conflicts'] == 0 else 'highlight-error'}">{ilp_stats['conflicts']}</td>
                    </tr>
                </tbody>
            </table>

            <hr/>

            <h2>Visualisasi Perbandingan</h2>
            <p>Berikut adalah visualisasi grafis dari perbandingan kinerja dan penggunaan sumber daya oleh ketiga algoritma.</p>

            <h3>Perbandingan Waktu Eksekusi Algoritma</h3>
            <div class="image-container">
                <img src="{perf_img}" alt="Perbandingan Waktu Eksekusi">
            </div>

            <h3>Perbandingan Jumlah Sesi Terjadwal per Hari</h3>
            <div class="image-container">
                <img src="{schedule_day_img}" alt="Perbandingan Sesi per Hari">
            </div>

            <h3>Perbandingan Penggunaan Mata Kuliah</h3>
            <div class="image-container">
                <img src="{mk_usage_img}" alt="Perbandingan Penggunaan Mata Kuliah">
            </div>

            <h3>Perbandingan Penggunaan Ruangan</h3>
            <div class="image-container">
                <img src="{room_usage_img}" alt="Perbandingan Penggunaan Ruangan">
            </div>

            <h3>Perbandingan Penggunaan Slot Waktu</h3>
            <div class="image-container">
                <img src="{slot_usage_img}" alt="Perbandingan Penggunaan Slot Waktu">
            </div>

            <hr/>

            <h2>Detail Jadwal yang Dihasilkan</h2>
            <div class="tab-container">
                <button class="tab-button active" onclick="openTab(event, 'backtracking-schedule-tab')">Backtracking</button>
                <button class="tab-button" onclick="openTab(event, 'greedy-schedule-tab')">Greedy</button>
                <button class="tab-button" onclick="openTab(event, 'ilp-schedule-tab')">ILP</button>
            </div>

            <div id="backtracking-schedule-tab" class="tab-content" style="display: block;">
                {backtracking_schedule_content}
            </div>

            <div id="greedy-schedule-tab" class="tab-content">
                {greedy_schedule_content}
            </div>

            <div id="ilp-schedule-tab" class="tab-content">
                {ilp_schedule_content}
            </div>

            <hr/>

            <h2>Sesi Gagal Dijadwalkan (Konflik)</h2>
            <div class="tab-container">
                <button class="tab-button active" onclick="openTab(event, 'backtracking-failed-tab')">Backtracking Gagal</button>
                <button class="tab-button" onclick="openTab(event, 'greedy-failed-tab')">Greedy Gagal</button>
                <button class="tab-button" onclick="openTab(event, 'ilp-failed-tab')">ILP Gagal</button>
            </div>

            <div id="backtracking-failed-tab" class="tab-content" style="display: block;">
                {backtracking_failed_content}
            </div>

            <div id="greedy-failed-tab" class="tab-content">
                {greedy_failed_content}
            </div>

            <div id="ilp-failed-tab" class="tab-content">
                {ilp_failed_content}
            </div>
        </div>

        <script>
            // JavaScript for Tabs
            function openTab(evt, tabName) {{
                var i, tabcontent, tabbuttons;
                
                // Determine if we are opening a schedule tab or a failed tab
                var isScheduleTab = tabName.includes('-schedule-tab');

                // Hide all tab contents
                tabcontent = document.getElementsByClassName("tab-content");
                for (i = 0; i < tabcontent.length; i++) {{
                    tabcontent[i].style.display = "none";
                }}

                // Deactivate all tab buttons
                tabbuttons = document.getElementsByClassName("tab-button");
                for (i = 0; i < tabbuttons.length; i++) {{
                    tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
                }}

                // Show the specific tab content and activate its button
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";

                // If opening a schedule tab, ensure its first accordion is open
                if (isScheduleTab) {{
                    var firstAccordion = document.getElementById(tabName).querySelector('.accordion');
                    if (firstAccordion && !firstAccordion.classList.contains('active')) {{
                        firstAccordion.click(); // Programmatically click to open
                    }}
                }}
            }}

            // JavaScript for Accordion
            document.addEventListener('DOMContentLoaded', (event) => {{
                // Initialize the first schedule tab
                var firstScheduleTabButton = document.querySelector('.tab-container:nth-of-type(1) .tab-button');
                if (firstScheduleTabButton) {{
                    firstScheduleTabButton.click();
                }}
                
                // Initialize the first failed sessions tab
                var firstFailedTabButton = document.querySelector('.tab-container:nth-of-type(2) .tab-button');
                if (firstFailedTabButton) {{
                    firstFailedTabButton.click();
                }}


                var accordions = document.getElementsByClassName("accordion");
                for (let i = 0; i < accordions.length; i++) {{
                    accordions[i].addEventListener("click", function() {{
                        this.classList.toggle("active");
                        var panel = this.nextElementSibling;
                        if (panel.style.maxHeight) {{
                            panel.style.maxHeight = null;
                        }} else {{
                            panel.style.maxHeight = panel.scrollHeight + "px";
                        }} 
                    }});
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # Simpan file HTML inside the timestamped directory
    full_path = os.path.join(report_dir, output_filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\nLaporan lengkap berhasil dibuat: {full_path}")