import yaml


def parse_yaml(filename):
    with open(filename, 'r') as stream:
        config = yaml.safe_load(stream)
    if config:
        return config
    else:
        return True
