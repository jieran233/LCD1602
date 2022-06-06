from lcd1602 import *
from datetime import *
# import commands
import subprocess


def get_cpu_temp():
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    cpu_temp='{:.2f}'.format(float(cpu) / 1000) + ' C'
    #print(cpu_temp)
    return cpu_temp


def get_gpu_temp():
    tmp = subprocess.getoutput('vcgencmd measure_temp|awk -F= \'{print $2}\'').replace('\'C', '')
    gpu = float(tmp)
    gpu_temp='{:.2f}'.format(gpu) + ' C'
    #print(gpu_temp)
    return gpu_temp


def get_time_now():
    time_now= datetime.now().strftime('    %H:%M:%S\n   %Y-%m-%d')
    return time_now


def get_ip_info():
    my_ip = subprocess.getoutput('sudo hostname -I').split(' ')[0]
    return my_ip


def get_mem_info():
    men_info = []
    info = subprocess.getoutput('free -m|grep Mem:').split(' ')
    for i in info:
        if i != '':
            men_info.append(i)
        else:
            continue
    men_info_str='Mem: '+men_info[3] + 'M/' + men_info[1] + 'M'
    return men_info_str

def get_disk_info():
    disk_info = []
    info = subprocess.getoutput('df -h | grep /dev/root').split(' ')
    for i in info:
        if i != '':
            disk_info.append(i)
        else:
            continue
    # print(disk_info)
    if (len(info) != 1):
        disk_info_str=disk_info[0] + ' ' + disk_info[4]
        return disk_info_str
    else:
        return ""

def get_usbdisk_info():
    disk_info = []
    info = subprocess.getoutput('df -h | grep /dev/sda2').split(' ')
    for i in info:
        if i != '':
            disk_info.append(i)
        else:
            continue
    # print(disk_info)
    if (len(info) != 1):
        disk_info_str=disk_info[0] + ' ' + disk_info[4]
        return disk_info_str
    else:
        return ""

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
    r = str('%.2f' % (float(100) - float(o[len(o)-1])))
    return r

def get_mem_usage_rate():
    o = subprocess.getoutput("sar -r 1 1").split(' ')
    while '' in o:
        o.remove('')
    # print(o)
    r = o[20]
    return r


lcd = lcd1602()
lcd.clear()

if __name__ == '__main__':

    while True:
        # lcd.clear()
        # lcd.message(get_ip_info()+'\n')
        # lcd.message(get_mem_info())
        # sleep(3)

        line0 = '%CPU ' + get_cpu_usage_rate()
        line1 = '%Mem ' + get_mem_usage_rate()
        lcd.clear()
        lcd.message(line0 + '\n')
        lcd.message(line1)
        sleep(3)

        line0 = '%dev8-0  ' + get_disk_IO_util('dev8-0')
        line1 = '%dev8-16 ' + get_disk_IO_util('dev8-16')
        lcd.clear()
        lcd.message(line0 + '\n')
        lcd.message(line1)
        sleep(3)

        line0 = '< ' + get_network_speed()['u'] + 'KB/s'
        line1 = '> ' + get_network_speed()['d'] + 'KB/s'
        lcd.clear()
        lcd.message(line0 + '\n')
        lcd.message(line1)
        sleep(3)

        # lcd.clear()
        # lcd.message(get_disk_info() + '\n')
        # lcd.message(get_usbdisk_info())
        # sleep(3)

        # lcd.clear()
        # lcd.message('CPU: ' + get_cpu_temp() + '\n')
        # lcd.message('GPU: ' + get_gpu_temp())
        # sleep(3)

