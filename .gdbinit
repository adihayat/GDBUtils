set print pretty
set print static-members off
handle SIG34 nostop noprint pass
#in gdb att you need to do:
#   sudo chmod +s /usr/bin/gdb
#   vim /etc/sysctl.d/10-ptrace.conf : 1 -> 0
define init_debug
    py import pysigset, signal
    #py old_sig = pysigset.SIGSET()
    #py new_sig = pysigset.SIGSET()
    #py pysigset.sigaddset(new_sig, signal.SIGCHLD)
    #py pysigset.sigprocmask(pysigset.SIG_SETMASK, new_sig , old_sig)
    source /home/or/caffe/utils/matrix-viewer/GDB-ImageWatch/blobget.py
    source /home/or/caffe/utils/matrix-viewer/GDB-ImageWatch/cv_imshow.py
    source /home/or/caffe/utils/matrix-viewer/GDB-ImageWatch/cvget.py
    py import matplotlib
    py matplotlib.use('TKAgg')
    py import matplotlib.pyplot as plt
end
