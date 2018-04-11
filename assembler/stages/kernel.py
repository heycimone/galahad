from stages.core.ssh_stage import SSHStage
import time
import subprocess, os

class KernelStage(SSHStage):
    ''' This stage is a demo stage for how to use SSHStage tools '''
    NAME = 'KernelStage'
    DEPENDS = ['UserStage']

    def run(self):
        if not self._has_run:
            super().run()
            deb_file_path = os.path.join('..', 'unity', 'latest-debs')
            files = ['linux-headers-4.13.0-36_4.13.0-36.40+unity1_all.deb', 'linux-image-4.13.0-36-generic_4.13.0-36.40+unity1_amd64.deb']
            for f in files:
                self._copy_file(os.path.join(deb_file_path, f), f)
            self._exec_cmd('sudo dpkg -i --force-all '+' '.join(files))
            for f in files:
                self._exec_cmd('rm %s' % (f))
            try:
                self._exec_cmd('sudo reboot')
            except subprocess.CalledProcessError as e:
                if e.returncode == 255: # reboot will kill the connection causing 255 error code
                    pass
                else:
                    raise
            time.sleep(10) # wait 10 seconds to reboot