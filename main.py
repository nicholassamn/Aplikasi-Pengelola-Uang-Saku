import os
import json
from datetime import datetime

DATA_FILE = 'data.json'

saldo = 0.0
history = []  # each item: {'type': 'Pemasukan'|'Pengeluaran', 'amount': float, 'description': str, 'time': iso_str}


def clear_screen():
    # Cross-platform clear
    os.system('cls' if os.name == 'nt' else 'clear')


def load_data():
    global saldo, history
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            saldo = float(data.get('saldo', 0.0))
            history = data.get('history', [])
    except FileNotFoundError:
        saldo = 0.0
        history = []
    except (ValueError, json.JSONDecodeError):
        saldo = 0.0
        history = []


def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({'saldo': saldo, 'history': history}, f, ensure_ascii=False, indent=2)


def format_rp(amount):
    # Simple currency formatter
    try:
        if float(amount).is_integer():
            return f"Rp {int(amount):,}".replace(',', '.')
        return f"Rp {amount:,.2f}".replace(',', '.')
    except Exception:
        return f"Rp {amount}"


def tambah_pemasukan():
    global saldo, history
    print('\n=== Tambah Pemasukan ===')
    try:
        jumlah = float(input("Masukkan jumlah pemasukan (Rp): ").replace('.', '').replace(',', '.'))
        if jumlah <= 0:
            print("Jumlah harus positif.")
            return
    except ValueError:
        print("Input harus berupa angka.")
        return

    keterangan = input("Keterangan (opsional): ").strip()
    if not keterangan:
        keterangan = "(tidak ada keterangan)"

    saldo += jumlah
    entry = {
        'type': 'Pemasukan',
        'amount': jumlah,
        'description': keterangan,
        'time': datetime.now().isoformat()
    }
    history.append(entry)
    save_data()
    print(f"\n✅ Pemasukan {format_rp(jumlah)} berhasil ditambahkan!")


def tambah_pengeluaran():
    global saldo, history
    print('\n=== Tambah Pengeluaran ===')
    try:
        jumlah = float(input("Masukkan jumlah pengeluaran (Rp): ").replace('.', '').replace(',', '.'))
        if jumlah <= 0:
            print("Jumlah harus positif.")
            return
    except ValueError:
        print("Input harus berupa angka.")
        return

    if saldo < jumlah:
        print("Saldo tidak cukup.")
        return

    keterangan = input("Keterangan (opsional): ").strip()
    if not keterangan:
        keterangan = "(tidak ada keterangan)"

    saldo -= jumlah
    entry = {
        'type': 'Pengeluaran',
        'amount': jumlah,
        'description': keterangan,
        'time': datetime.now().isoformat()
    }
    history.append(entry)
    save_data()
    print(f"\n✅ Pengeluaran {format_rp(jumlah)} berhasil dicatat!")


def lihat_saldo():
    print('\n' + '=' * 40)
    print("Saldo saat ini:", format_rp(saldo))
    print('=' * 40)


def show_history(filter_type=None):
    print('\n=== Riwayat Transaksi ===')
    filtered = [h for h in history if (filter_type is None or h['type'] == filter_type)]
    if not filtered:
        print("Belum ada transaksi yang dicatat.")
        return

    # Print table-like view
    print(f"{'No.':<4} {'Waktu':<20} {'Tipe':<12} {'Jumlah':>15}  Keterangan")
    print('-' * 70)
    for i, h in enumerate(filtered, start=1):
        waktu = datetime.fromisoformat(h['time']).strftime('%Y-%m-%d %H:%M')
        tipe = h['type']
        jumlah = format_rp(h['amount'])
        keterangan = h['description']
        print(f"{i:<4} {waktu:<20} {tipe:<12} {jumlah:>15}  {keterangan}")


def reset_data():
    global saldo, history
    confirm = input("Yakin ingin menghapus semua data? Ketik 'YA' untuk konfirmasi: ")
    if confirm == 'YA':
        saldo = 0.0
        history = []
        save_data()
        print("Data berhasil direset.")
    else:
        print("Reset dibatalkan.")


def menu():
    clear_screen()
    print("=== Aplikasi Pengelola Uang Saku ===")
    print("1. Tambah Pemasukan")
    print("2. Tambah Pengeluaran")
    print("3. Lihat Saldo")
    print("4. Lihat Riwayat Pemasukan")
    print("5. Lihat Riwayat Pengeluaran")
    print("6. Lihat Semua Riwayat")
    print("7. Reset Data")
    print("8. Keluar")
    print("-" * 40)


if __name__ == '__main__':
    load_data()
    while True:
        menu()
        pilihan = input("Pilih menu (1-8): ").strip()

        if pilihan == '1':
            tambah_pemasukan()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '2':
            tambah_pengeluaran()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '3':
            lihat_saldo()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '4':
            show_history(filter_type='Pemasukan')
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '5':
            show_history(filter_type='Pengeluaran')
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '6':
            show_history()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '7':
            reset_data()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '8':
            print("\nTerima kasih telah menggunakan aplikasi!")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 1-8.")
            input("\nTekan Enter untuk kembali ke menu...")
