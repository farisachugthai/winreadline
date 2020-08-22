================
``winreadline``
================

.. index:: module: readline

.. sectionauthor:: Faris A. Chugthai

.. moduleauthor:: Faris A. Chugthai

.. highlight:: python

:date: |today|


Introduction
------------

`winreadline` is a package inspired by GNU readline which aims to improve the
command line editing experience. In most UNIX based implementations of python,
GNU readline is available and used by CPython.

Unfortunately,this is not the case on Windows.

This repository aims to implement readline on Windows as so.

It's largely inspired by `pyreadline
<https://github.com/pyreadline/pyreadline>`_.

However that package is seemingly abandoned. While there have been sporadic
commits over the last few years, the repository overall has swaths of code
that have not been updated in more than 15 years.


Installation
------------
Install with a :command:`python` invocation of something similar to.::

   python -m pip install -U -e.


Features
--------
*  Keybindings in accordance with the GNU readline library

*  :kbd:`Shift`-Arrow keys for text selection

*  :kbd:`Control-C` for copy

   * Activate with `allow_ctrl_c(True)` in config file. An example is given at
     :file:`pyreadline/configuration/pyreadlineconfig.ini`

*  Double tapping :kbd:`Control-C` will raise a `KeyboardInterrupt`

   * use `ctrl_c_tap_time_interval(x)` where x is your preferred tap time window

   * default 0.3s

*  standard `paste` which pastes first line of content on clipboard

*  Alternatively, users can set the option ``IPython_paste``

   * which pastes tab-separated data as list of lists or numpy array if all data is numeric

*  `paste_multiline_code` pastes code that spans multiple lines or has
   embedded newlines in it.

   * Useful for copy pasting code


History
-------
Pyreadline is based on the UNC readline package by Gary Bishop which in turn is
based on the `ctypes` module in the standard library.
The pyreadline package is based on the ctypes based UNC readline package by Gary Bishop.

It is not complete. It has been tested for use with Windows 2000 and Windows XP
as well as Windows 10.

Version 2.0 runs on Python 2.6, 2.7, and 3+ using the same code.


Development
------------
The latest development version is always available at the GitHub `repository`_.

The current trunk version can be cloned with git, :command:`git clone
https://github.com/pyreadline/pyreadline.git`.
Pyreadline is based on the UNC readline package by Gary Bishop which in turn is
based on the `ctypes` module in the standard library.

It is not complete. It has been tested for use with Windows 2000 and Windows XP
as well as Windows 10.

Version 2.0 runs on Python 2.6, 2.7, and 3+ using the same code.

.. _repository: https://github.com/farisachugthai/winreadline
