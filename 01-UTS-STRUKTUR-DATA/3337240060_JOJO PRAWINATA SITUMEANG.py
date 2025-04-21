import pandas as pd

# Ambil data dari Google Sheets
url = "https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/export?format=csv&gid=743838712"
df = pd.read_csv(url)

# Normalisasi kolom jadi string dan rapi
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# Hilangkan ".0" dari Tahun Terbit kalau ada
df['Tahun Terbit'] = df['Tahun Terbit'].str.replace(r'\.0$', '', regex=True)

# ===============================
# Fungsi-fungsi Pencarian
# ===============================
def linear_search(data, column, keyword):
    return data[data[column].str.contains(keyword, case=False, na=False)]

def binary_search(data, column, keyword):
    data_sorted = data.sort_values(by=column, key=lambda x: x.str.lower()).reset_index(drop=True)
    keyword = keyword.lower()
    low, high = 0, len(data_sorted) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = data_sorted.loc[mid, column].lower()

        if mid_val == keyword:
            return data_sorted.iloc[[mid]]
        elif keyword < mid_val:
            high = mid - 1
        else:
            low = mid + 1

    return pd.DataFrame()

# ===============================
# Fungsi Tampilkan Data
# ===============================
def tampilkan(data):
    if data.empty:
        print("⛔ Data tidak ditemukan.")
    else:
        for _, row in data.iterrows():
            print(f"\n📘 Judul Paper : {row['Judul Paper']}")
            print(f"📅 Tahun Terbit: {row['Tahun Terbit']}")
            print(f"🖋️  Penulis     : {row['Nama Penulis']}")
            print(f"🆔 NIM         : {row['NIM']}")
            print(f"🎓 Nama Mahasiswa : {row['Nama Mahasiswa']}")
            print(f"📝 Abstrak     : {row['Abstrak (langusung copas dari paper)']}")
            print(f"✅ Kesimpulan  : {row['Kesimpulan (Langusung copas dari paper)']}")
            print("-" * 60)

# ===============================
# Program Utama
# ===============================
def menu():
    print("\n=== MENU PENCARIAN DATA PAPER ===")
    print("1. Judul Paper")
    print("2. Nama Penulis")
    print("3. Tahun Terbit")
    pilihan = input("Pilih berdasarkan (1-3): ")

    kolom_dict = {
        '1': "Judul Paper",
        '2': "Nama Penulis",
        '3': "Tahun Terbit"
    }

    if pilihan in kolom_dict:
        kolom = kolom_dict[pilihan]
        keyword = input(f"Masukkan kata kunci untuk '{kolom}': ").strip()
        return kolom, keyword
    else:
        print("Pilihan tidak valid.")
        return None, None

def main():
    while True:
        kolom, keyword = menu()
        if kolom is None:
            continue

        print("\n🔍 Hasil Linear Search:")
        tampilkan(linear_search(df, kolom, keyword))

        print("\n🔍 Hasil Binary Search:")
        tampilkan(binary_search(df, kolom, keyword))

        lanjut = input("\nIngin mencari lagi? (y/n): ").lower()
        if lanjut != 'y':
            print("Terima kasih! 👋")
            break

# Jalankan program
main()
