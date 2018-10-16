import asyncio
import random
import time
import matplotlib.pyplot as plt
import nmap
import pyspeedtest


class GetData:

    def __init__(self):
        self.devices = []
        self.average_ping = ''
        self.average_download = ''
        self.average_upload = ''

    async def get_devices(self):
        nm = nmap.PortScanner()
        print('Gathering Devices...')
        print('----------------------------------------------------')
        start = time.time()
        nm.scan(hosts='192.168.0.1/24', arguments='-n -sP')
        self.devices = nm.all_hosts()
        end = time.time()
        ptime = end-start
        print('Gathered Devices. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.devices

    async def get_average_ping(self):
        st = pyspeedtest.SpeedTest()
        print('Calculating average ping...')
        print('----------------------------------------------------')
        start = time.time()
        pings = []
        for i in range(0, len(self.devices)):
            pings.append(st.ping())
        self.average_ping = round(sum(pings)/len(pings))
        end = time.time()
        ptime = end-start
        print('Calculated average ping. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_ping

    async def get_average_download(self):
        st = pyspeedtest.SpeedTest()
        print('Calculating average download...')
        print('----------------------------------------------------')
        start = time.time()
        downloads = []
        for i in range(0, len(self.devices)):
            downloads.append(st.download()/1000000)
        self.average_download = round(sum(downloads)/len(downloads))
        end = time.time()
        ptime = end - start
        print('Calculated average download. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_download

    async def get_average_upload(self):
        st = pyspeedtest.SpeedTest()
        print('Calculating average upload...')
        print('----------------------------------------------------')
        start = time.time()
        uploads = []
        for i in range(0, len(self.devices)):
            uploads.append(st.upload()/1000000)
        self.average_upload = round(sum(uploads)/len(uploads))
        end = time.time()
        ptime = end - start
        print('Calculated average upload. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return self.average_upload

    async def plot(self):
        st = pyspeedtest.SpeedTest()
        print('Drawing network...')
        print('----------------------------------------------------')
        start = time.time()
        responses = []
        downloads = []
        uploads = []
        for ip in self.devices:
            if round(st.ping()) > (int(self.average_ping)*1.5):
                responses.append('HIGH')
            else:
                responses.append('NORMAL')
            if round(st.download()/1000000) < (int(self.average_download)/2):
                downloads.append('LOW')
            else:
                downloads.append('NORMAL')
            if round(st.upload()/1000000) < (int(self.average_upload)/2):
                uploads.append('LOW')
            else:
                uploads.append('NORMAL')
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

        plt.scatter(x, y, s=area, marker='o')
        plt.xticks([])
        plt.yticks([])
        #plt.plot(x, y, '-o')

        for i, txt in enumerate(self.devices):
            txt = 'Device Name: ' + str(hostnames[i]) + '\n' +\
                  'Device IP: ' + str(self.devices[i]) + '\n' + \
                  'Ping: ' + str(responses[i]) + '\n' + \
                  'Download: ' + str(downloads[i]) + '\n' + \
                  'Upload: ' + str(uploads[i])
            plt.annotate(txt, (x[i], y[i]))
        end = time.time()
        ptime = end - start
        print('Calculated average upload. Finished in {} seconds.'.format(ptime))
        print('====================================================')
        return plt.show()

def main():

    print('Scanning your network...')
    data = GetData()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(data.get_devices())
    loop.run_until_complete(data.get_average_ping())
    loop.run_until_complete(data.get_average_download())
    loop.run_until_complete(data.get_average_upload())
    loop.run_until_complete(data.plot())

    loop.close()

if __name__ == '__main__':
    main()