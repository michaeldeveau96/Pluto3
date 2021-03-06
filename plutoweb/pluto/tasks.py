from __future__ import absolute_import, unicode_literals

import time

import matplotlib
import nmap
import pyspeedtest
from celery import Task

matplotlib.use('agg')
import random

class GetData(Task):
    ignore_result = True

    def run(self, *args, **kwargs):
        devices = self.get_devices()
        average_ping = self.get_average_ping(devices)
        average_download = self.get_average_download(devices)
        average_upload = self.get_average_upload(devices)
        #return devices, average_ping, average_download, average_upload
        return self.plot(devices, average_ping, average_download, average_upload)


    def get_devices(self):
        nm = nmap.PortScanner()
        print('Gathering Devices...')
        print('----------------------------------------------------')
        start = time.time()
        nm.scan(hosts='192.168.0.1/24', arguments='-n -sP')
        self.devices = nm.all_hosts()
        end = time.time()
        ptime = end - start
        print('Gathered Devices. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.devices


    def get_average_ping(self, devices):
        st = pyspeedtest.SpeedTest()
        print('Calculating average ping...')
        print('----------------------------------------------------')
        start = time.time()
        pings = []
        for i in range(0, len(self.devices)):
            pings.append(st.ping())
        self.average_ping = round(sum(pings) / len(pings))
        end = time.time()
        ptime = end - start
        print('Calculated average ping. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_ping


    def get_average_download(self, devices):
        st = pyspeedtest.SpeedTest()
        print('Calculating average download...')
        print('----------------------------------------------------')
        start = time.time()
        downloads = []
        for i in range(0, len(self.devices)):
            downloads.append(st.download() / 1000000)
        self.average_download = round(sum(downloads) / len(downloads))
        end = time.time()
        ptime = end - start
        print('Calculated average download. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_download


    def get_average_upload(self, devices):
        st = pyspeedtest.SpeedTest()
        print('Calculating average upload...')
        print('----------------------------------------------------')
        start = time.time()
        uploads = []
        for i in range(0, len(self.devices)):
            uploads.append(st.upload() / 1000000)
        self.average_upload = round(sum(uploads) / len(uploads))
        end = time.time()
        ptime = end - start
        print('Calculated average upload. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_upload


    def plot(self, devices, average_ping, average_download, average_upload):
        st = pyspeedtest.SpeedTest()
        print('Drawing network...')
        print('----------------------------------------------------')
        responses = []
        downloads = []
        uploads = []
        phealth = []
        dhealth = []
        uhealth = []
        devices = self.devices
        for ip in self.devices:
            ping = st.ping()
            download = st.download()
            upload = st.upload()
            responses.append(round(ping))
            downloads.append(round(download/1000000))
            uploads.append(round(upload/1000000))
            if round(ping) > (int(self.average_ping) * 1.5):
                phealth.append('HIGH')
            else:
                phealth.append('NORMAL')
            if round(download / 1000000) < (int(self.average_download) * .75):
                dhealth.append('LOW')
            else:
                dhealth.append('NORMAL')
            if round(upload / 1000000) < (int(self.average_upload) * .75):
                uhealth.append('LOW')
            else:
                uhealth.append('NORMAL')
        hostnames = []
        p = 1
        for ip in self.devices:
            if ip == '192.168.0.1':
                hostnames.append('Router')
            else:
                hostnames.append('Computer ' + str(p))
            p += 1
        x = []
        y = []
        for i in range(0, len(self.devices)):
            x.append(random.random())
            y.append(random.random())
        area = 20
        return responses, downloads, uploads, hostnames, phealth, dhealth, uhealth, self.devices, x, y

