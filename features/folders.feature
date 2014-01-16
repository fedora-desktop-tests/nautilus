Feature: Folders

  Background:
    * Make sure that nautilus is running
    * Go to temporary directory

  @create_folder
  Scenario: Create local folder
    * Create a new folder
    Then new folder named "Untitled Folder" is displayed

  @show_folder_contents
  Scenario: Show local folder contents
    * Create a new folder named "folder"
    * Create an empty file named "Test File" in "folder" folder in temporary directory
    * Open "folder" folder
    Then new file named "Test File" is displayed

  @rename_folder
  Scenario: Rename folder
    * Create a new folder named "folder"
    * Create an empty file named "Test File" in "folder" folder in temporary directory
    * Rename folder "folder" to "renamed"
    Then new folder named "folder" is not displayed
     And new folder named "renamed" is displayed
    * Open "renamed" folder
    Then new file named "Test File" is displayed

  @copy_and_paste_folder
  Scenario: Copy folder and paste into folder
    * Create a new folder named "folder"
    * Create a new folder named "directory"
    * Copy "directory"
    * Paste into "folder" folder
    * Open "folder" folder
    Then new folder named "directory" is displayed

  @cut_and_paste_folder
  Scenario: Cut file and paste into folder
    * Create a new folder named "folder"
    * Create a new folder named "directory"
    * Cut "directory"
    * Paste into "folder" folder
    Then new folder named "directory" is not displayed
    * Open "folder" folder
    Then new file named "directory" is displayed

  @copy_and_paste_folder_via_drag_n_drop
  Scenario: Copy folder to folder via drag and drop
    * Create a new folder named "folder"
    * Create a new folder named "directory"
    * Copy "directory" to "folder" via drag and drop
    * Go to temporary directory
    Then new folder named "directory" is displayed
    * Open "folder" folder
    Then new folder named "directory" is displayed

  @cut_and_paste_folder_via_drag_n_drop
  Scenario: Cut file and paste into folder
    * Create a new folder named "folder"
    * Create a new folder named "directory"
    * Move "directory" to "folder" via drag and drop
    * Go to temporary directory
    Then new folder named "directory" is not displayed
    * Open "folder" folder
    Then new folder named "directory" is displayed
