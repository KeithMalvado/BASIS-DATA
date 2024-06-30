import psycopg2
from tabulate import tabulate
import time, random, shutil, os
import tabulate

conn = psycopg2.connect(
            dbname="coba",
            user="postgres",
            password="ipan",
            host="localhost",
            port=5432,
        )
cur = conn.cursor() 
# ---------------------------------------------------- fitur tambahan -----------------------------------------------------------
def mengetik(s):
    terminal_width, _ = shutil.get_terminal_size()
    padding = (terminal_width - len(s)) // 2
    print(" " * padding + s)
    time.sleep(random.random() * 0.001)
    
def loading():
    mengetik('\033[32m')
    mengetik("╔══════════════════════════════════════════════════════════════════════╗")
    mengetik("║ Loading ..............                                               ║")
    mengetik("╚══════════════════════════════════════════════════════════════════════╝")
    time.sleep(1)
    os.system("cls")
    
# ---------------------------------------------------- fitur tambahan -----------------------------------------------------------


def terima_stok():
    try:
        curr = conn.cursor()
        curr.execute("SELECT id_barang,jumlah_barang FROM barang_datang")
        data_barang_datang = curr.fetchall()

        for id_barang, jumlah_barang in data_barang_datang:
            print("Menambahkan stok untuk barang dengan ID:", id_barang, "dengan jumlah:", jumlah_barang)
            curr.execute("UPDATE stok SET jumlah_barang = jumlah_barang + %s WHERE id_barang = %s", (jumlah_barang, id_barang))

        conn.commit()
        print("Stok berhasil ditambah berdasarkan barang datang.")
    except psycopg2.Error as e:
        print("Kesalahan saat tambah stok:", e)
    finally:
        curr.close()
        conn.close()

def lihat_stok(data_stok, keyword=None):
    try:
        if keyword:
            data_stok = [barang for barang in data_stok if keyword in barang[1]]

        if not data_stok:
            print("Tidak ada barang yang ditemukan.")
            return

        def binary_search(data, low, high, keyword):
            if high >= low:
                mid = (high + low) // 2
                if data[mid][1] == keyword or (data[mid][1].lower() == keyword.lower()):
                    return mid
                elif data[mid][1] < keyword:
                    return binary_search(data, mid + 1, high, keyword)
                else:
                    return binary_search(data, low, mid - 1, keyword)
            else:
                return -1

        data_stok.sort(key=lambda x: x[1])
        headers = ["ID Barang", "Nama Barang", "Jumlah Barang", "Harga"]

        for item in data_stok:
            idx = binary_search(data_stok, 0, len(data_stok) - 1, item[1])
            if idx != -1:
                item.insert(0, idx)

        table = tabulate(data_stok, headers=headers, tablefmt="grid")
        print("Daftar Stok:")
        print(table)
    except psycopg2.Error as e:
        print("Kesalahan saat melihat stok:", e)
    finally:
        curr.close()

keyword = input("Masukkan kata kunci untuk pencarian: ")
curr = conn.cursor()
if keyword:
    query = "SELECT * FROM stok WHERE nama_barang LIKE %s"
    curr.execute(query, ('%' + keyword + '%',))
else:
    curr.execute("SELECT * FROM stok")
data_stok = curr.fetchall()
lihat_stok(data_stok, keyword)


def penjualan():
    try:
        curr = conn.cursor()
        id_barang = int(input("Masukkan ID barang yang dijual: ")) 
        jumlah_jual = int(input("Masukkan jumlah barang yang dijual: "))

        curr.execute("SELECT id_barang, nama_barang, jumlah_barang FROM stok WHERE id_barang = %s", (id_barang,))
        barang = curr.fetchone()

        if not barang:
            print("Barang dengan ID tersebut tidak ditemukan di stok.")
            return
        
        id_barang, nama_barang, jumlah_barang = barang

        if jumlah_barang < jumlah_jual:
            print("Jumlah barang di stok tidak mencukupi untuk penjualan.")
            return


        curr.execute("SELECT harga FROM stok WHERE id_barang = %s", (id_barang,))
        harga_barang_row = curr.fetchone()

        if harga_barang_row:
            harga_barang = harga_barang_row[0]
        else:
            print("Harga barang tidak dapat ditemukan.")
            return

        curr.execute("UPDATE stok SET jumlah_barang = jumlah_barang - %s WHERE id_barang = %s", (jumlah_jual, id_barang))

        total_harga = jumlah_jual * harga_barang
        curr.execute(
            "INSERT INTO penjualan_hari_ini (id_barang, nama_barang, jumlah_barang, harga) VALUES (%s, %s, %s, %s)",
            (id_barang, nama_barang, jumlah_jual, total_harga)
        )

        conn.commit()
        print("Penjualan berhasil dilakukan.")
    except psycopg2.Error as e:
        print("Kesalahan saat melakukan penjualan:", e)
    finally:
        curr.close()
        conn.close()

def hapus_stok_barang():
    try:
        curr = conn.cursor()

        id_barang = input("Masukkan ID barang yang ingin dihapus dari stok: ")
        jumlah_hapus = int(input("Masukkan jumlah barang yang ingin dihapus dari stok: "))

        curr.execute("SELECT jumlah_barang FROM stok WHERE id_barang = %s", (id_barang,))
        stok_barang = curr.fetchone()

        if not stok_barang:
            print("Barang dengan ID tersebut tidak ditemukan di stok.")
            return
        
        stok_sekarang = stok_barang[0]

        if stok_sekarang < jumlah_hapus:
            print("Jumlah barang di stok tidak mencukupi untuk dihapus.")
            return

        stok_baru = stok_sekarang - jumlah_hapus
        curr.execute("UPDATE stok SET jumlah_barang = %s WHERE id_barang = %s", (stok_baru, id_barang))
        conn.commit()
        print("Data stok barang berhasil dihapus.")

    except psycopg2.Error as e:
        print("Kesalahan saat menghapus data stok barang:", e)
    finally:
        if curr:
            curr.close()
        if conn:
            conn.close()


# ============================================Toko Utama=========================================
def barang_terlaris():
    try:
        curr = conn.cursor()
        curr.execute("""
            SELECT id_barang, nama_barang, SUM(jumlah_barang) AS total_terjual
            FROM penjualan_hari_ini
            GROUP BY id_barang, nama_barang
        """)
        data_penjualan = curr.fetchall()
        for i in range(len(data_penjualan)):
            for j in range(len(data_penjualan)):
                if i >= j:
                    continue
                if data_penjualan[i][2] < data_penjualan[j][2]:  
                    data_penjualan[i], data_penjualan[j] = data_penjualan[j], data_penjualan[i]

        headers = ["ID Barang", "Nama Barang", "Total Terjual"]
        table = tabulate(data_penjualan, headers=headers, tablefmt="grid")

        print("Barang Terlaris (diurutkan berdasarkan penjualan terbanyak):")
        print(table)

    except psycopg2.Error as e:
        print("Kesalahan saat mengambil data penjualan:", e)
    finally:
        curr.close()
        
def lihat_penjualan():
    try:
        curr = conn.cursor()

        curr.execute("SELECT * FROM penjualan_hari_ini")
        data_penjualan = curr.fetchall()

        headers = ["ID Penjualan", "ID Barang", "Nama Barang", "Jumlah Barang", "Harga"]
        table = tabulate(data_penjualan, headers=headers, tablefmt="grid")

        print("Daftar Penjualan:")
        print(table)

    except psycopg2.Error as e:
        print("Kesalahan saat melihat penjualan:", e)
    finally:
        curr.close()

def hapus_penjualan():
    try:
        conn = psycopg2.connect(
            dbname="coba",
            user="postgres",
            password="ipan",
            host="localhost",
            port=5432,
        )
        curr = conn.cursor()

        konfirmasi = input("Apakah Anda yakin ingin menghapus semua data penjualan? (y/n): ")
        if konfirmasi.lower() == 'y':
            curr.execute("DELETE FROM penjualan_hari_ini")
            conn.commit()
            print("Semua data penjualan berhasil dihapus.")
        else:
            print("Penghapusan semua data penjualan dibatalkan.")

    except psycopg2.Error as e:
        print("Kesalahan saat menghapus data penjualan:", e)
    finally:
        if curr:
            curr.close()
        if conn:
            conn.close()

def login():
    mengetik("╔══════════════════════════════════════════════════════════════════════╗")
    mengetik("║                                  Welcome                             ║")
    mengetik("╠══════════════════════════════════════════════════════════════════════╣")
    mengetik("║                           HR-AL BUKHARI NO 7152                      ║")
    mengetik("╚══════════════════════════════════════════════════════════════════════╝")
    username = input("Username: ")
    password = input("Password: ")

    loading()
    if username == "bos" and password == "bos":
        mengetik("Anda login sebagai bos")
        return "bos"
    elif username == "babu" and password == "babu":
        return "babu"
    else:
        mengetik("Login gagal. Cek username dan password Anda.")
        return None

def main():
    role = login()

    if role == "bos":
        while True:
            print("\n===== Aplikasi Manajemen Toko - Toko Utama =====")
            print("1. Lihat Penjualan")
            print("2. Hapus Penjualan")
            print("3. Kirim Stock Ke Cabang")
            print("4. Keluar")
            pilihan = input("Masukkan pilihan Anda: ")
            if pilihan == '1':
                lihat_penjualan()
            elif pilihan == '2':
                hapus_penjualan()
            elif pilihan == '3':
                print("Terima kasih telah menggunakan aplikasi.")
                break
            else:
                print("Pilihan tidak valid. Silakan pilih kembali.")

    elif role == "babu":
        while True:
            print("\n===== Aplikasi Manajemen Toko - Toko Cabang =====")
            print("1. Terima Stok")
            print("2. Hapus Stok")
            print("3. Penjualan")
            print("4. Lihat Total Stok")
            print("5. Barang Terlaris")
            print("6. Keluar")
            pilihan = input("Masukkan pilihan Anda: ")

            if pilihan == '1':
                terima_stok()
            elif pilihan == '2':
                hapus_stok_barang()
            elif pilihan == '3':
                penjualan()
            elif pilihan == '4':
                lihat_stok()
            elif pilihan == '5':
                lihat_penjualan
            elif pilihan == '6':
                print("Terima kasih telah menggunakan aplikasi.")
                break
            else:
                print("Pilihan tidak valid. Silakan pilih kembali.")

    else:
        print("Anda tidak memiliki akses ke aplikasi ini.")
        
main()