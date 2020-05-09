# optmatch - Python command line parsing made easy

Full documentation: https://coderazzi.net/python/optmatch

*   [Quick introduction](#quick-introduction)
*   [Purpose](#purpose)
*   [Concepts](#concepts)
*   [Tutorial](#tutorial)
*   [History](#history)
*   [Issues](#issues)
*   [Install](#install)

## Quick introduction
**optmatch** is a python library that allows parsing command line options in a simple way. For example, a tool supporting two options called _mode_ and _verbose_, and requiring two arguments, called _file_ and _where_, would be coded as:

    class Example(OptionMatcher):
    
        @optmatcher
        def handle(self, file, verbose_flag=False, mode_option='simple', where=None):
            ... 

This tool would support a syntax such as:

    [--verbose] [--mode MODE] file [where]

In the previous example, the suffix of the method's parameters define the role of each parameter. Alternatively, the decorator can embed this information, like in:

    class Example(OptionMatcher):
    
        @optmatcher(flags='verbose', options='mode')
        def handle(self, file, verbose=False, mode='simple', where=None):
            ... 

Which is equivalent to the initial example. A more complicated case would be:

    class Example(OptionMatcher):
    
        @optmatcher
        def handle_help(self, help_flag):
            ... 
    
        @optmatcher
        def handle_compression(self, file, compress_flag=False):
            ...
    
        @optmatcher(flags='verbose', options='mode')
        def handle(self, file, verbose=False, mode='simple', where=None):
            ... 

In this case, the tool supports three possible alternatives:

    [--help]
    
    [--compress] file
    
    [--verbose] [--mode MODE] file [where]

And the library issues usage error messages if the user enters invalid arguments, like _--compress_ and _--mode_--, which are mutually incompatible.

The previous examples show the simplest ways to access this library, which contains quite a lof of functionality to cover most aspects related to command line parsing, including printing usage messages, handling aliases, etc.

## Purpose

**optmatch** defines the command line parsing by setting the handler or handlers than will process the command line. The library then matches the received input with these handlers, invoking the most convenient one, or issuing error messages if the input does not match the expected syntax.

In addition to these handlers, **optmatch** supports a specific interface to define aliases, documentation associated to each argument/option, etc, and it is able to automatize the generation of usage messages.

Its initial purpose was to extend the existing related functionality. There are two existing libraries to handle command line options parsing in python: [getopt](http://docs.python.org/library/getopt.html) and [optparse](http://docs.python.org/library/optparse.html).

*   **getopt** usage is rather simple, and it is almost just limited to split the received arguments into a list of expected arguments: the programmer must still make sense of the received input, checking that all arguments are there, that they are not incompatible, and then, invoking the handler or handlers to process them.
*   **optparse** provides a much richer interface, although it mostly makes the usage of **getopt** convenient -and it also provides printing usage messages-. Using **optparse** requires a set of well defined steps: defining the flags/options, etc, its aliases and documentation. For each option is possible to associate some actions, like storing a variable or invoking a function, all defined in a completely procedural way.

The initial purpose behind **optmatch** was to extend **optparse** to handle some usual operations: defining incompatibilities between arguments, or whether an option would require the presence of some other options. Eventually, it came the idea of just matching command line options to the signature of the parameters, which allows for most of the initial planned checks, and makes handling the command line options very simple.

## Concepts

**optmatch** is not limited to GNU style command line options. In this style, options can be specified in short format or long format. For example, an alias can be defined between the short option _v_ and the long one _verbose_. The user can then enter _-v_ or _--verbose_, indistinctly.

Other valid styles also supported in **optmatch** include the typical Windows format, like in _/help_ or using _-_ as prefix for short and long options, like in _-help_. In this document, the GNU style is refered as **getopt** mode.

In any case, some terms apply to both styles:

*   option: is an argument prefixed with the option prefix -normally _-_ or _--_, and with a value associated. For example:

        --mode=optimized

*   flag: is an option without associated value. If present, it is assumed to have the boolean value _True_. For example:

        --verbose

*   prefix: is an option that can be specified multiple times. For example:

        -I/usr/include -I/opt/include

*   parameter: any argument in the command line that does not include the option prefix.

Note that, in this document, it is normally used the word option to cover not only options, but also flags and prefixes.

In **getopt** mode, there are two option prefixes:

*   _-_: short prefix. Only short options apply, containing a single letter. The user can enter multiple short options together, like in:

        -iof here

    which stands for the short flags _i_, _o_, and the short option _f_, with value _here_
*   _--_: long prefix. Only long options apply, containing two or more letters. The user cannot enter multiple long options together. If a value is specified, it can be done on a separate argument, like in:

        --mode optimized

    Or, alternatively, in the same argument, separated by _=_ (or any other pre-specified character):

        --mode=optimized

In non-**getopt** mode, only one option prefix applies, normally _-_ or _/_. In this case, there is no distinction between short and long options, and the user must enter each option on a separate argument, like in:

    /mode:optimized

Finally, **optmatch** uses the concept 'gnu mode'. If specifically defined, it implies that all option arguments must be specified at the beginning of the command line. Otherwise (the default), options and parameters can be freely intermixed.

## Tutorial

*   [The Basics](#the-basics)
*   [Parameters mapping](#parameters-mapping)
*   [Valid identifiers](#valid-identifiers)
*   [Aliases](#aliases)
*   [Defining common options](#defining-common-options)
*   [Decorators](#decorators)
*   [Advanced optset](#advanced-optset)
*   [Usage mode](#usage-mode)
*   [Handling incorrect usage](#handling-incorrect-usage)
*   [Handling incorrect syntax](#handling-incorrect-syntax)
*   [Basic help](#basic-help)
*   [More on help](#more-on-help)
*   [Var names](#var-names)

### The basics

There are three main elements to import from **optmatch**:

*   **OptionMatcher**: the main class; users must implement the methods that handle the command line options as part of a subclass of OptionMatcher.
*   **optmatcher**: a decorator that specifies that a method in a class is a command line handler.
*   **optset**: a decorator that specifies that a method in a class handles common options to one or more handlers.

The following code defines two such handlers, and processes the command line arguments:

    from optmatch import OptionMatcher, optmatcher, optset
    
    class Example(OptionMatcher):
    
        @optmatcher
        def handle_compression(self, file, compress_flag):
            '''Compress the specified file'''
            ...
    
        @optmatcher
        def handle_move(self, file, where=None, verbose_flag=False):
            '''Moves the file to the specified directory'''
            ... 
    
    Example().process(sys.argv)

This code allows the tool to handle command line arguments where the user specifies one of:

    [--compress] file
    
    [--verbose] file [where]

### Parameters mapping

Methods defined with **@optmatcher** will handle the parameters given in the command line. The mapping between the options/flags and the method parameters can be defined in two ways:

*   By convention on the parameter names: the suffix for each parameter on the handlers define the parameter role. The valid suffixes are:
    *   **Flag** or **_flag**
    *   **Option** or **_option**
    *   **Prefix** or **_prefix**
    *   **OptionInt** or **_option_int**: the associated value is converted to an integer
    *   **OptionFloat** or **_option_float**: the associated value is converted to a float number
*   Providing full information in the _@optmatcher_ decorator: the following method defines a flag called compress:

        @optmatcher(flags='compress')
        def handle_compression(self, file, compress):
                ...

Full information on the _@optmatcher_ decorator is given [below](#decorators). Note that it is not allowed to mix both alternatives: if the _@optmatcher_ decorator includes any information, the method names will not be processed.

### Valid identifiers

A flag such as _--dry-run_ would be mapped to a parameter called _dry-run/dry-run_flag/dry-runFlag_, which are not valid python identifiers. The library will automatically convert a parameter name such as _dryRunFlag_ or _dry_run_flag_ into a command line option called _--dry-run_.

This is convenient, but it still does not support options that would be converted to invalid python identifiers. For example, _-$_, _-2_ or _--import_. In this case, it is needed to specify the option using the full **@optmatcher** decoration. For example:

    @optmatcher(flags='2) def handle(_2): pass

In this example, it will be expected a flag called _2_, and it will be mapped to the first parameter, whose name, once removed any non alpha-numerical characters, match the given flag.

Full control about the mapping flag-parameter can be specified using the decorator, using the operator **as**:

    @optmatcher(flags='load as import') def handle(load): pass

In this case, the parameter load is mapped to a flag called _--import_.

### Aliases

Aliases are the way to connect short and long options, like specifying that _-v_ is equivalent to _--verbose_

In **getopt** mode, an alias must always match a short option (one letter) to a long one, or viceversa. There are two ways ot specify aliases: on the _OptionMatcher_ constructor, or using its _set_aliases_ method, which expects a dictionary, such as:

    OptionMatcher.set_aliases({'v':'verbose'})

The help system automatically displays the option's aliases.

### Defining common options

There are cases where one or more options apply to multiple handlers. A typical example would be the verbose flag. Instead of defining it on all the matchers, it is possible to use the decorator **optset**, like in:

    @optset
    def handle_help(self, help_flag):
            ... 

It is quite equivalent to the **optmatcher** decorator, so it is possible to specify its behaviour through the decorator:

    @optset(flags='help')
    def handle_help(self, help):
            ...

These handlers are called, for convenience, when possible. That it, if, in the previous example does not include the flag _--help_, the method _handle_help_ is not invoked. However, if could have been defined with default values, like in:

    @optset(flags='help')
    def handle_help(self, help=False):
            ... 

In this case, the method will be always called, which simplifies setting some common variables

### Decorators

The two decorators in this module, **optmatcher** and **optset**, allows defining the behaviour of the underlying matcher via their parameters. Both decorators share most of the parameters:

*   **options**: defines which of the parameters are considered options. This parameter is a string, where the defined options are separated by commas, like in:

        @optmatcher(options='mode, file')
        def matcher(self, mode, file):
           ...

    Each of the parameters can be defined like:

        parameter as public_name

    For example:

        @optmatcher(options='mode as verbose-mode, file as target.file')
        def matcher(self, mode, file):
           ...

    In this example, the matcher expects two options, named <span class="code">verbose-mode</span> and <span class="code">target-file</span>
*   **int_options**: defines which of the parameters are considered options associated to integer values. The remarks given to the normal options also apply for integer options.
*   **float_options**: defines which of the parameters are considered options associated to floatvalues. The remarks given to the normal options also apply for float options.
*   **prefixes**: defines which of the parameters are considered prefixes. The remarks given to the normal options also apply for prefixes.
*   **flags**: defines which of the parameters are considered flags. The remarks given to the normal options also apply for flags. As additional feature, it is possible to define **orphan flags**, which are specified in the decorator, but have no associated matching parameter. For example:

        @optset(flags='quiet')
        def set_quiet(self):
           ...
    
    In this case, only when the user enters <span class="code">--quiet</span>, this matcher is invoked. Note that it would be possible to introduce a parameter <span class="code">quiet</span> in this matcher, but, when invoked, it would always be set to True. Hereby, it is possible to define it on the decorator only.
*   **priority**. Matchers are tried in order, being the order defined by alphabetical sorting on the matcher method names. This order can be observed when the help lists all the alternatived for the current **OptionMatcher**. It is possible to alter this order by defining the priorities of each matcher. Higher priorities are invoked first.

The _optset_ decorator can define one additional attribute called _applies_, and the _optmatch_ decorator has also one related attribute called _exclusive_, both explained in the following section

### Advanced optset

**optset** is also useful to define mandatory options. For example, a tool could require that the flag _--test_ is provided with an option _--file=FILENAME_ where the file to test is specified.

This could be defined as:

    @optset
    def handle_test(self, test_flag, file_option):
            ... 

If the user specifies _--test_ but not _--file=_ an exception is automatically raised.

Now, there could be multiple matchers, but this option _--test_ could only apply to one of the matchers. It is possible to limit the scope of a **optset** handler to one or several matchers:

    @optset(applies='zip')
    def handle_test(self, test_flag, file_option):
            ... 
    
    @optmatcher
    def zip(self, file):
            ... 

It is possible to define multiple matchers, separated by commas or using limited regular expressions:

    @optset(applies='zip, test*')
    def handle_test(self, test_flag, file_option):
            ... 

In this case, it would apply to the method _zip_, and to all methods starting with _test_.

If a **optset** handler has no _applies_ specification, it would apply to all defined matchers, unless a matcher specifies **exclusive=True**, such as:

    @optmatcher(exclusive=True)
    def handle(self, test_flag, file_option):
            ... 

### Usage mode

By default, **OptionMatcher** works on **getopt** mode. In other words, it is compatible with **getopt** and **optparse**: there are short options, prefixed with _-_, and long options, prefixed with _--_.

By default also, the **gnu mode** is disabled: option arguments can be freely intermixed with required arguments. This mode can be disabled on the _OptionMatcher.process_ method, specifying the argument _gnu=False_.

This mode can be overriden by specifying a different option prefix. As usual, this can be done on the contructor, or using a specific method, in this case: _OptionMatcher.set_mode_. For example,

    OptionMatcher.set_mode(option_prefix='-')

In this example, the distinction between short and long arguments dissapear, and all options are expected with the simple prefix _-_.

It is also possible to define the character that specifies the assignment, which is by default _=_. For example,

    OptionMatcher.set_mode(option_prefix='/', assigner=':')

enables Windows typical mode:

    /mode:optimized

###  Handling incorrect usage

When the user's input does not match the expected input, an exception is raised.

This exception is the _UsageException_, defined in the **optmatcher** library. However, by default, it is automatically handled, so that a message is printed on the standard error stream.

To disable this behaviour, allowing the library's client to process it at will, it is needed to invoke the _OptionMatcher.process_ like in:

    .process(handle_usage_problems=False)

### Handling incorrect syntax

_UsageException_ is a class that inherits from _OptionMatcherException_; this exception is raised when the syntax or aliases are incorrectly defined. It does not depend on the user's input.

### Basic help

In the previous example, in addition to the two specified cases, the user can enter _--help_ to receive some basic usage information. It would look like:

    Usage: [common options] file where
    
    options:
      --compress
      -h, --help            shows this help message
      --verbose
    
    alternatives:
    
    * --compress file       Compress the specified file
    
    * [--verbose (False)] file [where]
                            Moves the file to the specified directory
    
    * -h                    shows the help message

Note that the documentation for each handlers is used to document the alternatives, but the options are not documented. To document them, it is needed to supply it as:

    OptionMatcher.set_usage_info(options_help={'compress':'compress the specified file'})

The information for all the options must be provided at once, in a dictionary.

### More on help

By default, **optmatcher** adds a matcher to handle help requests. That is, _-h_ or _--help_, or even _/help_ it the correct prefix was setup, will automatically display the normal usage message.

There are a few ways to override this behaviour:

*   Disabling the default help: this can be done on the **OptionMatcher** constructor, or invoking its _OptionMatcher.enable_default_help_ method.
*   Overriding the _OptionMatcher.print_help_ method, that will be automatically invoked by the default help.
*   Defining an explicit help matcher, such as:

        optmatcher
        def handle_help(self, help_flag):
                ... 

In these two last cases, the **OptionMatcher** class provides some functionality to display the required information. The method _OptionMatcher.get_usage_ returns a _OptionMatcher.print_help_ UsageAccessor instance, that can be used to format the usage message and to retrieve the required information, related to defined options, paraeters, etc.

### Var names

**varnames** is a concept related to the help system. If it is defined an option called _filename_, the default usage for this option will print something like:

    filename = FILENAME

It is possible to redefine the associated variable (hence the var name), by setting the var names on the constructor:

    OptionMatcher(option_var_names{'filename':'ORIGIN'})

This would print a usage message such as:

    filename = ORIGIN

## <a name="history">History</a>

*   Version 1.0.0, 10th May 2020.
    * No functionality update, documentation reworked.
*   Version 0.9.2, 19th June 2018.
    *   **rename_pars** functionality removed.
    *   **public names** functionality modified: not possible anymore to invoke set_public_names, and the matching between parameters and flags/options is modified -see [valid identifiers](#valid_identifiers)-
*   Version 0.9.1, 14th May 2018.
    *   Single file supporting now python 2 and 3.
    *   Include as standard Pypi packages
*   Version 0.9.0, 13th May 2018\. Included support for naming convention based on underscores (not only camelCase). Also, the library itself is now using the default python syntax, with all methods, variables using underscores.
*   Version 0.8.7, 13th June 2009\. Minor leftover changes
*   Version 0.8.6, 13th June 2009\. Added version for Python 3.0
*   Version 0.8.5, 2nd June 2009.
    *   Improves help format
    *   All provided options are automatically expanded (shell and user variables)
*   Version 0.8.4, 29th May 2009\. First downloadable version.
*   Version 0.8, 14th May 2009\. API totally simplified, including minor refactoring.
*   Version 0.7, 1st May 2009\. Introduction of **varnames** in help system, help support vastly improved.
*   Version 0.6, 2nd April 2009\. Introduction of functionality to help checking the syntax (this was removed on 0.8).
*   Version 0.5, 15th January 2009\. Introduction of decorators.
*   Version 0.4, 10th December 2008\. Basic help system.
*   Version 0.3, 3rd November 2008\. Support for non-getopt mode.
*   Version 0.2, 25th September 2008\. Introduction of common handler concept.
*   Version 0.1, 12th September 2008\. First working version, totally functional.

## Issues

Issues or bugs can be reported at the Github repository [issues site](https://github.com/coderazzi/optmatch/issues).

There is also a [forum](https://groups.google.com/forum/#!forum/optmatch) to discuss any related topics

## Install

The project is hosted on a **git [repository](https://github.com/coderazzi/optmatch)** at Github (project name: optmatch)

The easiest way to install it is using the standard **pip**:

    pip install optmatch

It works for python 2 and 3\. In any case, the library is a single python file, which can be tested without updating any site packages.

*   Current version is 1.0, released the 10h May 2020:
    *   [optmatch.py](https://raw.githubusercontent.com/coderazzi/optmatch/master/src/optmatch.py)
    *   Unit tests: [tests.py](https://raw.githubusercontent.com/coderazzi/optmatch/master/test/tests.py)

**optmatch** is open source, distributed with MIT license:

    Copyright (c) Luis M. Pena <lu@coderazzi.net>  All rights reserved.
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
