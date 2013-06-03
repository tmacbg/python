#!/usr/bin/python


import sys, os, string
try:
    import hashlib
    md5_new = hashlib.md5
except ImportError:
    import md5
    md5_new = md5.new

if os.geteuid() != 0:
    sys.stderr.write("Sorry, root permission required.\n");
    sys.exit(1)

split_args=False
if len(sys.argv)==2 and sys.argv[1] == "--split-args":
    split_args = True

PAGESIZE=os.sysconf("SC_PAGE_SIZE")/1024 #KiB
our_pid=os.getpid()

def kernel_ver():
    kv=open("/proc/sys/kernel/osrelease", "rt").readline().split(".")[:3]
    for char in "-_":
        kv[2]=kv[2].split(char)[0]
    return (int(kv[0]), int(kv[1]), int(kv[2]))

kv=kernel_ver()

have_pss=0

def getMemStats(pid):
    global have_pss
    mem_id = pid #unique
    Private_lines=[]
    Shared_lines=[]
    Pss_lines=[]
    Rss=int(open("/proc/"+str(pid)+"/statm", "rt").readline().split()[1])*PAGESIZE
    if os.path.exists("/proc/"+str(pid)+"/smaps"): #stat
        digester = md5_new()
        for line in open("/proc/"+str(pid)+"/smaps", "rb").readlines(): #open
            digester.update(line)
            line = line.decode("ascii")
            if line.startswith("Shared"):
                Shared_lines.append(line)
            elif line.startswith("Private"):
                Private_lines.append(line)
            elif line.startswith("Pss"):
                have_pss=1
                Pss_lines.append(line)
        mem_id = digester.hexdigest()
        Shared=sum([int(line.split()[1]) for line in Shared_lines])
        Private=sum([int(line.split()[1]) for line in Private_lines])
        if have_pss:
            pss_adjust=0.5 
            Pss=sum([float(line.split()[1])+pss_adjust for line in Pss_lines])
            Shared = Pss - Private
    elif (2,6,1) <= kv <= (2,6,9):
        Shared=0 
        Private = Rss
    else:
        Shared=int(open("/proc/"+str(pid)+"/statm", "rt").readline().split()[2])
        Shared*=PAGESIZE
        Private = Rss - Shared
    return (Private, Shared, mem_id)

def getCmdName(pid):
    cmdline = open("/proc/%d/cmdline" % pid, "rt").read().split("\0")
    if cmdline[-1] == '' and len(cmdline) > 1:
        cmdline = cmdline[:-1]
    path = os.path.realpath("/proc/%d/exe" % pid) 
    if split_args:
        return " ".join(cmdline)
    if path.endswith(" (deleted)"):
        path = path[:-10]
        if os.path.exists(path):
            path += " [updated]"
        else:
            if os.path.exists(cmdline[0]):
                path = cmdline[0] + " [updated]"
            else:
                path += " [deleted]"
    exe = os.path.basename(path)
    cmd = open("/proc/%d/status" % pid, "rt").readline()[6:-1]
    if exe.startswith(cmd):
        cmd=exe 
    return cmd

cmds={}
shareds={}
mem_ids={}
count={}
for pid in os.listdir("/proc/"):
    if not pid.isdigit():
        continue
    pid = int(pid)
    if pid == our_pid:
        continue
    try:
        cmd = getCmdName(pid)
    except:
        continue
    try:
        private, shared, mem_id = getMemStats(pid)
    except:
        continue 
    if shareds.get(cmd):
        if have_pss: 
            shareds[cmd]+=shared
        elif shareds[cmd] < shared: 
            shareds[cmd]=shared
    else:
        shareds[cmd]=shared
    cmds[cmd]=cmds.setdefault(cmd,0)+private
    if cmd in count:
       count[cmd] += 1
    else:
       count[cmd] = 1
    mem_ids.setdefault(cmd,{}).update({mem_id:None})

total=0
for cmd in cmds:
    cmd_count = count[cmd]
    if len(mem_ids[cmd]) == 1 and cmd_count > 1:
        cmds[cmd] /= cmd_count
        if have_pss:
            shareds[cmd] /= cmd_count
    cmds[cmd]=cmds[cmd]+shareds[cmd]
    total+=cmds[cmd] 

if sys.version_info >= (2, 6):
    sort_list = sorted(cmds.items(), key=lambda x:x[1])
else:
    sort_list = cmds.items()
    sort_list.sort(lambda x,y:cmp(x[1],y[1]))
sort_list=list(filter(lambda x:x[1],sort_list)) 

def human(num, power="Ki"):
    powers=["Ki","Mi","Gi","Ti"]
    while num >= 1000:
        num /= 1024.0
        power=powers[powers.index(power)+1]
    return "%.1f %s" % (num,power)

def cmd_with_count(cmd, count):
    if count>1:
       return "%s (%u)" % (cmd, count)
    else:
       return cmd

sys.stdout.write(" Private  +   Shared  =  RAM used\tProgram \n\n")
for cmd in sort_list:
    sys.stdout.write("%8sB + %8sB = %8sB\t%s\n" % (human(cmd[1]-shareds[cmd[0]]),
                                      human(shareds[cmd[0]]), human(cmd[1]),
                                      cmd_with_count(cmd[0], count[cmd[0]])))
if have_pss:
    sys.stdout.write("%s\n%s%8sB\n%s\n" % ("-" * 33,
        " " * 24, human(total), "=" * 33))
sys.stdout.write("\n Private  +   Shared  =  RAM used\tProgram \n\n")

def shared_val_accuracy():
    """http://wiki.apache.org/spamassassin/TopSharedMemoryBug"""
    if kv[:2] == (2,4):
        if open("/proc/meminfo", "rt").read().find("Inact_") == -1:
            return 1
        return 0
    elif kv[:2] == (2,6):
        if os.path.exists("/proc/"+str(os.getpid())+"/smaps"):
            if open("/proc/"+str(os.getpid())+"/smaps", "rt").read().find("Pss:")!=-1:
                return 2
            else:
                return 1
        if (2,6,1) <= kv <= (2,6,9):
            return -1
        return 0
    else:
        return 1

vm_accuracy = shared_val_accuracy()
if vm_accuracy == -1:
    sys.stderr.write(
     "Warning: Shared memory is not reported by this system.\n"
    )
    sys.stderr.write(
     "Values reported will be too large, and totals are not reported\n"
    )
elif vm_accuracy == 0:
    sys.stderr.write(
     "Warning: Shared memory is not reported accurately by this system.\n"
    )
    sys.stderr.write(
     "Values reported could be too large, and totals are not reported\n"
    )
elif vm_accuracy == 1:
    sys.stderr.write(
     "Warning: Shared memory is slightly over-estimated by this system\n"
     "for each program, so totals are not reported.\n"
    )


