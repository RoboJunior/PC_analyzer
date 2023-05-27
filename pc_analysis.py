import datetime
import streamlit as st
import psutil
import time
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import matplotlib.pyplot as plt
import plotly.express as px
import platform
import cpuinfo
import wmi

pc = wmi.WMI()
st.set_page_config(layout='wide')
st.header("Realtime pc data analysis 📈")
menu_items = ["About","Real time data","Results"]
menu_icons = ["🔍","📈","📊"]
default_index = 0
select = st.sidebar.selectbox("Menu", menu_items, index=default_index)
if select=="Results":
    t = st.time_input('Set your runtime time', datetime.datetime.now())
    total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(t).split(':'))))
    st.write('Runtime is set for', t)
    user_button = st.button('Submit here to start analyzing your pc')
    cpu_usage = []
    ram_usage = []
    time_now = []
    i = 0
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    if user_button:
        while i<=total_seconds:
            cpu_usage.append(psutil.cpu_percent())
            ram_usage.append(psutil.virtual_memory().percent)
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            time_now.append(curr_time)
            time.sleep(0.5)
            i += 1
        df = pd.DataFrame(cpu_usage,columns=["CPU_Usage"])
        df1 = pd.DataFrame(ram_usage,columns=["Ram_Usage"])
        df3 = pd.DataFrame(time_now,columns=["Time"])
        df.reset_index(drop=True,inplace=True)
        df1.reset_index(drop=True,inplace=True)
        df3.reset_index(drop=True,inplace=True)
        total_df = pd.concat([df,df1,df3],axis=1)
        with st.spinner("Be paitent this might take some time"):
            time.sleep(20)
            st.success("Your data is ready",icon="✅")
            st.dataframe(total_df)
            st.line_chart(total_df)
            df_xlsx = to_excel(total_df)
            st.download_button(label='📥 Download your analysis Results here',
                                    data=df_xlsx ,
                                    file_name= 'Pc_analysis.xlsx')
    else:
        pass

if select == "Real time data":
    st.write("Here the realtime data of your pc is analyzed and its compared with the other parameters visualizing how well is your pc performing under load situations!")
    t = st.time_input('Set your runtime time', datetime.datetime.now())
    total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(t).split(':'))))
    st.write('Runtime is set for', t)
    user_button = st.button('Submit here to start visualizing your pc')
    cpu_usage = []
    ram_usage = []
    time_now = []
    i = 0
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    if user_button:
        data1,data2,data3 = st.columns(3)
        while i<=total_seconds:
            cpu_usage.append(psutil.cpu_percent())
            ram_usage.append(psutil.virtual_memory().percent)
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            time_now.append(curr_time)
            time.sleep(0.5)
            i += 1
        df = pd.DataFrame(cpu_usage,columns=["CPU_Usage"])
        df1 = pd.DataFrame(ram_usage,columns=["Ram_Usage"])
        df3 = pd.DataFrame(time_now,columns=["Time"])
        df.reset_index(drop=True,inplace=True)
        df1.reset_index(drop=True,inplace=True)
        df3.reset_index(drop=True,inplace=True)
        total_df = pd.concat([df,df1,df3],axis=1)
        with st.spinner("Be paitent this might take some time"):
            time.sleep(20)
            st.success("Your data is ready",icon="✅")
        with data1:
            st.markdown("### CPU Load")
            fig = px.line(total_df,x="CPU_Usage",y="Time",title="CPU load regarding the time")
            st.write(fig)
        with data2:   
            st.markdown("### Ram Load")
            fig2 = px.line(total_df,x="Ram_Usage",y="Time",title="Ram load regarding the time")
            st.write(fig2)
        with data3:   
            st.markdown("### CPU and Ram Load")
            fig3 = px.histogram(total_df,x="CPU_Usage",y="Ram_Usage",title="CPU and ram load parallelly")
            st.write(fig3)




if select == "About":
    example_df = pd.read_excel(r"C:/Users/jeyar/Downloads/Pc_analysis (1).xlsx")
    st.write("This is a project which analyses your system cpu and ram usage realtime the realtime data is stored in a csv file so that u can download it for further analysis this program helps you to find out anykind of faulty issues in the system!")
    st.write("This help you to find out that how much of ram and cpu is your pc using realtime even while your playing games or doing work you can monitor the cpu and ram usage and store it so you can refer to the data for any further advancements")
    st.write("Here is an example dataframe where you can view the reatime cpu usage,ram usage and the time")
    st.dataframe(example_df)
    st.write('***Your system specifications are listed here***')
    st.write(f"Architecture: {platform.architecture()}")
    st.write(f"Processor type: {platform.platform()}")
    st.write(f'Operating system: {platform.processor()}')
    my_cpu = cpuinfo.get_cpu_info()
    st.write(f"Processor name: {my_cpu['brand_raw']}")
    st.write(f"Total ram installed: {psutil.virtual_memory().total/1024/1024/1024:.2f} GB")
    st.write(f"Graphics card installed: {pc.Win32_VideoController()[0].name}")



