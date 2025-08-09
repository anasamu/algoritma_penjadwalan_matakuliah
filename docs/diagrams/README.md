# Diagrams

Koleksi diagram arsitektur dan struktur sistem penjadwalan mata kuliah.

## Daftar Diagrams

### 🏗️ [System Architecture Diagram](system-architecture.md)
Diagram arsitektur lengkap sistem menunjukkan:
- **High-Level Architecture**: Layer presentation, application, service, dan data
- **Component Interaction**: Interaksi antar komponen utama
- **Technology Stack**: Stack teknologi yang digunakan
- **Module Dependencies**: Dependensi antar modul
- **Design Patterns**: Implementasi design patterns
- **Scalability Architecture**: Pertimbangan skalabilitas

## Jenis Diagram

### 1. Architectural Diagrams
- **Layered Architecture**: Pemisahan concern dalam layer
- **Component Diagram**: Komponen dan interface
- **Deployment Diagram**: Struktur deployment

### 2. Interaction Diagrams
- **Component Interaction**: Komunikasi antar komponen
- **Data Flow**: Aliran data dalam sistem
- **Process Flow**: Aliran proses bisnis

### 3. Technical Diagrams
- **Technology Stack**: Teknologi yang digunakan
- **Module Dependencies**: Struktur dependensi
- **Design Patterns**: Implementasi pola desain

## Cara Membaca Diagrams

### Konvensi Visual

```
╔══════════════════╗     Layer/Boundary
║     LAYER        ║
╚══════════════════╝

┌──────────────────┐     Component/Module
│    Component     │
└──────────────────┘

─────────────────▶      Data Flow/Dependency

┌────┐    ┌────┐         Interaction
│ A  │◄──▶│ B  │
└────┘    └────┘
```

### Hierarki Informasi

1. **High-Level Views**: Overview arsitektur
2. **Component Level**: Detail komponen
3. **Implementation**: Detail implementasi
4. **Dependencies**: Relasi dan dependensi

## Tujuan Diagrams

### 📋 **Documentation**
- Memahami struktur sistem
- Onboarding developer baru
- Referensi maintenance

### 🔧 **Development**
- Panduan implementasi
- Identifikasi dependencies
- Planning refactoring

### 📊 **Analysis**
- Performance bottlenecks
- Scalability planning
- Security considerations

## Navigation

- [← Kembali ke Documentation](../README.md)
- [→ Lihat Flowcharts](../flowcharts/)

---

**Note**: Semua diagram menggunakan format text ASCII untuk:
- **Portability**: Dapat dibuka di editor apapun
- **Version Control**: Git-friendly, mudah tracking changes
- **Accessibility**: Tidak memerlukan software khusus
- **Maintainability**: Mudah diupdate oleh developer