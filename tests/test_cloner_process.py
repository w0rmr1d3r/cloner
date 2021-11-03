import unittest
from unittest import mock

from cloner.cloner_process import ClonerProcess
from tests.stub.repository_stub import random_repository


class TestClonerProcess(unittest.TestCase):
    @mock.patch('os.system', return_value=0)
    def test_should_clone_one_repo(self, os_system):
        repo = random_repository()
        repos = [repo]
        subject = ClonerProcess(repos_to_clone=repos, process_id=0)
        os_system.assert_called_none()
        #os_system.assert_called_once_with(f"git clone {repo.clone_url} --quiet ./repos/{repo.name}")


    # def test_should_not_clone_if_none_given_repos(self):
    #     self.assertEqual(True, False)  # add assertion here
    #
    # def test_should_clone_all_the_repos(self):
    #     self.assertEqual(True, False)  # add assertion here

    #fails if repo exists test
