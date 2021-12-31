import os
from multiprocessing import Process

from cloner.repository import Repository


class ClonerProcess(Process):
    """Class to clone a list of given repositories when started."""

    def __init__(self, repos_to_clone: list[Repository], process_id: int):
        Process.__init__(self)
        self.repos_list = repos_to_clone
        self.process_id = process_id

    def run(self):
        """Clones each repo given in the constructor."""
        for repo in self.repos_list:
            # git options? --depth 1  ???
            # todo -> path as an option?
            # https://pypi.org/project/multiprocessing-logging/ not in windows
            # logging.debug(f"Process {self.process_id} cloning {repo}")
            os.system(f"git clone {repo.clone_url} --quiet ./repos/{repo.name}")
