import os


def get_project_path(project_name):
    """Walks up in the path to find `pytest.ini`."""

    current = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(current, 'pytest.ini')):
            return os.path.join(current, project_name)
        current, _ = os.path.split(current)
        if not _:
            raise Exception('No `pytest.ini` found.')
