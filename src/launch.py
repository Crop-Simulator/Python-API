import argparse

from controllers.crop_controller import CropController
from renderers.scene_renderer import SceneRenderer
from controllers.camera_controller import CameraController

class LaunchAPI:
    
    def __init__(self):
        '''
        adding parser arguments for Python CLI interface
        -------
        example CLI command: python src/launch.py -i data.yml -o test.png 

        ''' 
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-i", "--infile", nargs="+")
        self.parser.add_argument("-o", "--outfile", nargs="+")
        self.args = self.parser.parse_args()
        self.collection = 'Cube Collection'

    def main(self):
        cameracon = CameraController()
        cropcon = CropController(self.args.infile[0], self.collection)
        scenerender = SceneRenderer(self.args.outfile[0], self.collection)
        cameracon.setup_camera('camera_one', (10,0,0), 
                     (1.57057,0.00174533,1.57057), "Cube Collection")
        cropcon.setup_crops()
        scenerender.render_scene()
        
if __name__ == "__main__":
    LaunchAPI().main()