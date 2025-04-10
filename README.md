
# 🕵️‍♂️ Streamlit App: Cheat Detection for Online Exams

**CHEATDETECTION** adalah aplikasi berbasis Streamlit yang dirancang untuk mendeteksi potensi kecurangan dalam pelaksanaan tes atau ujian online. Aplikasi ini memanfaatkan teknologi **OpenCV**, **Deep Learning**, serta **gaze tracking** dan pengenalan wajah untuk mendeteksi aktivitas mencurigakan selama ujian berlangsung.

## 🚀 Fitur Utama

- 🔐 **Login Akun**: Akses peserta dan pengawas berbeda.
- 🎥 **Monitoring Real-Time**: Mendeteksi perilaku mencurigakan seperti melihat ke samping, tidak melihat layar, dan banyak lagi.
- 📸 **Pengambilan Screenshot Otomatis**: Menyimpan bukti visual dari momen mencurigakan.
- 📄 **Laporan dan Analisis**: Menampilkan data hasil pengawasan dalam bentuk tabel dan visualisasi interaktif menggunakan Plotly.
- 📤 **Ekspor CSV**: Laporan dapat diunduh untuk keperluan dokumentasi atau audit.

## 🧰 Teknologi yang Digunakan

- `Python`
- `Streamlit`
- `OpenCV`
- `Deep Learning (dlib, face landmarks)`
- `Pandas`, `Numpy`
- `Plotly`, `st_aggrid`

## 📁 Struktur Direktori

```
├── main.py
├── facemain.py
├── facedetector.py
├── facetraining.py
├── facerecognition.py
├── facelandmarks.py
├── objectdetection.py
├── mouthdetector.py
├── dataset/
├── models/
├── img/
├── trainer/
├── gaze_tracking/
├── Cascades/
├── requirements.txt
└── README.md
```

## 🧪 Cara Menjalankan

1. Clone repository ini:
    ```bash
    git clone https://github.com/alexandertiopan1212/Streamlit_App_Cheat_Detection.git
    cd Streamlit_App_Cheat_Detection
    ```

2. Buat virtual environment dan install dependensi:
    ```bash
    pip install -r requirements.txt
    ```

3. Jalankan aplikasi:
    ```bash
    streamlit run main.py
    ```

## 🧪 Akun Uji Coba

| Role      | Username  | Password |
|-----------|-----------|----------|
| Peserta   | raff      | 123      |
| Peserta   | Dyah      | 123      |
| Peserta   | Yusuf     | 123      |
| Pengawas  | Pengawas  | 123      |

## 📸 Contoh Screenshot

_Tambahkan contoh screenshot antarmuka aplikasi dan hasil deteksi di sini._

---

## 🏷️ Tags

`streamlit` `cheating detection` `online exam` `opencv` `face detection` `gaze tracking` `deep learning` `education tech` `python project`

## 👨‍💻 Kontributor

- **Alexander Tiopan** – _Developer & AI Engineer_

---
