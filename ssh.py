#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author: nthqn
# @File: .py
# @CreateTime: 5/15/2022 5:46 PM


import os
from ftplib import FTP  # 引入ftp模块
import sys
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


if __name__ == '__main__':
    # 初始化参数为主机地址、用户名、密码，端口号默认为21,如果不是21另行指定即可
    with SSHClient('25.8.2.1', 'hnu_qsl', '870603Vpn$',22) as s:
        stdin, stdout, stderr = s.exec_command("cd /vol6/home/hnu_qsl/hqn/ && mkdir testdir")
        print(stdin, '\n', str(stdout.read()).split('\\n'))
        a=s.upload('C:/Users/nthqn/Downloads/Compressed/expchem3_input_files/chapter_02/e2_03ss.gjf', os.path.join('/vol6/home/hnu_qsl/hqn/job_test_1/','e2_03ss.gjf'))
        stdin, stdout, stderr = s.exec_command("cd /vol6/home/hnu_qsl/hqn/testdir && ls")
        print(stdin, '\n', str(stdout.read()).split('\\n'))


