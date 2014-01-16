Feature: Files

  Background:
    * Make sure that nautilus is running
    * Go to temporary directory

  @move_folder_to_trash
  Scenario: Move folder to Trash
    * Create a new folder named "folder"
    * Delete folder named "folder"
    * Go to Trash
    Then new folder named "folder" is displayed

  @move_file_to_trash
  Scenario: Move file to trash
    * Create an empty file named "Test File" in temporary directory
    * Delete file named "Test File"
    * Go to Trash
    Then new file named "Test File" is displayed

  @restore_file_from_trash
  Scenario: Restore file from Trash
    * Create a file named "Test File" in temporary directory with the following contents:
    """
    Some important text data here
    """
    * Delete file named "Test File"
    * Go to Trash
    * Restore "Test File" from Trash
    * Go to temporary directory
    Then new file named "Test File" is displayed
     And File "Test File" in temporary directory contents is:
     """
     Some important text data here
     """

  @empty_trash
  Scenario: Empty Trash
    * Create an empty file named "Test File" in temporary directory
    * Delete file named "Test File"
    * Create a new folder named "folder"
    * Delete folder named "folder"
    * Go to Trash
    * Empty trash
    Then new file named "Test File" is not displayed
     And new folder named "folder" is not displayed


