import subprocess

def get_disk_IO_util(device='dev8-0'):
    o = subprocess.getoutput("sar -d 1 1 | grep '" + device + "'").split(' ')
    while '' in o:
        o.remove('')
    # print(o)
    r = o[9].split('\n')
    return r[0]

def get_network_speed(device='eth0'):
    o = subprocess.getoutput("sar -n DEV --iface=eth0 1 1 | grep '" + device + "'").split(' ')
    while '' in o:
        o.remove('')
    # print(o)
    r = {'d': o[4], 'u': o[5]}
    return r

def get_cpu_usage_rate():
    o = subprocess.getoutput("sar -u 1 1").split(' ')
    while '' in o:
        o.remove('')
    # print(o)
    r = float(100) - float(o[len(o)-1])
    return r

def get_mem_usage_rate():
    o = subprocess.getoutput("sar -r 1 1").split(' ')
    while '' in o:
        o.remove('')
    print(o)
    r = o[20]
    return r

if __name__ == '__main__':
    print(get_mem_usage_rate())
    # print(get_network_speed())
    # print(get_disk_IO_util('dev8-0'))
    # print(get_disk_IO_util('dev8-16'))