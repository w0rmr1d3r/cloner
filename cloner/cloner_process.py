import os
from multiprocessing import Process
from typing import Optional

from cloner.repository import Repository


class ClonerProcess(Process):
    """Class to clone a list of given repositories when started."""

    def __init__(
        self,
        repos_to_clone: list[Repository],
        process_id: int,
        clone_path: Optional[str] = None,
        git_options: Optional[str] = None,
    ):
        Process.__init__(self)
        self.repos_list = repos_to_clone
        self.process_id = process_id
        self._clone_path = clone_path
        self._git_options = git_options

    @property
    def clone_path(self):
        if self._clone_path is not None:
            return self._clone_path
        return "./repos/"

    @property
    def git_options(self):
        default_option = "--quiet "
        if self._git_options is not None:
            return default_option + self._git_options + " "
        return default_option

    def _execute_system_command(self, command):
        return os.system(command=command)

    def run(self):
        """Clones each repo given in the constructor."""
        for repo in self.repos_list:
            self._execute_system_command(
                command=f"git clone {self.git_options}{repo.clone_url} {self.clone_path}{repo.name}"
            )
