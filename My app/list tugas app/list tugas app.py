import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime

class TaskListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task List App")
        self.tasks = []

        # Menambahkan gaya warna vintage
        style = ttk.Style()
        style.theme_use('clam')  # Tema 'clam' memberikan tampilan vintage

        # Membuat UI
        tk.Label(root, text="Tugas", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="Deadline", font=('Helvetica', 12)).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(root, text="Mapel", font=('Helvetica', 12)).grid(row=0, column=2, padx=10, pady=10)

        self.task_entry = tk.Entry(root, width=20, font=('Helvetica', 12))
        self.task_entry.grid(row=1, column=0, padx=10, pady=10)

        self.deadline_entry = tk.Entry(root, width=10, font=('Helvetica', 12))
        self.deadline_entry.grid(row=1, column=1, padx=10, pady=10)

        self.subject_entry = tk.Entry(root, width=20, font=('Helvetica', 12))
        self.subject_entry.grid(row=1, column=2, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Tambah Tugas", command=self.add_task, font=('Helvetica', 12), bg='#D2B48C')  # Warna vintage
        self.add_button.grid(row=1, column=3, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="Hapus Tugas", command=self.delete_task, font=('Helvetica', 12), bg='#D2B48C')  # Warna vintage
        self.delete_button.grid(row=1, column=4, padx=10, pady=10)

        # Membuat Treeview untuk menampilkan tugas dalam bentuk tabel
        self.task_tree = ttk.Treeview(root, columns=("Tugas", "Deadline", "Mapel"), show="headings", height=10)
        self.task_tree.heading("Tugas", text="Tugas")
        self.task_tree.heading("Deadline", text="Deadline")
        self.task_tree.heading("Mapel", text="Mapel")
        self.task_tree.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        # Menambahkan label untuk menampilkan total tugas
        self.total_label = tk.Label(root, text="Total Tugas: 0", font=('Helvetica', 12), pady=10)
        self.total_label.grid(row=3, column=0, columnspan=5)

        self.save_button = tk.Button(root, text="Simpan", command=self.save_tasks, font=('Helvetica', 12), bg='#D2B48C')  # Warna vintage
        self.save_button.grid(row=4, column=0, columnspan=5, pady=10)

        # Memuat tugas dari file CSV jika ada
        self.load_tasks()

        # Mengikat fungsi keluar aplikasi ke event handler
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_task(self):
        task_text = self.task_entry.get()
        deadline_text = self.deadline_entry.get()
        subject_text = self.subject_entry.get()

        if task_text and deadline_text and subject_text:
            self.tasks.append((task_text, deadline_text, subject_text))
            self.task_tree.insert("", tk.END, values=(task_text, deadline_text, subject_text))
            self.task_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
            self.subject_entry.delete(0, tk.END)
            self.update_total_label()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            item = selected_item[0]
            deleted_task = tuple(self.task_tree.item(item, "values"))
            self.task_tree.delete(item)
            self.tasks.remove(deleted_task)
            self.update_total_label()

    def update_total_label(self):
        total_tasks = len(self.tasks)
        self.total_label.config(text=f"Total Tugas: {total_tasks}")

    def save_tasks(self):
        with open("tasks.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Tugas", "Deadline", "Mapel"])
            for task in self.tasks:
                writer.writerow(task)
        messagebox.showinfo("Simpan", "Tugas berhasil disimpan!")

    def load_tasks(self):
        try:
            with open("tasks.csv", mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                for row in reader:
                    task = tuple(row)
                    self.tasks.append(task)
                    self.task_tree.insert("", tk.END, values=task)
                self.update_total_label()
        except FileNotFoundError:
            pass

    def on_closing(self):
        if messagebox.askokcancel("Keluar", "Anda yakin ingin keluar?"):
            self.save_tasks()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskListApp(root)
    root.mainloop()
