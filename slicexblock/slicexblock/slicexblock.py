"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from xblock.fragment import Fragment
from slice_video import SliceVideo
from xblockutils.studio_editable import StudioEditableXBlockMixin


class SliceXBlock(XBlock):
    """
    Convert a video to slices
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
        The primary view of the SliceXBlock, shown to authors
        when viewing courses.
        """
        html = self.resource_string("static/html/slicexblock_cms.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/slicexblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/slicexblock.js"))
        frag.initialize_js('SliceXBlock')
        return frag

    def studio_view(self, _context):
        """
        The setting view of the SliceXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/slicexblock_cms.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/slicexblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/slicexblock.js"))
        frag.initialize_js('SliceXBlock')
        return frag

    def prepare_studio_editor_fields(self, field_names):
        """
        Order xblock fields in studio editor modal.
        Arguments:
            field_names (tuple): Names of Xblock fields.
        Returns:
            prepared_fields (list): XBlock fields prepared to be rendered in a studio edit modal.
        """
        prepared_fields = []
        for field_name in field_names:
            # set default from json XBLOCK_SETTINGS config:
            populated_field = self.populate_default_value(
                self.fields[field_name]  # pylint:disable=unsubscriptable-object
            )
            # make extra field configuration for frontend rendering:
            field_info = self._make_field_info(field_name, populated_field)
            prepared_fields.append(field_info)

        return prepared_fields

    def _make_field_info(self, field_name, field):
        """
        Override and extend data of built-in method.
        Create the information that the template needs to render a form field for this field.
        Reference:
            https://github.com/edx/xblock-utils/blob/v1.0.3/xblockutils/studio_editable.py#L96
        Arguments:
            field_name (str): Name of a video XBlock field whose info is to be made.
            field (xblock.fields): Video XBlock field object.
        Returns:
            info (dict): Information on a field to be rendered in the studio editor modal.
        """
        if field_name in ('video_id'):
            info = self.initialize_studio_field_info(field_name, field, field_type=field_name)
        else:
            info = self.initialize_studio_field_info(field_name, field)
        return info

    def initialize_studio_field_info(self, field_name, field, field_type=None):
        """
        Initialize studio editor's field info.
        Arguments:
            field_name (str): Name of a video XBlock field whose info is to be made.
            field (xblock.fields): Video XBlock field object.
            field_type (str): Type of field.
        Returns:
            info (dict): Information on a field.
        """
        info = super(SliceXBlock, self)._make_field_info(field_name, field)
        info['help'] = self._get_field_help(field_name, field)
        if field_type:
            info['type'] = field_type
        if field_name == 'handout':
            info['file_name'] = self.get_file_name_from_path(self.handout)
            info['value'] = self.get_path_for(self.handout)
        return info

    def get_file_name_from_path(self, field):
        """
        Helper for getting filename from string with path to MongoDB storage.
        Example of string:
            asset-v1-RaccoonGang+1+2018+type@asset+block@<filename>
        Arguments:
            field (str): The path to file.
        Returns:
            The name of file with an extension.
        """
        return field.split('@')[-1]

    def get_path_for(self, file_field):
        """
        Return downloaded asset url with slash in start of it.
        Url, retrieved after storing of the file field in MongoDB, looks like this:
            'asset-v1-RaccoonGang+1+2018+type@asset+block@<filename>'
        Arguments:
            file_field (str): name a file is stored in MongoDB under.
        Returns:
            Full path of a downloaded asset.
        """
        if file_field:
            return os.path.join('/', file_field)
        return ''

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