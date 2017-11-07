"""Ok this is for slicing video"""
import os
import threading
import time

class SliceVideo(threading.Thread):
    """
    Slice the video to images
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
        download_cmd = ('youtube-dl https://www.youtube.com/watch?v={0} -o /vids/{0}/{0}.mp4').format(self.video_id)
        os.system(download_cmd)
        os.system(r'"scenedetect -i /vids/{0}/{0}.mp4 -co {0}.csv -d content -si -df 4"'.format(self.video_id))
        print "Exiting " + self.name

# def print_time(thread_name, counter, delay):
#     "OK docstring"
#     threadName = ""
#     return
