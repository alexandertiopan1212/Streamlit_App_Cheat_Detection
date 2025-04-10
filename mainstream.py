# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid
from st_aggrid.shared import JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import base64

def ReadPictureFile(wch_fl):
    try:
        return base64.b64encode(open(wch_fl, 'rb').read()).decode()

    except:
        return ""



ShowImage = JsCode("""function (params) {
            var element = document.createElement("span");
            var imageElement = document.createElement("img");
        
            if (params.data.image_url != '') {
                imageElement.src = params.data.ImgPath;
                imageElement.width="200";
                imageElement.height="200";
            } else { imageElement.src = ""; }
            element.appendChild(imageElement);
            return element;
            }""")

# Import .py file
from facemain import run_facemain




# Main function
def main():
    st.title(':blue[CHEATDETECTION]')
    st.header('_:blue[Aplikasi Pendeteksi Kecurangan Tes Online]_')
    st.write("""
Aplikasi ini digunakan untuk mendeteksi kecurangan dalam tes atau ujian online berbasis opencv dan deep learning.
             """)
    
    # Session handling
    if 'login_accepted' not in st.session_state:
        st.session_state.login_accepted = 0
    
    if 'cheat_report' not in st.session_state:
        st.session_state.cheat_report = []

    if 'username' not in st.session_state:
        st.session_state.username = ''

    if 'password' not in st.session_state:
        st.session_state.password = ''

    if 'df_f' not in st.session_state:
        st.session_state.df_f = []
    


    # Sidebar initiation
    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Home", ["Default", "Akun", "Mulai Ujian", "Keluar"])
    menu2 = st.sidebar.selectbox("Laporan", ["Default", "Laporan Kecurangan", "Analisis"])


    if menu == "Akun" and menu2 == "Default":
        st.subheader("Selamat Datang. Silahkan Masuk.")
        st.session_state.username = st.text_input("Username")
        st.session_state.password = st.text_input("Password", type="password")
        login_button = st.button("Masuk")

        if st.session_state.username == "raff" and st.session_state.password == "123" and login_button:
            st.success(f"Selamat Datang {st.session_state.username}. Akun Berhasil Masuk. Silahkan Akses Menu Lain.")
            st.session_state.login_accepted = 1
        
        if st.session_state.username == "Dyah" and st.session_state.password == "123" and login_button:
            st.success(f"Selamat Datang {st.session_state.username}. Akun Berhasil Masuk. Silahkan Akses Menu Lain.")
            st.session_state.login_accepted = 1

        if st.session_state.username == "Yusuf" and st.session_state.password == "123" and login_button:
            st.success(f"Selamat Datang {st.session_state.username}. Akun Berhasil Masuk. Silahkan Akses Menu Lain.")
            st.session_state.login_accepted = 1

        if st.session_state.username == "Pengawas" and st.session_state.password == "123" and login_button:
            st.success(f"Selamat Datang {st.session_state.username}. Akun Berhasil Masuk. Silahkan Akses Menu Lain.")
            st.session_state.login_accepted = 2

        
    if menu == "Mulai Ujian" and menu2 == "Default":
        if st.session_state.login_accepted == 1:
            st.subheader("Masukkan Lama Waktu Ujian (dalam detik)")
            waktu_ujian = st.number_input("Waktu Ujian:", min_value=3, step=1)
            if st.button("Mulai Ujian"):
                st.subheader("Selamat Datang. Silahkan Mulai Ujian.")
                st.session_state.cheat_report = run_facemain(waktu_ujian)
                st.subheader("UJIAN SELESAI")
        
        if st.session_state.login_accepted == 2:
            st.subheader("Anda masuk sebagai pengawas. Menu tidak bisa diakses.")
        
        if st.session_state.login_accepted == 0:
            st.subheader("Anda Belum Login. Silahkan Login atau Daftar Terlebih Dahulu.")

    if menu == "Keluar" and menu2 == "Default":
        if st.session_state.login_accepted == 1 or st.session_state.login_accepted == 2:
            st.subheader("Ingin Keluar dari Aplikasi?")
            logout_button = st.button("Keluar")
            cancel_logout_button = st.button("Batalkan")
            if logout_button:
                st.session_state.login_accepted = 0

            if cancel_logout_button:
                st.write("Proses Keluar dibatalkan. Silahkan Kembali Akses Menu Lain.")

        if st.session_state.login_accepted == 0:
            st.subheader("Anda Belum Login. Silahkan Login atau Daftar Terlebih Dahulu.")


    if menu2 == "Laporan Kecurangan" and menu == "Default":
        if st.session_state.login_accepted == 2:
            st.subheader("Laporan Kecurangan:")

            df = pd.DataFrame(st.session_state.cheat_report, columns = ["Nama", "Waktu", "Kecurangan Lihat", "Notifikasi", "Screenshoot", "ImgPath"])
            for i in range(len(df['Screenshoot'])):
                from PIL import Image
                df['Screenshoot'][i] = Image.fromarray(df['Screenshoot'][i])
                df['Screenshoot'][i].save('img/' + df["Nama"][i] + str(i) + '.jpg')
                df['ImgPath'][i] = 'img/' + df["Nama"][i] + str(i) + '.jpg'
                imgExtn = df['ImgPath'][i][-4:]
                df['ImgPath'][i] = f'data:image/{imgExtn};base64,' + ReadPictureFile(df['ImgPath'][i])

            st.session_state.df_f.append(df)

            df_n = pd.concat(st.session_state.df_f, axis=0)

            defaultColDef = {
            "filter": True,
            "resizable": True,
            "sortable": True,
            
            }
            
            gb = GridOptionsBuilder.from_dataframe(df_n)
            gb.configure_default_column(**defaultColDef)
            gb.configure_column('Screenshoot', cellRenderer=ShowImage)
            gb.configure_column("ImgPath", hide = "True")
            gb.configure_grid_options(rowHeight=300)
 

            vgo = gb.build()
            AgGrid(df_n, gridOptions=vgo, theme='blue', height=800, allow_unsafe_jscode=True )


            df_ = df[["Waktu", "Kecurangan Lihat", "Notifikasi"]]
            # st.dataframe(df_, 1000, 300)

            def convert_df(df_):
                return df_.to_csv(index=False).encode('utf-8')
        
            csv = convert_df(df_)

            st.download_button(
                "Press to Download",
                csv,
                f"Hasil.csv",
                "text/csv",
                key='download-csv')
        
        if st.session_state.login_accepted == 1:
            st.subheader("Anda masuk sebagai peserta. Menu tidak bisa diakses.")

    if menu2 == "Analisis" and menu == "Default":
        if st.session_state.login_accepted == 2:
            st.subheader("Analisis")
            df_n = pd.concat(st.session_state.df_f, axis=0)
            # st.write(df_n)
            df_ = df_n[["Waktu", "Kecurangan Lihat", "Notifikasi"]]
            df_['size'] = 10

            # Create scatter plot
            fig = px.scatter(df_,
            x = "Waktu",
            y = "Kecurangan Lihat",
            title = f"Kecurangan Lihat",
            size = "size")
                    
            # Plot
            st.plotly_chart(fig, use_container_width=True)

            # Create scatter plot
            fig = px.scatter(df_,
            x = "Waktu",
            y = "Notifikasi",
            title = f"Notifikasi Person",
            size = "size")
                    
            # Plot
            st.plotly_chart(fig, use_container_width=True)

        if st.session_state.login_accepted == 1:
            st.subheader("Anda masuk sebagai peserta. Menu tidak bisa diakses.")



if __name__ == '__main__':
    main()