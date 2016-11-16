#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import paramiko

'''
负责将文件传输到cnr指定的机器
'''

class NeedAuthException(Exception):
    '''need auth exception'''


class ScpSender:

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
        if 'crawler_m4a' not in dirs:
            self.sftp_m4a.mkdir('crawler_m4a')
        self.sftp_m4a.chdir('crawler_m4a')
        self.img_base = self.sftp_m4a.getcwd()
        print(self.img_base)


        '''
        print self.sftp.listdir()
        print self.sftp.put(
            '/Users/xiyuanbupt/sxs/m_interact/files/full/8f6fc95a07d29b3059bdd8966e6c8e54f4787ea9.jpg',
            './8f6fc95a07d29b3059bdd8966e6c8e54f4787ea9.jpg'
        )
        '''

    def put_audio(self, localpath, remotepath):
        sftpAttris = self.sftp_m4a.put(
            localpath, remotepath
        )
        pass
        '''
        sftpAttris = self.sftp.put(localpath,remotepath)
        print sftpAttris
        '''


if __name__ == "__main__":
    scpSender = ScpSender('10.109.247.29', 'wxy', password='jiaohuan')
    '''
    scpSender.put_audio(
        '/Users/xiyuanbupt/sxs/m_interact/files/full/8f6fc95a07d29b3059bdd8966e6c8e54f4787ea9.jpg',
        '8f6fc95a07d29b3059bdd8966e6c8e54f4787ea9.jpg'
    )
    '''
