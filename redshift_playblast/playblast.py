import argparse

"""
Parameters:
start_frame
end_frame
width
height

frame_path

camera

DOF
Motionblur
quality: LOW, MED, HIGH
"""
import pymel.core as pm
import maya.mel as mel

QUALITY_PRESETS={
    'low': {
            'min_samples': 2,
            'max_samples': 16,
            'threshold': 0.25,
            },
    'med': {
            'min_samples': 2,
            'max_samples': 32,
            'threshold': 0.05,
            },
    'medium': {
            'min_samples': 2,
            'max_samples': 32,
            'threshold': 0.05,
            },
    'high': {
            'min_samples': 2,
            'max_samples': 64,
            'threshold': 0.01
            },
}

class Redshift(object):

    def __init__(self, args):
        #TODO validate args
        self.args=args
        #load file
        pm.openFile(self.args.file_path, force=True)
        # load redshift plugin
        pm.loadPlugin('redshift4maya')
        if len(pm.ls('redshiftOptions'))==0:
            pm.createNode('RedshiftOptions')
        #change renderer
        self._get_object_by_name("defaultRenderGlobals").currentRenderer.set('redshift')
        #set file format and other render setting stuff
        self._get_object_by_name("redshiftOptions").imageFormat.set(2)

        self._get_object_by_name("defaultRenderGlobals").animation.set(1)
        self._get_object_by_name("defaultRenderGlobals").extensionPadding.set(4)

        self.set_start_end_frame(self.args.start_frame, self.args.end_frame)

        self.set_resolution(self.args.width, self.args.height)

        self.set_frame_path(self.args.frame_path)

        self.set_camera(self.args.camera)

        self.set_dof(self.args.dof)

        self.set_motion_blur(self.args.motion_blur)

        self.set_quality(self.args.quality)

    def _get_object_by_name(self, name):
        """
        Returns a PyMel object by its name
        :param name:
        :return:
        """
        candidates=pm.ls(name)
        if len(candidates)==1:
            return candidates[0]
        else:
            error="Object with name {0} does not exists".format(name)
            raise ObjectNotExistsError(error)

    def set_start_end_frame(self, start_frame, end_frame):
        print "settings start and end frame to ", start_frame, end_frame
        self._get_object_by_name("defaultRenderGlobals").startFrame.set(start_frame)
        self._get_object_by_name("defaultRenderGlobals").endFrame.set(end_frame)

    def set_resolution(self, width, height):
        print "set resolution to ", width, " x ", height
        default_resolution=self._get_object_by_name('defaultResolution')
        default_resolution.width.set(width)
        default_resolution.height.set(height)

    def set_frame_path(self, frame_path):
        print "set frame path to ", frame_path
        print "replaced path to ", frame_path.replace("_####.png", "")
        self._get_object_by_name('defaultRenderGlobals').imageFilePrefix.set(frame_path.replace(".####.png", ""))

    def set_camera(self, camera):
        print "set camera to ", camera
        self.camera=self._get_object_by_name(camera)
        mel.eval('makeCameraRenderable("{0}")'.format(camera))

    def set_dof(self, dof_enabled):
        print "set dof enabled: ", dof_enabled
        self.camera.depthOfField.set(1 if dof_enabled else 0)

    def set_motion_blur(self, motion_blur):
        print "set motion_blur enabled: ", motion_blur
        self._get_object_by_name("redshiftOptions").motionBlurEnable.set(motion_blur)
        self._get_object_by_name("redshiftOptions").motionBlurDeformationEnable.set(motion_blur)

    def set_quality(self, quality):
        print "set quality to: ", quality
        self._get_object_by_name("redshiftOptions").unifiedMinSamples.set(QUALITY_PRESETS[quality.lower()]['min_samples'])
        self._get_object_by_name("redshiftOptions").unifiedMaxSamples.set(QUALITY_PRESETS[quality.lower()]['max_samples'])
        self._get_object_by_name("redshiftOptions").unifiedAdaptiveErrorThreshold.set(QUALITY_PRESETS[quality.lower()]['threshold'])

    def render_frame(self, frame_number):
        """
        renders frame with given number
        :return:
        """
        old_start=self._get_object_by_name("defaultRenderGlobals").startFrame.get()
        old_end = self._get_object_by_name("defaultRenderGlobals").endFrame.get()
        self._get_object_by_name("defaultRenderGlobals").startFrame.set(frame_number)
        self._get_object_by_name("defaultRenderGlobals").endFrame.set(frame_number)
        mel.eval('mayaBatchRenderProcedure(0, "", "' + str('') + '", "' + 'redshift' + '", "")')
        self._get_object_by_name("defaultRenderGlobals").startFrame.set(old_start)
        self._get_object_by_name("defaultRenderGlobals").endFrame.set(old_end)

    def render_frames(self):
        """
        renders frame with given number
        :return:
        """
        mel.eval('mayaBatchRenderProcedure(0, "", "' + str('') + '", "' + 'redshift' + '", "")')



class PlayblastQualityError(Exception):
    """
    Exception thrown when a non-valid quality settings was supplied
    """
    pass
class ObjectNotExistsError(Exception):
    """
    Exception thrown when there is no object with the given name, for example persp_ysdf
    """
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-file_path', help='File to  playblast')
    parser.add_argument('-start_frame', help='Starting frame for playblast')
    parser.add_argument('-end_frame', help='Ending frame for playblast')
    parser.add_argument('-width', help='width for playblast')
    parser.add_argument('-height', help='width for playblast')
    parser.add_argument('-frame_path', help='Path where to place the rendered images')
    parser.add_argument('-camera', help='camera to use')
    parser.add_argument('-dof', help='Use DOF or not')
    parser.add_argument('-motion-blur', help='Use Motion Blur or not')
    parser.add_argument('-quality', help='Quality, LOW, MED or HIGH')

    args = parser.parse_args()

    #validate args
    if args.quality.lower() not in ['low', 'med', 'high', 'medium']:
        error="Unsupported quality settings: "+args.quality+". Supported are LOW, MED or HIGH"
        raise PlayblastQualityError(error)

    #convert args to correct data types
    args.start_frame=float(args.start_frame)
    args.end_frame = float(args.end_frame)
    args.width=int(args.width)
    args.height = int(args.height)
    args.motion_blur=True if 'True' in args.motion_blur else False
    args.dof = True if 'True' in args.dof else False


    renderer=Redshift(args)

    renderer.render_frames()

if __name__ == '__main__':
    main()