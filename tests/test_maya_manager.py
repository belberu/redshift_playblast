import unittest

import os

from ktrack_metadata import ktrack_metadata
from mock import patch, Mock

from redshift_playblast.logic import maya_manager

def get_resource(name):
    return os.path.join(os.path.dirname(__file__), 'resources', name)

class Redshift_Playblast_Test(unittest.TestCase):

    @patch('ktrack_metadata.from_scene')
    def test_create(self, from_scene_mock):
        """
        Tests the creation of a new maya manager
        """

        from_scene_mock.return_value=Mock()

        manager=maya_manager.Maya_Manager()

        self.assertNotEqual(manager, None)

        self.assertNotEqual(manager.job.file_path, None)
        self.assertNotEqual(manager.job.start_frame, None)
        self.assertNotEqual(manager.job.end_frame, None)
        self.assertNotEqual(manager.job.width, None)
        self.assertNotEqual(manager.job.height, None)
        self.assertNotEqual(manager.job.frame_path, None)
        self.assertNotEqual(manager.job.movie_path, None)
        self.assertNotEqual(manager.job.camera, None)
        self.assertNotEqual(manager.job.dof, None)
        self.assertNotEqual(manager.job.motion_blur, None)
        self.assertNotEqual(manager.job.quality, None)
        self.assertNotEqual(manager.job.context, None)

