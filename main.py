import sqlite3
import os

def create_database():
    if os.path.exists("analiz.db"):
        os.remove("analiz.db")

    conn = sqlite3.connect("analiz.db")
    cursor = conn.cursor()
    return conn, cursor

def create_tables(cursor):

    cursor.execute('''
    CREATE TABLE Students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_no INTEGER NOT NULL,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        department varchar(255),
        class INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE Lessons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_code varchar(30),
        lesson_name varchar(255),
        credits INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE Nots(
        student_id INTEGER NOT NULL,
        lesson_id INTEGER NOT NULL,
        midterm float,
        final_exam float,
        average float,
        situation varchar(255)
    )
    ''')

def insert_data(cursor):

    students = [
        (1, 240205400, 'Büşra', 'Işım', 'Yazılım Mühendisliği', 2),
        (2, 240205401, 'Cemre', 'Sevim', 'Genetik Nühendisliği', 1),
        (3, 240205402, 'Yağmur', 'Dinç', 'İktisat', 3),
        (4, 240205403, 'Beyza', 'Girgin', 'Endüstri Mühendisliği', 2),
        (5, 240205404, 'Sıla', 'Bulut', 'Eczacılık', 5),
        (6, 240205405, 'Kartal', 'Yıldırım', 'Tıp', 6),
        (7, 240205406, 'Göktuğ', 'Yılmaz', 'Yapay Zeka Mühendisliği', 4),
        (8, 240205407, 'Selim', 'Aydoğdu', 'Bilgisayar Mühendisliği', 3),
        (9, 240205408, 'Enes', 'Sancar', 'Psikoloji', 3),
        (10, 240205409, 'Serenay', 'Aslan', 'Hukuk', 4),
        (11, 240205409, 'Barlas', 'Eryiğit', 'Yazılım Mühendisliği', 2),
        (12, 240205410, 'Zehra', 'Coşkun', 'Kimya Mühendisliği', 1)
    ]

    cursor.executemany("INSERT INTO Students VALUES (?,?,?,?,?,?)", students)

    lessons = [
        (1, 'YZM211', 'Veri Tabanı Yönetimi', 5),
        (2, 'MAT101', 'Mühendislik Matematiği 1', 7),
        (3, 'FZK102', 'Mühendislik Fiziği 2', 6),
        (4, 'ENG102', 'İngilizce 2', 3),
        (5, 'ECZ501', 'Farmasötik Bakım', 3),
        (6, 'PSK302', 'Kişilik Kuramları', 4),
        (7, 'CHK412', 'Ceza Usul Hukuku', 5),
        (8, 'EKM321', 'Ekonometri', 6),
        (9, 'BLM3O4', 'Gömülü Sistemler', 4),
        (10, 'MBY432', 'Mikrobiyoloji', 5)
    ]

    cursor.executemany("INSERT INTO Lessons VALUES (?,?,?,?)", lessons)

    nots = [
        (1, 1, 70, 80, 76.0, 'Geçti'),
        (2, 2, 45, 55, 51.0, 'Kaldı'),
        (3, 8, 80, 85, 83.0, 'Geçti'),
        (4, 2, 90, 95, 93.0, 'Geçti'),
        (5, 5, 50, 40, 44.0, 'Kaldı'),
        (6, 10, 85, 90, 88.0, 'Geçti'),
        (7, 1, 95, 100, 98.0, 'Geçti'),
        (8, 9, 30, 45, 39.0, 'Kaldı'),
        (9, 6, 75, 80, 78.0, 'Geçti'),
        (10, 7, 55, 60, 58.0, 'Kaldı'),
        (11, 1, 65, 75, 71.0, 'Geçti'),
        (12, 3, 40, 30, 34.0, 'Kaldı')
    ]

    cursor.executemany("INSERT INTO Nots VALUES (?,?,?,?,?,?)", nots)

    print("Data inserted successfully")

def basic_sql_operations(cursor):
    print("----------Full Students Data----------")
    cursor.execute("SELECT * FROM Students")
    records = cursor.fetchall()
    for record in records:
        print(record)

    print("----------Midterm Data----------")
    cursor.execute('''
        SELECT Students.name, Nots.midterm
        FROM Students
        INNER JOIN Nots ON Students.id = Nots.student_id
    ''')
    records = cursor.fetchall()
    for record in records:
        name = record[0]
        midterm = record[1]
        print(f"Name: {name} - Midterm: {midterm}")

def sql_operation(conn, cursor):
    cursor.execute("INSERT INTO Students Values (13, 240205411, 'Cenk', 'Şen', 'Makine Mühendisliği', 2)")
    conn.commit()

    cursor.execute("UPDATE Students SET class = 3 WHERE student_no = 240205405")
    conn.commit()

    cursor.execute("DELETE FROM Students WHERE student_no = 240205410")

def aggregate_functions(cursor):
    cursor.execute("SELECT COUNT(*) FROM Students")
    records = cursor.fetchall()
    for record in records:
        print("----------Student Count----------")
        print(record[0])

    cursor.execute("SELECT MAX(final_exam) FROM Nots")
    max_final_exam = cursor.fetchall()
    print("----------Max Final Not----------")
    print(max_final_exam[0])

    cursor.execute("SELECT AVG(average) FROM Nots")
    records = cursor.fetchall()
    for record in records:
        print("----------Students Average Not----------")
        print(record[0])

def main():
    conn, cursor = create_database()

    try:
        create_tables(cursor)
        insert_data(cursor)
        sql_operation(conn, cursor)
        basic_sql_operations(cursor)
        aggregate_functions(cursor)
        conn.commit()

    except sqlite3.Error as e:
        print(e)

    finally:
        conn.close()

if __name__ == '__main__':
    main()
