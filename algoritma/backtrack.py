# algoritma/dynamic_programing.py (Backtracking-like Scheduler)

import utils
import time # Import time for execution tracking

class BacktrackingScheduler:
    def __init__(self, data):
        self.matakuliah = data["matakuliah"]
        self.dosen = data["dosen"]
        self.slot_waktu = data["slot_waktu"]
        self.ruangan = data["ruangan"]
        self.jadwal = []

        self.used_rooms = {} # Tracks occupied room slots: {hari: {ruangan_id: [(mulai_menit, selesai_menit)]}}
        self.used_dosen = {} # Tracks occupied lecturer slots: {hari: {dosen_id: [(mulai_menit, selesai_menit)]}}
        self.failed_sessions = [] # Stores details of sessions that could not be scheduled
        self.total_attempted_sessions_count = 0 # To be calculated in solve()

    def calculate_stats(self):
        # This method aggregates statistics from the scheduler's state
        conflicts = len(self.failed_sessions)
        return {
            "total_slots_attempted": self.total_attempted_sessions_count,
            "scheduled_slots": len(self.jadwal),
            "conflicts": conflicts,
            "failed_details": self.failed_sessions
        }

    def is_conflict(self, hari, jam_mulai_menit, jam_selesai_sesi_menit, ruangan_id, dosen_id):
        # We need to return the specific reason for conflict
        # Check for room conflicts
        if hari in self.used_rooms and ruangan_id in self.used_rooms[hari]:
            for mulai, selesai in self.used_rooms[hari][ruangan_id]:
                if not (jam_selesai_sesi_menit <= mulai or jam_mulai_menit >= selesai):
                    return "Konflik Ruangan"

        # Check for lecturer conflicts
        if hari in self.used_dosen and dosen_id in self.used_dosen[hari]:
            for mulai, selesai in self.used_dosen[hari][dosen_id]:
                if not (jam_selesai_sesi_menit <= mulai or jam_mulai_menit >= selesai):
                    return "Konflik Dosen"

        return None # No conflict

    def mark_used(self, hari, jam_mulai_menit, jam_selesai_sesi_menit, ruangan_id, dosen_id):
        self.used_rooms.setdefault(hari, {}).setdefault(ruangan_id, []).append((jam_mulai_menit, jam_selesai_sesi_menit))
        self.used_dosen.setdefault(hari, {}).setdefault(dosen_id, []).append((jam_mulai_menit, jam_selesai_sesi_menit))

    def solve(self):
        start_time = time.time()
        
        urutan_hari = {"Senin": 1, "Selasa": 2, "Rabu": 3, "Kamis": 4, "Jumat": 5, "Sabtu": 6, "Minggu": 7}

        # Calculate total attempted sessions upfront
        self.total_attempted_sessions_count = 0
        for mk in self.matakuliah:
            kapasitas_max = max(r["kapasitas"] for r in self.ruangan) if self.ruangan else 1
            jumlah_sesi_mk = (mk["jumlah_mahasiswa"] + kapasitas_max - 1) // kapasitas_max
            self.total_attempted_sessions_count += jumlah_sesi_mk

        # Pre-process all possible granular time slots
        all_time_slots = []
        for slot in self.slot_waktu:
            hari_name = slot["hari"]
            start_minutes_slot = utils.time_to_minutes(slot["jam_mulai"])
            end_minutes_slot = utils.time_to_minutes(slot["jam_selesai"])
            # Iterate every 15 minutes as a potential start time
            for start_interval in range(start_minutes_slot, end_minutes_slot, 15):
                all_time_slots.append({
                    "hari": hari_name,
                    "jam_mulai_menit": start_interval,
                    "jam_selesai_slot_menit": end_minutes_slot # End boundary of the original slot
                })
        
        # Sort these granular slots by day, then by start time
        sorted_all_time_slots = sorted(
            all_time_slots,
            key=lambda x: (urutan_hari.get(x["hari"], 99), x["jam_mulai_menit"])
        )

        # Sort courses: SKS ascending, then number of students ascending (Greedy heuristic)
        sorted_matakuliah = sorted(self.matakuliah, key=lambda x: (x["sks"], x["jumlah_mahasiswa"]))

        for mk in sorted_matakuliah:
            durasi_menit = utils.sks_to_minutes(mk["sks"])
            total_peserta = mk["jumlah_mahasiswa"]
            
            kapasitas_max_ruangan = max(r["kapasitas"] for r in self.ruangan) if self.ruangan else 1
            jumlah_sesi_needed = (total_peserta + kapasitas_max_ruangan - 1) // kapasitas_max_ruangan if total_peserta > 0 else 0
            
            peserta_per_sesi = (total_peserta + jumlah_sesi_needed - 1) // jumlah_sesi_needed if jumlah_sesi_needed > 0 else total_peserta

            for sesi_ke in range(1, jumlah_sesi_needed + 1):
                assigned_this_session = False
                current_session_failed_reason = "Tidak ada slot/ruangan yang cocok ditemukan." # Default reason

                # Sort rooms by capacity (smallest first, might help fit more courses)
                sorted_ruangan = sorted(self.ruangan, key=lambda r: r["kapasitas"])

                for slot_info in sorted_all_time_slots:
                    current_hari = slot_info["hari"]
                    current_jam_mulai_menit = slot_info["jam_mulai_menit"]
                    current_slot_end_menit = slot_info["jam_selesai_slot_menit"]

                    jam_selesai_sesi_menit = current_jam_mulai_menit + durasi_menit

                    # Check if the course duration fits within the remaining time of the current slot interval
                    if jam_selesai_sesi_menit > current_slot_end_menit:
                        current_session_failed_reason = "Durasi mata kuliah melebihi slot waktu yang tersedia."
                        continue 

                    for ruang in sorted_ruangan:
                        # Check if room capacity is sufficient
                        if ruang["kapasitas"] < peserta_per_sesi:
                            current_session_failed_reason = f"Kapasitas ruangan '{ruang['nama']}' ({ruang['kapasitas']}) tidak cukup untuk {peserta_per_sesi} mahasiswa."
                            continue # Try next room

                        # Check for conflicts
                        conflict_type = self.is_conflict(
                            current_hari,
                            current_jam_mulai_menit,
                            jam_selesai_sesi_menit,
                            ruang["id"],
                            mk["dosen_id"]
                        )
                        
                        if conflict_type is None: # No conflict
                            # Schedule the session
                            self.mark_used(current_hari, current_jam_mulai_menit, jam_selesai_sesi_menit, ruang["id"], mk["dosen_id"])
                            self.jadwal.append({
                                "matakuliah": mk["nama"],
                                "dosen": utils.get_dosen_name(mk["dosen_id"], self.dosen),
                                "ruangan": ruang["nama"],
                                "hari": current_hari,
                                "jam_mulai": utils.minutes_to_time(current_jam_mulai_menit),
                                "jam_selesai": utils.minutes_to_time(jam_selesai_sesi_menit),
                                "jumlah_mahasiswa": peserta_per_sesi,
                                "sesi": sesi_ke
                            })
                            assigned_this_session = True
                            break # Session assigned, move to the next session for this course
                        else:
                            # Conflict detected, update specific reason
                            current_session_failed_reason = f"{conflict_type} pada {current_hari} {utils.minutes_to_time(current_jam_mulai_menit)}-{utils.minutes_to_time(jam_selesai_sesi_menit)} di {ruang['nama']} atau dengan dosen {utils.get_dosen_name(mk['dosen_id'], self.dosen)}."
                    
                    if assigned_this_session:
                        break # Session assigned, move to the next session for this course

                if not assigned_this_session:
                    # If after checking all slots and rooms, the session still isn't assigned
                    self.failed_sessions.append({
                        "matakuliah": mk["nama"],
                        "dosen": utils.get_dosen_name(mk["dosen_id"], self.dosen),
                        "sesi": sesi_ke,
                        "jumlah_mahasiswa": peserta_per_sesi,
                        "reason": current_session_failed_reason # The most recent failure reason
                    })
        
        end_time = time.time()

        # Sort the final schedule for consistent reporting
        sorted_final_schedule = sorted(
            self.jadwal,
            key=lambda x: (urutan_hari.get(x["hari"], 99), utils.time_to_minutes(x["jam_mulai"]), x["matakuliah"])
        )
        
        # Calculate statistics and add execution time
        stats_data = self.calculate_stats()
        stats_data['execution_time'] = end_time - start_time

        # Return a dictionary containing both 'schedule' and 'stats'
        return {
            'schedule': sorted_final_schedule,
            'stats': stats_data
        }