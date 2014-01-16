# -*- coding: UTF-8 -*-
from behave import step

from dogtail.tree import root
from behave_common_steps.app import *
from behave_common_steps.appmenu import *
import tempfile
from dogtail.rawinput import typeText
import os.path
from dogtail.rawinput import drag


@step(u'Help section "{name}" is displayed')
def help_is_displayed(context, name):
    context.yelp = root.application('yelp')
    frame = context.yelp.child(roleName='frame')
    context.assertion.assertEquals(name, frame.name)


@step(u'Click "{name}" in sidebar')
def click_item_in_sidebar(context, name):
    context.app.instance.child(roleName='table').child(name).click()


@step(u'Go to directory "{name}"')
def go_to_directory(context, name):
    keyCombo("<Ctrl>L")
    keyCombo("<Delete>")
    typeText(name)
    keyCombo("<Enter>")


@step(u'Go to temporary directory')
def go_to_temp_dir(context):
    if not hasattr(context, 'temp_dir'):
        context.temp_dir = tempfile.mkdtemp()
    context.execute_steps(u"""
        * Go to directory "%s"
    """ % context.temp_dir)


@step(u'Create an empty file named "{filename}" in temporary directory')
@step(u'Create an empty file named "{filename}" in "{folder}" folder in temporary directory')
def touch_file_in_tempdir_subfolder(context, filename, folder=None, contents=None):
    full_file_name = None
    if folder:
        full_file_name = os.path.join(context.temp_dir, folder, filename)
    else:
        full_file_name = os.path.join(context.temp_dir, filename)
    with open(full_file_name, 'w') as f:
        if contents:
            f.write(contents)


@then(u'File "{filename}" in temporary directory contents is')
@then(u'File "{filename}" in "{folder}" folder in temporary directory contents is')
def file_in_tempdir_contents_is(context, filename, folder=None):
    full_file_name = None
    if folder:
        full_file_name = os.path.join(context.temp_dir, folder, filename)
    else:
        full_file_name = os.path.join(context.temp_dir, filename)
    actual = None
    with open(full_file_name, 'r') as f:
        actual = f.read()
    expected = context.text
    assert actual == expected,\
        "Incorrect file contents, expected '\n%s\n' but was '\n%s\n'" % (expected, actual)



@step(u'Create a file named "{name}" in temporary directory with the following contents')
def create_file_in_tempdir_with_contents(context, name):
    touch_file_in_tempdir_subfolder(context, filename=name, folder=None, contents=context.text)


@step(u'Go to "{name}" folder in temporary directory')
def go_to_dir_in_temp_dir(context, name):
    context.execute_steps(u'* Go to directory "%s"' % os.path.join(context.temp_dir, name))


@step(u'Create a new folder')
@step(u'Create a new folder named "{name}"')
def create_a_folder_random_name(context, name=None):
    # Open folder menu
    context.app.instance.child("Content View").click(button=3)
    context.app.instance.child(roleName='window').menuItem('New Folder').click()
    if name:
        typeText(name)
    keyCombo("<Enter>")
    sleep(0.1)


@then(u'new file named "{name}" is displayed')
@then(u'new folder named "{name}" is displayed')
@then(u'new file named "{name}" is {negative:w} displayed')
@then(u'new folder named "{name}" is {negative:w} displayed')
def new_item_named_is_displayed(context, name, negative=None):
    pane = context.app.instance.findChildren(lambda x: x.roleName == 'scroll pane')[-1]
    all_items = pane.findChildren(lambda x: x.roleName == 'canvas')
    if negative:
        assert name not in [x.name for x in all_items]
    else:
        assert name in [x.name for x in all_items]


@step(u'Open context menu for "{name}"')
def open_context_menu_for(context, name):
    pane = context.app.instance.findChildren(lambda x: x.roleName == 'scroll pane')[-1]
    pane.child(name).click(button=3)


@step(u'Delete file named "{name}"')
@step(u'Delete folder named "{name}"')
def delete_folder(context, name):
    context.execute_steps(u'* Open context menu for "%s"' % name)
    context.app.instance.child(roleName='window').menuItem('Move to Trash').click()


@step(u'Open "{name}" folder')
@step(u'Open file "{name}" using default application')
def open_file_via_default_app(context, name):
    pane = context.app.instance.findChildren(lambda x: x.roleName == 'scroll pane')[-1]
    pane.child(name).doubleClick()


@step(u'{action:w} "{name}"')
def do_action_on_file(context, action, name):
    context.execute_steps(u'* Open context menu for "%s"' % name)
    if action not in ['Copy', 'Cut']:
        raise RuntimeError("Unknown action: %s" % action)
    context.app.instance.child(roleName='window').menuItem(action).click()


@step(u'Paste into "{name}" folder')
def paste_into_folder(context, name):
    context.execute_steps(u'* Open context menu for "%s"' % name)
    context.app.instance.child(roleName='window').menuItem('Paste Into Folder').click()

@step(u'{action:w} "{source}" to "{dest}" via drag and drop')
def do_action_on_source_to_dest_via_drag_and_drop(context, action, source, dest):
    if action not in ['Copy', 'Move']:
        raise RuntimeError("Unknown action: %s" % action)
    pane = context.app.instance.findChildren(lambda x: x.roleName == 'scroll pane')[-1]
    source_item = pane.child(source)
    dest_item = pane.child(dest)

    source_center = (source_item.position[0] + source_item.size[0]/2, source_item.position[1] + source_item.size[1]/2)
    dest_center = (dest_item.position[0] + dest_item.size[0]/2, dest_item.position[1] + dest_item.size[1]/2)
    drag(source_center, dest_center, button=2)
    context.app.instance.menuItem('%s Here' % action).click()
    sleep(0.1)


@step(u'Go to Trash')
def go_to_trash(context):
    context.execute_steps(u'* Click "Trash" in sidebar')

@step(u'Restore "{name}" from Trash')
def restore_from_trash(context, name):
    context.execute_steps(u'* Open context menu for "%s"' % name)
    context.app.instance.child(roleName='window').menuItem('Restore').click()

@step(u'Empty Trash')
def empty_trash(context):
    context.app.instance.child('Empty').click()
    context.app.instance.child('Empty Trash').click()

@step(u'Rename folder "{source}" to "{dest}"')
@step(u'Rename file "{source}" to "{dest}"')
def rename_file_to(context, source, dest):
    context.execute_steps(u'* Open context menu for "%s"' % source)
    context.app.instance.child(roleName='window').findChildren(lambda x: x.roleName=='menu item' and 'Rename' in x.name)[0].click()
    typeText(dest)
    keyCombo("<Enter>")
