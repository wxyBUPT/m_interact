#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

'''
负责将文件传输到cnr指定的机器
'''
import paramiko

from conf_util import ConfUtil

class NeedAuthException(Exception):
    '''need auth exception'''

class ScpSender:

    m4a_dir = ConfUtil.getTranscodeServerM4aDir()
    jpg_dir = ConfUtil.getTranscodeServerJpgDir()

    def __init__(self, host, user, port=22, password=None, keyfile=None):
        self.ssh = paramiko.SSHClient()
        # 可以连接不在knownhost 的服务器
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if password:
            self.ssh.connect(host, port, user, password)
        elif keyfile:
            self.ssh.connect(host, port, username=user, key_filename=keyfile)
        else:
            raise NeedAuthException
        self.sftp_m4a = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        self.sftp_jpg = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        dirs = self.sftp_m4a.listdir()
        if self.m4a_dir not in dirs:
            self.sftp_m4a.mkdir(self.m4a_dir)
        self.sftp_m4a.chdir(self.m4a_dir)

        self.audio_base = self.sftp_m4a.getcwd()
        if self.jpg_dir not in dirs:
            self.sftp_jpg.mkdir(self.jpg_dir)
        self.sftp_jpg.chdir(self.jpg_dir)
        self.img_base = self.sftp_jpg.getcwd()

    def put_audio(self, localpath, remotepath):
        pass
