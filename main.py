import os

saldo = 0

def clear_screen():
    os.system('clear')

def tambah_pemasukan():
    global saldo
    try:
        jumlah = float(input("Masukkan jumlah pemasukan (Rp): "))
        if jumlah > 0:
            saldo += jumlah
            print(f"Pemasukan Rp {jumlah} berhasil ditambahkan!")
        else:
            print("Jumlah harus positif.")
    except ValueError:
        print("Input harus berupa angka.")

def tambah_pengeluaran():
    global saldo
    try:
        jumlah = float(input("Masukkan jumlah pengeluaran (Rp): "))
        if jumlah > 0:
            if saldo >= jumlah:
                saldo -= jumlah
                print(f"Pengeluaran Rp {jumlah} berhasil dilakukan!")
            else:
                print("Saldo tidak cukup.")
        else:
            print("Jumlah harus positif.")
    except ValueError:
        print("Input harus berupa angka.")

def lihat_saldo():
    print(f"Saldo saat ini: Rp {saldo}")

def menu():
    clear_screen()
    print("=== Aplikasi Pengelola Uang Saku ===")
    print("1. Tambah Pemasukan")
    print("2. Tambah Pengeluaran")
    print("3. Lihat Saldo")
    print("4. Keluar")
    print("-" * 40)

while True:
    menu()
    pilihan = input("Pilih menu (1-4): ").strip()

    if pilihan == "1":
        tambah_pemasukan()
        input("Tekan Enter untuk kembali ke menu...")
    elif pilihan == "2":
        tambah_pengeluaran()
        input("Tekan Enter untuk kembali ke menu...")
    elif pilihan == "3":
        lihat_saldo()
        input("Tekan Enter untuk kembali ke menu...")
    elif pilihan == "4":
        print("Terima kasih telah menggunakan aplikasi!")
        break
    else:
        print("Pilihan tidak valid. Silakan pilih 1-4.")
        input("Tekan Enter untuk kembali ke menu...")
