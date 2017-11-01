"""Ok this is for slicing video"""
import os
import threading
import time

class SliceVideo(threading.Thread):
    """
    TO-DO: document what your XBlock does.
    """

    def __init__(self, threadID, video_id, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.video_id = video_id
        self.counter = counter
    def run(self):
        # print "Starting " + self.name
        # new_path = 'E:/vids/new_days.txt'
        # new_days = open(new_path, 'w')

        # title = 'Video Test writing\n'
        # new_days.write(title)
        #print(title)
        # new_days.close()
        download_cmd = ('C:/Users/nguye/Dropbox/edx/libs/youtube-dl.exe https://www.youtube.com/watch?v={0} -o E:/vids/{0}.mp4').format(self.video_id)
        os.system(download_cmd)
        os.system(r'"scenedetect -i E:/vids/{0}.mp4 -co scenes_list.csv -d content -si -df 4"'.format(self.video_id))
        print "Exiting " + self.name

# def print_time(thread_name, counter, delay):
#     "OK docstring"
#     threadName = ""
#     return
