from socket import *
import sys
import getpass

def main():
    if len(sys.argv)<3:
        print('argv is error')
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    s=socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return

    while True:
        print('''
            =============Welcome=============
            --1.注册　　　2.登录　　 3.退出--
            =================================
            ''')

        try:
            cmd=int(input('输入选项>>'))
        except Exception as e:
            print('输入错误',e)
            continue

        if cmd not in [1,2,3]:
            print('没有该选项')
            sys.stdin.flush()
            continue
        elif cmd==1:
            r=do_register(s)
            if r==0:
                print('注册成功')
                # login(s,name)
            elif r==1:
                print("用户名存在")
            else:
                print('注册失败') 

        elif cmd==2:
            name=do_login(s) 
            if name:
                print('登录成功')
                login(s,name)
            else:
                print('用户名或密码不正确')
        elif cmd==3:
            s.send(b'E')
            sys.exit('谢谢使用')


def do_register(s):
    while True:
        name=input('请输入用户名：')
        passwd=getpass.getpass()
        passwd1=getpass.getpass('再次输入密码：')

        if (' ' in name) or (' ' in passwd):
            print('用户名或密码不合法')
            continue
        if passwd!=passwd1:
            print('密码不一致，请重新输入')
            continue

        msg='R {} {}'.format(name,passwd)
        s.send(msg.encode())
        data=s.recv(128).decode()

        if data=='ok':
            return 0
        elif data=='EXISTS':
            return 1
        else:
            return 2

def do_login(s):
    while True:
        name=input('请输入用户名：')
        passwd=getpass.getpass()
        # if (' ' in name)or(' ' in passwd):
        #     print('用户名或密码不合法')
        #     continue
        msg='L {} {}'.format(name,passwd)
        s.send(msg.encode())
        data=s.recv(128).decode()
        if data=='ok':
            return name
        else:
            return 

def login(s,name):
    while True:
        print('''
        ==============查询界面==============
        1.查词　　　　2.历史记录　　　　3.退出
        ====================================
        ''')
        try:
            cmd=int(input('输入选项>>'))
        except Exception as e:
            print('输入错误',e)
            continue

        if cmd not in [1,2,3]:
            print('没有该选项')
            sys.stdin.flush()
            continue
        elif cmd==1:
            do_query(s,name)
        elif cmd==2:
            do_hist(s,name)
        elif cmd==3:
            return
            
def do_query(s,name):
    while True:
        word=input('单词：')
        if word=='##':
            break
        msg='Q {} {}'.format(name,word)
        s.send(msg.encode())
        data=s.recv(128).decode()
        if data=='ok':
            data=s.recv(2048).decode()
            print(data)
        else:
            print('没有查到该单词')


def do_hist(s,name):
    msg='H {}'.format(name)
    s.send(msg.encode())
    data=s.recv(128).decode()
    if data=='ok':
        while True:
            data=s.recv(1024).decode()
            if data=='##':
                break
            print(data)
    else:
        print('没有历史记录')



if __name__=='__main__':
    main()
