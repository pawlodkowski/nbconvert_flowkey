import os
import sys

from setuptools import setup
from setuptools.command.develop import develop
from jupyter_packaging import get_data_files

try:
    import jupyter_core.paths as jupyter_core_paths
except ModuleNotFoundError:
    jupyter_core_paths = None

NAME = 'nbconvert_flowkey'
HERE = os.path.abspath(os.path.dirname(__file__))


class DevelopCmd(develop):

    prefix_targets = [
    ("nbconvert/templates", 'flowkey')
    ]

    def run(self):
        target_dir = os.path.join(sys.prefix, 'share', 'jupyter')
        if jupyter_core_paths:
            #TODO: potentially brittle logic: see https://jupyter.readthedocs.io/en/latest/use/jupyter-directories.html#envvar-JUPYTER_PATH
            target_dir = jupyter_core_paths.jupyter_path()[1]
        target_dir = os.path.join(target_dir)

        for prefix_target, name in self.prefix_targets:
            source = os.path.join('share', 'jupyter', prefix_target, name)
            target = os.path.join(target_dir, prefix_target, name)
            target_subdir = os.path.dirname(target)
            if not os.path.exists(target_subdir):
                os.makedirs(target_subdir)
            rel_source = os.path.relpath(os.path.abspath(source), os.path.abspath(target_subdir))
            try:
                os.remove(target)
            except:
                pass
            print(rel_source, '->', target)
            os.symlink(rel_source, target)

        super().run()

data_files = get_data_files(
        [
            ("share", str(os.path.join(HERE, "share")), "**"),
        ]
    )

setup_args = {
    'name': NAME,
    'version': '0.1.0',
    'packages': [],
    'data_files': data_files,
    'install_requires': [
    ],
    'author': 'Paul Wlodkowski',
    'author_email': 'paul@flowkey.com',
    'url': 'https://github.com/pawlodkowski/nbconvert_flowkey',
    'cmdclass': {
        'develop': DevelopCmd, #https://stackoverflow.com/a/27820612/17242197
    } if jupyter_core_paths else {},
    'extras_require': {
        "dev": ['jupyter_packaging'],
    },
    'entry_points':{
        "nbconvert.exporters": ["html_toc=nbconvert_flowkey:TocExporter"]
    }
}

if __name__ == '__main__':
    setup(**setup_args)
