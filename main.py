import tkinter as tk
import random
from tkinter import messagebox

class Hucre(tk.Button):
    """Her bir kareyi temsil eden sınıf."""
    def __init__(self, master, x, y, **kwargs):
        super().__init__(master, **kwargs)
        self.x = x
        self.y = y
        self.mayin_mi = False
        self.acildi_mi = False
        self.isaretli_mi = False
        self.komsu_mayin_sayisi = 0

class MayinTarlasi:
    def __init__(self, root, satir=10, sutun=10, mayin_sayisi=10):
        self.root = root
        self.root.title("OOP Mayın Tarlası")
        self.satir = satir
        self.sutun = sutun
        self.mayin_sayisi = mayin_sayisi
        self.butonlar = []
        
        self.arayuzu_kur()
        self.oyunu_baslat()

    def arayuzu_kur(self):
        """Oyun tahtasını oluşturur."""
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        for r in range(self.satir):
            satir_listesi = []
            for c in range(self.sutun):
                btn = Hucre(self.frame, r, c, width=2, height=1, font=('Arial', 12, 'bold'), relief="raised")
                btn.grid(row=r, column=c)
                # Sol tık: Hücreyi aç
                btn.bind('<Button-1>', lambda e, b=btn: self.hucre_ac(b))
                # Sağ tık: Bayrak koy
                btn.bind('<Button-3>', lambda e, b=btn: self.bayrak_koy(b))
                satir_listesi.append(btn)
            self.butonlar.append(satir_listesi)

    def oyunu_baslat(self):
        """Mayınları yerleştirir ve komşulukları hesaplar."""
        # Rastgele mayın yerleşimi
        hucreler = [btn for satir in self.butonlar for btn in satir]
        secilen_mayinlar = random.sample(hucreler, self.mayin_sayisi)
        for m in secilen_mayinlar:
            m.mayin_mi = True

        # Komşu mayın sayılarını önceden hesapla
        for r in range(self.satir):
            for c in range(self.sutun):
                if not self.butonlar[r][c].mayin_mi:
                    self.butonlar[r][c].komsu_mayin_sayisi = self.komsu_say(r, c)

    def komsu_say(self, r, c):
        sayac = 0
        for i in range(max(0, r-1), min(self.satir, r+2)):
            for j in range(max(0, c-1), min(self.sutun, c+2)):
                if self.butonlar[i][j].mayin_mi:
                    sayac += 1
        return sayac

    def hucre_ac(self, btn):
        if btn.acildi_mi or btn.isaretli_mi:
            return

        btn.acildi_mi = True
        
        if btn.mayin_mi:
            btn.config(text="💣", bg="red")
            self.oyun_bitti(False)
        else:
            if btn.komsu_mayin_sayisi > 0:
                btn.config(text=btn.komsu_mayin_sayisi, bg="lightgrey", relief="sunken")
            else:
                btn.config(bg="lightgrey", relief="sunken")
                # Boş hücre ise komşuları otomatik aç (Recursive)
                for i in range(max(0, btn.x-1), min(self.satir, btn.x+2)):
                    for j in range(max(0, btn.y-1), min(self.sutun, btn.y+2)):
                        self.hucre_ac(self.butonlar[i][j])
            
            self.kazanma_kontrol()

    def bayrak_koy(self, btn):
        if btn.acildi_mi: return
        
        if not btn.isaretli_mi:
            btn.config(text="🚩", fg="red")
            btn.isaretli_mi = True
        else:
            btn.config(text="")
            btn.isaretli_mi = False

    def kazanma_kontrol(self):
        acilmali = (self.satir * self.sutun) - self.mayin_sayisi
        acilanlar = sum(1 for satir in self.butonlar for b in satir if b.acildi_mi)
        if acilanlar == acilmali:
            self.oyun_bitti(True)

    def oyun_bitti(self, kazandi):
        msg = "Tebrikler, kazandınız!" if kazandi else "Mayına bastınız."
        messagebox.showinfo("Oyun Bitti", msg)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    oyun = MayinTarlasi(root)
    root.mainloop() 