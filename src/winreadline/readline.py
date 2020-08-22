# -*- coding: utf-8 -*-
"""Python implementation of readline.

Help on module readline:

NAME
    readline - Importing this module enables command line editing using GNU readline.

MODULE REFERENCE
    /root/python/official-python-docs/3.7/library/build/html/readline.html

    The following documentation is automatically generated from the Python
    source files.  It may be incomplete, incorrect or include features that
    are considered implementation detail and may vary between Python
    implementations.  When in doubt, consult the module reference at the
    location listed above.

FUNCTIONS
    add_history(...)
        add_history(string) -> None
        add an item to the history buffer

    append_history_file(...)
        append_history_file(nelements[, filename]) -> None
        Append the last nelements items of the history list to file.
        The default filename is ~/.history.

    clear_history(...)
        clear_history() -> None
        Clear the current readline history.

    get_begidx(...)
        get_begidx() -> int
        get the beginning index of the completion scope

    get_completer(...)
        get_completer() -> function

        Returns current completer function.

    get_completer_delims(...)
        get_completer_delims() -> string
        get the word delimiters for completion

    get_completion_type(...)
        get_completion_type() -> int
        Get the type of completion being attempted.

    get_current_history_length(...)
        get_current_history_length() -> integer
        return the current (not the maximum) length of history.

    get_endidx(...)
        get_endidx() -> int
        get the ending index of the completion scope

    get_history_item(...)
        get_history_item() -> string
        return the current contents of history item at index.

    get_history_length(...)
        get_history_length() -> int
        return the maximum number of lines that will be written to
        the history file.

    get_line_buffer(...)
        get_line_buffer() -> string
        return the current contents of the line buffer.

    insert_text(...)
        insert_text(string) -> None
        Insert text into the line buffer at the cursor position.

    parse_and_bind(...)
        parse_and_bind(string) -> None
        Execute the init line provided in the string argument.

    read_history_file(...)
        read_history_file([filename]) -> None
        Load a readline history file.
        The default filename is ~/.history.

    read_init_file(...)
        read_init_file([filename]) -> None
        Execute a readline initialization file.
        The default filename is the last filename used.

    redisplay(...)
        redisplay() -> None
        Change what's displayed on the screen to reflect the current
        contents of the line buffer.

    remove_history_item(...)
        remove_history_item(pos) -> None
        remove history item given by its position

    replace_history_item(...)
        replace_history_item(pos, line) -> None
        replaces history item given by its position with contents of line

    set_auto_history(...)
        set_auto_history(enabled) -> None
        Enables or disables automatic history.

    set_completer(...)
        set_completer([function]) -> None
        Set or remove the completer function.
        The function is called as function(text, state),
        for state in 0, 1, 2, ..., until it returns a non-string.
        It should return the next possible completion starting with 'text'.

    set_completer_delims(...)
        set_completer_delims(string) -> None
        set the word delimiters for completion

    set_completion_display_matches_hook(...)
        set_completion_display_matches_hook([function]) -> None
        Set or remove the completion display function.
        The function is called as
          function(substitution, [matches], longest_match_length)
        once each time matches need to be displayed.

    set_history_length(...)
        set_history_length(length) -> None
        set the maximal number of lines which will be written to
        the history file. A negative length is used to inhibit
        history truncation.

    set_pre_input_hook(...)
        set_pre_input_hook([function]) -> None
        Set or remove the function invoked by the rl_pre_input_hook callback.
        The function is called with no arguments after the first prompt
        has been printed and just before readline starts reading input
        characters.

    set_startup_hook(...)
        set_startup_hook([function]) -> None
        Set or remove the function invoked by the rl_startup_hook callback.
        The function is called with no arguments just
        before readline prints the first prompt.

    write_history_file(...)
        write_history_file([filename]) -> None
        Save a readline history file.
        The default filename is ~/.history.

FILE
    /usr/lib/python3.8/lib-dynload/readline.cpython-38-x86_64-linux-gnu.so


"""
import logging
import sys
import time

from .logging import log
from .history import OrderedHistory

# here's the end goal

__all__ = [
    "add_history",
    "append_history_file",
    "clear_history",
    "get_begidx",
    "get_completer",
    "get_completer_delims",
    "get_completion_type",
    "get_current_history_length",
    "get_endidx",
    "get_history_item",
    "get_history_length",
    "get_line_buffer",
    "insert_text",
    "parse_and_bind",
    "read_history_file",
    "read_init_file",
    "redisplay",
    # new functions!
    "remove_history_item",
    "replace_history_item",
    "set_auto_history",
    "set_completer",
    "set_completer_delims",
# another oen
    "set_completion_display_matches_hook",
    "set_history_length",
    "set_pre_input_hook",
    "set_startup_hook",
    "write_history_file",
]
# Some other objects are added below

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(name=__name__)

start = time.perf_counter()


# In order to know where to save the history file, we need
# to read user preferences
# So implementing a ConfigReader and then reading in
# user configuration is basically one of the first thins we should do

# History:
rl = OrderedHistory()
write_history_file = rl.write_history_file
read_history_file = rl.read_history_file
clear_history = rl.clear_history
add_history = rl.add_history
get_current_history_length = rl.get_current_history_length
get_history_length = rl.get_history_length
get_history_item = rl.get_history_item
set_history_length = rl.set_history_length

# del rl


# get_line_buffer = rl.get_line_buffer
# set_completer = rl.set_completer
# get_completer = rl.get_completer
# get_begidx = rl.get_begidx
# get_endidx = rl.get_endidx

# redisplay = rl.redisplay

# set_completer_delims = rl.set_completer_delims
# set_pre_input_hook = rl.set_pre_input_hook
# set_startup_hook = rl.set_startup_hook

# insert_text = rl.insert_text
# get_completer_delims = rl.get_completer_delims

end_time = time.perf_counter()
logger.debug("Readline setup complete. %d" % (end_time - start))

del end_time, start
