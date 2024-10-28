import customtkinter
import cv2
from PIL import Image, ImageTk
import os
import json
import warnings
import datetime
import time
import shutil
from tkinter import messagebox


# 忽略CTkImage赋值警告
warnings.filterwarnings('ignore', category=UserWarning)

# 主题设置
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")


# 创建窗口
app = customtkinter.CTk()
app.geometry("1200x600+50+50")
app.title('签到程序')


# 设置文件夹路径
folder = '_internal/images/'


# 检查并清空文件夹
def clear_folder(folder):
    shutil.rmtree(folder)
    os.mkdir(folder)


with open('_internal/json_statistics.json', 'r', encoding='utf-8') as f:
    f_statistics = json.load(f)
clear_view = list(f_statistics.keys())
try:
    last_view = clear_view[-1]
    last_time_view = last_view[0:-9]
    if last_time_view == datetime.datetime.today().strftime('%Y-%m-%d'):
        pass
    else:
        clear_folder(folder)
except Exception as e:
    pass


# 签到页函数
def sign_in():
    _time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    name = opm.get()
    if name == '无':
        messagebox.showinfo('错误', '姓名不可为无！')
    else:
        with open('_internal/json_statistics.json', 'r', encoding='utf-8') as f:
            f_statistics = json.load(f)
        _list = list(f_statistics.keys())
        try:
            last = _list[-1]
            last_time = last[0:-9]
            if last_time == datetime.datetime.today().strftime('%Y-%m-%d'):
                f_statistics[_time] = f"{name}------{_time}"
            else:
                f_statistics[_time] = f"↓-------------↓ 以下为 {datetime.datetime.today().strftime('%Y-%m-%d')}↓-------------↓"
                messagebox.showinfo('请稍等', '请稍等，点击确定以继续~~')
                time.sleep(1)
                f_statistics[f'{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'] = f"{name}------{_time}"
        except:
            f_statistics[_time] = f"{name}------{_time}"
        with open('_internal/json_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(f_statistics, f)

        name_time = datetime.datetime.now().strftime('%H:%M')
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite(f'_internal/images/{name}.jpg', frame)
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo('签到成功', f'{name}签到成功！')


# 选项菜单values获取
with open('_internal/json_name_list.json', "r", encoding='utf-8') as f:
    file_name_dict = json.load(f)
    file_name_list = list(file_name_dict.values())


# 历史统计为空时显示的文本
def lbl_htry_sta():
    label_htry_sta = customtkinter.CTkLabel(master=tab.tab('统计'))
    label_htry_sta.configure(text='暂无统计文件', font=customtkinter.CTkFont(size=50), bg_color='white')
    label_htry_sta.place(relx=0.5, rely=0.5, anchor='center')


# 历史签到统计页代码
with open('_internal/json_statistics.json', 'r', encoding='utf-8') as f:
    dict_statistics = json.load(f)
list_statistics = list(dict_statistics.values())
content_statistics = '\n'.join(list_statistics)


# 查看图片文件夹下是否有文件
def view_file(folder_path):
    for dirname, subdirs, files in os.walk(folder_path):
        if not files:
            lbl_nofile()
        else:
            pass


# 获取文件中的图片

def load_images(folder):
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            path = os.path.join(folder, filename)
            image = Image.open(path)
            img = ImageTk.PhotoImage(image)
            label = customtkinter.CTkLabel(scrollable_frame, image=img, text='')
            label.pack()
            label_text = customtkinter.CTkLabel(scrollable_frame, text=f'{filename}\n',
                                                font=customtkinter.CTkFont(size=20))
            label_text.pack()


# 今日统计页面未检测到摄像头是的文本组件
def lbl_td_sta():
    label_td_sta = customtkinter.CTkLabel(master=tab.tab('今日'))
    label_td_sta.configure(text='未检测到摄像头', font=customtkinter.CTkFont(size=50))
    label_td_sta.place(relx=0.5, rely=0.5, anchor='center')


# 图片文件夹下没有内容时显示的文本内容
def lbl_nofile():
    label_nofile = customtkinter.CTkLabel(master=tab.tab('今日'))
    label_nofile.configure(text='未找到图片文件', font=customtkinter.CTkFont(size=50))
    label_nofile.place(relx=0.5, rely=0.5, anchor='center')


# 管理员密码验证函数
def verify_admin_pwd():
    with open('_internal/_json_pwd.json', 'r', encoding='utf-8') as f:
        f_admin_pwd = json.load(f)
        if f_admin_pwd['管理员密码'] == en_admin_pwd.get():
            frame_admin()
        else:
            messagebox.showinfo('密码错误', '密码错误，请重新输入！')


# 选项窗口组件
tab = customtkinter.CTkTabview(master=app)
tab.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.9)

tab.add("签到")
tab.add("统计")
tab.add('今日')
tab.add("管理")
tab.set("签到")


# 签到页
lbl_sign = customtkinter.CTkLabel(master=tab.tab('签到'))
lbl_sign.configure(text='签到', font=customtkinter.CTkFont(size=60))
lbl_sign.place(relx=0.5, rely=0.2, anchor="center")

opm = customtkinter.CTkOptionMenu(master=tab.tab('签到'), values=file_name_list)
opm.set('无')
opm.configure(font=customtkinter.CTkFont(size=40))
opm.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.2, relheight=0.1)

button_1 = customtkinter.CTkButton(master=tab.tab("签到"))
button_1.configure(text='签到', command=sign_in, font=customtkinter.CTkFont(size=40),
                   border_width=3, corner_radius=10)
button_1.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.3, relheight=0.2)


# 历史签到统计页
textbox = customtkinter.CTkTextbox(tab.tab('统计'))
textbox.configure(font=customtkinter.CTkFont(size=40))
textbox.place(x=0, y=0, relwidth=1, relheight=1)
if not content_statistics:
    lbl_htry_sta()
textbox.insert("0.0", f"{content_statistics}")


# 今日统计页
scrollable_frame = customtkinter.CTkScrollableFrame(tab.tab('今日'))
scrollable_frame.place(relwidth=1, relheight=1)

# 检测是否有摄像头并查看图片文件是否存在
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    lbl_td_sta()
else:
    view_file(folder)
    load_images(folder)
# 释放资源
cap.release()
cv2.destroyAllWindows()


# 管理员密码验证页
labal_admin = customtkinter.CTkLabel(master=tab.tab('管理'))
labal_admin.configure(text='管理员登录', font=customtkinter.CTkFont(size=50))
labal_admin.place(relx=0.5, rely=0.2, anchor="center")

en_admin_pwd = customtkinter.CTkEntry(master=tab.tab('管理'))
en_admin_pwd.configure(placeholder_text="管理员密码", font=customtkinter.CTkFont(size=30), show='*')
en_admin_pwd.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.4, relheight=0.1)

button_admin = customtkinter.CTkButton(master=tab.tab('管理'))
button_admin.configure(text="提交", command=verify_admin_pwd, font=customtkinter.CTkFont(size=40), border_width=3,
                       corner_radius=10)
button_admin.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.4, relheight=0.2)


# 管理员管理页编辑成员函数
def add_members():
    window_add_mem = customtkinter.CTkInputDialog(title='添加成员', text='请输入成员姓名：')
    window_add_mem.geometry('100+100')

    add_name = window_add_mem.get_input()
    time_add_mem = datetime.datetime.now().strftime('%H:%M:%S')
    with open('_internal/json_name_list.json', "r", encoding='utf-8') as f:
        name_dict_add = json.load(f)
    name_dict_add[time_add_mem] = add_name
    json.dump(name_dict_add, open('_internal/json_name_list.json', "w", encoding='utf-8'))
    messagebox.showinfo('Success', '成员添加成功！')


# 管理员管理页删除成员函数
def del_members():
    window_del_mem = customtkinter.CTkInputDialog(title='删除成员', text='请输入成员姓名：')
    window_del_mem.geometry('100+100')
    del_neme = window_del_mem.get_input()
    with open('_internal/json_name_list.json', "r", encoding='utf-8') as f:
        del_name_dict = json.load(f)
    new_name_dict = {key: value for key, value in del_name_dict.items() if value != del_neme}
    json.dump(new_name_dict, open('_internal/json_name_list.json', "w", encoding='utf-8'))
    messagebox.showinfo('Success', '成员删除成功！')


# 管理员管理页修改密码函数
def change_pwd():
    def but_get_np():
        new_pwd = en_new_pwd.get()
        with open('_internal/_json_pwd.json', "r", encoding='utf-8') as f:
            pwd_dict = json.load(f)
            pwd_dict['管理员密码'] = new_pwd
        json.dump(pwd_dict, open('_internal/_json_pwd.json', "w", encoding='utf-8'))
        messagebox.showinfo('Success', '密码修改成功！')
        window_change_pwd.destroy()

    window_change_pwd = customtkinter.CTk()
    window_change_pwd.geometry('300x300+100+100')

    en_new_pwd = customtkinter.CTkEntry(master=window_change_pwd, placeholder_text='请输入新密码',
                                        font=customtkinter.CTkFont(size=20), show='#')
    en_new_pwd.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.6, relheight=0.2)

    butt_get_np = customtkinter.CTkButton(master=window_change_pwd, text='提交', command=but_get_np,
                                          font=customtkinter.CTkFont(size=20))
    butt_get_np.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.6, relheight=0.2)

    window_change_pwd.mainloop()


# 管理员清空历史统计函数
def clear_json_sta():
    statistics_dict_clear = {}
    json.dump(statistics_dict_clear, open('_internal/json_statistics.json', "w", encoding='utf-8'))
    messagebox.showinfo('Success', '已清空！')


# 管理员管理页
def frame_admin():
    frame_admin = customtkinter.CTkFrame(master=tab.tab('管理'))
    frame_admin.place(relwidth=1, relheight=1)

    button_frame_edit = customtkinter.CTkButton(master=frame_admin)
    button_frame_edit.configure(text='添加成员', command=add_members,
                                font=customtkinter.CTkFont(size=40), border_width=3, corner_radius=10)
    button_frame_edit.place(relx=0.5, rely=0.15, anchor="center", relwidth=0.4, relheight=0.2)

    button_frame_edit = customtkinter.CTkButton(master=frame_admin)
    button_frame_edit.configure(text='删除成员', command=del_members, font=customtkinter.CTkFont(size=40),
                                border_width=3, corner_radius=10)
    button_frame_edit.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.4, relheight=0.2)

    button_modify_pwd = customtkinter.CTkButton(master=frame_admin)
    button_modify_pwd.configure(text='修改密码', command=change_pwd,
                                font=customtkinter.CTkFont(size=40), border_width=3, corner_radius=10)
    button_modify_pwd.place(relx=0.5, rely=0.65, anchor="center", relwidth=0.4, relheight=0.2)

    button_clear_sta = customtkinter.CTkButton(master=frame_admin)
    button_clear_sta.configure(text='清空历史统计', command=clear_json_sta,
                               font=customtkinter.CTkFont(size=40), border_width=3, corner_radius=10)
    button_clear_sta.place(relx=0.5, rely=0.9, anchor="center", relwidth=0.4, relheight=0.2)


# 署名/签名
lbl_signature = customtkinter.CTkLabel(master=app, text='The program was written by Tuo423')
lbl_signature.pack(side="bottom")


app.mainloop()
