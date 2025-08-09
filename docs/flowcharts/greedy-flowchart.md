# Greedy Algorithm Flowchart

## Greedy Scheduling Process

```
┌─────────────────┐
│ GREEDY START    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Sort Mata Kuliah│
│ by Priority:    │
│ - Student Count │
│ - SKS           │
│ - Semester      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Initialize:     │
│ - used_rooms{}  │
│ - used_dosen{}  │
│ - jadwal[]      │
│ - failed[]      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ mata_kuliah     │
│ in sorted_list  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Calculate       │
│ Required Sessions│
│ based on SKS    │
│ - 2 SKS = 1 sesi│
│ - 3 SKS = 1 sesi│
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ required_session│
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ time_slot       │
│ (hari + jam)    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ ruangan         │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Capacity  │
│ Constraint:     │
│ students ≤      │
│ room_capacity   │
└─────────┬───────┘
          │
      ┌───v───┐
      │ OK?   │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Try Next  │
    │ Room      │
    └─────┬─────┘
          │
          │ Yes
          v
┌─────────────────┐
│ Calculate       │
│ Time Window:    │
│ start = slot    │
│ end = start +   │
│       duration  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check if Time   │
│ Fits in Slot    │
└─────────┬───────┘
          │
      ┌───v───┐
      │ Fits? │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Try Next  │
    │ Time Slot │
    └─────┬─────┘
          │
          │ Yes
          v
┌─────────────────┐
│ Check Conflicts:│
│ - Room Conflict │
│ - Dosen Conflict│
└─────────┬───────┘
          │
      ┌───v───┐
      │Conflict?│
      └───┬───┘
          │ Yes
    ┌─────v─────┐
    │ Try Next  │
    │ Option    │
    └─────┬─────┘
          │
          │ No
          v
┌─────────────────┐
│ ASSIGN SESSION: │
│ - Add to jadwal │
│ - Mark room used│
│ - Mark dosen    │
│   used          │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Move to Next    │
│ Session         │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ All sessions    │
│ for this course │
│ processed?      │
└─────────┬───────┘
          │ No
          │ (back to session loop)
          │
          │ Yes
          v
┌─────────────────┐
│ All courses     │
│ processed?      │
└─────────┬───────┘
          │ No
          │ (back to course loop)
          │
          │ Yes
          v
┌─────────────────┐
│ Calculate Final │
│ Statistics:     │
│ - Success rate  │
│ - Conflicts     │
│ - Usage stats   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Return Results: │
│ {schedule,      │
│  stats}         │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ GREEDY END      │
└─────────────────┘
```

## Conflict Detection Process

```
┌─────────────────┐
│ is_conflict()   │
│ Parameters:     │
│ - hari          │
│ - jam_mulai     │
│ - jam_selesai   │
│ - ruangan_id    │
│ - dosen_id      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Room      │
│ Conflicts:      │
│ used_rooms      │
│ [hari][room]    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ existing time   │
│ interval        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Time      │
│ Overlap:        │
│ NOT (end1 ≤     │
│ start2 OR       │
│ start1 ≥ end2)  │
└─────────┬───────┘
          │
      ┌───v───┐
      │Overlap?│
      └───┬───┘
          │ Yes
    ┌─────v─────┐
    │ Return    │
    │"Konflik   │
    │ Ruangan"  │
    └───────────┘
          │ No
          v
┌─────────────────┐
│ Check Dosen     │
│ Conflicts:      │
│ used_dosen      │
│ [hari][dosen]   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ existing time   │
│ interval        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Time      │
│ Overlap         │
└─────────┬───────┘
          │
      ┌───v───┐
      │Overlap?│
      └───┬───┘
          │ Yes
    ┌─────v─────┐
    │ Return    │
    │"Konflik   │
    │ Dosen"    │
    └───────────┘
          │ No
          v
┌─────────────────┐
│ Return None     │
│ (No Conflict)   │
└─────────────────┘
```

## Greedy Strategy Characteristics

### Time Complexity: O(n²)
- **n** = number of courses
- **For each course**: Try all time slots and rooms
- **Worst case**: All assignments fail

### Space Complexity: O(n)
- **used_rooms**: Store occupied time intervals per room
- **used_dosen**: Store occupied time intervals per lecturer
- **jadwal**: Store successful assignments

### Decision Strategy: First-Fit
1. **Sort courses** by priority (student count DESC)
2. **For each course**: Find first available slot
3. **No backtracking** - decisions are final
4. **Greedy choice**: Locally optimal assignment

### Pros:
- ⚡ **Very fast execution**
- 💾 **Low memory usage**
- 📈 **Predictable performance**
- 🔧 **Simple to implement**

### Cons:
- 🎯 **Not optimal** - can get stuck in local optima
- 🔒 **No backtracking** - can't undo bad decisions
- 📊 **Quality depends** on input order and priorities
- ⚠️ **May fail** on tightly constrained problems

---

[← Main System Flow](main-system-flow.md) | [→ Backtracking Flowchart](backtracking-flowchart.md)