import subprocess

def getBusnoFromModel(modeln):
    cmd = "ddcutil detect --nousb --brief | grep '"+modeln+"' -B 1 | head -n1 | awk '{$1=$1};1' | sed 's/I2C\ bus:\ \/dev\/i2c-//g'"
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode
    
    if not errcode and out:
        return out.decode().strip()
    else:
        return None

def getbrightness(busno=16):
    cmd="ddcutil -b "+str(busno)+" --brief getvcp 10 | cut -d ' ' -f4"
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode

    return int(out.decode().strip())

def setbrightness(busno=16,brightness_value=50):
    cmd="ddcutil -b "+str(busno)+" --brief setvcp 10 "+str(brightness_value)
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode

    return errcode
