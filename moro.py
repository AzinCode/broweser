import tkinter as tk
from tkinter import ttk
import webview

# برای اجرای این کد، ابتدا کتابخانه مورد نیاز را با دستور زیر در ترمینال خود نصب کنید:
# pip install "pywebview[tkinter]"
#
# توجه: در ویندوز، این کتابخانه به Microsoft Edge WebView2 Runtime نیاز دارد.
# اگر نصب نیست، می‌توانید آن را از لینک زیر دریافت کنید:
# https://developer.microsoft.com/en-us/microsoft-edge/webview2/

class Browser:
    HOME_URL = "https://www.google.com"

    def __init__(self, master):
        """سازنده کلاس مرورگر"""
        self.master = master
        master.title("کنترل پنل مرورگر")
        master.geometry("800x80")

        # فریم برای نوار ابزار
        toolbar_frame = ttk.Frame(master, padding="5")
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # دکمه خانه (جدید)
        self.home_button = ttk.Button(toolbar_frame, text="⌂", command=self.go_home, width=3)
        self.home_button.pack(side=tk.LEFT, padx=2)

        # دکمه بازگشت
        self.back_button = ttk.Button(toolbar_frame, text="<", command=self.go_back, width=3)
        self.back_button.pack(side=tk.LEFT, padx=2)

        # دکمه بعدی
        self.forward_button = ttk.Button(toolbar_frame, text=">", command=self.go_forward, width=3)
        self.forward_button.pack(side=tk.LEFT, padx=2)

        # دکمه تازه‌سازی (جدید)
        self.reload_button = ttk.Button(toolbar_frame, text="⟳", command=self.reload_page, width=3)
        self.reload_button.pack(side=tk.LEFT, padx=2)
        
        # نوار آدرس
        self.url_entry = ttk.Entry(toolbar_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.bind("<Return>", self.load_url)

        # دکمه برو
        self.go_button = ttk.Button(toolbar_frame, text="برو", command=self.load_url)
        self.go_button.pack(side=tk.LEFT, padx=2)

        # ایجاد پنجره وب‌ویو
        self.webview = webview.create_window('مرورگر ساده پایتون', url=self.HOME_URL)
        self.webview.events.loaded += self.on_loaded

        # مقداردهی اولیه نوار آدرس
        self.url_entry.insert(0, self.HOME_URL)

    def load_url(self, event=None):
        """بارگذاری URL از نوار آدرس"""
        url = self.url_entry.get()
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
        
        self.webview.load_url(url)

    def go_back(self):
        """رفتن به صفحه قبلی در تاریخچه"""
        self.webview.go_back()

    def go_forward(self):
        """رفتن به صفحه بعدی در تاریخچه"""
        self.webview.go_forward()

    def reload_page(self):
        """بارگذاری مجدد صفحه فعلی (جدید)"""
        self.webview.reload()

    def go_home(self):
        """رفتن به صفحه اصلی (جدید)"""
        self.webview.load_url(self.HOME_URL)

    def on_loaded(self):
        """این تابع زمانی که صفحه جدیدی بارگذاری می‌شود، فراخوانی می‌شود"""
        current_url = self.webview.get_current_url()
        page_title = self.webview.get_title()
        
        # به‌روزرسانی عنوان پنجره وب‌ویو
        if page_title:
            self.webview.set_title(f"مرورگر من - {page_title}")

        # به‌روزرسانی امن رابط کاربری tkinter از thread اصلی
        if current_url:
            self.master.after(0, self.update_ui, current_url, page_title)

    def update_ui(self, url, title):
        """تابع کمکی برای به‌روزرسانی نوار آدرس و عنوان پنجره کنترل پنل (جدید)"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        if title:
            self.master.title(f"کنترل پنل - {title}")
        else:
            self.master.title("کنترل پنل مرورگر")


if __name__ == '__main__':
    root = tk.Tk()
    app = Browser(root)
    webview.start()
