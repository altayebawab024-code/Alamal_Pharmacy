import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, colorchooser
from datetime import datetime, timedelta
import json
import os
import sqlite3
from PIL import Image, ImageTk
import barcode
from barcode.writer import ImageWriter
import webbrowser
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import tempfile
import hashlib

# ---------------------------- إعدادات اللغة ----------------------------
class Translation:
    translations = {
        'ar': {
            'app_title': 'نظام إدارة الصيدلية',
            'login': 'تسجيل الدخول',
            'username': 'اسم المستخدم',
            'password': 'كلمة السر',
            'login_btn': 'دخول',
            'logout': 'خروج',
            'back': 'رجوع',
            'save': 'حفظ',
            'delete': 'حذف',
            'search': 'بحث',
            'add': 'إضافة',
            'edit': 'تعديل',
            'cancel': 'إلغاء',
            'welcome': 'مرحباً',
            'error': 'خطأ',
            'success': 'تم بنجاح',
            'warning': 'تحذير',
            'confirm': 'تأكيد',
            'yes': 'نعم',
            'no': 'لا',
            'customers': 'العملاء',
            'medicines': 'الأدوية',
            'invoices': 'الفواتير',
            'reports': 'التقارير',
            'expiry': 'صلاحية الأدوية',
            'suppliers': 'الموردين',
            'settings': 'الإعدادات',
            'barcode': 'الباركود',
            'pos': 'نقطة البيع',
            'cashbox': 'الصندوق المالي',
            'customer_management': 'إدارة العملاء',
            'customer_name': 'الاسم',
            'customer_phone': 'الهاتف',
            'customer_address': 'العنوان',
            'customer_points': 'نقاط الولاء',
            'add_customer': 'إضافة عميل',
            'delete_customer': 'حذف عميل',
            'medicine_management': 'إدارة الأدوية',
            'medicine_code': 'الكود',
            'medicine_name': 'اسم الدواء',
            'medicine_category': 'التصنيف',
            'medicine_expiry': 'تاريخ الصلاحية',
            'medicine_quantity': 'الكمية',
            'medicine_price': 'السعر',
            'medicine_supplier': 'المورد',
            'add_medicine': 'إضافة دواء',
            'edit_medicine': 'تعديل دواء',
            'delete_medicine': 'حذف دواء',
            'invoice_management': 'إدارة الفواتير',
            'invoice_no': 'رقم الفاتورة',
            'invoice_date': 'التاريخ',
            'invoice_customer': 'العميل',
            'invoice_total': 'المجموع',
            'print_invoice': 'طباعة الفاتورة',
            'statistics': 'الإحصائيات',
            'total_customers': 'إجمالي العملاء',
            'total_medicines': 'إجمالي الأدوية',
            'total_invoices': 'إجمالي الفواتير',
            'total_sales': 'إجمالي المبيعات',
            'low_stock': 'أدوية منخفضة الكمية',
            'expired_medicines': 'أدوية منتهية الصلاحية',
            'pos_title': 'نقطة البيع',
            'cart': 'سلة المشتريات',
            'add_to_cart': 'إضافة للسلة',
            'remove_from_cart': 'إزالة من السلة',
            'total': 'الإجمالي',
            'payment': 'الدفع',
            'cash': 'نقدي',
            'card': 'بطاقة',
            'change': 'الباقي',
            'cashbox_title': 'الصندوق المالي',
            'opening_balance': 'رصيد الافتتاح',
            'closing_balance': 'رصيد الإغلاق',
            'cash_in': 'إيداع',
            'cash_out': 'سحب',
            'transactions': 'المعاملات',
            'background': 'الخلفية',
            'change_background': 'تغيير الخلفية',
            'reset_background': 'إعادة تعيين الخلفية',
            'currency': 'العملة',
            'currency_symbol': 'رمز العملة',
            'generate_barcode': 'إنشاء باركود',
            'add_supplier': 'إضافة مورد',
            'delete_supplier': 'حذف مورد',
            'supplier_name': 'اسم المورد',
            'supplier_phone': 'هاتف المورد',
            'supplier_address': 'عنوان المورد',
            'contact_person': 'جهة الاتصال',
            'user_management': 'إدارة المستخدمين',
            'add_user': 'إضافة مستخدم',
            'edit_user': 'تعديل مستخدم',
            'delete_user': 'حذف مستخدم',
            'change_password': 'تغيير كلمة السر',
            'username_login': 'اسم المستخدم للدخول',
            'role': 'الصلاحية',
            'manager': 'مدير',
            'cashier': 'موظف مبيعات',
            'customer_user': 'عميل',
            'add_customer_with_login': 'إضافة عميل مع صلاحيات دخول',
            'system_name': 'اسم الصيدلية',
            'address': 'العنوان',
            'phone': 'الهاتف',
            'tax_rate': 'نسبة الضريبة',
            'primary_color': 'اللون الأساسي',
            'pharmacy_info': 'معلومات الصيدلية',
            'good_morning': '🌅 صباح الخير',
            'good_evening': '🌙 مساء الخير',
            'good_afternoon': '☀️ مساء الخير',
        },
        'en': {
            'app_title': 'Pharmacy Management System',
            'login': 'Login',
            'username': 'Username',
            'password': 'Password',
            'login_btn': 'Login',
            'logout': 'Logout',
            'back': 'Back',
            'save': 'Save',
            'delete': 'Delete',
            'search': 'Search',
            'add': 'Add',
            'edit': 'Edit',
            'cancel': 'Cancel',
            'welcome': 'Welcome',
            'error': 'Error',
            'success': 'Success',
            'warning': 'Warning',
            'confirm': 'Confirm',
            'yes': 'Yes',
            'no': 'No',
            'customers': 'Customers',
            'medicines': 'Medicines',
            'invoices': 'Invoices',
            'reports': 'Reports',
            'expiry': 'Expiry Alerts',
            'suppliers': 'Suppliers',
            'settings': 'Settings',
            'barcode': 'Barcode',
            'pos': 'POS',
            'cashbox': 'Cash Box',
            'customer_management': 'Customer Management',
            'customer_name': 'Name',
            'customer_phone': 'Phone',
            'customer_address': 'Address',
            'customer_points': 'Loyalty Points',
            'add_customer': 'Add Customer',
            'delete_customer': 'Delete Customer',
            'medicine_management': 'Medicine Management',
            'medicine_code': 'Code',
            'medicine_name': 'Medicine Name',
            'medicine_category': 'Category',
            'medicine_expiry': 'Expiry Date',
            'medicine_quantity': 'Quantity',
            'medicine_price': 'Price',
            'medicine_supplier': 'Supplier',
            'add_medicine': 'Add Medicine',
            'edit_medicine': 'Edit Medicine',
            'delete_medicine': 'Delete Medicine',
            'invoice_management': 'Invoice Management',
            'invoice_no': 'Invoice No',
            'invoice_date': 'Date',
            'invoice_customer': 'Customer',
            'invoice_total': 'Total',
            'print_invoice': 'Print Invoice',
            'statistics': 'Statistics',
            'total_customers': 'Total Customers',
            'total_medicines': 'Total Medicines',
            'total_invoices': 'Total Invoices',
            'total_sales': 'Total Sales',
            'low_stock': 'Low Stock Items',
            'expired_medicines': 'Expired Medicines',
            'pos_title': 'Point of Sale',
            'cart': 'Shopping Cart',
            'add_to_cart': 'Add to Cart',
            'remove_from_cart': 'Remove from Cart',
            'total': 'Total',
            'payment': 'Payment',
            'cash': 'Cash',
            'card': 'Card',
            'change': 'Change',
            'cashbox_title': 'Cash Box',
            'opening_balance': 'Opening Balance',
            'closing_balance': 'Closing Balance',
            'cash_in': 'Cash In',
            'cash_out': 'Cash Out',
            'transactions': 'Transactions',
            'background': 'Background',
            'change_background': 'Change Background',
            'reset_background': 'Reset Background',
            'currency': 'Currency',
            'currency_symbol': 'Currency Symbol',
            'generate_barcode': 'Generate Barcode',
            'add_supplier': 'Add Supplier',
            'delete_supplier': 'Delete Supplier',
            'supplier_name': 'Supplier Name',
            'supplier_phone': 'Supplier Phone',
            'supplier_address': 'Supplier Address',
            'contact_person': 'Contact Person',
            'user_management': 'User Management',
            'add_user': 'Add User',
            'edit_user': 'Edit User',
            'delete_user': 'Delete User',
            'change_password': 'Change Password',
            'username_login': 'Login Username',
            'role': 'Role',
            'manager': 'Manager',
            'cashier': 'Cashier',
            'customer_user': 'Customer',
            'add_customer_with_login': 'Add Customer with Login',
            'system_name': 'Pharmacy Name',
            'address': 'Address',
            'phone': 'Phone',
            'tax_rate': 'Tax Rate',
            'primary_color': 'Primary Color',
            'pharmacy_info': 'Pharmacy Info',
            'good_morning': '🌅 Good Morning',
            'good_evening': '🌙 Good Evening',
            'good_afternoon': '☀️ Good Afternoon',
        }
    }
    
    def __init__(self):
        self.current_lang = 'ar'
        self.load_language()
    
    def load_language(self):
        if os.path.exists("language.json"):
            with open("language.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.current_lang = data.get("language", "ar")
    
    def save_language(self):
        with open("language.json", "w", encoding="utf-8") as f:
            json.dump({"language": self.current_lang}, f)
    
    def get(self, key):
        return self.translations[self.current_lang].get(key, key)
    
    def toggle(self):
        self.current_lang = 'en' if self.current_lang == 'ar' else 'ar'
        self.save_language()

trans = Translation()

# ---------------------------- قاعدة بيانات SQLite ----------------------------
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT,
                customer_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                points INTEGER DEFAULT 0,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                barcode TEXT,
                name TEXT NOT NULL,
                category TEXT,
                expiry_date DATE,
                quantity INTEGER DEFAULT 0,
                price REAL DEFAULT 0,
                supplier TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                customer_name TEXT,
                total_amount REAL,
                discount REAL DEFAULT 0,
                tax REAL DEFAULT 0,
                final_amount REAL,
                payment_method TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                medicine_id INTEGER,
                medicine_name TEXT,
                quantity INTEGER,
                price REAL,
                total REAL,
                FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                contact_person TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cash_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cashbox_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opening_balance REAL DEFAULT 0,
                closing_balance REAL DEFAULT 0,
                date TEXT UNIQUE,
                is_closed INTEGER DEFAULT 0
            )
        ''')
        
        try:
            self.cursor.execute("ALTER TABLE customers ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass
        
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN customer_id INTEGER")
        except sqlite3.OperationalError:
            pass
        
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            admin_pass = hashlib.sha256('pharmacy2024'.encode()).hexdigest()
            self.cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                              ('manager', admin_pass, 'manager', 'المدير'))
            user_pass = hashlib.sha256('sales123'.encode()).hexdigest()
            self.cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                              ('sales', user_pass, 'cashier', 'موظف مبيعات'))
        
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        if self.cursor.fetchone()[0] == 0:
            sample_customers = [
                ('أحمد محمد', '0123456789', 'الخرطوم - بحري', 100, None),
                ('سارة علي', '0112345678', 'أم درمان - السوق الشعبي', 50, None),
                ('محمد عبدالله', '0152345678', 'الخرطوم - الرياض', 75, None),
                ('فاطمة حسن', '0123456790', 'بورتسودان - وسط البلد', 30, None),
                ('عمر إبراهيم', '0112345689', 'كسلا - حي النصر', 45, None),
            ]
            for customer in sample_customers:
                self.cursor.execute("INSERT INTO customers (name, phone, address, points, user_id) VALUES (?, ?, ?, ?, ?)", customer)
        
        self.cursor.execute("SELECT COUNT(*) FROM medicines")
        if self.cursor.fetchone()[0] == 0:
            sample_medicines = [
                ('MED001', '1234567890123', 'باراسيتامول', 'مسكنات', '2025-12-31', 100, 5.0, 'شركة الأدوية العربية'),
                ('MED002', '1234567890124', 'إيبوبروفين', 'مسكنات', '2025-10-31', 50, 8.0, 'شركة الأدوية العربية'),
                ('MED003', '1234567890125', 'أموكسيسيلين', 'مضادات حيوية', '2024-12-31', 30, 15.0, 'شركة العالمية للأدوية'),
                ('MED004', '1234567890126', 'فيتامين سي', 'فيتامينات', '2026-01-31', 200, 12.0, 'فيتاهيلث'),
                ('MED005', '1234567890127', 'باراسيتامول أطفال', 'مسكنات', '2024-11-15', 5, 3.5, 'شركة الأدوية العربية'),
                ('MED006', '1234567890128', 'مضاد حيوي', 'مضادات حيوية', '2024-10-01', 20, 25.0, 'شركة العالمية'),
            ]
            for medicine in sample_medicines:
                self.cursor.execute("INSERT INTO medicines (code, barcode, name, category, expiry_date, quantity, price, supplier) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", medicine)
        
        self.cursor.execute("SELECT COUNT(*) FROM suppliers")
        if self.cursor.fetchone()[0] == 0:
            sample_suppliers = [
                ('شركة الأدوية العربية', '0123456789', 'الخرطوم - الخرطوم شرق', 'أحمد محمود'),
                ('شركة العالمية للأدوية', '0112345678', 'أم درمان - السوق الكبير', 'سامي ربيع'),
                ('مستودعات الدواء', '0152345678', 'الخرطوم - شارع النيل', 'محمد علي'),
                ('شركة سودافارما', '0123456791', 'بورتسودان - المنطقة الصناعية', 'ياسر خليل'),
            ]
            for supplier in sample_suppliers:
                self.cursor.execute("INSERT INTO suppliers (name, phone, address, contact_person) VALUES (?, ?, ?, ?)", supplier)
        
        self.conn.commit()
    
    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor
    
    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()

db = Database()

# ---------------------------- إعدادات التطبيق ----------------------------
class AppSettings:
    def __init__(self):
        self.theme = "light"
        self.pharmacy_name = "صيدلية الأمل"
        self.pharmacy_address = "الخرطوم - السودان"
        self.pharmacy_phone = "0123456789"
        self.tax_rate = 0.14
        self.primary_color = "#90EE90"
        self.secondary_color = "#98FB98"
        self.background_image = None
        self.background_photo = None
        self.currency = "جنيه"
        self.currency_symbol = "ج.س"
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists("app_settings.json"):
            with open("app_settings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.theme = data.get("theme", "light")
                self.pharmacy_name = data.get("pharmacy_name", "صيدلية الأمل")
                self.pharmacy_address = data.get("pharmacy_address", "الخرطوم - السودان")
                self.pharmacy_phone = data.get("pharmacy_phone", "0123456789")
                self.tax_rate = data.get("tax_rate", 0.14)
                self.primary_color = data.get("primary_color", "#90EE90")
                self.secondary_color = data.get("secondary_color", "#98FB98")
                self.background_image = data.get("background_image", None)
                self.currency = data.get("currency", "جنيه")
                self.currency_symbol = data.get("currency_symbol", "ج.س")
    
    def save_settings(self):
        with open("app_settings.json", "w", encoding="utf-8") as f:
            json.dump({
                "theme": self.theme,
                "pharmacy_name": self.pharmacy_name,
                "pharmacy_address": self.pharmacy_address,
                "pharmacy_phone": self.pharmacy_phone,
                "tax_rate": self.tax_rate,
                "primary_color": self.primary_color,
                "secondary_color": self.secondary_color,
                "background_image": self.background_image,
                "currency": self.currency,
                "currency_symbol": self.currency_symbol
            }, f, ensure_ascii=False)

settings = AppSettings()

# ---------------------------- فئة النافذة الرئيسية ----------------------------
class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{settings.pharmacy_name} - {trans.get('app_title')}")
        self.root.geometry("1200x700")
        self.current_user = None
        self.current_user_id = None
        self.current_user_role = None
        self.current_customer_id = None
        self.background_label = None
        self.cart_items = []
        self.current_screen = None
        self.current_frame = None
        self.dashboard_buttons = []
        self.show_login()
    
    def get_greeting(self):
        now = datetime.now()
        hour = now.hour
        if 5 <= hour < 12:
            return trans.get('good_morning')
        elif 12 <= hour < 17:
            return trans.get('good_afternoon')
        else:
            return trans.get('good_evening')
    
    def get_text(self, key):
        return trans.get(key)
    
    def format_currency(self, amount):
        return f"{amount:.2f} {settings.currency_symbol}"
    
    def get_bg_color(self):
        if settings.theme == "dark":
            return "#1e1e1e"
        return "#ffffff"
    
    def get_fg_color(self):
        if settings.theme == "dark":
            return "white"
        return "black"
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def set_background(self, frame):
        if settings.background_image and os.path.exists(settings.background_image):
            try:
                img = Image.open(settings.background_image)
                frame.update_idletasks()
                frame_width = frame.winfo_width() if frame.winfo_width() > 100 else self.root.winfo_width()
                frame_height = frame.winfo_height() if frame.winfo_height() > 100 else self.root.winfo_height()
                img = img.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
                bg_image = ImageTk.PhotoImage(img)
                if hasattr(frame, 'bg_label') and frame.bg_label:
                    frame.bg_label.destroy()
                frame.bg_label = tk.Label(frame, image=bg_image)
                frame.bg_label.image = bg_image
                frame.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                frame.bg_label.lower()
                frame.configure(bg='')
                return True
            except Exception as e:
                print(f"خطأ: {e}")
                return False
        else:
            frame.configure(bg=self.get_bg_color())
            return False
    
    def add_back_button(self, parent, command):
        back_btn = tk.Button(parent, text=f"🔙 {trans.get('back')}", command=command,
                            bg="#95a5a6", fg="white", font=("Arial", 10), padx=15, pady=3)
        back_btn.pack(pady=5)
        return back_btn
    
    def toggle_language(self):
        trans.toggle()
        self.root.title(f"{settings.pharmacy_name} - {trans.get('app_title')}")
        if self.current_screen and self.current_frame:
            self.refresh_current_screen()
        else:
            self.show_main_dashboard()
    
    def refresh_current_screen(self):
        if self.current_screen == "login":
            self.refresh_login_screen()
        elif self.current_screen == "dashboard":
            self.refresh_dashboard_texts()
        elif self.current_screen == "customers":
            self.refresh_customers_screen()
        elif self.current_screen == "medicines":
            self.refresh_medicines_screen()
        elif self.current_screen == "suppliers":
            self.refresh_suppliers_screen()
        elif self.current_screen == "invoices":
            self.refresh_invoices_screen()
        elif self.current_screen == "pos":
            self.refresh_pos_screen()
        elif self.current_screen == "reports":
            self.refresh_reports_screen()
        elif self.current_screen == "expiry":
            self.refresh_expiry_screen()
        elif self.current_screen == "barcode":
            self.refresh_barcode_screen()
        elif self.current_screen == "cashbox":
            self.refresh_cashbox_screen()
        elif self.current_screen == "settings":
            self.refresh_settings_screen()
        elif self.current_screen == "advanced_dashboard":
            self.show_advanced_dashboard()
    
    # ---------------------------- شاشة الدخول ----------------------------
    def show_login(self):
        self.current_screen = "login"
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        self.set_background(self.current_frame)
        
        login_frame = tk.Frame(self.current_frame, bg="white", relief="ridge", bd=2)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        login_frame.logo_label = tk.Label(login_frame, text="🏥", font=("Arial", 48), bg="white", fg=settings.primary_color)
        login_frame.logo_label.pack(pady=15)
        
        login_frame.title_label = tk.Label(login_frame, text=settings.pharmacy_name, font=("Arial", 22, "bold"), bg="white")
        login_frame.title_label.pack(pady=8)
        
        login_frame.subtitle_label = tk.Label(login_frame, text=trans.get('app_title'), font=("Arial", 14), bg="white")
        login_frame.subtitle_label.pack(pady=5)
        
        tk.Label(login_frame, text=f"👤 {trans.get('username')}:", font=("Arial", 11), bg="white").pack(pady=3)
        entry_user = tk.Entry(login_frame, font=("Arial", 11), width=25)
        entry_user.pack(pady=3)
        
        tk.Label(login_frame, text=f"🔒 {trans.get('password')}:", font=("Arial", 11), bg="white").pack(pady=3)
        entry_pass = tk.Entry(login_frame, show="*", font=("Arial", 11), width=25)
        entry_pass.pack(pady=3)
        
        def do_login():
            user = entry_user.get()
            pwd = self.hash_password(entry_pass.get())
            result = db.fetch_one("SELECT id, username, role, customer_id FROM users WHERE username = ? AND password = ?", (user, pwd))
            if result:
                self.current_user_id, self.current_user, self.current_user_role, self.current_customer_id = result
                self.show_main_dashboard()
                return
            messagebox.showerror(trans.get('error'), "اسم المستخدم أو كلمة السر غير صحيحة")
        
        login_frame.login_btn = tk.Button(login_frame, text=trans.get('login_btn'), command=do_login, 
                 bg=settings.primary_color, fg="white", font=("Arial", 12), width=12, height=1)
        login_frame.login_btn.pack(pady=15)
        
        btn_frame = tk.Frame(login_frame, bg="white")
        btn_frame.pack(pady=8)
        login_frame.lang_btn = tk.Button(btn_frame, text="🌐 عربي/English", command=self.toggle_language,
                 bg="#95a5a6", fg="white", font=("Arial", 9))
        login_frame.lang_btn.pack(side="left", padx=5)
    
    def refresh_login_screen(self):
        if self.current_frame:
            for child in self.current_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    if hasattr(child, 'subtitle_label'):
                        child.subtitle_label.config(text=trans.get('app_title'))
                    if hasattr(child, 'login_btn'):
                        child.login_btn.config(text=trans.get('login_btn'))
    
    # ---------------------------- الشاشة الرئيسية ----------------------------
    def show_main_dashboard(self):
        self.current_screen = "dashboard"
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        self.set_background(self.current_frame)
        
        # الإطار العلوي (شريط العنوان)
        top_frame = tk.Frame(self.current_frame, bg=settings.primary_color, height=50)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)
        
        # ========== القسم الأيسر من الشريط العلوي (الرسالة الترحيبية + اسم الصيدلية + اسم المستخدم) ==========
        left_info_frame = tk.Frame(top_frame, bg=settings.primary_color)
        left_info_frame.pack(side="left", padx=10, pady=5)
        
        # الرسالة الترحيبية (صباح الخير / مساء الخير)
        greeting_text = self.get_greeting()
        greeting_label = tk.Label(left_info_frame, text=greeting_text, font=("Arial", 11, "bold"),
                                   fg="white", bg=settings.primary_color)
        greeting_label.pack(anchor="w")
        
        # تحديث الرسالة الترحيبية كل دقيقة
        def update_greeting():
            greeting_label.config(text=self.get_greeting())
            self.root.after(60000, update_greeting)
        self.root.after(60000, update_greeting)
        
        # اسم الصيدلية واسم المستخدم في نفس السطر
        info_frame = tk.Frame(left_info_frame, bg=settings.primary_color)
        info_frame.pack(anchor="w")
        
        pharmacy_label = tk.Label(info_frame, text=f"🏥 {settings.pharmacy_name}", 
                                   font=("Arial", 9), fg="white", bg=settings.primary_color)
        pharmacy_label.pack(side="left", padx=(0, 10))
        
        role_name = "مدير" if self.current_user_role == "manager" else "موظف مبيعات" if self.current_user_role == "cashier" else "عميل"
        user_label = tk.Label(info_frame, text=f"👤 {self.current_user} - {role_name}", 
                               font=("Arial", 9), fg="white", bg=settings.primary_color)
        user_label.pack(side="left")
        
        # الأزرار الجانبية
        btn_frame = tk.Frame(top_frame, bg=settings.primary_color)
        btn_frame.pack(side="right", padx=10)
        
        theme_btn = tk.Button(btn_frame, text="🌙" if settings.theme == "light" else "☀️", 
                              command=self.toggle_theme, font=("Arial", 10), bg="#34495e", fg="white")
        theme_btn.pack(side="left", padx=3)
        
        lang_btn = tk.Button(btn_frame, text="🌐", command=self.toggle_language, 
                             font=("Arial", 10), bg="#34495e", fg="white")
        lang_btn.pack(side="left", padx=3)
        
        bg_btn = tk.Button(btn_frame, text="🎨", command=self.change_background, 
                           font=("Arial", 10), bg="#e67e22", fg="white")
        bg_btn.pack(side="left", padx=3)
        
        logout_btn = tk.Button(btn_frame, text=f"🚪 {trans.get('logout')}", command=self.logout, 
                               bg="#e74c3c", fg="white", font=("Arial", 9))
        logout_btn.pack(side="left", padx=3)
        
        # ==================== إطار المحتوى الرئيسي ====================
        main_container = tk.Frame(self.current_frame)
        main_container.pack(fill="both", expand=True)
        self.set_background(main_container)
        
        # الجانب الأيمن - شريط الأزرار العمودي
        right_sidebar = tk.Frame(main_container, bg=settings.primary_color, width=240)
        right_sidebar.pack(side="right", fill="y")
        right_sidebar.pack_propagate(False)
        
        sidebar_title = tk.Label(right_sidebar, text="📋 القائمة الرئيسية", font=("Arial", 12, "bold"),
                                 bg=settings.primary_color, fg="white")
        sidebar_title.pack(pady=8)
        
        separator = tk.Frame(right_sidebar, bg="white", height=2)
        separator.pack(fill="x", padx=10, pady=3)
        
        self.dashboard_buttons = []
        
        if self.current_user_role == "manager":
            buttons_list = [
                ("📊", "Dashboard متقدم", self.show_advanced_dashboard),
                ("👥", trans.get('customers'), self.show_customers),
                ("💊", trans.get('medicines'), self.show_medicines),
                ("📄", trans.get('invoices'), self.show_invoices),
                ("💰", trans.get('pos'), self.show_pos),
                ("📊", trans.get('reports'), self.show_reports),
                ("⚠️", trans.get('expiry'), self.show_expiry),
                ("🏭", trans.get('suppliers'), self.show_suppliers),
                ("📱", trans.get('barcode'), self.show_barcode_scanner),
                ("💰", trans.get('cashbox'), self.show_cashbox),
                ("⚙️", trans.get('settings'), self.show_settings),
            ]
        elif self.current_user_role == "cashier":
            buttons_list = [
                ("👥", trans.get('customers'), self.show_customers),
                ("💊", trans.get('medicines'), self.show_medicines),
                ("💰", trans.get('pos'), self.show_pos),
                ("📄", trans.get('invoices'), self.show_invoices),
                ("⚠️", trans.get('expiry'), self.show_expiry),
                ("📱", trans.get('barcode'), self.show_barcode_scanner),
            ]
        else:
            buttons_list = [
                ("💊", trans.get('medicines'), self.show_medicines),
                ("📄", trans.get('invoices'), self.show_invoices),
                ("⭐", "نقاط الولاء", self.show_loyalty_points),
            ]
        
        for icon, text, cmd in buttons_list:
            btn = tk.Button(right_sidebar, text=f"{icon}  {text}", command=cmd,
                           bg=self.get_bg_color(), fg=self.get_fg_color(),
                           font=("Arial", 10), 
                           relief="flat", padx=10, pady=8,
                           anchor="w",
                           width=22)
            btn.pack(pady=4, padx=10, fill="x")
            self.dashboard_buttons.append(btn)
        
        spacer = tk.Frame(right_sidebar, bg=settings.primary_color, height=20)
        spacer.pack(fill="x", pady=10)
        
        # ==================== الجانب الأيسر - مساحة فارغة تماماً (بدون أي عناصر) ====================
        left_content = tk.Frame(main_container, bg=self.get_bg_color())
        left_content.pack(side="left", fill="both", expand=True)
    
    def show_loyalty_points(self):
        if self.current_customer_id:
            customer = db.fetch_one("SELECT name, points FROM customers WHERE id = ?", (self.current_customer_id,))
            if customer:
                messagebox.showinfo("نقاط الولاء", f"العميل: {customer[0]}\nنقاط الولاء: {customer[1]}\n\nكل 100 نقطة = خصم 5%")
            else:
                messagebox.showinfo("نقاط الولاء", "لم يتم العثور على بيانات العميل")
    
    def refresh_dashboard_texts(self):
        if self.current_frame:
            for child in self.current_frame.winfo_children():
                if isinstance(child, tk.Frame) and child.cget("bg") == settings.primary_color:
                    role_name = "مدير" if self.current_user_role == "manager" else "موظف مبيعات" if self.current_user_role == "cashier" else "عميل"
                    pass
            
            if self.current_user_role == "manager":
                new_texts = [
                    "Dashboard متقدم", trans.get('customers'), trans.get('medicines'), trans.get('invoices'),
                    trans.get('pos'), trans.get('reports'), trans.get('expiry'),
                    trans.get('suppliers'), trans.get('barcode'), trans.get('cashbox'),
                    trans.get('settings')
                ]
                icons = ["📊", "👥", "💊", "📄", "💰", "📊", "⚠️", "🏭", "📱", "💰", "⚙️"]
            elif self.current_user_role == "cashier":
                new_texts = [
                    trans.get('customers'), trans.get('medicines'), trans.get('pos'),
                    trans.get('invoices'), trans.get('expiry'), trans.get('barcode')
                ]
                icons = ["👥", "💊", "💰", "📄", "⚠️", "📱"]
            else:
                new_texts = [
                    trans.get('medicines'), trans.get('invoices'), "نقاط الولاء"
                ]
                icons = ["💊", "📄", "⭐"]
            
            for i, btn in enumerate(self.dashboard_buttons):
                if i < len(new_texts):
                    btn.config(text=f"{icons[i]}  {new_texts[i]}")
    
    # ---------------------------- العملاء ----------------------------
    def show_customers(self):
        self.current_screen = "customers"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.set_background(self.current_frame)
        
        self.customers_title = tk.Label(self.current_frame, text=f"👥 {trans.get('customer_management')}", 
                                        font=("Arial", 16, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.customers_title.pack(pady=5)
        
        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(fill="x", pady=3)
        self.set_background(btn_frame)
        
        self.add_customer_btn = tk.Button(btn_frame, text=f"➕ {trans.get('add_customer')}", 
                                         command=self.add_customer_dialog, bg=settings.secondary_color, 
                                         fg="white", font=("Arial", 10))
        self.add_customer_btn.pack(side="left", padx=3)
        
        self.add_customer_with_login_btn = tk.Button(btn_frame, text=f"🔐 {trans.get('add_customer_with_login')}", 
                                                    command=self.add_customer_with_login, bg="#3498db", 
                                                    fg="white", font=("Arial", 10))
        self.add_customer_with_login_btn.pack(side="left", padx=3)
        
        self.delete_customer_btn = tk.Button(btn_frame, text=f"🗑️ {trans.get('delete_customer')}", 
                                            command=self.delete_customer, bg="#e74c3c", fg="white", font=("Arial", 10))
        self.delete_customer_btn.pack(side="left", padx=3)
        
        columns = ("id", "name", "phone", "address", "points")
        self.customer_tree = ttk.Treeview(self.current_frame, columns=columns, show="headings", height=15)
        self.update_customer_headings()
        self.customer_tree.pack(fill="both", expand=True, pady=5)
        
        self.refresh_customer_list()
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def update_customer_headings(self):
        headings = ["ID", trans.get('customer_name'), trans.get('customer_phone'), 
                   trans.get('customer_address'), trans.get('customer_points')]
        columns = ("id", "name", "phone", "address", "points")
        for col, head in zip(columns, headings):
            self.customer_tree.heading(col, text=head)
            self.customer_tree.column(col, width=100)
    
    def refresh_customer_list(self):
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        customers = db.fetch_all("SELECT id, name, phone, address, points FROM customers ORDER BY id")
        for customer in customers:
            self.customer_tree.insert("", "end", values=customer)
    
    def refresh_customers_screen(self):
        if hasattr(self, 'customers_title'):
            self.customers_title.config(text=f"👥 {trans.get('customer_management')}")
        if hasattr(self, 'add_customer_btn'):
            self.add_customer_btn.config(text=f"➕ {trans.get('add_customer')}")
        if hasattr(self, 'add_customer_with_login_btn'):
            self.add_customer_with_login_btn.config(text=f"🔐 {trans.get('add_customer_with_login')}")
        if hasattr(self, 'delete_customer_btn'):
            self.delete_customer_btn.config(text=f"🗑️ {trans.get('delete_customer')}")
        if hasattr(self, 'customer_tree'):
            self.update_customer_headings()
            self.refresh_customer_list()
    
    def add_customer_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('add_customer'))
        dialog.geometry("350x300")
        dialog.grab_set()
        
        tk.Label(dialog, text=f"{trans.get('customer_name')}:", font=("Arial", 11)).pack(pady=3)
        name_entry = tk.Entry(dialog, width=25, font=("Arial", 10))
        name_entry.pack()
        tk.Label(dialog, text=f"{trans.get('customer_phone')}:", font=("Arial", 11)).pack(pady=3)
        phone_entry = tk.Entry(dialog, width=25, font=("Arial", 10))
        phone_entry.pack()
        tk.Label(dialog, text=f"{trans.get('customer_address')}:", font=("Arial", 11)).pack(pady=3)
        address_entry = tk.Entry(dialog, width=25, font=("Arial", 10))
        address_entry.pack()
        
        def save():
            if name_entry.get():
                db.execute_query("INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)",
                               (name_entry.get(), phone_entry.get(), address_entry.get()))
                self.refresh_customer_list()
                dialog.destroy()
                messagebox.showinfo(trans.get('success'), "تمت الإضافة بنجاح")
        
        tk.Button(dialog, text=trans.get('save'), command=save, bg=settings.secondary_color, fg="white", font=("Arial", 11)).pack(pady=15)
    
    def add_customer_with_login(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('add_customer_with_login'))
        dialog.geometry("380x420")
        dialog.grab_set()
        
        tk.Label(dialog, text=f"{trans.get('customer_name')}:", font=("Arial", 11)).pack(pady=3)
        name_entry = tk.Entry(dialog, width=28, font=("Arial", 10))
        name_entry.pack()
        
        tk.Label(dialog, text=f"{trans.get('customer_phone')}:", font=("Arial", 11)).pack(pady=3)
        phone_entry = tk.Entry(dialog, width=28, font=("Arial", 10))
        phone_entry.pack()
        
        tk.Label(dialog, text=f"{trans.get('customer_address')}:", font=("Arial", 11)).pack(pady=3)
        address_entry = tk.Entry(dialog, width=28, font=("Arial", 10))
        address_entry.pack()
        
        tk.Label(dialog, text=f"{trans.get('username_login')}:", font=("Arial", 11)).pack(pady=3)
        username_entry = tk.Entry(dialog, width=28, font=("Arial", 10))
        username_entry.pack()
        
        tk.Label(dialog, text=f"{trans.get('password')}:", font=("Arial", 11)).pack(pady=3)
        password_entry = tk.Entry(dialog, width=28, font=("Arial", 10), show="*")
        password_entry.pack()
        
        def save():
            if name_entry.get() and username_entry.get() and password_entry.get():
                existing = db.fetch_one("SELECT id FROM users WHERE username = ?", (username_entry.get(),))
                if existing:
                    messagebox.showerror(trans.get('error'), "اسم المستخدم موجود بالفعل")
                    return
                
                db.execute_query("INSERT INTO customers (name, phone, address, points) VALUES (?, ?, ?, ?)",
                               (name_entry.get(), phone_entry.get(), address_entry.get(), 0))
                customer_id = db.cursor.lastrowid
                
                hashed_pass = self.hash_password(password_entry.get())
                db.execute_query("INSERT INTO users (username, password, role, full_name, customer_id) VALUES (?, ?, ?, ?, ?)",
                               (username_entry.get(), hashed_pass, 'customer', name_entry.get(), customer_id))
                
                db.execute_query("UPDATE customers SET user_id = ? WHERE id = ?", (db.cursor.lastrowid, customer_id))
                
                self.refresh_customer_list()
                dialog.destroy()
                messagebox.showinfo(trans.get('success'), f"تمت إضافة العميل {name_entry.get()} مع صلاحيات دخول")
            else:
                messagebox.showwarning(trans.get('warning'), "الرجاء إدخال جميع البيانات")
        
        tk.Button(dialog, text=trans.get('save'), command=save, bg=settings.secondary_color, fg="white", font=("Arial", 11)).pack(pady=15)
    
    def delete_customer(self):
        selected = self.customer_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء تحديد عميل")
            return
        if messagebox.askyesno(trans.get('confirm'), "هل أنت متأكد؟"):
            item = self.customer_tree.item(selected[0])
            customer_id = item['values'][0]
            
            user = db.fetch_one("SELECT id FROM users WHERE customer_id = ?", (customer_id,))
            if user:
                db.execute_query("DELETE FROM users WHERE id = ?", (user[0],))
            
            db.execute_query("DELETE FROM customers WHERE id = ?", (customer_id,))
            self.refresh_customer_list()
            messagebox.showinfo(trans.get('success'), "تم الحذف بنجاح")
    
    # ---------------------------- الأدوية ----------------------------
    def show_medicines(self):
        self.current_screen = "medicines"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.set_background(self.current_frame)
        
        self.medicines_title = tk.Label(self.current_frame, text=f"💊 {trans.get('medicine_management')}", 
                                        font=("Arial", 16, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.medicines_title.pack(pady=5)
        
        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(fill="x", pady=3)
        self.set_background(btn_frame)
        
        self.add_medicine_btn = tk.Button(btn_frame, text=f"➕ {trans.get('add_medicine')}", 
                                         command=self.add_medicine_dialog, bg=settings.secondary_color, 
                                         fg="white", font=("Arial", 10))
        self.add_medicine_btn.pack(side="left", padx=3)
        
        self.edit_medicine_btn = tk.Button(btn_frame, text=f"✏️ {trans.get('edit_medicine')}", 
                                          command=self.edit_medicine_dialog, bg="#3498db", 
                                          fg="white", font=("Arial", 10))
        self.edit_medicine_btn.pack(side="left", padx=3)
        
        self.delete_medicine_btn = tk.Button(btn_frame, text=f"🗑️ {trans.get('delete_medicine')}", 
                                            command=self.delete_medicine, bg="#e74c3c", fg="white", font=("Arial", 10))
        self.delete_medicine_btn.pack(side="left", padx=3)
        
        columns = ("id", "code", "name", "category", "expiry_date", "quantity", "price", "supplier")
        self.medicine_tree = ttk.Treeview(self.current_frame, columns=columns, show="headings", height=15)
        self.update_medicine_headings()
        self.medicine_tree.pack(fill="both", expand=True, pady=5)
        
        self.refresh_medicine_list()
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def update_medicine_headings(self):
        headings = ["ID", trans.get('medicine_code'), trans.get('medicine_name'), 
                   trans.get('medicine_category'), trans.get('medicine_expiry'), 
                   trans.get('medicine_quantity'), f"{trans.get('medicine_price')} ({settings.currency_symbol})", 
                   trans.get('medicine_supplier')]
        columns = ("id", "code", "name", "category", "expiry_date", "quantity", "price", "supplier")
        for col, head in zip(columns, headings):
            self.medicine_tree.heading(col, text=head)
            self.medicine_tree.column(col, width=85)
    
    def refresh_medicine_list(self):
        for item in self.medicine_tree.get_children():
            self.medicine_tree.delete(item)
        medicines = db.fetch_all("SELECT id, code, name, category, expiry_date, quantity, price, supplier FROM medicines ORDER BY id")
        for med in medicines:
            tags = []
            if med[5] < 10:
                tags.append('lowstock')
            if med[4] and med[4] <= datetime.now().strftime("%Y-%m-%d"):
                tags.append('expired')
            elif med[4] and med[4] <= (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"):
                tags.append('expiring')
            
            self.medicine_tree.insert("", "end", values=(med[0], med[1], med[2], med[3], med[4], med[5], f"{med[6]:.2f}", med[7]), tags=tags)
        
        self.medicine_tree.tag_configure('lowstock', background='#fff3cd')
        self.medicine_tree.tag_configure('expired', background='#f8d7da')
        self.medicine_tree.tag_configure('expiring', background='#d1ecf1')
    
    def refresh_medicines_screen(self):
        if hasattr(self, 'medicines_title'):
            self.medicines_title.config(text=f"💊 {trans.get('medicine_management')}")
        if hasattr(self, 'add_medicine_btn'):
            self.add_medicine_btn.config(text=f"➕ {trans.get('add_medicine')}")
        if hasattr(self, 'edit_medicine_btn'):
            self.edit_medicine_btn.config(text=f"✏️ {trans.get('edit_medicine')}")
        if hasattr(self, 'delete_medicine_btn'):
            self.delete_medicine_btn.config(text=f"🗑️ {trans.get('delete_medicine')}")
        if hasattr(self, 'medicine_tree'):
            self.update_medicine_headings()
            self.refresh_medicine_list()
    
    def add_medicine_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('add_medicine'))
        dialog.geometry("450x480")
        dialog.grab_set()
        
        fields = [
            (trans.get('medicine_code'), "code"),
            (trans.get('medicine_name'), "name"),
            (trans.get('medicine_category'), "category"),
            (f"{trans.get('medicine_expiry')} (YYYY-MM-DD)", "expiry"),
            (trans.get('medicine_quantity'), "quantity"),
            (trans.get('medicine_price'), "price"),
            (trans.get('medicine_supplier'), "supplier")
        ]
        entries = {}
        
        for label, key in fields:
            tk.Label(dialog, text=f"{label}:", font=("Arial", 11)).pack(pady=3)
            entry = tk.Entry(dialog, width=30, font=("Arial", 10))
            entry.pack()
            entries[key] = entry
        
        def save():
            if entries['name'].get():
                db.execute_query("""
                    INSERT INTO medicines (code, name, category, expiry_date, quantity, price, supplier)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (entries['code'].get(), entries['name'].get(), entries['category'].get(),
                      entries['expiry'].get(), int(entries['quantity'].get() or 0),
                      float(entries['price'].get() or 0), entries['supplier'].get()))
                self.refresh_medicine_list()
                dialog.destroy()
                messagebox.showinfo(trans.get('success'), "تمت الإضافة بنجاح")
        
        tk.Button(dialog, text=trans.get('save'), command=save, bg=settings.secondary_color, fg="white", font=("Arial", 11)).pack(pady=15)
    
    def edit_medicine_dialog(self):
        selected = self.medicine_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء تحديد دواء للتعديل")
            return
        
        item = self.medicine_tree.item(selected[0])
        medicine_id = item['values'][0]
        
        medicine = db.fetch_one("SELECT code, name, category, expiry_date, quantity, price, supplier FROM medicines WHERE id = ?", (medicine_id,))
        if not medicine:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('edit_medicine'))
        dialog.geometry("450x500")
        dialog.grab_set()
        
        fields = [
            (trans.get('medicine_code'), medicine[0]),
            (trans.get('medicine_name'), medicine[1]),
            (trans.get('medicine_category'), medicine[2]),
            (f"{trans.get('medicine_expiry')} (YYYY-MM-DD)", medicine[3]),
            (trans.get('medicine_quantity'), medicine[4]),
            (trans.get('medicine_price'), medicine[5]),
            (trans.get('medicine_supplier'), medicine[6])
        ]
        entries = {}
        
        for label, value in fields:
            tk.Label(dialog, text=f"{label}:", font=("Arial", 11)).pack(pady=3)
            entry = tk.Entry(dialog, width=30, font=("Arial", 10))
            entry.insert(0, str(value) if value else "")
            entry.pack()
            entries[label.split()[0]] = entry
        
        def save():
            db.execute_query("""
                UPDATE medicines 
                SET code = ?, name = ?, category = ?, expiry_date = ?, quantity = ?, price = ?, supplier = ?
                WHERE id = ?
            """, (entries[trans.get('medicine_code').split()[0]].get(), 
                  entries[trans.get('medicine_name').split()[0]].get(),
                  entries[trans.get('medicine_category').split()[0]].get(),
                  entries[trans.get('medicine_expiry').split()[0]].get(),
                  int(entries[trans.get('medicine_quantity').split()[0]].get() or 0),
                  float(entries[trans.get('medicine_price').split()[0]].get() or 0),
                  entries[trans.get('medicine_supplier').split()[0]].get(),
                  medicine_id))
            self.refresh_medicine_list()
            dialog.destroy()
            messagebox.showinfo(trans.get('success'), "تم تعديل الدواء بنجاح")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text=trans.get('save'), command=save, bg=settings.secondary_color, fg="white", font=("Arial", 11), width=8).pack(side="left", padx=8)
        tk.Button(btn_frame, text=trans.get('cancel'), command=dialog.destroy, bg="#95a5a6", fg="white", font=("Arial", 11), width=8).pack(side="left", padx=8)
    
    def delete_medicine(self):
        selected = self.medicine_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء تحديد دواء")
            return
        if messagebox.askyesno(trans.get('confirm'), "هل أنت متأكد؟"):
            item = self.medicine_tree.item(selected[0])
            db.execute_query("DELETE FROM medicines WHERE id = ?", (item['values'][0],))
            self.refresh_medicine_list()
            messagebox.showinfo(trans.get('success'), "تم الحذف بنجاح")
    
    # ---------------------------- الموردين ----------------------------
    def show_suppliers(self):
        self.current_screen = "suppliers"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.set_background(self.current_frame)
        
        self.suppliers_title = tk.Label(self.current_frame, text=f"🏭 {trans.get('suppliers')}", 
                                        font=("Arial", 16, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.suppliers_title.pack(pady=5)
        
        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(fill="x", pady=3)
        self.set_background(btn_frame)
        
        self.add_supplier_btn = tk.Button(btn_frame, text=f"➕ {trans.get('add_supplier')}", 
                                         command=self.add_supplier_dialog, bg=settings.secondary_color, 
                                         fg="white", font=("Arial", 10), padx=10)
        self.add_supplier_btn.pack(side="left", padx=3)
        
        self.delete_supplier_btn = tk.Button(btn_frame, text=f"🗑️ {trans.get('delete_supplier')}", 
                                            command=self.delete_supplier, bg="#e74c3c", fg="white", font=("Arial", 10), padx=10)
        self.delete_supplier_btn.pack(side="left", padx=3)
        
        columns = ("id", "name", "phone", "address", "contact_person")
        self.supplier_tree = ttk.Treeview(self.current_frame, columns=columns, show="headings", height=15)
        self.update_supplier_headings()
        
        scrollbar = ttk.Scrollbar(self.current_frame, orient="vertical", command=self.supplier_tree.yview)
        self.supplier_tree.configure(yscrollcommand=scrollbar.set)
        self.supplier_tree.pack(side="left", fill="both", expand=True, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        self.refresh_supplier_list()
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def update_supplier_headings(self):
        headings = ["ID", trans.get('supplier_name'), trans.get('supplier_phone'), 
                   trans.get('supplier_address'), trans.get('contact_person')]
        columns = ("id", "name", "phone", "address", "contact_person")
        for col, head in zip(columns, headings):
            self.supplier_tree.heading(col, text=head)
            self.supplier_tree.column(col, width=120)
    
    def refresh_supplier_list(self):
        for item in self.supplier_tree.get_children():
            self.supplier_tree.delete(item)
        suppliers = db.fetch_all("SELECT id, name, phone, address, contact_person FROM suppliers ORDER BY id")
        for sup in suppliers:
            self.supplier_tree.insert("", "end", values=sup)
    
    def refresh_suppliers_screen(self):
        if hasattr(self, 'suppliers_title'):
            self.suppliers_title.config(text=f"🏭 {trans.get('suppliers')}")
        if hasattr(self, 'add_supplier_btn'):
            self.add_supplier_btn.config(text=f"➕ {trans.get('add_supplier')}")
        if hasattr(self, 'delete_supplier_btn'):
            self.delete_supplier_btn.config(text=f"🗑️ {trans.get('delete_supplier')}")
        if hasattr(self, 'supplier_tree'):
            self.update_supplier_headings()
            self.refresh_supplier_list()
    
    def add_supplier_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('add_supplier'))
        dialog.geometry("400x350")
        dialog.grab_set()
        
        tk.Label(dialog, text=f"{trans.get('supplier_name')}:", font=("Arial", 11)).pack(pady=3)
        name_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        name_entry.pack(pady=3)
        
        tk.Label(dialog, text=f"{trans.get('supplier_phone')}:", font=("Arial", 11)).pack(pady=3)
        phone_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        phone_entry.pack(pady=3)
        
        tk.Label(dialog, text=f"{trans.get('supplier_address')}:", font=("Arial", 11)).pack(pady=3)
        address_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        address_entry.pack(pady=3)
        
        tk.Label(dialog, text=f"{trans.get('contact_person')}:", font=("Arial", 11)).pack(pady=3)
        contact_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        contact_entry.pack(pady=3)
        
        def save_supplier():
            if name_entry.get():
                db.execute_query("""
                    INSERT INTO suppliers (name, phone, address, contact_person)
                    VALUES (?, ?, ?, ?)
                """, (name_entry.get(), phone_entry.get(), address_entry.get(), contact_entry.get()))
                self.refresh_supplier_list()
                dialog.destroy()
                messagebox.showinfo(trans.get('success'), "تمت إضافة المورد بنجاح")
            else:
                messagebox.showwarning(trans.get('warning'), "الرجاء إدخال اسم المورد")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text=trans.get('save'), command=save_supplier, 
                 bg=settings.secondary_color, fg="white", font=("Arial", 11), width=8).pack(side="left", padx=8)
        tk.Button(btn_frame, text=trans.get('cancel'), command=dialog.destroy, 
                 bg="#95a5a6", fg="white", font=("Arial", 11), width=8).pack(side="left", padx=8)
    
    def delete_supplier(self):
        selected = self.supplier_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء تحديد مورد للحذف")
            return
        
        if messagebox.askyesno(trans.get('confirm'), "هل أنت متأكد من حذف هذا المورد؟"):
            item = self.supplier_tree.item(selected[0])
            supplier_id = item['values'][0]
            db.execute_query("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
            self.refresh_supplier_list()
            messagebox.showinfo(trans.get('success'), "تم حذف المورد بنجاح")
    
    # ---------------------------- الفواتير ----------------------------
    def show_invoices(self):
        self.current_screen = "invoices"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.set_background(self.current_frame)
        
        self.invoices_title = tk.Label(self.current_frame, text=f"📄 {trans.get('invoice_management')}", 
                                       font=("Arial", 16, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.invoices_title.pack(pady=5)
        
        columns = ("id", "invoice_number", "customer_name", "total_amount", "final_amount", "payment_method", "created_at")
        self.invoice_tree = ttk.Treeview(self.current_frame, columns=columns, show="headings", height=15)
        self.update_invoice_headings()
        self.invoice_tree.pack(fill="both", expand=True, pady=5)
        
        self.refresh_invoice_list()
        
        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(pady=3)
        self.set_background(btn_frame)
        
        self.details_btn = tk.Button(btn_frame, text="🔍 عرض التفاصيل", command=self.view_invoice_details, 
                                    bg=settings.primary_color, fg="white", font=("Arial", 10))
        self.details_btn.pack(side="left", padx=3)
        
        self.print_btn = tk.Button(btn_frame, text="🖨️ طباعة", command=self.print_selected_invoice, 
                                  bg="#e67e22", fg="white", font=("Arial", 10))
        self.print_btn.pack(side="left", padx=3)
        
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def update_invoice_headings(self):
        headings = ["ID", trans.get('invoice_no'), trans.get('invoice_customer'), 
                   f"{trans.get('invoice_total')} ({settings.currency_symbol})", 
                   f"الإجمالي ({settings.currency_symbol})", "طريقة الدفع", trans.get('invoice_date')]
        columns = ("id", "invoice_number", "customer_name", "total_amount", "final_amount", "payment_method", "created_at")
        for col, head in zip(columns, headings):
            self.invoice_tree.heading(col, text=head)
            self.invoice_tree.column(col, width=100)
    
    def refresh_invoice_list(self):
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)
        
        if self.current_user_role == "customer" and self.current_customer_id:
            invoices = db.fetch_all("SELECT id, invoice_number, customer_name, total_amount, final_amount, payment_method, created_at FROM invoices WHERE customer_id = ? ORDER BY id DESC", (self.current_customer_id,))
        else:
            invoices = db.fetch_all("SELECT id, invoice_number, customer_name, total_amount, final_amount, payment_method, created_at FROM invoices ORDER BY id DESC")
        
        for inv in invoices:
            self.invoice_tree.insert("", "end", values=(inv[0], inv[1], inv[2], f"{inv[3]:.2f}", f"{inv[4]:.2f}", inv[5], inv[6]))
    
    def refresh_invoices_screen(self):
        if hasattr(self, 'invoices_title'):
            self.invoices_title.config(text=f"📄 {trans.get('invoice_management')}")
        if hasattr(self, 'details_btn'):
            self.details_btn.config(text="🔍 عرض التفاصيل")
        if hasattr(self, 'print_btn'):
            self.print_btn.config(text="🖨️ طباعة")
        if hasattr(self, 'invoice_tree'):
            self.update_invoice_headings()
            self.refresh_invoice_list()
    
    def view_invoice_details(self):
        selected = self.invoice_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء اختيار فاتورة")
            return
        item = self.invoice_tree.item(selected[0])
        invoice_id = item['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("تفاصيل الفاتورة")
        dialog.geometry("500x450")
        dialog.grab_set()
        
        invoice = db.fetch_one("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
        if invoice:
            tk.Label(dialog, text=f"رقم الفاتورة: {invoice[1]}", font=("Arial", 12, "bold")).pack(pady=3)
            tk.Label(dialog, text=f"العميل: {invoice[3]}", font=("Arial", 10)).pack()
            tk.Label(dialog, text=f"التاريخ: {invoice[10]}", font=("Arial", 10)).pack()
            tk.Label(dialog, text=f"المجموع: {self.format_currency(invoice[4])}", font=("Arial", 10)).pack()
            tk.Label(dialog, text=f"الضريبة: {self.format_currency(invoice[5])}", font=("Arial", 10)).pack()
            tk.Label(dialog, text=f"الإجمالي: {self.format_currency(invoice[7])}", font=("Arial", 11, "bold"), fg="red").pack()
            
            tk.Label(dialog, text="\n--- الأصناف ---", font=("Arial", 11, "bold")).pack(pady=3)
            items = db.fetch_all("SELECT medicine_name, quantity, price, total FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
            for it in items:
                tk.Label(dialog, text=f"{it[0]} - {it[1]} × {it[2]:.2f} = {it[3]:.2f} {settings.currency_symbol}", font=("Arial", 9)).pack()
        
        tk.Button(dialog, text="إغلاق", command=dialog.destroy, bg="#95a5a6", fg="white", font=("Arial", 11)).pack(pady=10)
    
    def print_selected_invoice(self):
        selected = self.invoice_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء اختيار فاتورة")
            return
        item = self.invoice_tree.item(selected[0])
        self.print_invoice(item['values'][0])
    
    def print_invoice(self, invoice_id):
        invoice = db.fetch_one("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
        if not invoice:
            return
        
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, f"invoice_{invoice_id}.pdf")
        
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, alignment=1)
        elements.append(Paragraph(f"{settings.pharmacy_name}", title_style))
        elements.append(Paragraph(f"فاتورة رقم: {invoice[1]}", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        info_data = [[f"التاريخ:", invoice[10]], [f"العميل:", invoice[3] or "نقدي"], [f"طريقة الدفع:", invoice[8]]]
        info_table = Table(info_data, colWidths=[100, 300])
        info_table.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
        elements.append(info_table)
        elements.append(Spacer(1, 12))
        
        items = db.fetch_all("SELECT medicine_name, quantity, price, total FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
        item_data = [[f"المنتج ({settings.currency_symbol})", "الكمية", f"السعر ({settings.currency_symbol})", f"المجموع ({settings.currency_symbol})"]]
        for it in items:
            item_data.append([it[0], str(it[1]), f"{it[2]:.2f}", f"{it[3]:.2f}"])
        
        item_table = Table(item_data, colWidths=[200, 80, 80, 80])
        item_table.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('BACKGROUND', (0,0), (-1,0), colors.grey), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke)]))
        elements.append(item_table)
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph(f"المجموع: {self.format_currency(invoice[4])}", styles['Normal']))
        elements.append(Paragraph(f"الضريبة: {self.format_currency(invoice[5])}", styles['Normal']))
        elements.append(Paragraph(f"الإجمالي النهائي: {self.format_currency(invoice[7])}", styles['Heading4']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("شكراً لثقتكم بنا", styles['Normal']))
        
        doc.build(elements)
        webbrowser.open(pdf_path)
    
    # ---------------------------- التقارير ----------------------------
    def show_reports(self):
        self.current_screen = "reports"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=15, pady=15)
        self.set_background(self.current_frame)
        
        self.reports_title = tk.Label(self.current_frame, text=f"📊 {trans.get('reports')}", 
                                      font=("Arial", 18, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.reports_title.pack(pady=8)
        
        self.stats_frame = tk.Frame(self.current_frame, relief="ridge", bd=2)
        self.stats_frame.pack(fill="x", pady=8)
        self.set_background(self.stats_frame)
        
        self.stats_label = tk.Label(self.stats_frame, font=("Arial", 11), justify="left", 
                                    bg=self.get_bg_color(), fg=self.get_fg_color())
        self.stats_label.pack(pady=8)
        
        self.refresh_stats_text()
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def refresh_stats_text(self):
        total_customers = db.fetch_one("SELECT COUNT(*) FROM customers")[0]
        total_medicines = db.fetch_one("SELECT COUNT(*) FROM medicines")[0]
        total_invoices = db.fetch_one("SELECT COUNT(*) FROM invoices")[0]
        total_sales = db.fetch_one("SELECT COALESCE(SUM(final_amount), 0) FROM invoices")[0]
        low_stock = db.fetch_one("SELECT COUNT(*) FROM medicines WHERE quantity < 10 AND quantity > 0")[0]
        out_of_stock = db.fetch_one("SELECT COUNT(*) FROM medicines WHERE quantity = 0")[0]
        expired = db.fetch_one("SELECT COUNT(*) FROM medicines WHERE expiry_date < date('now')")[0]
        expiring_soon = db.fetch_one("SELECT COUNT(*) FROM medicines WHERE expiry_date BETWEEN date('now') AND date('now', '+30 days') AND quantity > 0")[0]
        
        stats_text = f"""
        📈 {trans.get('statistics')}
        👥 {trans.get('total_customers')}: {total_customers}
        💊 {trans.get('total_medicines')}: {total_medicines}
        📄 {trans.get('total_invoices')}: {total_invoices}
        💰 {trans.get('total_sales')}: {self.format_currency(total_sales)}
        
        ⚠️ تنبيهات المخزون:
        - أدوية منخفضة الكمية (< 10): {low_stock}
        - أدوية نفذت من المخزون: {out_of_stock}
        
        ⚠️ تنبيهات الصلاحية:
        - أدوية منتهية الصلاحية: {expired}
        - أدوية شارفت على الانتهاء (30 يوم): {expiring_soon}
        """
        self.stats_label.config(text=stats_text)
    
    def refresh_reports_screen(self):
        if hasattr(self, 'reports_title'):
            self.reports_title.config(text=f"📊 {trans.get('reports')}")
        if hasattr(self, 'stats_label'):
            self.refresh_stats_text()
    
    # ---------------------------- الصلاحية ----------------------------
    def show_expiry(self):
        self.current_screen = "expiry"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.set_background(self.current_frame)
        
        self.expiry_title = tk.Label(self.current_frame, text=f"⚠️ {trans.get('expiry')}", 
                                     font=("Arial", 16, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.expiry_title.pack(pady=5)
        
        filter_frame = tk.Frame(self.current_frame)
        filter_frame.pack(fill="x", pady=3)
        self.set_background(filter_frame)
        
        tk.Label(filter_frame, text="عرض:", bg=self.get_bg_color(), fg=self.get_fg_color(), font=("Arial", 10)).pack(side="left", padx=3)
        self.expiry_filter = ttk.Combobox(filter_frame, values=["كل الأدوية", "منتهية الصلاحية", "شارفت على الانتهاء", "منخفضة الكمية"], width=18)
        self.expiry_filter.set("كل الأدوية")
        self.expiry_filter.pack(side="left", padx=3)
        self.expiry_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_expiry_list())
        
        columns = ("name", "expiry_date", "quantity", "status")
        self.expiry_tree = ttk.Treeview(self.current_frame, columns=columns, show="headings", height=15)
        self.update_expiry_headings()
        
        for col in columns:
            self.expiry_tree.column(col, width=130)
        self.expiry_tree.pack(fill="both", expand=True, pady=5)
        
        self.refresh_expiry_list()
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def update_expiry_headings(self):
        self.expiry_tree.heading("name", text=trans.get('medicine_name'))
        self.expiry_tree.heading("expiry_date", text=trans.get('medicine_expiry'))
        self.expiry_tree.heading("quantity", text=trans.get('medicine_quantity'))
        self.expiry_tree.heading("status", text="الحالة")
    
    def refresh_expiry_list(self):
        for item in self.expiry_tree.get_children():
            self.expiry_tree.delete(item)
        
        filter_type = self.expiry_filter.get()
        today = datetime.now().strftime("%Y-%m-%d")
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        if filter_type == "منتهية الصلاحية":
            medicines = db.fetch_all("SELECT name, expiry_date, quantity FROM medicines WHERE expiry_date < ? AND quantity > 0 ORDER BY expiry_date", (today,))
            status = "منتهي"
        elif filter_type == "شارفت على الانتهاء":
            medicines = db.fetch_all("SELECT name, expiry_date, quantity FROM medicines WHERE expiry_date BETWEEN ? AND ? AND quantity > 0 ORDER BY expiry_date", (today, future_date))
            status = "شارك على الانتهاء"
        elif filter_type == "منخفضة الكمية":
            medicines = db.fetch_all("SELECT name, expiry_date, quantity FROM medicines WHERE quantity < 10 AND quantity > 0 ORDER BY quantity")
            status = "مخزون منخفض"
        else:
            medicines = db.fetch_all("SELECT name, expiry_date, quantity FROM medicines WHERE quantity > 0 ORDER BY expiry_date")
            status = "ساري"
        
        for med in medicines:
            if filter_type == "كل الأدوية":
                if med[1] < today:
                    med_status = "منتهي"
                elif med[1] <= future_date:
                    med_status = "شارك على الانتهاء"
                elif med[2] < 10:
                    med_status = "مخزون منخفض"
                else:
                    med_status = "ساري"
            else:
                med_status = status
            
            self.expiry_tree.insert("", "end", values=(med[0], med[1], med[2], med_status))
    
    def refresh_expiry_screen(self):
        if hasattr(self, 'expiry_title'):
            self.expiry_title.config(text=f"⚠️ {trans.get('expiry')}")
        if hasattr(self, 'expiry_tree'):
            self.update_expiry_headings()
            self.refresh_expiry_list()
    
    # ---------------------------- الباركود ----------------------------
    def show_barcode_scanner(self):
        self.current_screen = "barcode"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=15, pady=15)
        self.set_background(self.current_frame)
        
        self.barcode_title = tk.Label(self.current_frame, text=f"📱 {trans.get('barcode')}", 
                                      font=("Arial", 18, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.barcode_title.pack(pady=8)
        
        self.barcode_instruction = tk.Label(self.current_frame, text="أدخل كود الباركود أو امسحه:", 
                                            font=("Arial", 12), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.barcode_instruction.pack()
        
        self.barcode_entry = tk.Entry(self.current_frame, font=("Arial", 12), width=25)
        self.barcode_entry.pack(pady=8)
        self.barcode_entry.focus()
        
        self.result_label = tk.Label(self.current_frame, text="", font=("Arial", 11), 
                                     fg="green", bg=self.get_bg_color())
        self.result_label.pack(pady=8)
        
        self.search_btn = tk.Button(self.current_frame, text="🔍 بحث", command=self.search_barcode, 
                                   bg=settings.primary_color, fg="white", font=("Arial", 11))
        self.search_btn.pack(pady=3)
        
        self.generate_btn = tk.Button(self.current_frame, text="🖨️ إنشاء باركود", command=self.generate_barcode, 
                                     bg=settings.secondary_color, fg="white", font=("Arial", 11))
        self.generate_btn.pack(pady=3)
        
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def search_barcode(self):
        val = self.barcode_entry.get()
        if val:
            med = db.fetch_one("SELECT name, price, quantity, expiry_date FROM medicines WHERE barcode = ? OR code = ?", (val, val))
            if med:
                expiry_status = ""
                if med[3]:
                    if med[3] < datetime.now().strftime("%Y-%m-%d"):
                        expiry_status = "\n⚠️ منتهي الصلاحية!"
                    elif med[3] <= (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"):
                        expiry_status = "\n⚠️ يوشك على الانتهاء!"
                
                self.result_label.config(text=f"✅ {med[0]}\nالسعر: {self.format_currency(med[1])}\nالمتبقي: {med[2]}{expiry_status}", 
                                        fg="orange" if expiry_status else "green")
            else:
                self.result_label.config(text="❌ لم يتم العثور على الدواء", fg="red")
    
    def generate_barcode(self):
        code = simpledialog.askstring(trans.get('generate_barcode'), "أدخل كود الدواء:")
        if code and db.fetch_one("SELECT id FROM medicines WHERE code = ?", (code,)):
            try:
                ean = barcode.get_barcode_class('ean13')
                ean(code.zfill(12), writer=ImageWriter()).save(f"barcode_{code}")
                self.result_label.config(text=f"تم إنشاء الباركود: barcode_{code}.png")
                webbrowser.open(f"barcode_{code}.png")
            except Exception as e:
                self.result_label.config(text=f"خطأ: {e}")
        else:
            self.result_label.config(text="الكود غير موجود")
    
    def refresh_barcode_screen(self):
        if hasattr(self, 'barcode_title'):
            self.barcode_title.config(text=f"📱 {trans.get('barcode')}")
        if hasattr(self, 'barcode_instruction'):
            self.barcode_instruction.config(text="أدخل كود الباركود أو امسحه:")
        if hasattr(self, 'search_btn'):
            self.search_btn.config(text="🔍 بحث")
        if hasattr(self, 'generate_btn'):
            self.generate_btn.config(text="🖨️ إنشاء باركود")
    
    # ---------------------------- الصندوق المالي ----------------------------
    def show_cashbox(self):
        if self.current_user_role != "manager":
            messagebox.showerror(trans.get('error'), "هذه الخاصية للمدير فقط")
            return
        
        self.current_screen = "cashbox"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=15, pady=15)
        self.set_background(self.current_frame)
        
        self.cashbox_title = tk.Label(self.current_frame, text=f"💰 {trans.get('cashbox_title')}", 
                                      font=("Arial", 18, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.cashbox_title.pack(pady=8)
        
        self.info_frame = tk.Frame(self.current_frame, relief="ridge", bd=2)
        self.info_frame.pack(fill="x", pady=8)
        self.set_background(self.info_frame)
        
        self.info_label = tk.Label(self.info_frame, font=("Arial", 11), justify="left", 
                                  bg=self.get_bg_color(), fg=self.get_fg_color())
        self.info_label.pack(pady=8)
        
        self.btn_frame = tk.Frame(self.current_frame)
        self.btn_frame.pack(pady=8)
        self.set_background(self.btn_frame)
        
        self.opening_btn = tk.Button(self.btn_frame, text="💰 رصيد الافتتاح", command=self.set_opening, 
                                    bg="#3498db", fg="white", font=("Arial", 10))
        self.opening_btn.pack(side="left", padx=3)
        
        self.income_btn = tk.Button(self.btn_frame, text="➕ إيداع", command=self.add_income, 
                                   bg=settings.secondary_color, fg="white", font=("Arial", 10))
        self.income_btn.pack(side="left", padx=3)
        
        self.expense_btn = tk.Button(self.btn_frame, text="➖ سحب", command=self.add_expense, 
                                    bg="#e74c3c", fg="white", font=("Arial", 10))
        self.expense_btn.pack(side="left", padx=3)
        
        columns = ("date", "type", "amount", "description", "user")
        self.cashbox_tree = ttk.Treeview(self.current_frame, columns=columns, show="headings", height=12)
        self.update_cashbox_headings()
        
        for col in columns:
            self.cashbox_tree.column(col, width=100)
        self.cashbox_tree.pack(fill="both", expand=True, pady=8)
        
        self.refresh_cashbox_data()
        self.refresh_cashbox_list()
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def update_cashbox_headings(self):
        headings = ["التاريخ", "النوع", f"المبلغ ({settings.currency_symbol})", "الوصف", "المستخدم"]
        columns = ("date", "type", "amount", "description", "user")
        for col, head in zip(columns, headings):
            self.cashbox_tree.heading(col, text=head)
    
    def refresh_cashbox_data(self):
        today = datetime.now().strftime("%Y-%m-%d")
        opening = db.fetch_one("SELECT opening_balance FROM cashbox_settings WHERE date = ?", (today,))
        opening_balance = opening[0] if opening else 0
        
        total_income = db.fetch_one("SELECT COALESCE(SUM(amount), 0) FROM cash_transactions WHERE transaction_type='income' AND date(created_at)=date('now')")[0]
        total_expense = db.fetch_one("SELECT COALESCE(SUM(amount), 0) FROM cash_transactions WHERE transaction_type='expense' AND date(created_at)=date('now')")[0]
        current = opening_balance + total_income - total_expense
        
        info_text = f"""
        {trans.get('opening_balance')}: {self.format_currency(opening_balance)}
        إجمالي الإيرادات: {self.format_currency(total_income)}
        إجمالي المصروفات: {self.format_currency(total_expense)}
        الرصيد الحالي: {self.format_currency(current)}
        """
        self.info_label.config(text=info_text)
    
    def refresh_cashbox_list(self):
        for item in self.cashbox_tree.get_children():
            self.cashbox_tree.delete(item)
        
        transactions = db.fetch_all("""
            SELECT ct.created_at, ct.transaction_type, ct.amount, ct.description, u.username
            FROM cash_transactions ct LEFT JOIN users u ON ct.user_id = u.id ORDER BY ct.id DESC
        """)
        for t in transactions:
            type_text = "إيداع" if t[1] == "income" else "سحب"
            self.cashbox_tree.insert("", "end", values=(t[0], type_text, f"{t[2]:.2f}", t[3], t[4]))
    
    def refresh_cashbox_screen(self):
        if hasattr(self, 'cashbox_title'):
            self.cashbox_title.config(text=f"💰 {trans.get('cashbox_title')}")
        if hasattr(self, 'opening_btn'):
            self.opening_btn.config(text="💰 رصيد الافتتاح")
        if hasattr(self, 'income_btn'):
            self.income_btn.config(text="➕ إيداع")
        if hasattr(self, 'expense_btn'):
            self.expense_btn.config(text="➖ سحب")
        if hasattr(self, 'cashbox_tree'):
            self.update_cashbox_headings()
            self.refresh_cashbox_data()
            self.refresh_cashbox_list()
    
    def set_opening(self):
        amount = simpledialog.askfloat(trans.get('opening_balance'), "أدخل رصيد الافتتاح:")
        if amount is not None:
            today = datetime.now().strftime("%Y-%m-%d")
            if db.fetch_one("SELECT id FROM cashbox_settings WHERE date = ?", (today,)):
                db.execute_query("UPDATE cashbox_settings SET opening_balance = ? WHERE date = ?", (amount, today))
            else:
                db.execute_query("INSERT INTO cashbox_settings (opening_balance, date) VALUES (?, ?)", (amount, today))
            self.show_cashbox()
    
    def add_income(self):
        amount = simpledialog.askfloat(trans.get('cash_in'), "المبلغ:")
        if amount:
            desc = simpledialog.askstring(trans.get('add'), "الوصف:")
            db.execute_query("INSERT INTO cash_transactions (transaction_type, amount, description, user_id) VALUES ('income', ?, ?, ?)", (amount, desc, self.current_user_id))
            self.show_cashbox()
    
    def add_expense(self):
        amount = simpledialog.askfloat(trans.get('cash_out'), "المبلغ:")
        if amount:
            desc = simpledialog.askstring(trans.get('add'), "الوصف:")
            db.execute_query("INSERT INTO cash_transactions (transaction_type, amount, description, user_id) VALUES ('expense', ?, ?, ?)", (amount, desc, self.current_user_id))
            self.show_cashbox()
    
    # ---------------------------- إعدادات النظام ----------------------------
    def show_settings(self):
        if self.current_user_role != "manager":
            messagebox.showerror(trans.get('error'), "هذه الخاصية للمدير فقط")
            return
        
        self.current_screen = "settings"
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=15, pady=15)
        self.set_background(self.current_frame)
        
        title_frame = tk.Frame(self.current_frame, bg=settings.primary_color, height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text=f"⚙️ {trans.get('settings')}", font=("Arial", 16, "bold"), 
                fg="white", bg=settings.primary_color).pack(pady=10)
        
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill="both", expand=True, pady=10, padx=10)
        
        # ===== التبويب الأول: إعدادات الصيدلية =====
        pharmacy_tab = tk.Frame(notebook, bg=self.get_bg_color())
        notebook.add(pharmacy_tab, text="🏪 إعدادات الصيدلية")
        self.set_background(pharmacy_tab)
        
        settings_frame = tk.Frame(pharmacy_tab, relief="ridge", bd=2, bg=self.get_bg_color())
        settings_frame.pack(pady=20, padx=40, fill="x")
        
        tk.Label(settings_frame, text=f"{trans.get('system_name')}:", font=("Arial", 11), 
                bg=self.get_bg_color(), fg=self.get_fg_color()).grid(row=0, column=0, pady=8, padx=8, sticky="e")
        self.name_entry = tk.Entry(settings_frame, width=30, font=("Arial", 10))
        self.name_entry.insert(0, settings.pharmacy_name)
        self.name_entry.grid(row=0, column=1, pady=8, padx=8)
        
        tk.Label(settings_frame, text=f"{trans.get('address')}:", font=("Arial", 11), 
                bg=self.get_bg_color(), fg=self.get_fg_color()).grid(row=1, column=0, pady=8, padx=8, sticky="e")
        self.address_entry = tk.Entry(settings_frame, width=30, font=("Arial", 10))
        self.address_entry.insert(0, settings.pharmacy_address)
        self.address_entry.grid(row=1, column=1, pady=8, padx=8)
        
        tk.Label(settings_frame, text=f"{trans.get('phone')}:", font=("Arial", 11), 
                bg=self.get_bg_color(), fg=self.get_fg_color()).grid(row=2, column=0, pady=8, padx=8, sticky="e")
        self.phone_entry = tk.Entry(settings_frame, width=30, font=("Arial", 10))
        self.phone_entry.insert(0, settings.pharmacy_phone)
        self.phone_entry.grid(row=2, column=1, pady=8, padx=8)
        
        tk.Label(settings_frame, text=f"{trans.get('tax_rate')} (%):", font=("Arial", 11), 
                bg=self.get_bg_color(), fg=self.get_fg_color()).grid(row=3, column=0, pady=8, padx=8, sticky="e")
        self.tax_entry = tk.Entry(settings_frame, width=30, font=("Arial", 10))
        self.tax_entry.insert(0, settings.tax_rate * 100)
        self.tax_entry.grid(row=3, column=1, pady=8, padx=8)
        
        tk.Label(settings_frame, text=f"{trans.get('currency')}:", font=("Arial", 11), 
                bg=self.get_bg_color(), fg=self.get_fg_color()).grid(row=4, column=0, pady=8, padx=8, sticky="e")
        self.currency_var = tk.StringVar(value=settings.currency)
        ttk.Combobox(settings_frame, textvariable=self.currency_var, 
                    values=["جنيه", "دولار", "ريال", "دينار", "يورو"], width=27).grid(row=4, column=1, pady=8, padx=8)
        
        tk.Label(settings_frame, text=f"{trans.get('currency_symbol')}:", font=("Arial", 11), 
                bg=self.get_bg_color(), fg=self.get_fg_color()).grid(row=5, column=0, pady=8, padx=8, sticky="e")
        self.symbol_entry = tk.Entry(settings_frame, width=30, font=("Arial", 10))
        self.symbol_entry.insert(0, settings.currency_symbol)
        self.symbol_entry.grid(row=5, column=1, pady=8, padx=8)
        
        btn_color_frame = tk.Frame(settings_frame, bg=self.get_bg_color())
        btn_color_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(btn_color_frame, text=f"🎨 تغيير اللون الأساسي", command=self.change_primary_color,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(btn_color_frame, text=f"🖼️ تغيير الخلفية", command=self.change_background,
                 bg="#e67e22", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(btn_color_frame, text=f"♻️ إعادة تعيين الخلفية", command=self.reset_background,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        
        # ===== التبويب الثاني: إدارة المستخدمين =====
        users_tab = tk.Frame(notebook, bg=self.get_bg_color())
        notebook.add(users_tab, text="👥 إدارة المستخدمين")
        self.set_background(users_tab)
        
        users_btn_frame = tk.Frame(users_tab, bg=self.get_bg_color())
        users_btn_frame.pack(fill="x", pady=10, padx=10)
        
        self.add_user_btn = tk.Button(users_btn_frame, text=f"➕ إضافة مستخدم", command=self.add_user_dialog, 
                                     bg=settings.secondary_color, fg="white", font=("Arial", 10))
        self.add_user_btn.pack(side="left", padx=3)
        
        self.edit_user_btn = tk.Button(users_btn_frame, text=f"✏️ تعديل مستخدم", command=self.edit_user_dialog, 
                                      bg="#3498db", fg="white", font=("Arial", 10))
        self.edit_user_btn.pack(side="left", padx=3)
        
        self.delete_user_btn = tk.Button(users_btn_frame, text=f"🗑️ حذف مستخدم", command=self.delete_user, 
                                        bg="#e74c3c", fg="white", font=("Arial", 10))
        self.delete_user_btn.pack(side="left", padx=3)
        
        self.change_pass_btn = tk.Button(users_btn_frame, text=f"🔑 تغيير كلمة السر", command=self.change_user_password, 
                                        bg="#f39c12", fg="white", font=("Arial", 10))
        self.change_pass_btn.pack(side="left", padx=3)
        
        columns = ("id", "username", "full_name", "role", "created_at")
        self.user_tree = ttk.Treeview(users_tab, columns=columns, show="headings", height=12)
        headings = ["ID", "اسم المستخدم", "الاسم الكامل", "الصلاحية", "تاريخ الإضافة"]
        for col, head in zip(columns, headings):
            self.user_tree.heading(col, text=head)
            self.user_tree.column(col, width=120)
        self.user_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_user_list()
        
        btn_save_frame = tk.Frame(self.current_frame, bg=self.get_bg_color())
        btn_save_frame.pack(pady=15)
        self.save_btn = tk.Button(btn_save_frame, text=trans.get('save'), command=self.save_pharmacy_settings, 
                                 bg=settings.secondary_color, fg="white", font=("Arial", 12), width=10)
        self.save_btn.pack(side="left", padx=10)
        cancel_btn = tk.Button(btn_save_frame, text=trans.get('cancel'), command=self.show_main_dashboard, 
                              bg="#95a5a6", fg="white", font=("Arial", 12), width=10)
        cancel_btn.pack(side="left", padx=10)
        
        self.add_back_button(self.current_frame, self.show_main_dashboard)
    
    def save_pharmacy_settings(self):
        settings.pharmacy_name = self.name_entry.get()
        settings.pharmacy_address = self.address_entry.get()
        settings.pharmacy_phone = self.phone_entry.get()
        settings.currency = self.currency_var.get()
        settings.currency_symbol = self.symbol_entry.get()
        try:
            settings.tax_rate = float(self.tax_entry.get()) / 100
        except:
            pass
        settings.save_settings()
        self.root.title(f"{settings.pharmacy_name} - {trans.get('app_title')}")
        messagebox.showinfo(trans.get('success'), "تم حفظ إعدادات الصيدلية بنجاح")
        self.show_main_dashboard()
    
    def refresh_settings_screen(self):
        if hasattr(self, 'save_btn'):
            self.save_btn.config(text=trans.get('save'))
    
    def refresh_user_list(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        role_names = {'manager': 'مدير', 'cashier': 'موظف مبيعات', 'customer': 'عميل'}
        for user in db.fetch_all("SELECT id, username, full_name, role, created_at FROM users ORDER BY id"):
            role_name = role_names.get(user[3], user[3])
            self.user_tree.insert("", "end", values=(user[0], user[1], user[2] if user[2] else "-", role_name, user[4]))
    
    def add_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('add_user'))
        dialog.geometry("380x400")
        dialog.grab_set()
        
        tk.Label(dialog, text=f"{trans.get('username_login')}:", font=("Arial", 11)).pack(pady=3)
        username_entry = tk.Entry(dialog, width=28, font=("Arial", 10))
        username_entry.pack()
        
        tk.Label(dialog, text=f"{trans.get('password')}:", font=("Arial", 11)).pack(pady=3)
        password_entry = tk.Entry(dialog, width=28, font=("Arial", 10), show="*")
        password_entry.pack()
        
        tk.Label(dialog, text="الاسم الكامل:", font=("Arial", 11)).pack(pady=3)
        fullname_entry = tk.Entry(dialog, width=28, font=("Arial", 10))
        fullname_entry.pack()
        
        tk.Label(dialog, text=f"{trans.get('role')}:", font=("Arial", 11)).pack(pady=3)
        role_var = tk.StringVar(value="cashier")
        tk.Radiobutton(dialog, text=trans.get('manager'), variable=role_var, value="manager", font=("Arial", 10)).pack()
        tk.Radiobutton(dialog, text=trans.get('cashier'), variable=role_var, value="cashier", font=("Arial", 10)).pack()
        tk.Radiobutton(dialog, text=trans.get('customer_user'), variable=role_var, value="customer", font=("Arial", 10)).pack()
        
        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            fullname = fullname_entry.get()
            role = role_var.get()
            
            if not username or not password:
                messagebox.showerror(trans.get('error'), "الرجاء إدخال اسم المستخدم وكلمة السر")
                return
            
            existing = db.fetch_one("SELECT id FROM users WHERE username = ?", (username,))
            if existing:
                messagebox.showerror(trans.get('error'), "اسم المستخدم موجود بالفعل")
                return
            
            hashed_pass = self.hash_password(password)
            db.execute_query("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                           (username, hashed_pass, role, fullname))
            self.refresh_user_list()
            dialog.destroy()
            messagebox.showinfo(trans.get('success'), "تمت إضافة المستخدم بنجاح")
        
        tk.Button(dialog, text=trans.get('save'), command=save_user, bg=settings.secondary_color, fg="white", font=("Arial", 11)).pack(pady=15)
    
    def edit_user_dialog(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء تحديد مستخدم للتعديل")
            return
        
        item = self.user_tree.item(selected[0])
        user_id = item['values'][0]
        current_username = item['values'][1]
        current_fullname = item['values'][2] if item['values'][2] != "-" else ""
        current_role = item['values'][3]
        
        role_map = {'مدير': 'manager', 'موظف مبيعات': 'cashier', 'عميل': 'customer'}
        role_value = role_map.get(current_role, 'cashier')
        
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('edit_user'))
        dialog.geometry("380x400")
        dialog.grab_set()
        
        tk.Label(dialog, text=f"{trans.get('username_login')}:", font=("Arial", 11)).pack(pady=3)
        username_entry = tk.Entry(dialog, width=28, font=("Arial", 10))
        username_entry.insert(0, current_username)
        username_entry.pack()
        
        tk.Label(dialog, text="الاسم الكامل:", font=("Arial", 11)).pack(pady=3)
        fullname_entry = tk.Entry(dialog, width=28, font=("Arial", 10))
        fullname_entry.insert(0, current_fullname)
        fullname_entry.pack()
        
        tk.Label(dialog, text=f"{trans.get('role')}:", font=("Arial", 11)).pack(pady=3)
        role_var = tk.StringVar(value=role_value)
        tk.Radiobutton(dialog, text=trans.get('manager'), variable=role_var, value="manager", font=("Arial", 10)).pack()
        tk.Radiobutton(dialog, text=trans.get('cashier'), variable=role_var, value="cashier", font=("Arial", 10)).pack()
        tk.Radiobutton(dialog, text=trans.get('customer_user'), variable=role_var, value="customer", font=("Arial", 10)).pack()
        
        def update_user():
            username = username_entry.get()
            fullname = fullname_entry.get()
            role = role_var.get()
            
            if not username:
                messagebox.showerror(trans.get('error'), "الرجاء إدخال اسم المستخدم")
                return
            
            existing = db.fetch_one("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
            if existing:
                messagebox.showerror(trans.get('error'), "اسم المستخدم موجود بالفعل")
                return
            
            db.execute_query("UPDATE users SET username = ?, full_name = ?, role = ? WHERE id = ?",
                           (username, fullname, role, user_id))
            self.refresh_user_list()
            dialog.destroy()
            messagebox.showinfo(trans.get('success'), "تم تعديل المستخدم بنجاح")
        
        tk.Button(dialog, text=trans.get('save'), command=update_user, bg=settings.secondary_color, fg="white", font=("Arial", 11)).pack(pady=15)
    
    def delete_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء تحديد مستخدم للحذف")
            return
        item = self.user_tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        if user_id == self.current_user_id:
            messagebox.showerror(trans.get('error'), "لا يمكن حذف المستخدم الحالي")
            return
        
        if messagebox.askyesno(trans.get('confirm'), f"هل أنت متأكد من حذف المستخدم {username}؟"):
            db.execute_query("DELETE FROM users WHERE id = ?", (user_id,))
            self.refresh_user_list()
            messagebox.showinfo(trans.get('success'), "تم حذف المستخدم بنجاح")
    
    def change_user_password(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء تحديد مستخدم لتغيير كلمة السر")
            return
        item = self.user_tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('change_password'))
        dialog.geometry("350x200")
        dialog.grab_set()
        
        tk.Label(dialog, text=f"تغيير كلمة السر للمستخدم: {username}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text=f"{trans.get('password')}:", font=("Arial", 11)).pack(pady=3)
        password_entry = tk.Entry(dialog, width=25, font=("Arial", 10), show="*")
        password_entry.pack()
        tk.Label(dialog, text="تأكيد كلمة السر:", font=("Arial", 11)).pack(pady=3)
        confirm_entry = tk.Entry(dialog, width=25, font=("Arial", 10), show="*")
        confirm_entry.pack()
        
        def save_password():
            pwd = password_entry.get()
            if not pwd:
                messagebox.showerror(trans.get('error'), "الرجاء إدخال كلمة السر")
                return
            if pwd != confirm_entry.get():
                messagebox.showerror(trans.get('error'), "كلمة السر غير متطابقة")
                return
            hashed_pass = self.hash_password(pwd)
            db.execute_query("UPDATE users SET password = ? WHERE id = ?", (hashed_pass, user_id))
            dialog.destroy()
            messagebox.showinfo(trans.get('success'), "تم تغيير كلمة السر بنجاح")
        
        tk.Button(dialog, text=trans.get('save'), command=save_password, bg=settings.secondary_color, fg="white", font=("Arial", 11)).pack(pady=15)
    
    # ---------------------------- نقطة البيع ----------------------------
    def show_pos(self):
        self.current_screen = "pos"
        self.clear_window()
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        self.set_background(main_frame)
        self.current_frame = main_frame
        
        self.pos_title = tk.Label(main_frame, text=f"💰 {trans.get('pos_title')}", 
                                  font=("Arial", 18, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        self.pos_title.pack(pady=8)
        
        paned = tk.PanedWindow(main_frame, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=8, pady=8)
        
        right_frame = tk.Frame(paned)
        paned.add(right_frame, width=550)
        self.set_background(right_frame)
        
        self.right_title = tk.Label(right_frame, text="💊 قائمة الأدوية", font=("Arial", 13, "bold"), 
                                   bg=self.get_bg_color(), fg=self.get_fg_color())
        self.right_title.pack(pady=3)
        
        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill="x", pady=3)
        self.set_background(search_frame)
        
        self.search_label = tk.Label(search_frame, text="بحث:", font=("Arial", 10), 
                                    bg=self.get_bg_color(), fg=self.get_fg_color())
        self.search_label.pack(side="left", padx=3)
        
        self.search_entry = tk.Entry(search_frame, width=25, font=("Arial", 10))
        self.search_entry.pack(side="left", padx=3)
        
        med_frame = tk.Frame(right_frame)
        med_frame.pack(fill="both", expand=True)
        self.set_background(med_frame)
        
        columns = ("id", "name", "price", "quantity", "expiry")
        self.pos_tree = ttk.Treeview(med_frame, columns=columns, show="headings", height=15)
        self.update_pos_headings()
        self.pos_tree.column("id", width=40)
        self.pos_tree.column("name", width=160)
        self.pos_tree.column("price", width=70)
        self.pos_tree.column("quantity", width=70)
        self.pos_tree.column("expiry", width=90)
        
        scrollbar = ttk.Scrollbar(med_frame, orient="vertical", command=self.pos_tree.yview)
        self.pos_tree.configure(yscrollcommand=scrollbar.set)
        self.pos_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        left_frame = tk.Frame(paned, relief="ridge", bd=2)
        paned.add(left_frame, width=350)
        self.set_background(left_frame)
        
        self.cart_title = tk.Label(left_frame, text=f"🛒 {trans.get('cart')}", font=("Arial", 13, "bold"), 
                                  bg=self.get_bg_color(), fg=self.get_fg_color())
        self.cart_title.pack(pady=3)
        
        cart_frame = tk.Frame(left_frame)
        cart_frame.pack(fill="both", expand=True, pady=3)
        self.set_background(cart_frame)
        
        cart_cols = ("name", "qty", "price", "total")
        self.cart_tree = ttk.Treeview(cart_frame, columns=cart_cols, show="headings", height=12)
        self.update_cart_headings()
        for col in cart_cols:
            self.cart_tree.column(col, width=80)
        self.cart_tree.pack(fill="both", expand=True)
        
        self.total_var = tk.StringVar(value="0.00")
        total_frame = tk.Frame(left_frame)
        total_frame.pack(fill="x", pady=8)
        self.set_background(total_frame)
        
        self.total_label = tk.Label(total_frame, text=f"{trans.get('total')}:", font=("Arial", 14, "bold"), 
                                   bg=self.get_bg_color(), fg=self.get_fg_color())
        self.total_label.pack(side="left", padx=8)
        
        self.total_value = tk.Label(total_frame, textvariable=self.total_var, font=("Arial", 14, "bold"), 
                                   fg="red", bg=self.get_bg_color())
        self.total_value.pack(side="right", padx=8)
        
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=8)
        self.set_background(btn_frame)
        
        self.add_cart_btn = tk.Button(btn_frame, text=f"➕ {trans.get('add_to_cart')}", command=self.add_to_cart, 
                                     bg=settings.secondary_color, fg="white", font=("Arial", 9))
        self.add_cart_btn.pack(side="left", padx=3)
        
        self.remove_cart_btn = tk.Button(btn_frame, text=f"🗑️ {trans.get('remove_from_cart')}", command=self.remove_from_cart, 
                                        bg="#e74c3c", fg="white", font=("Arial", 9))
        self.remove_cart_btn.pack(side="left", padx=3)
        
        self.payment_btn = tk.Button(btn_frame, text=f"💳 {trans.get('payment')}", command=self.process_payment, 
                                    bg=settings.primary_color, fg="white", font=("Arial", 9))
        self.payment_btn.pack(side="right", padx=3)
        
        self.cart_items = []
        self.refresh_pos_medicines()
        
        self.search_entry.bind('<KeyRelease>', lambda e: self.refresh_pos_medicines(self.search_entry.get()))
        self.pos_tree.bind("<Double-Button-1>", lambda e: self.add_to_cart())
        self.add_back_button(main_frame, self.show_main_dashboard)
    
    def update_pos_headings(self):
        self.pos_tree.heading("id", text="م")
        self.pos_tree.heading("name", text="اسم الدواء")
        self.pos_tree.heading("price", text=f"السعر ({settings.currency_symbol})")
        self.pos_tree.heading("quantity", text="الكمية")
        self.pos_tree.heading("expiry", text="تاريخ الصلاحية")
    
    def update_cart_headings(self):
        self.cart_tree.heading("name", text="الدواء")
        self.cart_tree.heading("qty", text="الكمية")
        self.cart_tree.heading("price", text=f"السعر ({settings.currency_symbol})")
        self.cart_tree.heading("total", text=f"المجموع ({settings.currency_symbol})")
    
    def refresh_pos_medicines(self, search=""):
        for item in self.pos_tree.get_children():
            self.pos_tree.delete(item)
        if search:
            meds = db.fetch_all("SELECT id, name, price, quantity, expiry_date FROM medicines WHERE name LIKE ? AND quantity>0", (f"%{search}%",))
        else:
            meds = db.fetch_all("SELECT id, name, price, quantity, expiry_date FROM medicines WHERE quantity>0")
        
        for med in meds:
            tags = []
            if med[4]:
                if med[4] <= datetime.now().strftime("%Y-%m-%d"):
                    tags.append('expired')
                elif med[4] <= (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"):
                    tags.append('expiring')
            if med[3] < 10:
                tags.append('lowstock')
            
            self.pos_tree.insert("", "end", values=(med[0], med[1], f"{med[2]:.2f}", med[3], med[4]), tags=tags)
        
        self.pos_tree.tag_configure('expired', background='#f8d7da')
        self.pos_tree.tag_configure('expiring', background='#d1ecf1')
        self.pos_tree.tag_configure('lowstock', background='#fff3cd')
    
    def add_to_cart(self):
        selected = self.pos_tree.selection()
        if not selected:
            messagebox.showwarning(trans.get('warning'), "الرجاء اختيار دواء")
            return
        item = self.pos_tree.item(selected[0])
        
        med_id = item['values'][0]
        name = item['values'][1]
        price = float(item['values'][2])
        max_qty = item['values'][3]
        expiry = item['values'][4]
        
        if expiry and expiry <= datetime.now().strftime("%Y-%m-%d"):
            messagebox.showerror(trans.get('error'), "هذا الدواء منتهي الصلاحية ولا يمكن بيعه")
            return
        
        qty = simpledialog.askinteger(trans.get('add'), f"الكمية (متوفر: {max_qty}):", minvalue=1, maxvalue=max_qty)
        if qty:
            self.cart_items.append({"id": med_id, "name": name, "qty": qty, "price": price, "total": qty * price})
            self.update_cart()
    
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if selected:
            idx = self.cart_tree.index(selected[0])
            del self.cart_items[idx]
            self.update_cart()
    
    def update_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        total = 0
        for item in self.cart_items:
            self.cart_tree.insert("", "end", values=(item["name"], item["qty"], f"{item['price']:.2f}", f"{item['total']:.2f}"))
            total += item["total"]
        self.total_var.set(self.format_currency(total))
    
    def refresh_pos_screen(self):
        if hasattr(self, 'pos_title'):
            self.pos_title.config(text=f"💰 {trans.get('pos_title')}")
        if hasattr(self, 'right_title'):
            self.right_title.config(text="💊 قائمة الأدوية")
        if hasattr(self, 'search_label'):
            self.search_label.config(text="بحث:")
        if hasattr(self, 'cart_title'):
            self.cart_title.config(text=f"🛒 {trans.get('cart')}")
        if hasattr(self, 'total_label'):
            self.total_label.config(text=f"{trans.get('total')}:")
        if hasattr(self, 'add_cart_btn'):
            self.add_cart_btn.config(text=f"➕ {trans.get('add_to_cart')}")
        if hasattr(self, 'remove_cart_btn'):
            self.remove_cart_btn.config(text=f"🗑️ {trans.get('remove_from_cart')}")
        if hasattr(self, 'payment_btn'):
            self.payment_btn.config(text=f"💳 {trans.get('payment')}")
        if hasattr(self, 'pos_tree'):
            self.update_pos_headings()
            self.refresh_pos_medicines(self.search_entry.get() if hasattr(self, 'search_entry') else "")
        if hasattr(self, 'cart_tree'):
            self.update_cart_headings()
            self.update_cart()
    
    def process_payment(self):
        if not self.cart_items:
            messagebox.showwarning(trans.get('warning'), "السلة فارغة")
            return
        
        total = sum(i["total"] for i in self.cart_items)
        dialog = tk.Toplevel(self.root)
        dialog.title(trans.get('payment'))
        dialog.geometry("380x420")
        dialog.grab_set()
        
        tk.Label(dialog, text=f"{trans.get('total')}: {self.format_currency(total)}", font=("Arial", 14, "bold")).pack(pady=8)
        
        tk.Label(dialog, text="اختر العميل:", font=("Arial", 11)).pack(pady=3)
        customer_var = tk.StringVar(value="نقدي")
        customer_frame = tk.Frame(dialog)
        customer_frame.pack(pady=3)
        
        tk.Radiobutton(customer_frame, text="عميل نقدي", variable=customer_var, value="نقدي", font=("Arial", 10)).pack(side="left", padx=8)
        tk.Radiobutton(customer_frame, text="عميل مسجل", variable=customer_var, value="مسجل", font=("Arial", 10)).pack(side="left", padx=8)
        
        customer_combo = ttk.Combobox(dialog, width=28, state="readonly")
        customer_combo.pack(pady=3)
        
        def update_customer_list():
            if customer_var.get() == "مسجل":
                customers = db.fetch_all("SELECT id, name, points FROM customers ORDER BY name")
                customer_combo['values'] = [f"{c[1]} (نقاط: {c[2]})" for c in customers]
                customer_combo.pack()
            else:
                customer_combo.pack_forget()
        
        customer_var.trace('w', lambda *args: update_customer_list())
        
        tk.Label(dialog, text="طريقة الدفع:", font=("Arial", 11)).pack(pady=3)
        payment_var = tk.StringVar(value="cash")
        tk.Radiobutton(dialog, text=trans.get('cash'), variable=payment_var, value="cash", font=("Arial", 10)).pack()
        tk.Radiobutton(dialog, text=trans.get('card'), variable=payment_var, value="card", font=("Arial", 10)).pack()
        
        tk.Label(dialog, text="المبلغ المدفوع:", font=("Arial", 11)).pack(pady=3)
        paid_entry = tk.Entry(dialog, font=("Arial", 12), width=18)
        paid_entry.pack(pady=3)
        
        change_label = tk.Label(dialog, text="", font=("Arial", 11))
        change_label.pack(pady=3)
        
        def calc_change():
            try:
                paid = float(paid_entry.get())
                change = paid - total
                if change >= 0:
                    change_label.config(text=f"{trans.get('change')}: {self.format_currency(change)}", fg="green")
                else:
                    change_label.config(text=f"المبلغ غير كافٍ: {self.format_currency(abs(change))}", fg="red")
            except:
                pass
        
        tk.Button(dialog, text="حساب الباقي", command=calc_change, bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=3)
        
        def complete():
            try:
                paid = float(paid_entry.get())
                if paid < total:
                    messagebox.showerror(trans.get('error'), "المبلغ أقل من الإجمالي")
                    return
                
                customer_id = None
                customer_name = "عميل نقدي"
                if customer_var.get() == "مسجل" and customer_combo.get():
                    selected_customer = customer_combo.get()
                    customer_name = selected_customer.split(" (نقاط:")[0]
                    customer = db.fetch_one("SELECT id, points FROM customers WHERE name = ?", (customer_name,))
                    if customer:
                        customer_id = customer[0]
                        points_to_add = int(total / 10)
                        db.execute_query("UPDATE customers SET points = points + ? WHERE id = ?", (points_to_add, customer_id))
                
                invoice_no = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                tax = total * settings.tax_rate
                final_total = total + tax
                
                db.execute_query("INSERT INTO invoices (invoice_number, customer_id, customer_name, total_amount, tax, final_amount, payment_method, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (invoice_no, customer_id, customer_name, total, tax, final_total, payment_var.get(), self.current_user_id))
                inv_id = db.cursor.lastrowid
                
                for item in self.cart_items:
                    db.execute_query("INSERT INTO invoice_items (invoice_id, medicine_id, medicine_name, quantity, price, total) VALUES (?, ?, ?, ?, ?, ?)",
                                   (inv_id, item["id"], item["name"], item["qty"], item["price"], item["total"]))
                    db.execute_query("UPDATE medicines SET quantity = quantity - ? WHERE id = ?", (item["qty"], item["id"]))
                
                db.execute_query("INSERT INTO cash_transactions (transaction_type, amount, description, user_id) VALUES ('income', ?, ?, ?)",
                               (final_total, f"فاتورة {invoice_no}", self.current_user_id))
                
                dialog.destroy()
                messagebox.showinfo(trans.get('success'), f"تم البيع بنجاح\nالإجمالي: {self.format_currency(final_total)}")
                self.cart_items = []
                self.update_cart()
                self.refresh_pos_medicines()
                
                if messagebox.askyesno(trans.get('print_invoice'), "طباعة الفاتورة؟"):
                    self.print_invoice(inv_id)
            except ValueError:
                messagebox.showerror(trans.get('error'), "المبلغ غير صحيح")
        
        tk.Button(dialog, text="تأكيد الدفع", command=complete, bg=settings.primary_color, fg="white", font=("Arial", 11), width=12).pack(pady=15)
    
    # ---------------------------- داشبورد متقدم ----------------------------
    def show_advanced_dashboard(self):
        self.current_screen = "advanced_dashboard"
        self.clear_window()
        
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        self.set_background(self.current_frame)
        
        title_frame = tk.Frame(self.current_frame, bg=settings.primary_color, height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        back_btn = tk.Button(title_frame, text=f"🔙 {trans.get('back')}", command=self.show_main_dashboard,
                            bg="#e74c3c", fg="white", font=("Arial", 10), padx=10, pady=3)
        back_btn.pack(side="left", padx=10)
        
        title_label = tk.Label(title_frame, text="📊 لوحة المعلومات المتقدمة (Dashboard)", 
                               font=("Arial", 16, "bold"), fg="white", bg=settings.primary_color)
        title_label.pack(pady=10)
        
        content_frame = tk.Frame(self.current_frame, bg=self.get_bg_color())
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.set_background(content_frame)
        
        cards_frame = tk.Frame(content_frame, bg=self.get_bg_color())
        cards_frame.pack(fill="x", pady=5)
        
        total_customers = db.fetch_one("SELECT COUNT(*) FROM customers")[0]
        total_medicines = db.fetch_one("SELECT COUNT(*) FROM medicines")[0]
        total_invoices = db.fetch_one("SELECT COUNT(*) FROM invoices")[0]
        total_sales = db.fetch_one("SELECT COALESCE(SUM(final_amount), 0) FROM invoices")[0]
        today_sales = db.fetch_one("SELECT COALESCE(SUM(final_amount), 0) FROM invoices WHERE date(created_at) = date('now')")[0]
        low_stock = db.fetch_one("SELECT COUNT(*) FROM medicines WHERE quantity < 10 AND quantity > 0")[0]
        out_of_stock = db.fetch_one("SELECT COUNT(*) FROM medicines WHERE quantity = 0")[0]
        expiring_soon = db.fetch_one("SELECT COUNT(*) FROM medicines WHERE expiry_date BETWEEN date('now') AND date('now', '+30 days') AND quantity > 0")[0]
        
        cards_data = [
            ("👥", "العملاء", total_customers, "#3498db"),
            ("💊", "الأدوية", total_medicines, "#2ecc71"),
            ("📄", "الفواتير", total_invoices, "#e67e22"),
            ("💰", "إجمالي المبيعات", self.format_currency(total_sales), "#9b59b6"),
            ("📈", "مبيعات اليوم", self.format_currency(today_sales), "#1abc9c"),
            ("⚠️", "مخزون منخفض", low_stock, "#f39c12"),
            ("❌", "نفد من المخزون", out_of_stock, "#e74c3c"),
            ("🗓️", "صالحيته قاربت", expiring_soon, "#e67e22"),
        ]
        
        for i, (icon, title, value, color) in enumerate(cards_data):
            card = tk.Frame(cards_frame, bg=color, relief="raised", bd=2)
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            
            tk.Label(card, text=icon, font=("Arial", 24), bg=color, fg="white").pack(pady=5)
            tk.Label(card, text=title, font=("Arial", 10), bg=color, fg="white").pack()
            tk.Label(card, text=str(value), font=("Arial", 14, "bold"), bg=color, fg="white").pack(pady=5)
            
            cards_frame.grid_columnconfigure(i, weight=1)
        
        charts_frame = tk.Frame(content_frame, bg=self.get_bg_color())
        charts_frame.pack(fill="both", expand=True, pady=10)
        
        chart1_frame = tk.LabelFrame(charts_frame, text="📈 المبيعات الأسبوعية", 
                                      font=("Arial", 11, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        chart1_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        weekly_sales = db.fetch_all("""
            SELECT date(created_at) as day, COALESCE(SUM(final_amount), 0) 
            FROM invoices 
            WHERE created_at >= date('now', '-7 days')
            GROUP BY date(created_at)
            ORDER BY day
        """)
        
        days_list = []
        sales_list = []
        for sale in weekly_sales:
            days_list.append(sale[0][5:] if sale[0] else "---")
            sales_list.append(sale[1])
        
        while len(days_list) < 7:
            days_list.insert(0, "-")
            sales_list.insert(0, 0)
        
        self.create_simple_chart(chart1_frame, days_list, sales_list, "المبيعات")
        
        chart2_frame = tk.LabelFrame(charts_frame, text="🥧 توزيع الأدوية حسب التصنيف", 
                                      font=("Arial", 11, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        chart2_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        categories = db.fetch_all("""
            SELECT COALESCE(category, 'غير مصنف'), COUNT(*) 
            FROM medicines 
            GROUP BY COALESCE(category, 'غير مصنف')
            ORDER BY COUNT(*) DESC
            LIMIT 5
        """)
        
        self.create_pie_chart_simple(chart2_frame, categories)
        
        tables_frame = tk.Frame(content_frame, bg=self.get_bg_color())
        tables_frame.pack(fill="both", expand=True, pady=10)
        
        lowstock_frame = tk.LabelFrame(tables_frame, text="⚠️ الأدوية منخفضة المخزون (أقل من 10)", 
                                        font=("Arial", 11, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        lowstock_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        lowstock_cols = ("name", "quantity", "price")
        lowstock_tree = ttk.Treeview(lowstock_frame, columns=lowstock_cols, show="headings", height=6)
        lowstock_tree.heading("name", text="اسم الدواء")
        lowstock_tree.heading("quantity", text="الكمية")
        lowstock_tree.heading("price", text=f"السعر ({settings.currency_symbol})")
        lowstock_tree.column("name", width=120)
        lowstock_tree.column("quantity", width=60)
        lowstock_tree.column("price", width=70)
        
        scroll1 = ttk.Scrollbar(lowstock_frame, orient="vertical", command=lowstock_tree.yview)
        lowstock_tree.configure(yscrollcommand=scroll1.set)
        lowstock_tree.pack(side="left", fill="both", expand=True)
        scroll1.pack(side="right", fill="y")
        
        low_stock_items = db.fetch_all("SELECT name, quantity, price FROM medicines WHERE quantity < 10 AND quantity > 0 ORDER BY quantity LIMIT 10")
        for item in low_stock_items:
            lowstock_tree.insert("", "end", values=(item[0], item[1], f"{item[2]:.2f}"))
        
        invoices_frame = tk.LabelFrame(tables_frame, text="🕐 آخر 5 فواتير", 
                                        font=("Arial", 11, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        invoices_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        invoice_cols = ("number", "customer", "amount", "date")
        invoice_tree = ttk.Treeview(invoices_frame, columns=invoice_cols, show="headings", height=6)
        invoice_tree.heading("number", text="رقم الفاتورة")
        invoice_tree.heading("customer", text="العميل")
        invoice_tree.heading("amount", text=f"المبلغ ({settings.currency_symbol})")
        invoice_tree.heading("date", text="التاريخ")
        invoice_tree.column("number", width=100)
        invoice_tree.column("customer", width=100)
        invoice_tree.column("amount", width=70)
        invoice_tree.column("date", width=80)
        
        scroll2 = ttk.Scrollbar(invoices_frame, orient="vertical", command=invoice_tree.yview)
        invoice_tree.configure(yscrollcommand=scroll2.set)
        invoice_tree.pack(side="left", fill="both", expand=True)
        scroll2.pack(side="right", fill="y")
        
        recent_invoices = db.fetch_all("SELECT invoice_number, customer_name, final_amount, date(created_at) FROM invoices ORDER BY id DESC LIMIT 5")
        for inv in recent_invoices:
            invoice_tree.insert("", "end", values=(inv[0], inv[1][:15] if inv[1] else "نقدي", f"{inv[2]:.2f}", inv[3]))
        
        expired_frame = tk.LabelFrame(content_frame, text="❌ أدوية منتهية الصلاحية", 
                                       font=("Arial", 11, "bold"), bg=self.get_bg_color(), fg=self.get_fg_color())
        expired_frame.pack(fill="x", pady=5)
        
        expired_cols = ("name", "expiry_date", "quantity", "supplier")
        expired_tree = ttk.Treeview(expired_frame, columns=expired_cols, show="headings", height=4)
        expired_tree.heading("name", text="اسم الدواء")
        expired_tree.heading("expiry_date", text="تاريخ الصلاحية")
        expired_tree.heading("quantity", text="الكمية")
        expired_tree.heading("supplier", text="المورد")
        
        for col in expired_cols:
            expired_tree.column(col, width=100)
        
        scroll3 = ttk.Scrollbar(expired_frame, orient="vertical", command=expired_tree.yview)
        expired_tree.configure(yscrollcommand=scroll3.set)
        expired_tree.pack(side="left", fill="both", expand=True)
        scroll3.pack(side="right", fill="y")
        
        expired_items = db.fetch_all("SELECT name, expiry_date, quantity, supplier FROM medicines WHERE expiry_date < date('now') AND quantity > 0")
        for item in expired_items:
            expired_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] if item[3] else "-"))
        
        refresh_btn = tk.Button(content_frame, text="🔄 تحديث البيانات", command=self.show_advanced_dashboard,
                                bg=settings.primary_color, fg="white", font=("Arial", 11), padx=20, pady=5)
        refresh_btn.pack(pady=10)
    
    def create_simple_chart(self, parent, labels, values, title):
        chart_canvas = tk.Canvas(parent, bg=self.get_bg_color(), height=180, highlightthickness=0)
        chart_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        if not values or max(values) == 0:
            chart_canvas.create_text(200, 80, text="لا توجد بيانات كافية", fill=self.get_fg_color(), font=("Arial", 12))
            return
        
        width = chart_canvas.winfo_reqwidth() if chart_canvas.winfo_reqwidth() > 100 else 400
        height = 150
        bar_width = (width - 60) / len(labels) - 4
        
        max_val = max(values)
        for i, (label, value) in enumerate(zip(labels, values)):
            x1 = 30 + i * (bar_width + 4)
            bar_height = (value / max_val) * (height - 40)
            y1 = height - bar_height
            x2 = x1 + bar_width
            y2 = height - 10
            
            color = "#3498db" if value > 0 else "#bdc3c7"
            chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            chart_canvas.create_text(x1 + bar_width/2, height - 5, text=label, angle=45, anchor="ne", font=("Arial", 7), fill=self.get_fg_color())
            chart_canvas.create_text(x1 + bar_width/2, y1 - 5, text=f"{value:.0f}", font=("Arial", 8), fill=self.get_fg_color())
    
    def create_pie_chart_simple(self, parent, data):
        pie_canvas = tk.Canvas(parent, bg=self.get_bg_color(), height=180, highlightthickness=0)
        pie_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        if not data:
            pie_canvas.create_text(200, 80, text="لا توجد بيانات", fill=self.get_fg_color(), font=("Arial", 12))
            return
        
        colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c", "#e67e22"]
        total = sum(row[1] for row in data)
        
        if total == 0:
            pie_canvas.create_text(200, 80, text="لا توجد بيانات", fill=self.get_fg_color(), font=("Arial", 12))
            return
        
        start_angle = 0
        legend_y = 20
        cx, cy = 120, 90
        radius = 60
        
        for i, (cat, count) in enumerate(data):
            angle = (count / total) * 360
            color = colors[i % len(colors)]
            pie_canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius, 
                                   start=start_angle, extent=angle, fill=color, outline="white")
            start_angle += angle
            
            pie_canvas.create_rectangle(220, legend_y-8, 240, legend_y+8, fill=color, outline="")
            pie_canvas.create_text(245, legend_y, text=f"{cat}: {count}", anchor="w", font=("Arial", 8), fill=self.get_fg_color())
            legend_y += 18
    
    # ---------------------------- دوال مساعدة ----------------------------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def toggle_theme(self):
        settings.theme = "dark" if settings.theme == "light" else "light"
        settings.save_settings()
        
        style = ttk.Style()
        if settings.theme == "dark":
            style.theme_use("clam")
            style.configure("Treeview", background="#2d2d2d", foreground="white", fieldbackground="#2d2d2d")
            style.configure("Treeview.Heading", background="#3d3d3d", foreground="white")
            style.configure("TCombobox", fieldbackground="#2d2d2d", background="#2d2d2d", foreground="white")
        else:
            style.theme_use("default")
            style.configure("Treeview", background="white", foreground="black")
            style.configure("Treeview.Heading", background="#e0e0e0", foreground="black")
        
        if self.current_user:
            self.show_main_dashboard()
        
        mode = "الليلي" if settings.theme == "dark" else "النهاري"
        messagebox.showinfo("تم التبديل", f"تم التبديل إلى الوضع {mode}")
    
    def logout(self):
        self.current_user = None
        self.current_user_id = None
        self.current_user_role = None
        self.current_customer_id = None
        self.show_login()
    
    def change_background(self):
        file_path = filedialog.askopenfilename(
            title="اختر صورة الخلفية",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            settings.background_image = file_path
            settings.save_settings()
            if self.current_user:
                self.show_main_dashboard()
            messagebox.showinfo(trans.get('success'), "تم تغيير الخلفية بنجاح")
    
    def reset_background(self):
        settings.background_image = None
        settings.save_settings()
        if self.current_user:
            self.show_main_dashboard()
        messagebox.showinfo(trans.get('success'), "تم إعادة تعيين الخلفية")
    
    def change_primary_color(self):
        color = colorchooser.askcolor(title="اختر اللون الأساسي")[1]
        if color:
            settings.primary_color = color
            settings.save_settings()
            if self.current_user:
                self.show_main_dashboard()

# ---------------------------- التشغيل ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()
