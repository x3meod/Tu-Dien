from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import os

# ======CLASS=======
class Translatorapp:
    def __init__(self):
        self.window = Tk()
        self.window.title("Từ Điển")
        self.window.geometry("450x550")

        self.window.protocol("WM_DELETE_WINDOW", self.khi_dong_ung_dung)

        self.ngon_ngu_nguon = "en"
        self.ngon_ngu_dich = "vi"

        self.khoi_tao_db()
        self.tao_giao_dien()
    def them_tu_can_hoc(self):
        tu_goc = self.txt_input.get("1.0", "end-1c").strip()
        nghia = self.ketq_output.get("1.0", "end-1c").strip()

        if not tu_goc or not nghia:
            messagebox.showwarning(
                "Cảnh báo",
                "Hãy tra một từ trước!"
            )
            return

        try:
            # Kiểm tra xem từ đã tồn tại chưa
            self.cursor.execute("""
                SELECT id
                FROM tu_can_hoc
                WHERE tu_goc = ? AND nghia = ?
            """, (tu_goc, nghia))

            if self.cursor.fetchone():
                messagebox.showinfo(
                    "Thông báo",
                    f"'{tu_goc}' đã có trong danh sách từ cần học!"
                )
                return

            # Thêm từ mới
            self.cursor.execute("""
                INSERT INTO tu_can_hoc (tu_goc, nghia)
                VALUES (?, ?)
            """, (tu_goc, nghia))

            self.conn.commit()

            messagebox.showinfo(
                "Thành công",
                f"Đã thêm '{tu_goc}' vào danh sách từ cần học!"
            )

        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"Không thể thêm từ: {e}"
            )
    def hoc_tu_ngau_nhien(self):
        self.cursor.execute("""
            SELECT tu_goc, nghia
            FROM tu_can_hoc
            ORDER BY RANDOM()
            LIMIT 1
        """)

        row = self.cursor.fetchone()

        if row:
            tu_goc, nghia = row

            messagebox.showinfo(
                "Từ ngẫu nhiên",
                f"Từ: {tu_goc}\n\nNghĩa: {nghia}"
            )
        else:
            messagebox.showinfo(
                "Thông báo",
                "Chưa có từ nào trong danh sách cần học!"
            )
    def khoi_tao_db(self):
        self.conn = sqlite3.connect("tudien.db")
        self.cursor= self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tu_vung (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tu_goc TEXT NOT NULL,
                nghia TEXT NOT NULL,
                ngon_ngu_nguon TEXT,
                ngon_ngu_dich TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lich_su (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tu_da_tra TEXT,
                ket_qua TEXT,
                thoi_gian DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tu_can_hoc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tu_goc TEXT NOT NULL,
            nghia TEXT NOT NULL,
            muc_do INTEGER DEFAULT 0,
            ngay_them DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
        self.conn.commit()

    def tao_giao_dien(self):
        self.main_menubar = Menu(self.window)

        self.file_menu = Menu(self.main_menubar, tearoff=0)
        self.file_menu.add_command(
            label="Xem lịch sử", command=self.xem_lich_su
        )
        self.main_menubar.add_cascade(label="File", menu=self.file_menu)

        self.tu_vung_menu = Menu(self.main_menubar, tearoff=0)
        self.tu_vung_menu.add_command(
            label="Thêm từ mới", command=self.mo_cua_so_them_tu
        )
        self.tu_vung_menu.add_command(
            label="Quản lý / Xóa từ", command=self.mo_cua_so_quan_ly
        )
        self.tu_vung_menu.add_command(
        label="Từ cần học",
        command=self.mo_cua_so_tu_can_hoc
        )
        self.main_menubar.add_cascade(
            label="Tùy chọn", menu=self.tu_vung_menu
        )

        self.window.config(menu=self.main_menubar)

        self.nhap_input = Label(
            self.window, text="Văn bản cần dịch: Tiếng Anh"
        )
        self.nhap_input.pack(pady=5)

        self.txt_input = Text(self.window, height=5, width=45)
        self.txt_input.pack(pady=5)

        self.btn_swap = Button(
            self.window,
            text="🔄 Đổi chiều dịch",
            command=self.doi_chieu,
            bg="#5f6368",
            fg="white",
        )
        self.btn_swap.pack(pady=5)

        self.btn_dich = Button(
            self.window,
            text="Tra từ / Dịch",
            command=self.dich_van_ban,
            bg="#1a73e8",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.btn_dich.pack(pady=5)

        self.kq_output = Label(self.window, text="Kết quả: Tiếng Việt")
        self.kq_output.pack(pady=5)

        self.ketq_output = Text(self.window, height=5, width=45)
        self.ketq_output.pack(pady=5)

        self.btn_them_hoc = Button(
        self.window,
            text="📚 Thêm vào từ cần học",
            command=self.them_tu_can_hoc,
            bg="#28a745",
            fg="white"
        )
        self.btn_them_hoc.pack(pady=5)

    def mo_cua_so_them_tu(self):
        self.cua_so_them = Toplevel(self.window)
        self.cua_so_them.geometry("380x320")
        self.cua_so_them.title("Thêm từ mới")

        Label(self.cua_so_them, text="Từ gốc:").pack(pady=(10, 2))
        self.entry_tu_goc = Entry(self.cua_so_them, width=35)
        self.entry_tu_goc.pack(pady=5)

        Label(self.cua_so_them, text="Nghĩa dịch:").pack(pady=(5, 2))
        self.entry_nghia = Entry(self.cua_so_them, width=35)
        self.entry_nghia.pack(pady=5)

        Label(self.cua_so_them, text="Ngôn ngữ nguồn (en hoặc vi):").pack(
            pady=(5, 2)
        )
        self.entry_ngon_ngu_nguon = Entry(self.cua_so_them, width=35)
        self.entry_ngon_ngu_nguon.insert(0, self.ngon_ngu_nguon)
        self.entry_ngon_ngu_nguon.pack(pady=5)

        Label(self.cua_so_them, text="Ngôn ngữ dịch (vi hoặc en):").pack(
            pady=(5, 2)
        )
        self.entry_ngon_ngu_dich = Entry(self.cua_so_them, width=35)
        self.entry_ngon_ngu_dich.insert(0, self.ngon_ngu_dich)
        self.entry_ngon_ngu_dich.pack(pady=5)

        btn_luu = Button(
            self.cua_so_them,
            text="Lưu vào CSDL",
            command=self.luu_tu_moi,
            bg="#28a745",
            fg="white",
        )
        btn_luu.pack(pady=15)

    def luu_tu_moi(self):
        tu_goc = self.entry_tu_goc.get().strip()
        nghia = self.entry_nghia.get().strip()
        nguon = self.entry_ngon_ngu_nguon.get().strip().lower()
        dich = self.entry_ngon_ngu_dich.get().strip().lower()

        if not tu_goc or not nghia or not nguon or not dich:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng nhập đầy đủ thông tin!",
                parent=self.cua_so_them,
            )
            return

        try:
            self.cursor.execute(
                """INSERT INTO tu_vung (tu_goc, nghia, ngon_ngu_nguon, ngon_ngu_dich) 
                   VALUES (?, ?, ?, ?)""",
                (tu_goc, nghia, nguon, dich),
            )

            self.conn.commit()
            messagebox.showinfo(
                "Thành công",
                f"Đã thêm từ '{tu_goc}' vào CSDL!",
                parent=self.cua_so_them,
            )
            self.cua_so_them.destroy()
        except Exception as e:
            messagebox.showerror(
                "Lỗi", f"Không thể lưu từ: {e}", parent=self.cua_so_them
            )
    def mo_cua_so_tu_can_hoc(self):
        self.cua_so_hoc = Toplevel(self.window)
        self.cua_so_hoc.geometry("550x400")
        self.cua_so_hoc.title("Từ cần học")

        columns = ("id", "tu_goc", "nghia", "muc_do")

        self.tree_hoc = ttk.Treeview(
            self.cua_so_hoc,
            columns=columns,
            show="headings"
        )

        self.tree_hoc.heading("id", text="ID")
        self.tree_hoc.heading("tu_goc", text="Từ")
        self.tree_hoc.heading("nghia", text="Nghĩa")
        self.tree_hoc.heading("muc_do", text="Mức độ")

        self.tree_hoc.column("id", width=50)
        self.tree_hoc.column("tu_goc", width=150)
        self.tree_hoc.column("nghia", width=250)
        self.tree_hoc.column("muc_do", width=80)

        self.tree_hoc.pack(
            fill=BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        self.cursor.execute("""
            SELECT id, tu_goc, nghia, muc_do
            FROM tu_can_hoc
            ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()

        for row in rows:
            self.tree_hoc.insert(
                "",
                END,
                values=row)
        btn_random = Button(
        self.cua_so_hoc,
        text="🎲 Học từ ngẫu nhiên",
        command=self.hoc_tu_ngau_nhien,
        bg="#ffc107")
        btn_random.pack(pady=10)
    def mo_cua_so_quan_ly(self):
        self.cua_so_ql = Toplevel(self.window)
        self.cua_so_ql.geometry("550x400")
        self.cua_so_ql.title("Quản lý & Xóa từ vựng")

        # Khung tìm kiếm
        frame_search = Frame(self.cua_so_ql)
        frame_search.pack(fill=X, padx=10, pady=10)

        Label(frame_search, text="Tìm kiếm:").pack(side=LEFT, padx=5)
        self.entry_tim_kiem = Entry(frame_search)
        self.entry_tim_kiem.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.entry_tim_kiem.bind("<KeyRelease>", self.cap_nhat_danh_sach_tu)

        # Bảng hiển thị danh sách từ (Treeview)
        columns = ("id", "tu_goc", "nghia", "nguon", "dich")
        self.tree_dict = ttk.Treeview(
            self.cua_so_ql, columns=columns, show="headings"
        )
        self.tree_dict.heading("id", text="ID")
        self.tree_dict.heading("tu_goc", text="Từ gốc")
        self.tree_dict.heading("nghia", text="Nghĩa")
        self.tree_dict.heading("nguon", text="Nguồn")
        self.tree_dict.heading("dich", text="Dịch")

        self.tree_dict.column("id", width=40, anchor=CENTER)
        self.tree_dict.column("tu_goc", width=120)
        self.tree_dict.column("nghia", width=180)
        self.tree_dict.column("nguon", width=60, anchor=CENTER)
        self.tree_dict.column("dich", width=60, anchor=CENTER)

        self.tree_dict.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Nút xóa từ
        btn_xoa = Button(
            self.cua_so_ql,
            text="❌ Xóa từ đang chọn",
            command=self.xoa_tu_da_chon,
            bg="#dc3545",
            fg="white",
        )
        btn_xoa.pack(pady=10)
    
        # Tải danh sách từ ban đầu
        self.cap_nhat_danh_sach_tu()

    def cap_nhat_danh_sach_tu(self, event=None):
        if not hasattr(self, "tree_dict") or not self.tree_dict.winfo_exists():
            return

        tu_khoa = self.entry_tim_kiem.get().strip()

        # Xóa các dòng cũ trên bảng
        for item in self.tree_dict.get_children():
            self.tree_dict.delete(item)

        # Truy vấn tìm kiếm gần đúng với LIKE
        if tu_khoa:
            query = """
                SELECT id, tu_goc, nghia, ngon_ngu_nguon, ngon_ngu_dich
                FROM tu_vung
                WHERE tu_goc LIKE ?
            """
            self.cursor.execute(query, (f"{tu_khoa}%",))
        else:
            query = "SELECT id, tu_goc, nghia, ngon_ngu_nguon, ngon_ngu_dich FROM tu_vung"
            self.cursor.execute(query)

        rows = self.cursor.fetchall()
        for row in rows:
            self.tree_dict.insert("", END, values=row)

    def xoa_tu_da_chon(self):
        selected_item = self.tree_dict.selection()
        if not selected_item:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng chọn một từ trong danh sách để xóa!",
                parent=self.cua_so_ql,
            )
            return

        item_data = self.tree_dict.item(selected_item[0])
        tu_id = item_data["values"][0]
        tu_goc = item_data["values"][1]

        xac_nhan = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa từ '{tu_goc}' khỏi cơ sở dữ liệu?",
            parent=self.cua_so_ql,
        )

        if xac_nhan:
            try:
                self.cursor.execute(
                    "DELETE FROM tu_vung WHERE id = ?", (tu_id,)
                )
                self.conn.commit()
                messagebox.showinfo(
                    "Thành công",
                    f"Đã xóa từ '{tu_goc}' thành công!",
                    parent=self.cua_so_ql,
                )
                self.cap_nhat_danh_sach_tu()
            except Exception as e:
                messagebox.showerror(
                    "Lỗi", f"Không thể xóa từ: {e}", parent=self.cua_so_ql
                )

    def doi_chieu(self):
        self.ngon_ngu_nguon, self.ngon_ngu_dich = (
            self.ngon_ngu_dich,
            self.ngon_ngu_nguon,
        )

        self.chu_o_tren = self.txt_input.get("1.0", "end-1c")
        self.chu_o_duoi = self.ketq_output.get("1.0", "end-1c")

        self.txt_input.delete("1.0", END)
        self.txt_input.insert(END, self.chu_o_duoi)

        self.ketq_output.delete("1.0", END)
        self.ketq_output.insert(END, self.chu_o_tren)

        self.ten_nguon = (
            "Tiếng Việt" if self.ngon_ngu_nguon == "vi" else "Tiếng Anh"
        )
        self.ten_dich = (
            "Tiếng Việt" if self.ngon_ngu_dich == "vi" else "Tiếng Anh"
        )

        self.nhap_input.config(text=f"Văn bản cần dịch: {self.ten_nguon}")
        self.kq_output.config(text=f"Kết quả: {self.ten_dich}")

    def dich_van_ban(self):
        self.van_ban = self.txt_input.get("1.0", "end-1c").strip()
        if not self.van_ban:
            self.ketq_output.delete("1.0", END)
            self.ketq_output.insert(END, "Vui lòng nhập văn bản cần dịch")
            return

        try:
            self.cursor.execute(
                """
                SELECT nghia
                FROM tu_vung
                WHERE LOWER(tu_goc)=LOWER(?)
                AND ngon_ngu_nguon=?
                AND ngon_ngu_dich=?
                """,
                (self.van_ban, self.ngon_ngu_nguon, self.ngon_ngu_dich),
            )
            row = self.cursor.fetchone()

            if row:
                self.ket_qua = row[0]
            else:
                self.ket_qua = f"Không tìm thấy nghĩa của '{self.van_ban}' trong cơ sở dữ liệu."

            self.cursor.execute(
                """
                INSERT INTO lich_su (tu_da_tra, ket_qua)
                VALUES (?, ?)
                """,
                (self.van_ban, self.ket_qua),
            )
            self.conn.commit()

            self.ketq_output.delete("1.0", END)
            self.ketq_output.insert(END, self.ket_qua)

        except Exception as e:
            self.ketq_output.delete("1.0", END)
            self.ketq_output.insert(END, f"Có lỗi xảy ra: {e}")

    def xem_lich_su(self):
        self.cua_so_phu = Toplevel(self.window)
        self.cua_so_phu.geometry("500x300")
        self.cua_so_phu.title("Lịch sử từ vựng (SQLite3)")

        self.txt_lich_su = Text(self.cua_so_phu)
        self.txt_lich_su.pack(fill=BOTH, expand=True)

        try:
            self.cursor.execute(
                """
                SELECT tu_da_tra, ket_qua, thoi_gian
                FROM lich_su
                ORDER BY id DESC
                """
            )
            rows = self.cursor.fetchall()

            if rows:
                for row in rows:
                    self.txt_lich_su.insert(
                        END,
                        f"[{row[2]}] {row[0]} -> {row[1]}\n",
                    )
            else:
                self.txt_lich_su.insert(END, "Chưa có lịch sử tra cứu.")
        except Exception as e:
            self.txt_lich_su.insert(END, f"Lỗi đọc cơ sở dữ liệu: {e}")

    def khi_dong_ung_dung(self):
        try:
            self.conn.close()
        except:
            pass
        self.window.destroy()

    def chay_ung_dung(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Translatorapp()
    app.chay_ung_dung()
# import cai file tu dien vao database
# them ds tu yeu thich
# them h/a
# chuc nang them tu can hoc hom nay(them chuc nang random de lam)