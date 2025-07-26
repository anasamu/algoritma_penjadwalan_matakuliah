import json
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import random
import datetime

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
    """Helper untuk menghitung penggunaan item berdasarkan nama kunci atau fungsi."""
    usage_counts = defaultdict(int)
    for item in schedule:
        if callable(key_name_or_func):
            key = key_name_or_func(item)
        else:
            key = item[key_name_or_func]
        usage_counts[key] += 1
    return dict(usage_counts)

# Global Order for Days
HARI_ORDER = {"Senin": 1, "Selasa": 2, "Rabu": 3, "Kamis": 4, "Jumat": 5, "Sabtu": 6, "Minggu": 7}

# Konflik Checker
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


# Visualization Functions
def performance_comparison(algorithm_results, report_dir, filename="performance_comparison.png"):
    """
    Membuat grafik perbandingan waktu eksekusi untuk berbagai algoritma.
    Menerima dictionary hasil algoritma: {'Nama Algoritma': {'schedule': [...], 'stats': {'execution_time': ...}}}
    """
    algorithms = [name for name in algorithm_results.keys()]
    times = [result['stats']['execution_time'] for result in algorithm_results.values()]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(algorithms, times, color=['skyblue', 'salmon', 'lightgreen', 'gold'][:len(algorithms)])
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

def schedule_comparison(algorithm_results, report_dir, filename="schedule_comparison.png"):
    """
    Membuat grafik perbandingan jumlah sesi terjadwal per hari untuk berbagai algoritma.
    Menerima dictionary hasil algoritma.
    """
    ordered_days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    
    all_counts = {}
    for algo_name, result in algorithm_results.items():
        schedule = result['schedule']
        all_counts[algo_name] = [sum(1 for item in schedule if item["hari"] == day) for day in ordered_days]

    x = range(len(ordered_days))
    width = 0.8 / len(algorithm_results) # Dynamically adjust bar width
    
    plt.figure(figsize=(15, 7))
    
    # Define a set of colors for dynamic plotting
    colors = ['skyblue', 'salmon', 'lightgreen', 'gold', 'plum', 'darkseagreen', 'lightcoral', 'cornflowerblue']
    
    for i, (algo_name, counts) in enumerate(all_counts.items()):
        plt.bar([pos + i * width - (len(algorithm_results) - 1) * width / 2 for pos in x], counts, width, label=algo_name, color=colors[i % len(colors)])

    plt.ylabel('Number of Scheduled Sessions')
    plt.title('Perbandingan Jumlah Sesi Terjadwal per Hari')
    plt.xticks(x, ordered_days)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    os.makedirs(report_dir, exist_ok=True) # Ensure the specific report directory exists
    plt.savefig(os.path.join(report_dir, filename))
    plt.close()

def compare_usage(algorithm_results, key_name_or_func, title, ylabel, report_dir, filename):
    """
    Membuat grafik perbandingan penggunaan (mata kuliah, ruangan, slot waktu) untuk berbagai algoritma.
    Menerima dictionary hasil algoritma, kunci untuk penggunaan, judul grafik, label Y, direktori laporan, dan nama file.
    """
    all_usage_counts = {}
    all_items = set()

    for algo_name, result in algorithm_results.items():
        schedule = result['schedule']
        usage = get_usage_counts(schedule, key_name_or_func)
        all_usage_counts[algo_name] = usage
        all_items.update(usage.keys())

    # Custom sorting for time slots
    if title == 'Perbandingan Penggunaan Slot Waktu':
        def sort_key_for_slots(slot_str):
            parts = slot_str.split(' ')
            hari = parts[0]
            jam_mulai = parts[1]
            return (HARI_ORDER.get(hari, 99), time_to_minutes(jam_mulai))
        sorted_items = sorted(list(all_items), key=sort_key_for_slots)
    else:
        sorted_items = sorted(list(all_items))

    x = range(len(sorted_items))
    width = 0.8 / len(algorithm_results) # Dynamically adjust bar width

    plt.figure(figsize=(max(12, len(sorted_items) * 0.8), 7)) # Adjust figure size based on number of items
    
    colors = ['skyblue', 'salmon', 'lightgreen', 'gold', 'plum', 'darkseagreen', 'lightcoral', 'cornflowerblue']

    for i, (algo_name, usage_data) in enumerate(all_usage_counts.items()):
        values = [usage_data.get(item, 0) for item in sorted_items]
        plt.bar([pos + i * width - (len(algorithm_results) - 1) * width / 2 for pos in x], values, width, label=algo_name, color=colors[i % len(colors)])

    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(x, sorted_items, rotation=90, fontsize=8)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    os.makedirs(report_dir, exist_ok=True)
    plt.savefig(os.path.join(report_dir, filename))
    plt.close()

# HTML Content Generation Helpers
def create_html_table(data_list, headers_map):
    """
    Menghasilkan tabel HTML dari list dictionaries dengan kelas Bootstrap.
    data_list: list of dictionaries [{key: value}, ...]
    headers_map: dictionary mapping {Header Display Name: data_key_in_dict}
                 e.g., {"Mata Kuliah ID": "id"}
    """
    if not data_list:
        return "<p>Tidak ada data.</p>"
    
    table_html = "<table class='table table-bordered table-striped table-hover'>\n<thead>\n<tr>"
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

def generate_html_schedule_content(schedule, ordered_days=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]):
    """
    Menghasilkan konten HTML (tabel jadwal per hari) untuk dimasukkan ke dalam accordion Bootstrap.
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

        # Use a unique ID for each algorithm's accordion parent
        # This will be passed from generate_full_report_html
        accordion_parent_id = "accordionPlaceholder" # This will be replaced by algo-specific ID

        html_content += f'<div class="accordion" id="{accordion_parent_id}">\n'
        for idx, day in enumerate(ordered_days):
            entries = schedule_per_day.get(day, [])
            if entries:
                # Generate unique IDs for each accordion item
                heading_id = f"heading{day.lower()}{idx}"
                collapse_id = f"collapse{day.lower()}{idx}"

                html_content += f"""
                <div class="accordion-item">
                    <h2 class="accordion-header" id="{heading_id}">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#{collapse_id}" aria-expanded="false" aria-controls="{collapse_id}">
                            {day} ({len(entries)} Sesi)
                        </button>
                    </h2>
                    <div id="{collapse_id}" class="accordion-collapse collapse" aria-labelledby="{heading_id}" data-bs-parent="#{accordion_parent_id}">
                        <div class="accordion-body">
                            <table class="table table-bordered table-striped table-hover">
                                <thead>
                                    <tr>
                                        <th>Waktu</th>
                                        <th>Ruangan</th>
                                        <th>Mata Kuliah</th>
                                        <th>Dosen</th>
                                        <th>Sesi Ke</th>
                                        <th>Jml. Mahasiswa</th>
                                    </tr>
                                </thead>
                                <tbody>
                """
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
                html_content += """
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                """
        html_content += '</div>\n' # Close accordion div

    return html_content

def generate_html_failed_sessions_content(failed_sessions):
    """
    Menghasilkan konten HTML untuk daftar sesi yang gagal dijadwalkan (konflik) dengan kelas Bootstrap.
    """
    html_content = ""
    if not failed_sessions:
        html_content += "<p>Tidak ada sesi yang gagal dijadwalkan (bebas konflik).</p>"
    else:
        html_content += "<table class='table table-bordered table-striped table-hover'>\n"
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

# MAIN FUNCTION TO GENERATE FULL REPORT
def generate_full_report_html(dataset, algorithm_results, output_filename="laporan_penjadwalan.html", template_path="./data/report_template.html"):
    """
    Menghasilkan laporan HTML lengkap yang membandingkan hasil dari berbagai algoritma penjadwalan.
    dataset: dictionary berisi data mentah (matakuliah, dosen, slot_waktu, ruangan).
    algorithm_results: dictionary berisi hasil dari setiap algoritma.
                       Contoh: {'Backtracking': {'schedule': [...], 'stats': {...}}, ...}
    output_filename: Nama file HTML yang akan dihasilkan.
    template_path: Path ke file template HTML.
    """
    
    # Generate a unique directory name based on timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.join('report', timestamp)
    os.makedirs(report_dir, exist_ok=True) # Create the timestamped directory

    # 1. Prepare matakuliah data to display dosen names
    matakuliah_data_for_table = []
    for mk in dataset['matakuliah']:
        mk_copy = mk.copy() # Create a copy to avoid modifying original dataset
        mk_copy['dosen_name'] = get_dosen_name(mk['dosen_id'], dataset['dosen'])
        matakuliah_data_for_table.append(mk_copy)

    # 2. Count number of courses taught by each dosen
    dosen_mk_counts = defaultdict(int)
    for mk in dataset['matakuliah']:
        dosen_mk_counts[mk['dosen_id']] += 1
    
    # 3. Combine dosen data with course counts
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

    # 4. Generate all visualization graphs, passing report_dir
    perf_img = "performance_comparison.png"
    schedule_day_img = "schedule_comparison.png"
    mk_usage_img = "matakuliah_usage_comparison.png"
    room_usage_img = "ruangan_usage_comparison.png"
    slot_usage_img = "slot_waktu_usage_comparison.png"

    # Pass the entire algorithm_results dictionary to the visualization functions
    performance_comparison(algorithm_results, report_dir, filename=perf_img)
    schedule_comparison(algorithm_results, report_dir, filename=schedule_day_img)
    compare_usage(algorithm_results, "matakuliah", 'Perbandingan Penggunaan Mata Kuliah', 'Number of Sessions Scheduled', report_dir, filename=mk_usage_img)
    compare_usage(algorithm_results, "ruangan", 'Perbandingan Penggunaan Ruangan', 'Number of Sessions Scheduled', report_dir, filename=room_usage_img)
    
    def get_slot_key(item):
        return f"{item['hari']} {item['jam_mulai']}"
    compare_usage(algorithm_results, get_slot_key, 'Perbandingan Penggunaan Slot Waktu', 'Number of Sessions Scheduled', report_dir, filename=slot_usage_img)

    # Define headers for dataset tables
    mk_headers = {"ID": "id", "Nama": "nama", "SKS": "sks", "Dosen": "dosen_name", "Jumlah Mahasiswa": "jumlah_mahasiswa"}
    dosen_headers = {"ID": "id", "Nama": "nama", "Jumlah Mata Kuliah Diampu": "jumlah_matakuliah_diampu"}
    slot_headers = {"Hari": "hari", "Jam Mulai": "jam_mulai", "Jam Selesai": "jam_selesai"}
    ruangan_headers = {"ID": "id", "Nama": "nama", "Kapasitas": "kapasitas"}

    # Generate HTML tables for dataset
    mk_table_html = create_html_table(matakuliah_data_for_table, mk_headers)
    dosen_table_html = create_html_table(dosen_data_for_table, dosen_headers)
    slot_table_html = create_html_table(dataset['slot_waktu'], slot_headers)
    ruangan_table_html = create_html_table(dataset['ruangan'], ruangan_headers)

    # Generate dynamic schedule and failed sessions tabs
    schedule_tabs_html = ""
    failed_tabs_html = ""
    schedule_tab_buttons_html = ""
    failed_tab_buttons_html = ""

    # Generate algorithm stats rows
    algorithm_stats_rows = ""
    for name, result in algorithm_results.items():
        algorithm_stats_rows += f"""
        <tr>
            <td>{name}</td>
            <td>{result['stats']['total_slots_attempted']}</td>
            <td>{result['stats']['scheduled_slots']}</td>
            <td class="{'' if result['stats']['conflicts'] == 0 else 'highlight-error'}">{result['stats']['conflicts']}</td>
            <td>{result['stats']['execution_time']:.4f}</td>
        </tr>
        """

    # Flags to determine which tab button should be active initially
    is_first_schedule_algo = True
    is_first_failed_algo = True

    for algo_name, result in algorithm_results.items():
        # Sanitize algo_name for HTML ID
        algo_id = algo_name.lower().replace(" ", "-")

        # Schedule Tab Content (using Bootstrap classes)
        # Add 'show active' classes directly for the first tab to ensure it's visible on load
        schedule_tabs_html += f"""
            <div class="tab-pane fade {'show active' if is_first_schedule_algo else ''}" id="{algo_id}-schedule-tab" role="tabpanel" aria-labelledby="{algo_id}-schedule-tab-button">
                {generate_html_schedule_content(result['schedule']).replace('accordionPlaceholder', f'accordion-{algo_id}')}
            </div>
        """
        # Schedule Tab Button (using Bootstrap classes and data attributes)
        schedule_tab_buttons_html += f"""
            <li class="nav-item" role="presentation">
                <button class="nav-link {'active' if is_first_schedule_algo else ''}" id="{algo_id}-schedule-tab-button" data-bs-toggle="tab" data-bs-target="#{algo_id}-schedule-tab" type="button" role="tab" aria-controls="{algo_id}-schedule-tab" aria-selected="{'true' if is_first_schedule_algo else 'false'}">{algo_name}</button>
            </li>
        """
        is_first_schedule_algo = False # Ensure only the first schedule tab button gets 'active'

        # Failed Sessions Tab Content (using Bootstrap classes)
        # Do NOT add 'show active' to failed sessions tabs by default
        failed_tabs_html += f"""
            <div class="tab-pane fade" id="{algo_id}-failed-tab" role="tabpanel" aria-labelledby="{algo_id}-failed-tab-button">
                {generate_html_failed_sessions_content(result['stats'].get('failed_details', []))}
            </div>
        """
        # Failed Sessions Tab Button (using Bootstrap classes and data attributes)
        failed_tab_buttons_html += f"""
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="{algo_id}-failed-tab-button" data-bs-toggle="tab" data-bs-target="#{algo_id}-failed-tab" type="button" role="tab" aria-controls="{algo_id}-failed-tab" aria-selected="false">{algo_name} Gagal</button>
            </li>
        """
        # is_first_failed_algo is not used here, as we don't want any failed tab active by default

    # Read the HTML template file
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        return

    # Replace placeholders in the template
    html_content = html_template.replace("{{MK_TABLE_HTML}}", mk_table_html)
    html_content = html_content.replace("{{DOSEN_TABLE_HTML}}", dosen_table_html)
    html_content = html_content.replace("{{SLOT_TABLE_HTML}}", slot_table_html)
    html_content = html_content.replace("{{RUANGAN_TABLE_HTML}}", ruangan_table_html)
    html_content = html_content.replace("{{SCHEDULE_TAB_BUTTONS}}", schedule_tab_buttons_html)
    html_content = html_content.replace("{{SCHEDULE_TAB_CONTENTS}}", schedule_tabs_html)
    html_content = html_content.replace("{{FAILED_TAB_BUTTONS}}", failed_tab_buttons_html)
    html_content = html_content.replace("{{FAILED_TAB_CONTENTS}}", failed_tabs_html)
    html_content = html_content.replace("{{ALGORITHM_STATS_ROWS}}", algorithm_stats_rows)
    html_content = html_content.replace("{{PERF_IMG}}", perf_img)
    html_content = html_content.replace("{{SCHEDULE_DAY_IMG}}", schedule_day_img)
    html_content = html_content.replace("{{MK_USAGE_IMG}}", mk_usage_img)
    html_content = html_content.replace("{{ROOM_USAGE_IMG}}", room_usage_img)
    html_content = html_content.replace("{{SLOT_USAGE_IMG}}", slot_usage_img)
    
    # Save the HTML file inside the timestamped directory
    full_path = os.path.join(report_dir, output_filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\nLaporan lengkap berhasil dibuat: {full_path}")

