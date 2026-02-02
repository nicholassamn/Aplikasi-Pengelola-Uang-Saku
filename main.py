import os
import json
from datetime import datetime

# Optional: use colorama on Windows for better support
try:
    import colorama
    colorama.init()
except Exception:
    pass

DATA_FILE = 'data.json'

saldo = 0.0
history = []  # each item: {'type': 'Pemasukan'|'Pengeluaran', 'amount': float, 'description': str, 'time': iso_str}


def clear_screen():
    # Cross-platform clear
    os.system('cls' if os.name == 'nt' else 'clear')


# ANSI color constants
class Colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def color_text(text: str, color: str) -> str:
    return f"{color}{text}{Colors.END}"


def print_header(text: str):
    print(color_text(f"\n{text}", Colors.CYAN + Colors.BOLD))


def print_success(text: str):
    print(color_text(text, Colors.GREEN))


def print_error(text: str):
    print(color_text(text, Colors.RED))


def print_warn(text: str):
    print(color_text(text, Colors.YELLOW))


def input_colored(prompt: str, color: str = Colors.BLUE) -> str:
    return input(color_text(prompt, color))


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
    print_header('=== Tambah Pemasukan ===')
    try:
        raw = input_colored("Masukkan jumlah pemasukan (Rp): ")
        jumlah = float(raw.replace('.', '').replace(',', '.'))
        if jumlah <= 0:
            print_error("Jumlah harus positif.")
            return
    except ValueError:
        print_error("Input harus berupa angka.")
        return

    keterangan = input_colored("Keterangan (opsional): ", Colors.YELLOW).strip()
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
    print_success(f"\n✅ Pemasukan {format_rp(jumlah)} berhasil ditambahkan!")


def tambah_pengeluaran():
    global saldo, history
    print_header('=== Tambah Pengeluaran ===')
    try:
        raw = input_colored("Masukkan jumlah pengeluaran (Rp): ")
        jumlah = float(raw.replace('.', '').replace(',', '.'))
        if jumlah <= 0:
            print_error("Jumlah harus positif.")
            return
    except ValueError:
        print_error("Input harus berupa angka.")
        return

    if saldo < jumlah:
        print_warn("Saldo tidak cukup.")
        return

    keterangan = input_colored("Keterangan (opsional): ", Colors.YELLOW).strip()
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
    print_success(f"\n✅ Pengeluaran {format_rp(jumlah)} berhasil dicatat!")


def lihat_saldo():
    print('\n' + '=' * 40)
    print(color_text("Saldo saat ini:", Colors.BOLD + Colors.CYAN), color_text(format_rp(saldo), Colors.GREEN))
    print('=' * 40)


def show_history(filter_type=None):
    title = '=== Riwayat Transaksi ===' if filter_type is None else f"=== Riwayat {filter_type} ==="
    print_header(title)
    filtered = [h for h in history if (filter_type is None or h['type'] == filter_type)]
    if not filtered:
        print_warn("Belum ada transaksi yang dicatat.")
        return

    # Print table-like view
    header = f"{'No.':<4} {'Waktu':<20} {'Tipe':<12} {'Jumlah':>15}  Keterangan"
    print(color_text(header, Colors.UNDERLINE + Colors.BOLD))
    print('-' * 70)
    for i, h in enumerate(filtered, start=1):
        waktu = datetime.fromisoformat(h['time']).strftime('%Y-%m-%d %H:%M')
        tipe = h['type']
        tipe_col = Colors.GREEN if tipe == 'Pemasukan' else Colors.RED
        jumlah = format_rp(h['amount'])
        keterangan = h['description']
        print(f"{i:<4} {waktu:<20} {color_text(tipe, tipe_col):<12} {color_text(jumlah, Colors.BOLD):>15}  {keterangan}")


def reset_data():
    global saldo, history
    confirm = input_colored("Yakin ingin menghapus semua data? Ketik 'YA' untuk konfirmasi: ", Colors.YELLOW)
    if confirm == 'YA':
        saldo = 0.0
        history = []
        save_data()
        print_success("Data berhasil direset.")
    else:
        print_warn("Reset dibatalkan.")


def menu():
    clear_screen()
    print(color_text("=== Aplikasi Pengelola Uang Saku ===", Colors.CYAN + Colors.BOLD))
    print(color_text("1.", Colors.YELLOW), "Tambah Pemasukan")
    print(color_text("2.", Colors.YELLOW), "Tambah Pengeluaran")
    print(color_text("3.", Colors.YELLOW), "Lihat Saldo")
    print(color_text("4.", Colors.YELLOW), "Lihat Riwayat Pemasukan")
    print(color_text("5.", Colors.YELLOW), "Lihat Riwayat Pengeluaran")
    print(color_text("6.", Colors.YELLOW), "Lihat Semua Riwayat")
    print(color_text("7.", Colors.YELLOW), "Reset Data")
    print(color_text("8.", Colors.YELLOW), "Keluar")
    print("-" * 40)


if __name__ == '__main__':
    load_data()
    while True:
        menu()
        pilihan = input_colored("Pilih menu (1-8): ").strip()

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
