# algoritma/ilp.py

import utils
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus
import time # Import time for execution tracking

class ILPScheduler:
    def __init__(self, data):
        self.matakuliah = data["matakuliah"]
        self.dosen = data["dosen"]
        self.slot_waktu = data["slot_waktu"]
        self.ruangan = data["ruangan"]

        # Helper dictionaries for quick lookups
        self.mk_dict = {mk["id"]: mk for mk in self.matakuliah}
        self.dosen_dict = {d["id"]: d for d in self.dosen}
        self.ruangan_dict = {r["id"]: r for r in self.ruangan}

        self.urutan_hari = {"Senin": 1, "Selasa": 2, "Rabu": 3, "Kamis": 4, "Jumat": 5, "Sabtu": 6, "Minggu": 7}

        # Pre-process all possible 15-minute time intervals for sessions
        self.all_possible_time_slots = self._generate_possible_time_slots()
        
        # Initialize lists to store results
        self.jadwal = []
        self.failed_sessions = []
        self.total_attempted_sessions_count = 0 # Will be calculated during variable creation

    def _generate_possible_time_slots(self):
        """Generates all valid 15-minute start times within provided slots."""
        possible_slots = []
        for slot in self.slot_waktu:
            hari_name = slot["hari"]
            start_minutes_slot = utils.time_to_minutes(slot["jam_mulai"])
            end_minutes_slot = utils.time_to_minutes(slot["jam_selesai"])

            # Iterate every 15 minutes as a potential start time
            for start_time_candidate in range(start_minutes_slot, end_minutes_slot, 15):
                possible_slots.append({
                    "hari": hari_name,
                    "jam_mulai_menit": start_time_candidate,
                    "jam_selesai_slot_menit": end_minutes_slot # Store original slot end for duration check
                })
        return possible_slots

    def solve(self):
        start_time = time.time()
        
        prob = LpProblem("Penjadwalan_Kuliah", LpMaximize)

        self.x_keys = []
        for mk_id in self.mk_dict:
            mk = self.mk_dict[mk_id]
            dosen_mk_id = mk["dosen_id"]

            durasi_mk = utils.sks_to_minutes(mk["sks"])
            total_peserta_mk = mk["jumlah_mahasiswa"]
            
            # Use max capacity from self.ruangan, defaulting to 1 if no rooms to avoid error
            kapasitas_max_ruangan = max(r["kapasitas"] for r in self.ruangan) if self.ruangan else 1
            
            # Calculate total sessions needed for this course. Ensure no division by zero.
            jumlah_sesi_mk = (total_peserta_mk + kapasitas_max_ruangan - 1) // kapasitas_max_ruangan if total_peserta_mk > 0 else 0
            
            # Accumulate total attempted sessions count
            self.total_attempted_sessions_count += jumlah_sesi_mk

            # Skip if no sessions are needed or if duration is 0 (prevents invalid variable creation)
            if jumlah_sesi_mk == 0 or durasi_mk == 0:
                continue

            # Calculate peserta_per_sesi for consistent reporting
            peserta_per_sesi_mk = (total_peserta_mk + jumlah_sesi_mk - 1) // jumlah_sesi_mk if jumlah_sesi_mk > 0 else total_peserta_mk

            for r_id in self.ruangan_dict:
                ruang = self.ruangan_dict[r_id]
                
                # Only consider rooms with adequate capacity
                if ruang["kapasitas"] < peserta_per_sesi_mk:
                    continue

                for hari_data in self.all_possible_time_slots:
                    hari = hari_data["hari"]
                    start_min = hari_data["jam_mulai_menit"]
                    jam_selesai_slot_menit = hari_data["jam_selesai_slot_menit"]
                    
                    # Ensure the session fits within the available slot duration
                    if start_min + durasi_mk > jam_selesai_slot_menit:
                        continue
                    
                    self.x_keys.append((mk_id, dosen_mk_id, r_id, hari, start_min))

        # 2. Define Decision Variables using the filtered keys
        # Only create variables for keys that were valid and added to self.x_keys
        self.x = LpVariable.dicts("x", self.x_keys, 0, 1, 'Binary')
        
        # 3. Define the Objective Function: Maximize the number of scheduled sessions
        prob += lpSum(self.x[key] for key in self.x_keys), "Total Sesi Terjadwal"

        # 4. Add Constraints
        
        # Constraint 1 & 2: Room Capacity & Lecturer for Course
        # Handled by filtering self.x_keys initially (only valid combinations are considered).
        
        # Constraint 3: No Room Conflicts
        # A room can only be used by one session at the same 15-minute interval
        for r_id in self.ruangan_dict:
            for hari_data in self.all_possible_time_slots: # Iterate through each 15-min interval
                current_hari = hari_data["hari"]
                current_start_min = hari_data["jam_mulai_menit"]
                
                # Collect all variables that represent a session potentially overlapping with this 15-min slot
                overlapping_sessions = []
                for key in self.x_keys:
                    mk_id, _, assigned_r_id, hari, session_start_min = key
                    
                    if assigned_r_id == r_id and hari == current_hari: # Same room and day
                        durasi_session = utils.sks_to_minutes(self.mk_dict[mk_id]["sks"])
                        session_end_min = session_start_min + durasi_session
                        
                        # Check if session_start_min and session_end_min overlap with (current_start_min, current_start_min + 15)
                        if not (current_start_min + 15 <= session_start_min or current_start_min >= session_end_min):
                            overlapping_sessions.append(self.x[key])
                
                # If there are any potential overlaps, ensure only one is chosen
                if overlapping_sessions:
                    prob += lpSum(overlapping_sessions) <= 1, \
                            f"KonflikRuangan_{r_id}_{current_hari}_{current_start_min}"

        # Constraint 4: No Lecturer Conflicts
        # A lecturer can only teach one session at the same 15-minute interval
        for d_id in self.dosen_dict:
            for hari_data in self.all_possible_time_slots: # Iterate through each 15-min interval
                current_hari = hari_data["hari"]
                current_start_min = hari_data["jam_mulai_menit"]

                overlapping_sessions_dosen = []
                for key in self.x_keys:
                    mk_id, assigned_d_id, _, hari, session_start_min = key
                    
                    if assigned_d_id == d_id and hari == current_hari: # Same lecturer and day
                        durasi_session = utils.sks_to_minutes(self.mk_dict[mk_id]["sks"])
                        session_end_min = session_start_min + durasi_session
                        
                        # Check if session_start_min and session_end_min overlap with (current_start_min, current_start_min + 15)
                        if not (current_start_min + 15 <= session_start_min or current_start_min >= session_end_min):
                            overlapping_sessions_dosen.append(self.x[key])
                
                # If there are any potential overlaps, ensure only one is chosen
                if overlapping_sessions_dosen:
                    prob += lpSum(overlapping_sessions_dosen) <= 1, \
                            f"KonflikDosen_{d_id}_{current_hari}_{current_start_min}"
        
        # Constraint 5: Each Course Session Must Be Scheduled Exactly The Required Number of Times
        # This is a critical hard constraint. If this cannot be met, the problem is infeasible.
        for mk_id in self.mk_dict:
            mk = self.mk_dict[mk_id]
            dosen_id = mk["dosen_id"]
            total_peserta = mk["jumlah_mahasiswa"]
            
            kapasitas_max_ruangan = max(r["kapasitas"] for r in self.ruangan) if self.ruangan else 1
            jumlah_sesi_mk = (total_peserta + kapasitas_max_ruangan - 1) // kapasitas_max_ruangan if total_peserta > 0 else 0
            
            # Filter x_keys for the current matakuliah and its assigned dosen only
            relevant_x_vars = [self.x[key] for key in self.x_keys if key[0] == mk_id and key[1] == dosen_id]

            # If no sessions are required for this course OR no valid keys were generated for it,
            # ensure no sessions are scheduled for it.
            if jumlah_sesi_mk == 0:
                if relevant_x_vars: # Only add if there are any variables to constrain
                    prob += lpSum(relevant_x_vars) == 0, f"Mk_{mk_id}_NoSesiNeeded_PreventScheduling"
                continue
            
            # If relevant_x_vars is empty here, it means no valid assignments (room/time) could be found for this MK.
            # This would make the problem infeasible if jumlah_sesi_mk > 0.
            if not relevant_x_vars and jumlah_sesi_mk > 0:
                 pass # No constraint to add if no variables exist for this MK

            # This ensures that exactly `jumlah_sesi_mk` sessions are scheduled for this course.
            prob += lpSum(relevant_x_vars) == jumlah_sesi_mk, \
                    f"Jumlah_Sesi_Mk_{mk_id}_Tepat_Target"

        # 5. Solve the Problem
        prob.solve()

        end_time = time.time()

        # 6. Interpret Results
        final_status = LpStatus[prob.status]
        
        if final_status == "Optimal" or final_status == "Feasible":
            print(f"ILP Solver Status: {final_status}. Solution found.")
            
            # Reconstruct scheduled sessions
            scheduled_count_per_mk = {mk_id: 0 for mk_id in self.mk_dict}

            for key in self.x_keys:
                if self.x[key].varValue == 1:
                    mk_id, dosen_id, r_id, hari, start_min = key
                    mk = self.mk_dict[mk_id]
                    
                    durasi = utils.sks_to_minutes(mk["sks"])
                    jam_selesai_sesi = start_min + durasi

                    total_peserta = mk["jumlah_mahasiswa"]
                    kapasitas_max_ruangan = max(r["kapasitas"] for r in self.ruangan) if self.ruangan else 1
                    jumlah_sesi_mk_calc = (total_peserta + kapasitas_max_ruangan - 1) // kapasitas_max_ruangan if total_peserta > 0 else 0
                    peserta_per_sesi = (total_peserta + jumlah_sesi_mk_calc - 1) // jumlah_sesi_mk_calc if jumlah_sesi_mk_calc > 0 else total_peserta

                    scheduled_count_per_mk[mk_id] += 1
                    self.jadwal.append({
                        "matakuliah": mk["nama"],
                        "dosen": utils.get_dosen_name(dosen_id, self.dosen),
                        "ruangan": self.ruangan_dict[r_id]["nama"],
                        "hari": hari,
                        "jam_mulai": utils.minutes_to_time(start_min),
                        "jam_selesai": utils.minutes_to_time(jam_selesai_sesi),
                        "jumlah_mahasiswa": peserta_per_sesi,
                        "sesi": scheduled_count_per_mk[mk_id] # Assign dynamic session number
                    })
            
            # If Optimal/Feasible, all required sessions (based on Constraint 5) were scheduled.
            # So, self.failed_sessions remains empty in this case.
            
        else: # Solver Status is Not Solved, Infeasible, Unbounded, etc.
            print(f"ILP Solver Status: {final_status}. No optimal or feasible solution found.")
            # If no feasible solution, all initially attempted sessions are considered failed.
            reason_for_failure = f"Sistem Penjadwalan ILP tidak dapat menemukan solusi yang memenuhi semua kendala ({final_status}). Mungkin karena batasan yang terlalu ketat atau data input yang tidak memungkinkan."
            
            for mk_id in self.mk_dict:
                mk = self.mk_dict[mk_id]
                dosen_id = mk["dosen_id"]
                total_peserta = mk["jumlah_mahasiswa"]
                kapasitas_max_ruangan = max(r["kapasitas"] for r in self.ruangan) if self.ruangan else 1
                jumlah_sesi_mk = (total_peserta + kapasitas_max_ruangan - 1) // kapasitas_max_ruangan if total_peserta > 0 else 0
                peserta_per_sesi = (total_peserta + jumlah_sesi_mk - 1) // jumlah_sesi_mk if jumlah_sesi_mk > 0 else 0
                
                # Add only sessions that were "expected" but couldn't be scheduled by the solver
                if jumlah_sesi_mk > 0: # Only add if the course actually needed sessions
                    for sesi_ke_num in range(1, jumlah_sesi_mk + 1):
                        self.failed_sessions.append({
                            "matakuliah": mk["nama"],
                            "dosen": utils.get_dosen_name(dosen_id, self.dosen),
                            "jumlah_mahasiswa": peserta_per_sesi,
                            "sesi": sesi_ke_num,
                            "reason": reason_for_failure # Assign the overarching reason for ILP failure
                        })
        
        # Sort the final schedule for consistent output
        sorted_final_schedule = sorted(self.jadwal, key=lambda x: (self.urutan_hari.get(x["hari"], 99), utils.time_to_minutes(x["jam_mulai"]), x["matakuliah"]))
        
        # Calculate statistics
        stats_data = self.calculate_stats()
        stats_data['execution_time'] = end_time - start_time

        # *** THIS IS THE CRITICAL FIX ***
        # Return a dictionary containing both 'schedule' and 'stats' as top-level keys
        return {
            'schedule': sorted_final_schedule,
            'stats': stats_data
        }

    def calculate_stats(self):
        conflicts = len(self.failed_sessions)
        return {
            "total_slots_attempted": self.total_attempted_sessions_count,
            "scheduled_slots": len(self.jadwal),
            "conflicts": conflicts,
            "failed_details": self.failed_sessions
        }