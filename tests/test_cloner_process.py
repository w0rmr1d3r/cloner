from unittest.mock import patch

from cloner.cloner_process import ClonerProcess


@patch.object(ClonerProcess, "_execute_system_call")
def test_cloner_process_can_clone_a_repo(mock_execute_system_command, random_repository):
    mock_execute_system_command.return_value = 0
    repository_list = [random_repository]

    cloner_process = ClonerProcess(repos_to_clone=repository_list, process_id=1)

    cloner_process.run()

    mock_execute_system_command.assert_called_once_with(
        command=f"git clone --quiet {random_repository.clone_url} ./repos/{random_repository.name}"
    )


@patch.object(ClonerProcess, "_execute_system_call")
def test_cloner_process_wont_clone_if_given_list_of_repositories_is_empty(
    mock_execute_system_command,
):
    mock_execute_system_command.return_value = 0

    cloner_process = ClonerProcess(repos_to_clone=[], process_id=1)

    cloner_process.run()

    mock_execute_system_command.assert_not_called()


@patch.object(ClonerProcess, "_execute_system_call")
def test_cloner_process_can_clone_a_repo_in_a_different_path(mock_execute_system_command, random_repository):
    mock_execute_system_command.return_value = 0
    repository_list = [random_repository]

    cloner_process = ClonerProcess(repos_to_clone=repository_list, process_id=1, clone_path="./other_folder/")

    cloner_process.run()

    mock_execute_system_command.assert_called_once_with(
        command=f"git clone --quiet {random_repository.clone_url} ./other_folder/{random_repository.name}"
    )


@patch.object(ClonerProcess, "_execute_system_call")
def test_cloner_process_can_clone_a_repo_with_clone_options(mock_execute_system_command, random_repository):
    mock_execute_system_command.return_value = 0
    repository_list = [random_repository]

    cloner_process = ClonerProcess(repos_to_clone=repository_list, process_id=1, git_options="--depth 1")

    cloner_process.run()

    mock_execute_system_command.assert_called_once_with(
        command=f"git clone --quiet --depth 1 {random_repository.clone_url} ./repos/{random_repository.name}"
    )
