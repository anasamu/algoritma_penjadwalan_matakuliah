import utils
import time

class DPScheduler:
    def __init__(self, data):
        self.matakuliah = data["matakuliah"]
        self.dosen = data["dosen"]
        self.slot_waktu = data["slot_waktu"]
        self.ruangan = data["ruangan"]
        self.jadwal = []
        self.failed_sessions = [] # This will hold original failed session objects
        self.total_attempted_sessions_count = 0
        self.urutan_hari = {"Senin": 1, "Selasa": 2, "Rabu": 3, "Kamis": 4, "Jumat": 5, "Sabtu": 6}

        self.all_time_slots = self._get_all_discrete_time_slots()
        self.resource_to_idx = {}
        self.idx_to_resource = {}
        self._setup_resource_indices()

    def _get_all_discrete_time_slots(self):
        """
        Mengambil semua slot waktu diskrit (per 15 menit) dari data slot_waktu.
        """
        discrete_slots = set()
        for slot in self.slot_waktu:
            hari = slot["hari"]
            start_minutes = utils.time_to_minutes(slot["jam_mulai"])
            end_minutes = utils.time_to_minutes(slot["jam_selesai"])
            # Iterasi per 15 menit untuk pelacakan sumber daya
            for t in range(start_minutes, end_minutes, 15):
                discrete_slots.add((hari, t))
        return sorted(list(discrete_slots), key=lambda x: (self.urutan_hari.get(x[0], 99), x[1]))

    def _setup_resource_indices(self):
        """
        Memetakan setiap kombinasi unik (hari, interval 15 menit, id_sumber_daya, jenis_sumber_daya)
        ke indeks integer unik. Ini penting untuk representasi state DP.
        """
        current_idx = 0
        for hari, jam_menit in self.all_time_slots:
            for ruang in self.ruangan:
                key = (hari, jam_menit, ruang["id"], "ruangan")
                self.resource_to_idx[key] = current_idx
                self.idx_to_resource[current_idx] = key
                current_idx += 1
            for dosen in self.dosen:
                key = (hari, jam_menit, dosen["id"], "dosen")
                self.resource_to_idx[key] = current_idx
                self.idx_to_resource[current_idx] = key
                current_idx += 1

    def generate_sessions(self):
        """
        Menghasilkan daftar semua sesi individual yang diperlukan berdasarkan data matakuliah.
        Setiap matakuliah mungkin dibagi menjadi beberapa sesi berdasarkan jumlah mahasiswa dan kapasitas ruangan.
        """
        sessions = []
        session_counter = 0 # Unique counter for all sessions
        for mk in self.matakuliah:
            durasi = utils.sks_to_minutes(mk["sks"])
            total_mahasiswa_mk = mk["jumlah_mahasiswa"]
            
            # Menentukan kapasitas ruangan maksimum yang masuk akal untuk menghitung sesi yang dibutuhkan
            # Default to 1 if no rooms to avoid division by zero, but ensure it's at least 1 for calculation
            max_room_capacity = max([r["kapasitas"] for r in self.ruangan]) if self.ruangan else 1 
            
            # Menghitung jumlah sesi yang dibutuhkan berdasarkan total mahasiswa dan kapasitas ruangan maksimum
            # Jika 0 mahasiswa, maka 0 sesi dibutuhkan.
            if total_mahasiswa_mk > 0:
                jumlah_sesi = (total_mahasiswa_mk + max_room_capacity - 1) // max_room_capacity
            else:
                jumlah_sesi = 0 # No students, no sessions needed
            
            # Menghitung mahasiswa per sesi
            if jumlah_sesi > 0:
                peserta_per_sesi = (total_mahasiswa_mk + jumlah_sesi - 1) // jumlah_sesi
            else:
                peserta_per_sesi = 0 # If no sessions, then 0 students per session

            for i in range(jumlah_sesi):
                session_counter += 1
                sessions.append({
                    "session_id": f"{mk['id']}-{i+1}", # Unique ID for each session
                    "matakuliah": mk["nama"],
                    "dosen_id": mk["dosen_id"],
                    "jumlah_mahasiswa": peserta_per_sesi,
                    "durasi": durasi,
                    "sesi": i + 1, # Nomor sesi untuk matakuliah spesifik ini
                    "original_matakuliah_id": mk["id"] # Melacak id matakuliah asli
                })
        return sessions

    def get_all_slots(self):
        """
        Menghasilkan daftar semua kemungkinan slot waktu mulai untuk sesi,
        mempertimbangkan slot_waktu yang ditentukan dan interval 15 menit.
        """
        slots = []
        for slot in self.slot_waktu:
            start = utils.time_to_minutes(slot["jam_mulai"])
            end = utils.time_to_minutes(slot["jam_selesai"])
            # Menghasilkan semua kemungkinan interval mulai 15 menit dalam slot_waktu
            for s in range(start, end, 15):
                slots.append({"hari": slot["hari"], "start": s, "end": end})
        # Urutkan untuk pemrosesan yang konsisten, penting untuk DP jika urutan berpengaruh pada transisi state
        return sorted(slots, key=lambda x: (self.urutan_hari.get(x["hari"], 99), x["start"]))

    def solve(self):
        """
        Menyelesaikan masalah penjadwalan menggunakan pendekatan pemrograman dinamis.
        Bertujuan untuk memaksimalkan jumlah sesi yang dijadwalkan sambil menghormati
        ketersediaan sumber daya (ruangan dan dosen).
        """
        start_time = time.time()
        sessions = self.generate_sessions()
        self.total_attempted_sessions_count = len(sessions)
        possible_start_slots = self.get_all_slots()

        # dp_table[i] akan menyimpan dictionary di mana kunci adalah frozenset dari indeks sumber daya yang ditempati
        # dan nilai adalah jadwal (daftar detail sesi) yang mengarah ke state tersebut.
        # dp_table[i][state] = schedule_list
        # Tujuannya adalah menemukan jadwal terpanjang untuk state tertentu.
        dp_table = [{} for _ in range(len(sessions) + 1)]
        dp_table[0][frozenset()] = [] # Kasus dasar: 0 sesi terjadwal, state kosong, jadwal kosong

        # Iterasi melalui setiap sesi yang akan dijadwalkan
        for i in range(len(sessions)):
            sesi = sessions[i] # Sesi saat ini yang sedang dicoba dijadwalkan
            durasi = sesi["durasi"]
            next_dp = {} # Menyimpan state untuk (i+1) sesi

            # Iterasi melalui semua state yang ada dari langkah sebelumnya (i sesi terjadwal)
            for state, schedule_so_far in dp_table[i].items():
                # Coba tempatkan 'sesi' saat ini ke slot yang tersedia
                for slot in possible_start_slots:
                    mulai = slot["start"]
                    selesai = mulai + durasi
                    
                    # Periksa apakah durasi sesi sesuai dalam slot waktu yang dipilih
                    if selesai > slot["end"]:
                        continue

                    for ruang in self.ruangan:
                        # Periksa apakah kapasitas ruangan cukup untuk mahasiswa sesi
                        if ruang["kapasitas"] < sesi["jumlah_mahasiswa"]:
                            continue
                        
                        # Kumpulkan semua indeks sumber daya yang akan ditempati oleh penempatan potensial ini
                        indices_to_occupy = set()
                        conflict_found = False
                        
                        # Periksa setiap interval 15 menit dalam durasi sesi
                        for t in range(mulai, selesai, 15):
                            # Kunci untuk sumber daya ruangan dan dosen pada interval waktu spesifik ini
                            r_key = (slot["hari"], t, ruang["id"], "ruangan")
                            d_key = (slot["hari"], t, sesi["dosen_id"], "dosen")
                            
                            # Dapatkan indeks yang sesuai
                            r_idx = self.resource_to_idx.get(r_key)
                            d_idx = self.resource_to_idx.get(d_key)
                            
                            # Jika indeks sumber daya tidak ditemukan (seharusnya tidak terjadi jika setup benar)
                            # atau jika sumber daya sudah ditempati dalam 'state' saat ini
                            if r_idx is None or d_idx is None or r_idx in state or d_idx in state:
                                conflict_found = True
                                break # Konflik ditemukan, penempatan ini tidak valid
                            
                            indices_to_occupy.add(r_idx)
                            indices_to_occupy.add(d_idx)
                        
                        if conflict_found:
                            continue # Coba ruangan atau slot berikutnya
                        
                        # Jika tidak ada konflik, buat state baru dengan menambahkan indeks yang ditempati
                        new_state = frozenset(state.union(indices_to_occupy))
                        
                        # Siapkan entri jadwal terperinci untuk sesi ini
                        detail = {
                            "session_id": sesi["session_id"], # Include the unique session ID
                            "matakuliah": sesi["matakuliah"],
                            "dosen": utils.get_dosen_name(sesi["dosen_id"], self.dosen),
                            "dosen_id": sesi["dosen_id"],
                            "ruangan": ruang["nama"],
                            "ruangan_id": ruang["id"],
                            "hari": slot["hari"],
                            "jam_mulai": utils.minutes_to_time(mulai),
                            "jam_selesai": utils.minutes_to_time(selesai),
                            "jumlah_mahasiswa": sesi["jumlah_mahasiswa"],
                            "sesi": sesi["sesi"],
                            "original_matakuliah_id": sesi["original_matakuliah_id"]
                        }
                        
                        # Perbarui next_dp: pertahankan jadwal yang menghasilkan urutan terpanjang
                        # untuk new_state tertentu. Ini memastikan kita memaksimalkan sesi yang dijadwalkan.
                        if new_state not in next_dp or len(schedule_so_far) + 1 > len(next_dp[new_state]):
                            next_dp[new_state] = schedule_so_far + [detail]
            
            dp_table[i + 1] = next_dp # Pindah ke langkah berikutnya dalam DP

        # Temukan state di entri tabel DP terakhir yang memiliki jadwal terpanjang
        # Ini mewakili jumlah maksimum sesi yang dapat dijadwalkan.
        final_state_entry = max(dp_table[-1].items(), key=lambda x: len(x[1]), default=(None, []))
        self.jadwal = final_state_entry[1] # Sesi yang berhasil dijadwalkan

        # Identifikasi sesi yang tidak dijadwalkan menggunakan session_id
        scheduled_session_ids = {item["session_id"] for item in self.jadwal}
        self.failed_sessions = [s for s in sessions if s["session_id"] not in scheduled_session_ids]

        # Urutkan jadwal akhir untuk pelaporan yang konsisten
        sorted_schedule = sorted(self.jadwal, key=lambda x: (
            self.urutan_hari.get(x["hari"], 99), utils.time_to_minutes(x["jam_mulai"]), x["matakuliah"]))

        # Hitung dan kembalikan statistik
        stats = self.calculate_stats()
        stats["execution_time"] = time.time() - start_time

        return {"schedule": sorted_schedule, "stats": stats}

    def calculate_stats(self):
        """
        Menghitung statistik untuk proses penjadwalan, termasuk
        alasan terperinci untuk sesi yang tidak dapat dijadwalkan.
        """
        detailed_failed_sessions = []
        
        # Verifikasi apakah jadwal yang dihasilkan memiliki konflik internal (seharusnya tidak ada untuk DP yang benar)
        internal_conflicts = utils.check_conflicts(self.jadwal)
        if internal_conflicts:
            # Ini menunjukkan kesalahan logika dalam DP jika konflik ditemukan di sini
            print("PERINGATAN: Konflik internal ditemukan dalam jadwal DP:", internal_conflicts)
            # Untuk saat ini, kita mengasumsikan DP menghasilkan jadwal bebas konflik secara internal,
            # jadi konflik ini tidak ditambahkan ke 'failed_details' yang ditujukan untuk item yang tidak terjadwal.

        # Untuk sesi yang tidak dijadwalkan, coba tentukan alasannya
        for failed_sesi in self.failed_sessions:
            # Default reason
            reason = "Tidak dapat dijadwalkan: Tidak ada slot waktu atau ruangan yang tersedia yang memenuhi semua kriteria."
            
            potential_reasons = set()
            found_theoretically_possible_slot = False

            # Iterasi melalui semua kemungkinan slot waktu dan ruangan untuk menemukan alasan kegagalan
            for slot_waktu_option in self.slot_waktu:
                mulai_opt = utils.time_to_minutes(slot_waktu_option["jam_mulai"])
                selesai_opt = utils.time_to_minutes(slot_waktu_option["jam_selesai"])
                durasi = failed_sesi["durasi"]

                # Periksa apakah durasi sesi sesuai dalam slot waktu yang dipilih
                if mulai_opt + durasi > selesai_opt:
                    continue 

                for ruang_option in self.ruangan:
                    # Periksa apakah kapasitas ruangan cukup
                    if ruang_option["kapasitas"] < failed_sesi["jumlah_mahasiswa"]:
                        potential_reasons.add(f"Ruangan '{ruang_option['nama']}' terlalu kecil ({ruang_option['kapasitas']} < {failed_sesi['jumlah_mahasiswa']} mahasiswa).")
                        continue 

                    # Simulasikan menambahkan sesi yang gagal ini ke jadwal *yang berhasil* saat ini
                    # dan periksa konflik menggunakan pemeriksa konflik umum.
                    temp_schedule_item = {
                        "hari": slot_waktu_option["hari"],
                        "jam_mulai": utils.minutes_to_time(mulai_opt),
                        "jam_selesai": utils.minutes_to_time(mulai_opt + durasi),
                        "ruangan": ruang_option["nama"],
                        "dosen": utils.get_dosen_name(failed_sesi["dosen_id"], self.dosen),
                        "matakuliah": failed_sesi["matakuliah"]
                    }
                    
                    # Tambahkan sementara ke jadwal *yang berhasil* untuk memeriksa konflik
                    temp_full_schedule = self.jadwal + [temp_schedule_item]
                    temp_conflicts = utils.check_conflicts(temp_full_schedule)

                    if not temp_conflicts:
                        # Jika tidak ada konflik yang ditemukan saat mencoba menempatkan sesi ini dengan jadwal *yang ada*,
                        # itu berarti sesi ini *bisa* ditempatkan jika DP memilihnya.
                        # Alasan sebenarnya adalah karena optimasi global DP (misalnya, sesi lain diprioritaskan).
                        reason = "Tidak dapat dijadwalkan: Tidak optimal secara global dengan sesi lain yang lebih prioritas."
                        found_theoretically_possible_slot = True
                        potential_reasons.clear() # Hapus alasan konflik spesifik jika slot yang valid ditemukan
                        break # Berhenti mencari slot untuk sesi yang gagal ini
                    else:
                        # Konflik ditemukan, tentukan alasan spesifiknya
                        for conflict_msg in temp_conflicts:
                            if f"[KONFLIK RUANGAN] {ruang_option['nama']}" in conflict_msg:
                                potential_reasons.add(f"Ruangan '{ruang_option['nama']}' bentrok pada {slot_waktu_option['hari']} {utils.minutes_to_time(mulai_opt)}-{utils.minutes_to_time(mulai_opt + durasi)}.")
                            if f"[KONFLIK DOSEN] {utils.get_dosen_name(failed_sesi['dosen_id'], self.dosen)}" in conflict_msg:
                                potential_reasons.add(f"Dosen '{utils.get_dosen_name(failed_sesi['dosen_id'], self.dosen)}' bentrok pada {slot_waktu_option['hari']} {utils.minutes_to_time(mulai_opt)}-{utils.minutes_to_time(mulai_opt + durasi)}.")
                
                if found_theoretically_possible_slot:
                    break # Berhenti mencari slot untuk sesi yang gagal ini

            if potential_reasons:
                reason = "Tidak dapat dijadwalkan: " + "; ".join(sorted(list(potential_reasons)))
            elif not found_theoretically_possible_slot:
                reason = "Tidak dapat dijadwalkan: Tidak ada slot waktu atau ruangan yang tersedia yang memenuhi semua kriteria."
            
            failed_sesi_copy = failed_sesi.copy()
            failed_sesi_copy["reason"] = reason
            detailed_failed_sessions.append(failed_sesi_copy)

        return {
            "total_slots_attempted": self.total_attempted_sessions_count,
            "scheduled_slots": len(self.jadwal),
            "conflicts": len(detailed_failed_sessions), # Jumlah sesi yang tidak terjadwal dengan alasan
            "failed_details": detailed_failed_sessions
        }
