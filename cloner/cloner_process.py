from multiprocessing import Process
from subprocess import DEVNULL, call
from typing import Optional

from click import progressbar

from cloner.repository import Repository


class ClonerProcess(Process):
    """Class to clone a list of given repositories when started."""

    SUCCESSFUL_EXIT_CODE = 0
    DIRECTORY_ALREADY_EXISTS_AND_NOT_EMPTY_EXIT_CODE = 128

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
    def clone_path(self):  # noqa: D102
        if self._clone_path is not None:
            return self._clone_path
        return "./repos/"

    @property
    def git_options(self):  # noqa: D102
        default_option = "--quiet "
        if self._git_options is not None:
            return default_option + self._git_options + " "
        return default_option

    @staticmethod
    def _execute_system_call(command: str) -> int:
        """
        Proceeds to call the OS with the given command. Does not output stderr.

        It returns the return code of the given command.

        Docs are in: https://docs.python.org/3/library/subprocess.html#subprocess.call
        """
        ret_code = call(command, shell=True, stderr=DEVNULL)
        return ret_code

    def run(self):
        """Clones each repo from the repos_to_clone list given in the constructor."""
        repos_not_cloned = []
        with progressbar(self.repos_list, label=f"Cloning repos in process {self.process_id}") as bar:
            for repo in bar:
                exit_code = self._execute_system_call(
                    command=f"git clone {self.git_options}{repo.clone_url} {self.clone_path}{repo.name}"
                )
                if exit_code == self.DIRECTORY_ALREADY_EXISTS_AND_NOT_EMPTY_EXIT_CODE:
                    repos_not_cloned.append(repo.name)
                    continue
                if exit_code != self.SUCCESSFUL_EXIT_CODE:
                    print(f"WARNING - <{repo.name}> couldn't be cloned due to: error code - {exit_code}")

        for r_not_cloned in repos_not_cloned:
            print(f"<{r_not_cloned}> wasn't cloned due to: directory already exists")
