import ftplib
import time


class FTPRetry:
    """Contains a ftplib.FTP instance, reconnect in case of disconnection

    Example:

    ```python
    ftpretry = FTPRetry(ftp_config)
    def f(ftp):
        ftp.cwd("/my_stuff")
        r = ftp.nlst()
        ftp.cwd("/my_other_stuff")
        r += ftp.nlst()
        return r
    my_stuff_and_other_stuff = ftpretry.call(f)
    ```
    In this example, `f` might be called multple times.
    Warning: The current working directory is most probably `/` when the function f starts, but not always.
    """

    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        self.ftp = ftplib.FTP(self.config["HOST"], timeout=None)
        self.ftp.login(self.config["LOGIN"], self.config["PASSWORD"])

    def call(self, func, *args, **kwargs):
        try_count = 0
        while True:  # for safety: see if retry_count >= 10 below
            try_count += 1
            try:
                return func(self.ftp, *args, **kwargs)
            except ftplib.error_temp as e:
                if not str(e).startswith("421 "):
                    # not a timeout: raise the exception
                    raise e
                # there is a timeout: retry
                if try_count >= 10:
                    # we have try more at least 10 time (about 20 minutes)
                    # forward the exception
                    raise e
                print("FTP error")
                time.sleep(22 * (try_count - 1))
                self.connect()

    def nlst(self, dir):
        def f(ftp):
            ftp.cwd(dir)
            return ftp.nlst()

        return self.call(f)

    def mkd(self, dir):
        def f(ftp):
            return ftp.mkd(dir)

        return self.call(f)

    def download(self, remote_filename, local_filname):
        def f(ftp):
            with open(local_filname, "wb") as f:
                ftp.retrbinary("RETR " + remote_filename, f.write)

        return self.call(f)

    def upload(self, remote_filename, local_filename):
        def f(ftp):
            with open(local_filename, "rb") as f:
                ftp.storbinary("STOR " + remote_filename, f)

        return self.call(f)

    def close(self):
        self.ftp.close()
