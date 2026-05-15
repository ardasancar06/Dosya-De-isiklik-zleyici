import os
import time
import hashlib
import tkinter as tk
from tkinter import filedialog

class IzleyiciArayuz:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Dosya İzleyici ")
        self.pencere.geometry("600x450")
        
        self.hedef_klasor = ""
        self.onceki_durum = {}
        self.izliyor_mu = False

        self.ust_frame = tk.Frame(pencere)
        self.ust_frame.pack(pady=15)

        self.btn_sec = tk.Button(self.ust_frame, text="Klasör Seç", command=self.klasor_sec, width=15)
        self.btn_sec.pack(side=tk.LEFT, padx=10)

        self.btn_baslat = tk.Button(self.ust_frame, text="İzlemeyi Başlat", command=self.baslat, state=tk.DISABLED, width=15)
        self.btn_baslat.pack(side=tk.LEFT, padx=10)

        self.btn_durdur = tk.Button(self.ust_frame, text="İzlemeyi Durdur", command=self.durdur, state=tk.DISABLED, width=15)
        self.btn_durdur.pack(side=tk.LEFT, padx=10)

        self.log_ekrani = tk.Text(pencere, bg="black", fg="lime", font=("Consolas", 10))
        self.log_ekrani.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def log_yaz(self, mesaj):
        zaman = time.strftime('%Y-%m-%d %H:%M:%S')
        tam_mesaj = f"[{zaman}] {mesaj}\n"
        self.log_ekrani.insert(tk.END, tam_mesaj)
        self.log_ekrani.see(tk.END)
       
        try:
            with open("sistem_log.txt", "a", encoding="utf-8") as f:
                f.write(tam_mesaj)
        except:
            pass

    def dosya_hash_hesapla(self, tam_yol):
        try:
            with open(tam_yol, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def dosya_bilgileri(self):
        dosyalar = {}
        if not self.hedef_klasor:
            return dosyalar
            
        try:
            for dosya_adi in os.listdir(self.hedef_klasor):
                tam_yol = os.path.join(self.hedef_klasor, dosya_adi)
                if os.path.isfile(tam_yol):
                    h_degeri = self.dosya_hash_hesapla(tam_yol)
                    if h_degeri:
                        dosyalar[dosya_adi] = h_degeri
        except:
            pass 
            
        return dosyalar

    def klasor_sec(self):
        secilen = filedialog.askdirectory()
        if secilen:
            self.hedef_klasor = secilen
            self.btn_baslat.config(state=tk.NORMAL)
            self.log_yaz(f"Hedef Klasör: {self.hedef_klasor}")

    def baslat(self):
        self.izliyor_mu = True
        self.btn_sec.config(state=tk.DISABLED)
        self.btn_baslat.config(state=tk.DISABLED)
        self.btn_durdur.config(state=tk.NORMAL)
        self.onceki_durum = self.dosya_bilgileri()
        self.log_yaz("Sistem: İzleme Aktif Edildi. Lütfen bir dosya ekleyip/değiştirip kaydedin.")
        self.kontrol_dongusu()

    def durdur(self):
        self.izliyor_mu = False
        self.btn_sec.config(state=tk.NORMAL)
        self.btn_baslat.config(state=tk.NORMAL)
        self.btn_durdur.config(state=tk.DISABLED)
        self.log_yaz("Sistem: İzleme Durduruldu.")

    def kontrol_dongusu(self):
        if not self.izliyor_mu:
            return

        try:
            suanki_durum = self.dosya_bilgileri()

            for dosya, h_degeri in suanki_durum.items():
                if dosya not in self.onceki_durum:
                    self.log_yaz(f"[YENİ OLUŞTURULDU] : {dosya}")
                elif h_degeri != self.onceki_durum[dosya]:
                    self.log_yaz(f"[İÇERİĞİ DEĞİŞTİ]  : {dosya}")

            for dosya in self.onceki_durum:
                if dosya not in suanki_durum:
                    self.log_yaz(f"[SİLİNDİ]          : {dosya}")

            self.onceki_durum = suanki_durum
        except Exception:
            pass 

        self.pencere.after(2000, self.kontrol_dongusu)

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = IzleyiciArayuz(root)
    root.mainloop()
