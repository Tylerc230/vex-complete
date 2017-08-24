import yaml
class Project(object):
    def __init__(self, yaml_file):
        self._parse_yaml(yaml_file)

    def _parse_yaml(self, yaml_file):
        with open(yaml_file, 'r') as stream:
            project_dict = yaml.load(stream)
            self.xcodeproj = project_dict.get('xcodeproj', None)
            self.xcodescheme = project_dict.get('scheme', None)


