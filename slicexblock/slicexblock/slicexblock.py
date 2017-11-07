"""TO-DO: Write a description of what this XBlock is."""
import os
import thread
import threading
import time
import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from xblock.fragment import Fragment
from slice_video import SliceVideo


class SliceXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    video_id = String(
        default="video_id", scope=Scope.settings,
        help="Youtube video id",
    )

    video_slices_div = String(
        default="<div>The div</div>", scope=Scope.settings,
        help="Youtube video slice div",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the SliceXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/slicexblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/slicexblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/slicexblock.js"))
        frag.initialize_js('SliceXBlock')
        return frag

    def author_view(self, context=None):
        """
        The primary view of the SliceXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/slicexblock_cms.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/slicexblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/slicexblock.js"))
        frag.initialize_js('SliceXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def generate_slices(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        self.video_id = data['video_id']

        # Create two threads as follows
        #thread.start_new_thread(download_video, ("Thread-1", 2, ))
        thread1 = SliceVideo(1, self.video_id, 1)
        thread1.start()
        self.video_slices_div = self.video_slices_div + self.video_id
        return# {"video_id" : self.video_id}

    @XBlock.json_handler
    def get_slices_div(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        return {"slices_div" : self.video_slices_div}

    # Define a function for the thread
    def download_video(threadName, delay):
        # new_path = 'E:/vids/new_days.txt'
        # new_days = open(new_path, 'w')

        # title = 'Video Test writing\n'
        # new_days.write(title)
        #print(title)
        # new_days.close()
        #os.system(r'"C:/Users/nguye/Dropbox/edx/libs/youtube-dl.exe https://www.youtube.com/watch?v=OMgIPnCnlbQ -o E:/vids/tung.mp4"')
        #os.system(r'"scenedetect -i E:/vids/tung.mp4 -co scenes_list.csv -d content -si -df 4"')
        return

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("SliceXBlock",
             """<slicexblock/>
             """),
            ("Multiple SliceXBlock",
             """<vertical_demo>
                <slicexblock/>
                <slicexblock/>
                <slicexblock/>
                </vertical_demo>
             """),
        ]