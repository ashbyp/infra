import psutil, os, socket,  platform


if __name__ == '__main__':
    process_names = [proc.name() for proc in psutil.process_iter()]
    print(process_names)
    print(psutil.cpu_percent())
    print(psutil.cpu_times())
    print(psutil.virtual_memory())
    print(os.getpid())
    print(socket.gethostname())
    print(socket.gethostbyname(socket.gethostname()))
    print(platform.platform())
    print(platform.system())
    print(platform.release())
    print(platform.version())