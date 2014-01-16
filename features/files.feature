Feature: Files

  Background:
    * Make sure that nautilus is running
    * Go to temporary directory

  @open_file_with_editor
  Scenario: Open local file
    * Create a new folder named "folder"
    * Create an empty file named "Test File" in temporary directory
    * Open file "Test File" using default application
    Then GEdit should start

  @rename_file
  Scenario: Rename file
    * Create a file named "Test File" in temporary directory with the following contents:
    """
    Some important text data here
    """
    * Rename file "Test File" to "New file"
    Then new file named "Test File" is not displayed
     And new file named "New file" is displayed
     And File "New file" in temporary directory contents is
     """
     Some important text data here
     """

  @copy_and_paste_file
  Scenario: Copy file and paste into folder
    * Create a new folder named "folder"
    * Create an empty file named "Test File" in temporary directory
    * Copy "Test File"
    * Paste into "folder" folder
    * Open "folder" folder
    Then new file named "Test File" is displayed

  @cut_and_paste_file
  Scenario: Cut file and paste into folder
    * Create a new folder named "folder"
    * Create an empty file named "Test File" in temporary directory
    * Cut "Test File"
    * Paste into "folder" folder
    Then new file named "Test File" is not displayed
    * Open "folder" folder
    Then new file named "Test File" is displayed

