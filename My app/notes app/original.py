import tkinter as tk
from tkinter import messagebox
import pickle
import hashlib

class DailyNoteApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Catatan Harian")
        self.master.geometry("400x400")

        # Variabel
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.note_title = tk.StringVar()
        self.note_text = tk.StringVar()

        # Widget
        self.label_username = tk.Label(self.master, text="Username:")
        self.entry_username = tk.Entry(self.master, textvariable=self.username)
        self.label_password = tk.Label(self.master, text="Password:")
        self.entry_password = tk.Entry(self.master, textvariable=self.password, show="*")
        self.label_note_title = tk.Label(self.master, text="Judul Catatan:")
        self.entry_note_title = tk.Entry(self.master, textvariable=self.note_title)
        self.label_note = tk.Label(self.master, text="Isi Catatan:")
        self.text_note = tk.Text(self.master, wrap="word", height=10, width=30)
        self.button_save = tk.Button(self.master, text="Simpan", command=self.save_note)
        self.button_load = tk.Button(self.master, text="Muat", command=self.load_note)
        self.button_show_notes = tk.Button(self.master, text="Tampilkan Catatan", command=self.show_notes_page)

        # Layout
        self.label_username.grid(row=0, column=0, pady=5)
        self.entry_username.grid(row=0, column=1, pady=5)
        self.label_password.grid(row=1, column=0, pady=5)
        self.entry_password.grid(row=1, column=1, pady=5)
        self.label_note_title.grid(row=2, column=0, pady=5)
        self.entry_note_title.grid(row=2, column=1, pady=5)
        self.label_note.grid(row=3, column=0, pady=5)
        self.text_note.grid(row=3, column=1, pady=5)
        self.button_save.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_load.grid(row=5, column=0, columnspan=2, pady=10)
        self.button_show_notes.grid(row=6, column=0, columnspan=2, pady=10)

        # Inisialisasi struktur data untuk menyimpan catatan
        self.notes_data = {}

    def save_note(self):
        username = self.username.get()
        password = self.password.get()
        note_title = self.note_title.get()

        # Enkripsi password sebelum menyimpan
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Membuat struktur data catatan jika belum ada
        if username not in self.notes_data:
            self.notes_data[username] = {}

        # Membuat catatan pada judul tertentu jika belum ada
        if note_title not in self.notes_data[username]:
            self.notes_data[username][note_title] = {}

        # Menyimpan data catatan
        self.notes_data[username][note_title] = {
            "password": hashed_password,
            "note": self.text_note.get("1.0", tk.END)
        }

        try:
            with open(f"{username}_notes.pkl", "wb") as file:
                pickle.dump(self.notes_data, file)
            messagebox.showinfo("Sukses", "Catatan harian berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def load_note(self):
        username = self.username.get()
        password = self.password.get()
        note_title = self.note_title.get()

        try:
            with open(f"{username}_notes.pkl", "rb") as file:
                data = pickle.load(file)

            # Verifikasi password sebelum memuat catatan
            if username in data and note_title in data[username]:
                hashed_password = data[username][note_title]["password"]
                if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                    self.text_note.delete("1.0", tk.END)
                    self.text_note.insert(tk.END, data[username][note_title]["note"])
                    messagebox.showinfo("Sukses", "Catatan harian berhasil dimuat!")
                else:
                    messagebox.showerror("Error", "Password salah!")
            else:
                messagebox.showerror("Error", "Catatan harian tidak ditemukan.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Catatan harian tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def show_notes_page(self):
        show_notes_window = tk.Toplevel(self.master)
        show_notes_window.title("Tampilkan Catatan")
        show_notes_window.geometry("400x400")

        # Widget di halaman tampilkan catatan
        label_username_show = tk.Label(show_notes_window, text="Username:")
        entry_username_show = tk.Entry(show_notes_window, textvariable=self.username, state='disabled')
        label_password_show = tk.Label(show_notes_window, text="Password:")
        entry_password_show = tk.Entry(show_notes_window, textvariable=self.password, show="*", state='disabled')
        label_note_title_show = tk.Label(show_notes_window, text="Judul Catatan:")
        entry_note_title_show = tk.Entry(show_notes_window, textvariable=self.note_title, state='disabled')
        button_load_notes = tk.Button(show_notes_window, text="Muat Catatan", command=self.load_notes)
        button_edit_note = tk.Button(show_notes_window, text="Edit Catatan", command=self.edit_note)

        # Layout di halaman tampilkan catatan
        label_username_show.grid(row=0, column=0, pady=5)
        entry_username_show.grid(row=0, column=1, pady=5)
        label_password_show.grid(row=1, column=0, pady=5)
        entry_password_show.grid(row=1, column=1, pady=5)
        label_note_title_show.grid(row=2, column=0, pady=5)
        entry_note_title_show.grid(row=2, column=1, pady=5)
        button_load_notes.grid(row=3, column=0, columnspan=2, pady=10)
        button_edit_note.grid(row=4, column=0, columnspan=2, pady=10)

    def load_notes(self):
        username = self.username.get()
        password = self.password.get()
        note_title = self.note_title.get()

        try:
            with open(f"{username}_notes.pkl", "rb") as file:
                data = pickle.load(file)

            # Verifikasi password sebelum menampilkan catatan
            if username in data and note_title in data[username]:
                hashed_password = data[username][note_title]["password"]
                if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                    show_notes_window = tk.Toplevel(self.master)
                    show_notes_window.title("Catatan Harian")
                    show_notes_window.geometry("400x400")

                    label_note_show = tk.Label(show_notes_window, text="Catatan Harian:")
                    text_note_show = tk.Text(show_notes_window, wrap="word", height=10, width=30)
                    text_note_show.insert(tk.END, data[username][note_title]["note"])

                    # Layout di halaman tampilkan catatan
                    label_note_show.grid(row=0, column=0, pady=5)
                    text_note_show.grid(row=1, column=0, pady=5)
                else:
                    messagebox.showerror("Error", "Password salah!")
            else:
                messagebox.showerror("Error", "Catatan harian tidak ditemukan.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Catatan harian tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def edit_note(self):
        username = self.username.get()
        password = self.password.get()
        note_title = self.note_title.get()

        try:
            with open(f"{username}_notes.pkl", "rb") as file:
                data = pickle.load(file)

            # Verifikasi password sebelum mengedit catatan
            if username in data and note_title in data[username]:
                hashed_password = data[username][note_title]["password"]
                if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                    show_notes_window = tk.Toplevel(self.master)
                    show_notes_window.title("Edit Catatan")
                    show_notes_window.geometry("400x400")

                    label_note_edit = tk.Label(show_notes_window, text="Edit Catatan:")
                    text_note_edit = tk.Text(show_notes_window, wrap="word", height=10, width=30)
                    text_note_edit.insert(tk.END, data[username][note_title]["note"])

                    button_save_edit = tk.Button(show_notes_window, text="Simpan Perubahan", command=lambda: self.save_edit(username, note_title, text_note_edit.get("1.0", tk.END)))
                    
                    # Layout di halaman edit catatan
                    label_note_edit.grid(row=0, column=0, pady=5)
                    text_note_edit.grid(row=1, column=0, pady=5)
                    button_save_edit.grid(row=2, column=0, pady=10)
                else:
                    messagebox.showerror("Error", "Password salah!")
            else:
                messagebox.showerror("Error", "Catatan harian tidak ditemukan.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Catatan harian tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def save_edit(self, username, note_title, edited_note):
        try:
            with open(f"{username}_notes.pkl", "rb") as file:
                data = pickle.load(file)

            # Update isi catatan
            data[username][note_title]["note"] = edited_note

            # Simpan perubahan
            with open(f"{username}_notes.pkl", "wb") as file:
                pickle.dump(data, file)

            messagebox.showinfo("Sukses", "Perubahan catatan berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DailyNoteApp(root)
    root.mainloop()
