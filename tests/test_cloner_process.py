from unittest.mock import patch

from cloner.cloner_process import ClonerProcess


@patch.object(ClonerProcess, "_execute_system_command")
def test_cloner_process_can_clone_a_repo(
    mock_execute_system_command, random_repository
):
    mock_execute_system_command.return_value = 0
    repository_list = [random_repository]

    cloner_process = ClonerProcess(repos_to_clone=repository_list, process_id=1)

    cloner_process.run()

    mock_execute_system_command.assert_called_once_with(
        command=f"git clone {random_repository.clone_url} --quiet ./repos/{random_repository.name}"
    )
