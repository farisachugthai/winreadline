# -*- coding: utf-8 -*-
"""History implemented in readline.

Should be an easy enough place to start.

"""
# *****************************************************************************
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************
from __future__ import print_function, unicode_literals, absolute_import

import collections
import io
import operator
import os
import shutil
import sys
import traceback
from inspect import getmro
from textwrap import dedent
from typing import List, Any, AnyStr, Optional, Union, Callable

from pyreadline.lineeditor import touch



class HistoryFile(io.TextIOWrapper):
    """Partially from the help docs on `pickle`.

    Here’s a larger example that shows how to modify pickling behavior for a
    class. The TextReader class opens a text file, and returns the line number
    and line contents each time its readline() method is called. If a
    TextReader instance is pickled, all attributes except the file object
    member are saved. When the instance is unpickled, the file is reopened,
    and reading resumes from the last location. The __setstate__() and
    __getstate__() methods are used to implement this behavior.

    Attributes
    ----------
    name : Path
        pathlib.Path instance.
    fh : Buffer
        File Handle.
        todo: Should we just leave an open file handle like that?
    lineno : int
    """

    def __init__(self, name, **kwargs):
        self.name = Path(name)
        self.fh = open(name)
        # atexit.register(ensure_that_shit_closed)?
        self.lineno = 0
        super().__init__(**kwargs)

    def __fspath__(self):
        """Implement the path protocol."""
        return str(self.name)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, repr(self.name))

    def touch(self, filename: str) -> os.PathLike:
        return touch(filename)

    def readline(self):
        self.lineno = self.lineno + 1
        line = self.fh.readline()
        if not line:
            return None
        if line.endswith("\n"):
            line = line[:-1]
        return "%d: %s" % (self.lineno, line)

    def __getstate__(self):
        odict = self.__dict__.copy()  # copy the dict since we change it
        del odict['fh']              # remove filehandle entry
        return odict

    def __setstate__(self, dict):
        fh = open(dict['file'])      # reopen file
        count = dict['lineno']       # read from file...
        while count:                 # until line count is restored
            fh.readline()
            count = count - 1
        self.__dict__.update(dict)   # update attributes
        self.fh = fh                 # save the file object

    def __copy__(self, dst, *args, follow_symlinks=True):
        """Copy data and mode bits ("cp src dst"). Return the file's destination.

        The destination may be a directory.

        If follow_symlinks is false, symlinks won't be followed. This
        resembles GNU's "cp -P src dst".

        If source and destination are the same file, a SameFileError will be
        raised.
        """
        shutil.copy(self, dst, *args, follow_symlinks=follow_symlinks)

# on god `self.assertIsInstance(OrderedHistory(), list)` just failed
# class OrderedHistory(collections.UserList):
class OrderedHistory(collections.abc.MutableSequence):
    """A History interface that more closely matches the standard library.

    Implements the new append_history_file function.
    Stores items in history as a string (pyreadline stores them as the
    non-standard ReadLineTextBuffer).

    Attributes
    ----------
    lastcommand :
    last_search_for
        Implemented as attributes because this information probably needs to be
        shared across instances.
    line_buffer : str
        current line of text the user is editing
        Actually don't make that same mistake. Implement it elsewhere.
    """
    lastcommand = None
    last_search_for = ""

    def __init__(self,
            history_length: Optional[int] =100,
            history: Optional[List[AnyStr]] =None,
            filename: Optional[os.PathLike] =None,
        ):
        """Initialize the LineHistory object.

        Parameters
        ----------
        history_length : int, optional
        history : list, optional
            Previously run commands to initialize with.
            If None, (the default), then :meth:`read_history_file` will be called.
        filename : os.PathLike, optional

        """
        self._history_length = history_length
        # so hold up i assume this means we don't read in the history file
        # upon initialization. TODO: who does?
        self.history = [] if history is None else history
        if len(self.history) == 0:
            self.read_history_file()

        try:
            self.filename = (
                filename
                if filename is not None
                else os.path.expanduser("~/.python_history")
            )
        except PermissionError:
            raise
        except OSError:
            traceback.print_exc(sys.last_traceback)
            self.filename = io.StringIO()

    # Dunders that make this easier to work with: {{{
    def __iter__(self):
        for i in self.history_length:
            return self.get_history_item(i)

    def __reversed__(self):
        for key in self.history:
            yield key


    def __repr__(self):
        return "<%s:>" % self.__class__.__name__

    def __eq__(self, other):
        return self.history == other

    def __hash__(self):
        return hash(self.history)

    def __mro__(self):
        mro = getmro(self.__class__)
        ha = ("list", mro)
        return ha

    def __len__(self):
        return self.get_current_history_length()

    def __getitem__(self, index):
        """

        Parameters
        ----------
        index :
        step :

        Returns
        -------

        """
        return self.history[index]

    def __setitem__(self, idx, line, *args):
        if args:
            self.history[idx] = [line, *args]
        else:
            self.history[idx] = [line]

    def __delitem__(self, idx):
        del self.history[idx]

    def __add__(self, line):
        if isinstance(line, OrderedHistory):
            self.history.extend(line)
            self.write_history_file()
        else:
            self.history.append(line)

    def __iadd__(self, line):
        self.__add__(line)

    # So i think this is supposed to return an int so don't do this
    # def __index__(self, key):
    # return self.history[key]

    # Implementing the MutableSequence protocol

    def insert(self, item, idx=0):
        self.history.insert(idx, item)

    # The actual Readline interface

    def add_history(self, line):
        """Append a line to the history buffer, as if it was the last line typed.

        Checks to ensure that line is not the same as the last line in history,
        as well as ensuring that line isn't empty.
        """
        if len(line) == 0:
            return
        elif self.history[-1] == line:
            return
        else:
            self.history.append(line)

    def read_history_file(self, filename=None, encoding=None):
        """Load a readline history file.

        Parameters
        ----------
        filename :
        encoding :

        Raises
        -------
        PermissionError
        UnicodeDecodeError
        """
        if encoding is None:
            encoding = sys.getdefaultencoding()
        if filename is None:
            filename = self.filename
        try:
            with io.open(filename, "rt", encoding=encoding) as fd:
                for line in fd:
                    self.add_history(dedent(line))
        except PermissionError:
            raise
        except OSError:
            traceback.print_exc(sys.last_traceback)
        except UnicodeDecodeError:
            raise  # TODO:

    def flush(self, filename: Optional[os.PathLike] =None, full: bool = False):
        """Flush working contents and save to disk.

        Parameters
        ----------
        full : bool, optional
            If True, ignore `history_length` and write the entire session's history
            to the file 'filename'.
        filename : os.PathLike, optional
            If not given, defaults to :attr:`history_filename` or '$HOME/.python_history'.

        """
        if filename is None:
            filename = self.history_filename
        with io.open(filename, "wb") as fp:
            if full:
                fp.writelines(self.history)
            for line in self.history[-self.history_length:]:
                fp.write(line)

    def write_history_file(self, filename : Optional[os.PathLike] =None):
        """Save a readline history file."""
        if filename is None:
            filename = self.history_filename
        with io.open(filename, "wb") as fp:
            for line in self.history[-self.history_length:]:
                fp.write(line)

    def append_history_file(self, nelements, filename : Optional[os.PathLike] =None):
        """Append the last nelements items of the history list to file.

        The default filename is ~/.python_history.
        Implemented so as to match the standard library addition.
        """
        if filename is None:
            filename = self.history_filename
        with io.open(filename, "wb") as fp:
            for line in self.history[-nelements:]:
                fp.write(line)

    def clear_history(self):
        """Clear readline history."""
        self.history[:] = []

    def get_current_history_length(self):
        """Return the number of lines currently in the history.

        (This is different from `get_history_length`, which returns
        the maximum number of lines that will be written to a history file.)
        """
        return len(self.history)

    def get_history_item(self, index : int):
        """Return the current contents of history item at index

        **NO LONGER STARTS AT 1! Python is a 0-indexed language.
        """
        # log("get_history_item: index:%d item:%r" % (index, item))
        try:
            return self.history[index]
        except IndexError:
            raise StopIteration  # right?

    def get_history_slice(self, start=0, stop=None, step=1):
        return slice(self.history[start], self.history[stop], step)

    def __slice__(self, start=0, stop=None, step=1):
        return self.get_history_slice(start, stop, step)

    @property
    def get_history_length(self) -> int:
        """Return the maximum number of lines that will be written to `filename`."""
        return self._history_length

    @_history_length.setter
    def set_history_length(self, value: int):
        """Set the new history length.

        In other words, set the maximal number of lines which will be written to
        the history file. A negative length is used to inhibit
        history truncation.

        Raises
        ------
        TypeError
            When not provided an int.
        """
        if not isinstance(value, int):
            raise TypeError
        self._history_length = value


class ACompletelyDifferentClass(OrderedHistory):

    # Bindable Commands: {{{

    def previous_history(self, current):  # (C-p)
        """Move back through the history list, fetching the previous command. """
        if self.history_cursor == len(self.history):
            self.history.append(
                current.copy()
            )  # do not use add_history since we do not want to increment cursor

        if self.history_cursor > 0:
            self.history_cursor -= 1
            current.set_line(self.history[self.history_cursor].get_line_text())
            current.point = lineobj.EndOfLine

    def next_history(self, current):  # (C-n)
        """Move forward through the history list, fetching the next command. """
        if self.history_cursor < len(self.history) - 1:
            self.history_cursor += 1
            current.set_line(self.history[self.history_cursor].get_line_text())

    def beginning_of_history(self):  # (M-<)
        """Move to the first line in the history."""
        self.history_cursor = 0
        if len(self.history) > 0:
            self.l_buffer = self.history[0]

    def end_of_history(self, current):  # (M->)
        """Move to the end of the input history."""
        self.history_cursor = len(self.history)
        current.set_line(self.history[-1].get_line_text())

    def _any_search(self, searchfor, startpos=None):

        for idx, line in enumerate(self.history):
            if searchfor in line:
                startpos = idx
                return self.history[startpos].get_line_text()

        if self.history:
            result = self.history[startpos].get_line_text()
        else:
            result = lineobj.ReadLineTextBuffer("")
        self.history_cursor = startpos
        self.last_search_for = searchfor

        return result

    def reverse_search_history(self, searchfor, startpos=None):
        if startpos is None:
            startpos = self.history_cursor
        # If we get a new search without change in search term it means
        # someone pushed ctrl-r and we should find the next match
        if self.last_search_for == searchfor and startpos > 0:
            startpos -= 1
            for idx, line in reversed(enumerate(self.history)):
                if searchfor in line:
                    startpos = idx
                    break
        return self._any_search(searchfor, startpos=startpos)

    def forward_search_history(self, searchfor, startpos=None):
        if startpos is None:
            startpos = min(
                self.history_cursor, max(
                    0, self.get_current_history_length() - 1)
            )
        # If we get a new search without change in search term it means
        # someone pushed ctrl-r and we should find the next match
        if (
            self.last_search_for == searchfor
            and startpos < self.get_current_history_length() - 1
        ):
            startpos += 1
            for idx, line in enumerate(self.history):
                if searchfor in line:
                    startpos = idx
                    break
        return self._any_search(searchfor, startpos=startpos)

    def _search(self, direction, partial):
        if len(self.history) == 0:
            return
        query = ""
        hcstart = max(self.history_cursor, 0)
        hc = self.history_cursor + direction

        if (
            self.lastcommand != self.history_search_forward
            and self.lastcommand != self.history_search_backward
        ):
            query = "".join(partial[0: partial.point].get_line_text())

        while (direction < 0 and hc >= 0) or (direction > 0 and hc < len(self.history)):
            try:
                h = self.history[hc]
            except IndexError:
                raise

            if not query:
                log(
                    "pyreadline.lineeditor.history.LineHistory._search: Why is `if not query` line 300 True?"
                )
                self.history_cursor = hc
                result = lineobj.ReadLineTextBuffer(
                    h, point=len(h.get_line_text()))
                return result
            elif h.get_line_text().startswith(query) and (h != partial.get_line_text()):
                self.history_cursor = hc
                result = lineobj.ReadLineTextBuffer(h, point=partial.point)
                return result
            else:
                if hc >= len(self.history) and not query:
                    self.history_cursor = len(self.history)
                    return lineobj.ReadLineTextBuffer("", point=0)
                elif (
                    self.history[max(min(hcstart, len(self.history) - 1), 0)]
                    .get_line_text()
                    .startswith(query)
                    and query
                ):
                    return lineobj.ReadLineTextBuffer(
                        self.history[max(
                            min(hcstart, len(self.history) - 1), 0)],
                        point=partial.point,
                    )
                else:
                    return lineobj.ReadLineTextBuffer(partial, point=partial.point)

    def history_search_forward(self, partial):  # ()
        """Search for 'partial' between the start of the line and the point.

        This is a non-incremental search. By default, this command is unbound.
        """
        return self._search(1, partial)

    def history_search_backward(self, partial):  # ()
        """Search backward for 'partial' between the line and the point.

        This is a non-incremental search. By default, this command is unbound.
        """
        return self._search(-1, partial)

