#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author: nthqn
# @File: .py
# @CreateTime: 5/14/2022 7:34 PM
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *  # 首先导入包
import re
import os
import paramiko


class SSHClient(object):

    def __init__(self, host, username, password, port=22):

        self.client = None
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def exec_command(self, command, timeout=6000):
        return self.client.exec_command(command, timeout=timeout)

    def invoke_shell(self):
        return self.client.invoke_shell()

    def callback(self, current, total):
        print('文件大小为: {}, 已经下载了: {}'.format(total, current))

    def download(self, from_path, to_path):
        sftp_client = paramiko.SFTPClient.from_transport(self.client.get_transport())
        sftp_client.get(from_path, to_path, callback=self.callback)
        sftp_client.close()

    def upload(self, from_path, to_path):
        sftp_client = paramiko.SFTPClient.from_transport(self.client.get_transport())
        sftp_client.put(from_path, to_path, callback=self.callback)
        sftp_client.close()

    def __enter__(self):
        if self.client is not None:
            raise RuntimeError('SSH already connected.')
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.client.connect(self.host, self.port, self.username, self.password)
        except Exception as e:
            raise RuntimeError('Connect to {} failed, {}.'.format(self.host, e.message))
        return self

    def __exit__(self, *args):
        if self.client is not None:
            try:
                self.client.close()
            except:
                pass
            finally:
                if self.client is not None:
                    self.client.close()


class gau():


    global file_list
    global name_list
    global bsh_list
    global info
    info=''
    file_list=[]
    name_list=[]
    bsh_list=[]
    def __init__(self,name,path,host,username,password):
        self.name=name
        self.remote_path=path
        self.username=username
        self.host=host
        self.password=password

    def set_window(self):
        self.name.title('convertion')
        self.name.geometry('500x200+600+400')
        self.bot1=tk.Button(self.name, text='选择文件', command=self.choice_file)
        self.bot1.grid(row=0,column=20)

        filename=('None',)

        self.fns = self.name.tk.splitlist(filename)
        # self.label['text'] = filename
        self.file = tk.StringVar()
        self.fileChosen = ttk.Combobox(self.name, width=12, textvariable=self.file, state='readonly')
        self.fileChosen['values'] = self.fns  #self.fns 设置下拉列表的值
        self.fileChosen.grid(column=10, row=0,columnspan=10,sticky='ew')  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.fileChosen.current(0)  # 设置下拉列表默认显示的值，0为 fileChosen['values'] 的下标值

        self.label2=tk.Label(text='节点配置：')
        self.label2.grid(column=10, row=3)

        self.label1=tk.Label(text='节点数')
        self.label1.grid(column=10, row=5,columnspan=10,sticky='ew')
        self.text1= tk.Entry()
        self.text1.insert(0, '2')
        self.text1.grid(column=20, row=5,columnspan=10,sticky='ew')



        self.label2=tk.Label(text='核数')
        self.label2.grid(column=40, row=5,columnspan=10,sticky='ew')
        self.text2= tk.Entry()
        self.text2.insert(0, '6')
        self.text2.grid(column=50, row=5,columnspan=10,sticky='ew')

        self.label2=tk.Label(text='计算配置')
        self.label2.grid(column=10, row=6)

        self.label3=tk.Label(text='nproc')
        self.label3.grid(column=10, row=7,columnspan=10,sticky='ew')
        self.text3= tk.Entry()
        self.text3.insert(0, '12')
        self.text3.grid(column=20, row=7,columnspan=10,sticky='ew')

        self.label4=tk.Label(text='内存（GB)')
        self.label4.grid(column=40, row=7,columnspan=10,sticky='ew')
        self.text4= tk.Entry()
        self.text4.insert(0, '20')
        self.text4.grid(column=50, row=7,columnspan=10,sticky='ew')

        self.label5=tk.Label(text='文件夹名')
        self.label5.grid(column=40, row=8,columnspan=10,sticky='ew')
        self.text5= tk.Entry()
        self.text5.insert(0, 'test')
        self.text5.grid(column=50, row=8,columnspan=10,sticky='ew')

        self.labellast = tk.Label(text=info)
        self.labellast.grid(column=20, row=100, columnspan=10)


        self.bot2=tk.Button(self.name, text='上传作业', command=self.comfirm)
        self.bot2.grid(row=10,column=20)

        self.bot3 = tk.Button(self.name, text='提交作业', command=self.start)
        self.bot3.grid(row=10, column=30)
        self.bot4 = tk.Button(self.name, text=' 取消 ', command=self.cancel)
        self.bot4.grid(row=10, column=40)



    def choice_file(self):
        filename = askopenfilenames(title='选择文件', initialdir='w:', filetypes=[('gaussian input file', '*.gjf'),('all','*')])
        print(filename)
        import re
        short=[]
        for i in filename:
            file_list.append(i)
            short_name=i[i.rfind('/')+1:]
            name_list.append(short_name)
            short.append(short_name)
        self.fns = self.name.tk.splitlist(short)
        # self.label['text'] = filename
        self.file = tk.StringVar()
        self.fileChosen = ttk.Combobox(self.name, width=12, textvariable=self.file, state='readonly')
        self.fileChosen['values'] = self.fns  #self.fns 设置下拉列表的值
        self.fileChosen.grid(column=10, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.fileChosen.current(0)  # 设置下拉列表默认显示的值，0为 fileChosen['values'] 的下标值
        return self.fns




    def comfirm(self):

        global info

        node=self.text1.get()
        N=self.text2.get()
        n = self.text3.get()
        mem = self.text4.get()
        dir_name = self.text5.get()
        print(self.host, self.username, self.password)
        # with SSHClient(self.host,self.username,self.password, 22) as s:
        #     stdin, stdout, stderr = s.exec_command('cd ' + self.remote_path +'/ && mkdir '+dir_name)

        for k in file_list:
            long = k[:-4] + '.com'
            short = long[long.rfind('/') + 1:]
            with open(k, 'r+') as f:

                a = f.read()
                s1 = re.findall('%nproc=', a, flags=re.IGNORECASE)
                s2 = re.findall('%mem=', a, flags=re.IGNORECASE)
                s3 = re.findall('%chk=', a, flags=re.IGNORECASE)
                if len(s1) == 0:
                    text = '%nproc=' + n + '\n'
                    a = text + a

                else:
                    new = re.sub('(?<=%nproc=).*?(?=\r?\n|(?<!\n)\r)', n, a, flags=re.IGNORECASE)
                    a = new
                if len(s2) == 0:
                    text = '%mem=' + mem + 'GB\n'

                    a = text + a
                else:
                    new = re.sub('(?<=%mem=).*?(?=\r?\n|(?<!\n)\r)', mem+'GB', a, flags=re.IGNORECASE)
                    a = new
                chk_name=short[:-4]+ '.chk\n'
                if len(s3) == 0:
                    text = '%Chk=' + chk_name
                    a = text + a
                else:
                    new = re.sub('(?<=%Chk=).*?(?=\r?\n|(?<!\n)\r)', chk_name, a, flags=re.IGNORECASE)
                    a = new

            with open(long, 'w') as f2:
                f2.write(a)

            with open('./sh1.txt', 'r+') as f:
                a = f.read()
                a = re.sub('(?<=ntasks-per-node=).*?(?=\r?\n|(?<!\n)\r)',N, a, flags=re.IGNORECASE)
                a = re.sub('(?<=yhrun -p work ).*?(?= hostname -s > hostfile)', '-N '+node+' -n '+N, a, flags=re.IGNORECASE)
                a = re.sub('(?<=SBATCH -N ).*?(?= --ntasks-per-node)', node, a, flags=re.IGNORECASE)
                a = re.sub('(?<=INPUT_FILE=).*?(?=\r?\n|(?<!\n)\r)', short[:-4], a, flags=re.IGNORECASE)
                a = re.sub('(?<=SBATCH -J ).*?(?=\r?\n|(?<!\n)\r)', short[:-4], a, flags=re.IGNORECASE)


            bsh=short[:-4]+'.sh'
            bshl=long[:-4]+'.sh'
            bsh_list.append('' + self.remote_path +'/' + dir_name + '/'+bsh)
            with open(bshl, 'w') as f:
                f.write(a)
            print(self.host,self.username,self.password)
            with SSHClient(self.host,self.username,self.password,22) as s:
                stdin, stdout, stderr = s.exec_command('cd ' + self.remote_path + '/ && mkdir ' + dir_name)
                s.upload(long, os.path.join('' + self.remote_path +'/'+dir_name+'/',short))
                print(short)
                print(bsh)
                s.upload(bshl, os.path.join('' + self.remote_path +'/' + dir_name + '/',bsh ))
        with SSHClient(self.host,self.username,self.password, 22) as s:
            s.upload('./file2.sh', os.path.join('' + self.remote_path +'/' + dir_name + '/', 'file2.sh'))
            stdin, stdout, stderr = s.exec_command('cd ' + self.remote_path +'/' + dir_name + ' && bash file2.sh')
            print(stdin, '\n', str(stdout.read()).split('\\n'))

        print('上传成功')


    def start(self):
        global file_list
        global name_list
        global bsh_list
        dir_name = self.text5.get()
        with SSHClient(self.host,self.username,self.password, 22) as s:
            for k in bsh_list:
                print(k)
                stdin, stdout, stderr = s.exec_command('cd ' + self.remote_path +'/' + dir_name +' && yhbatch '+ k)
                print(stdin, '\n', str(stdout.read()).split('\\n'))
        file_list = []
        name_list = []
        bsh_list = []

        self.labellast = tk.Label(text='任务提交成功')



    def cancel(self):
        global file_list
        global name_list
        global bsh_list
        global short
        short = []
        file_list = []
        name_list = []
        bsh_list = []
        filename=('None',)

        self.fns = self.name.tk.splitlist(filename)
        # self.label['text'] = filename
        self.file = tk.StringVar()
        self.fileChosen = ttk.Combobox(self.name, width=12, textvariable=self.file, state='readonly')
        self.fileChosen['values'] = self.fns  #self.fns 设置下拉列表的值
        self.fileChosen.grid(column=10, row=0,columnspan=10,sticky='ew')  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.fileChosen.current(0)  # 设置下拉列表默认显示的值，0为 fileChosen['values'] 的下标值
        self.labellast = tk.Label(text='已清除')
        self.labellast.grid(column=20, row=100, columnspan=10)
















if __name__ == '__main__':

    with open('remote.config') as f:
        ini=f.readlines()
        path=ini[0][:-1]
        host=ini[1][:-1]
        username=ini[2][:-1]
        password=ini[3][:-1]
    print(ini,path)
    n=tk.Tk(screenName=':0')
    k=gau(n,path,host,username,password)
    k.set_window()
    n.mainloop()