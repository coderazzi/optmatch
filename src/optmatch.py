"""optmatch - matching command line argument by method's signatures
Support usual GNU/Unix conventions, but not exclusively

Author:  LuisM Pena <luismi@coderazzi.net>
Site:    www.coderazzi.net/python/optmatch

Example, a OptionMatcher subclass could define the methods:
    
    @optmatcher
    def handle(suffixOption, file, verboseFlag=None, DPrefix=None):
        pass
       
    @optmatcher
    def handleHelp(usageFlag):
        pass
          
    This class would support one of the following inputs:
        [--verbose] --suffix=value [-Done -Dtwo ...] filename
        Or
        [--usage]

It is possible to specify one or more functions or methods -from
    now called matchers- to process command line arguments. 
    The role of each parameter in the function is defined in two
    ways:
    A- Via the parameter name: Its suffix determines if it is a flag, 
        and option, a prefix, or a simple non option argument. For
        example, verboseFlag identifies this parameter as the flag 'verbose'
    B- Via a decorator, setting the variable name as one of the 
          supported roles (flags, options, etc...)
       
It is also possible to specify a single matcher to handle options 
which are common to every other possible matcher.
       
"""

__version__ = "0.8.1"

__all__ = ['optcommon',
           'optmatcher',
           'OptionMatcher',
           'OptionMatcherException',
           'UsageException']
           
__copyright__ = """
Copyright (c) LuisM Pena <luismi@coderazzi.net>  All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

  * Neither the name of the author nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import re
import types

class Decoration(object):
    '''
    Namespace to define any decoration functionality
    optmatcher decorator adds an attribute 'optmatcher' that contains
        the list of parameters provided in the decorator definition, 
        like flags, options, etc, in a given order
    optcommon decorator behaves as the optmatcher one, but adds a 
        second attribute to the function/method: 'optcommon', with 
        value True
    '''
    
    @staticmethod
    def decorate(optcommon, *args):
        #Decoration method for optmatcher and optcommon decorators.
        #Param optcommon should be True for optcommon decorators
        #Param args is the ordered parameters allowed in those decorators
        
        def decorate(f, value):
            f.optmatcher = value
            if optcommon:
                f.optcommon = True          
            return f
        
        #perhaps the base decorator is called with the function to decorate
        #This happens for cases like: @optmatcher def handle(...)
        #No decorator parameter should be a function, so this case can
        # be handled as follows:
        if (args[0] and not filter(None, args[1:]) and 
            (isinstance(args[0], types.FunctionType) or 
              isinstance(args[0], types.MethodType))):
            return decorate(args[0], [])

        return lambda x: decorate(x, args)
    
    @staticmethod
    def parseDecoration(function):
        #Parses the optmatcher decoration in the given function.
        #If specified, it returns a tuple Info, priority, 
        #  or (None, None) otherwise, where Info is the ordered list
        #  of the decorator parameters
        
        def parser(flags=None, options=None, intOptions=None,
                   floatOptions=None, prefixes=None, parameters=None,
                   priority=None):
            return (flags, options, intOptions, floatOptions, prefixes,
                    parameters), priority
            
        try:
            return parser(*function.optmatcher)
        except:
            return None, None

    @staticmethod
    def getDecoratedMethods(instance, definedAsCommon):
        '''Returns the methods decorated with optmatcher, priority sorted'''
        functionsAndPriorities = []
        for att in dir(instance):
            f = getattr (instance, att)
            if definedAsCommon == hasattr(f, 'optcommon'):
                info, priority = Decoration.parseDecoration(f)
                if info:
                    functionsAndPriorities.append((priority or 0, f))
        #sort now by inverse priority, and return just the functions
        functionsAndPriorities.sort(lambda x, y: y[0] - x[0]) 
        return [f for p, f in functionsAndPriorities]    


class CommandLine(object):
    '''Class to handle the Command Line arguments
    
    It allows handling arguments one by one, even for short options, 
       where -cov could mean -c -o -v
    Available instance attributes:
       arg    : String, the whole argument, without the prefix option
                if the argument were '--option', arg would be 'option'
       name   : String, the name of the current argument
                if the argument were '--op=2', name would be 'op'
       value  : String, the value of the current argument
                if the argument were '--op=2', name would be '2'
       option : Bool, true if the current argument is an option
       isShort: Bool, true if the current arg is a short option
    ''' 
       
    def __init__(self, args, optionPrefix, delimiter, gnuMode):
        '''
        param args: the list of arguments to handle (first is dismissed)
        param optionPrefix: the prefix for the options. If '--', it will
              be enabled the usage of short options with '-'.
              Must be escaped for RE purposes
        param delimiter: the string to be used as separator between
              names and values. Must be escaped for RE purposes
        param gnuMode: if true, after a non option argument, all remaining
              arguments will be treated as non options 
        '''
        #reShort is hardcoded to '-' if the option is defined as '--'
        self.reShort = (optionPrefix == '--') and re.compile('-(.+)$')
        self.reOption = re.compile(optionPrefix + '(.+)$')
        self.reSeparation = re.compile('(.+?)' + delimiter + '(.+)$')
        self.args = args
        self.gnuMode = gnuMode
        self.canBeOption = True  
        self.reset()
        
    def reset(self):
        self.next = 1
        if len(self.args) > 1:
            self._next()
            
    def getPosition(self):
        if self.finished():
            return self.args, 0
        inShort = len(self.arg)
        if self.value:
            inShort -= len(self.value)
        return self.next, inShort 
        
    def finished(self):
        return self.next == 1
    
    def separate(self, what):
        '''Separates the passed string into name and value.
        Returns a tuple (status, name, value) where status is True
           if the string was separated
        '''
        m = self.reSeparation.match(what)
        return m and (True, m.group(1), m.group(2)) or (False, what, None)
        
    def setArgHandled(self):
        '''Reports that the current argument has been handled.
        It returns True if there are no more arguments to handle or the 
            next argument is an option
        '''
        if self.next >= len(self.args):
            self.next = 1
        return (self.next == 1) or self._next()
            
    def setShortArgHandled(self):
        '''Reports that the current (short!) argument has been handled.'''
        if self.value:
            self.name, self.value = self.value[0], self.value[1:]
        else:
            self.setArgHandled()
    
    def _next(self):
        '''Handles the next argument, returning True if it is an option'''
        self.arg = self.args[self.next]
        arg = self.arg #...
        self.next += 1
        self.option = False
        if self.canBeOption:
            match = self.reOption.match(self.arg)
            if match:
                self.option, self.isShort = True, False
                arg = match.group(1)
            else:               
                match = self.reShort and self.reShort.match(self.arg)
                if match:
                    arg = match.group(1)
                    self.name, self.value = arg[0], arg[1:]
                    self.option, self.isShort, self.split = True, True, False
                    return True
                self.canBeOption = not self.gnuMode
        self.split, self.name, self.value = self.separate(arg)
        return self.option


class OptMatcherInfo(object):
    '''Internal class, holds the information associated to each matcher'''
        
    DECORATOR_SPLIT = re.compile('\\s*,\\s*')
    DECORATOR_ASSIGN = re.compile('(.+?)\\s+as\\s+(.+)')
    FLAG_PATTERN = re.compile('(.+)' + 
                              '(Flag|Option|OptionInt|OptionFloat|Prefix)$')

    def __init__(self, func, getoptmode):
        #getoptmode is a boolean parameter that specifies whether
        #     to use getoptmode or not. In getoptmode, there is specific
        #     support for short/long options; in addition, kwargs
        #     parameters cannot be supported.
        self._initializeParametersInformation(func, getoptmode)
        
        #With getoptmode, in addition to the normal definitions, users
        # can specify short options, stored in sortedDefs 
        self.defs = set()       #definitions (flags/options/prefixes)
        if getoptmode:
            self.shortDefs = set()    
        else:
            self.shortDefs = self.defs
            
        #populate now self.shortDefs and short.defs
        for group in self.flags, self.options, self.prefixes:
            for name in group.keys():
                if len(name) == 1:
                    #note that, in non getopt mode, shortDefs points to defs
                    defSet = self.shortDefs
                else:
                    defSet = self.defs
                if name in defSet: #for example, defining kFlag and kOption
                    raise OptionMatcherException('Repeated option "' + name + 
                                                 '" in ' + self._describe())
                defSet.add(name)

    def _initializeParametersInformation(self, func, getoptmode):   
        #Initializes all parameter information associated to the function: 
        self.flags = {}      #maps flag name to parameter index
        self.options = {}    #maps option name to parameter index
        self.prefixes = {}   #maps prefix name to parameter index
        self.converts = {}   #maps from index (option) to convert function
        self.pars = {}       #maps parameter index to parameter name
        self.lastArg = 1     #the last available variable index plus 1
        #Note that the index number associated to the first parameter
        # is 1, not zero. This simplifies later many checks

        self.func = func
        self.getoptmode = getoptmode

        vars, self.vararg, kwarg = self._getParametersInfo(func)
        #if kwargs are supported, kwargs is used as a dictinary
        self.kwargs = kwarg and not getoptmode and {}
        
        decorationInfo, priority = Decoration.parseDecoration(func)
        if decorationInfo and filter(None, decorationInfo): 
            self._initializeParametersFromDecorator(vars, *decorationInfo)
        else:
            self._initializeParametersFromSignature(vars)            
           
        #get default values
        defs = list(func.func_defaults or [])
        firstDef = self.lastArg - len(defs)
        self.defaults = dict([(i + firstDef, d) for i, d in enumerate(defs)])
        
    def _initializeParametersFromSignature(self, vars): 
        #Initializes the metadata from the function's parameter names       
        for var in vars:
            match = self.FLAG_PATTERN.match(var)
            if match:
                useName, what = match.group(1), match.group(2)
                if what == 'Flag':
                    self.flags[useName] = self.lastArg
                elif what == 'Prefix':
                    self.prefixes[useName] = self.lastArg
                else:
                    self.options[useName] = self.lastArg
                    if what == 'OptionInt':
                        self.converts[self.lastArg] = self._asInt
                    elif what == 'OptionFloat':
                        self.converts[self.lastArg] = self._asFloat
            else:
                self.pars[self.lastArg] = var
            self.lastArg += 1        

    def _initializeParametersFromDecorator(self, vars, flags, options,
                                           intOptions, floatOptions, prefixes,
                                           parameters):
        #Initializes the metadata from the decorator information       
        ints, floats, used = {}, {}, []
        for att, group  in [(self.flags, flags),
                            (self.options, options),
                            (self.prefixes, prefixes),
                            (self.pars, parameters),
                            (ints, intOptions),
                            (floats, floatOptions)]:
            #in the following loop, n defines each parameter name given
            #in the decorator for each group (flags, options, etc), while
            #v defines the public name (n as v)
            for n, v in self._getDecorationDefinitions(group).items():
                #get the index of the var, raising an error if not found
                # or already used
                try:
                    index = vars.index(n)
                except ValueError:
                    raise OptionMatcherException(n + 
                                  ' is not a known variable')
                if index in used:
                    raise OptionMatcherException(n + 
                                  ' is defined multiple times')
                used.append(index)
                att[v] = 1 + index
        #all groups are created as maps (name -> variable index), but for
        #params the name is not that important, and we store it in the
        #oppossite way
        self.pars = dict([(a, b) for b, a in self.pars.items()])
        #the decorators allow define the parameters to change their known
        #names, for doc purposes, but all function parameters that are not
        #included as flags/options/prefixes are definitely considered 
        #parameters
        self.pars.update(dict([(i + 1, v) for i, v in enumerate(vars) 
                                          if i not in used]))
        #intOptions and floatOptions are options with additional checks:
        self.options.update(ints)
        self.options.update(floats)
        self.converts = dict([(i, self._asFloat) for i in floats.values()])
        self.converts.update(dict([(i, self._asInt) for i in ints.values()]))
        self.lastArg = len(vars) + 1
            
    def getFlags(self):
        '''Returns the defined flags as a map from tuples to 'required'
           The keys are tuples with all the aliases for a given flag
           The value is whether the flag is required or not
        '''
        ret = {}
        for k, v in self._getOptionsAndDefaults(self.flags, self).items():
            ret[k] = v != self
        return ret
                                        
    def getOptions(self, defnull):
        '''Returns the defined options as a tuple.
           The first element is a map from tuples to default values -or to
              defnull is no default provided-. In this map, the keys 
              are tuples with all the aliases for a given flag
           The second element is True if it supports any given option, 
              that is, ** kwargs 
        '''        
        return (self._getOptionsAndDefaults(self.options, defnull),
                self.kwargs != False)
                                        
    def getPrefixes(self):
        '''Returns the defined options as a list of tuples
           Each tuples contains all the aliases for a given prefix
        '''        
        return self._getOptionsAndDefaults(self.prefixes, self).keys()
    
    def getParameters(self, defnull):
        '''Returns the defined parameters as a tuple
           The first element of the tuple is a list of tuples, each
              providing the name of the parameter, and its default value
              This default value is defnull is not provided
           The second element is True if any additional parameters are 
              also supported (varargs is defined)
        '''
        ret = []
        for i in range(1, self.lastArg):
            try:
                name = self.pars[i]
            except KeyError:
                continue
            ret.append((name, self.defaults.get(i, defnull)))
        return ret, self.vararg > 0
                                            
    def setAliases(self, aliases):
        '''Sets aliases between option definitions.'''
        #Aliases affect to all possible options (flags/options/prefixes).
        #If there is a flag 'v' at index 2, and an alias is defined for 'v' 
        #  as 'verbose', flags will be extended with 'verbose' : 2
        #In addition, defs (and/or shortdefs) is extended with the new alias 
        def setAlias(a, b, aSet, bSet):
            #Defines b as an alias in bSet of a, if a is defined in aSet
            #As a result, any option defined as 'a' will be used if the 
            #      user specifies the 'b'
            if a in aSet:
                if b in bSet:
                    raise OptionMatcherException(
                        'Bad alias:' + a + '/' + b + ' in ' + self._describe())
                bSet.add(b)
                for each in self.flags, self.options, self.prefixes:
                    try:
                        each[b] = each[a]
                    except KeyError:
                        pass
            
        for s, l in aliases.items():
            if self.getoptmode:
                #In getoptmode, aliases must map short and long options, 
                #   that is, options with 1 character and options with more 
                #   than 1 character
                if len(s) > len(l):
                    s, l = l, s
                if len(s) > 1 or len(l) == 1:
                    raise OptionMatcherException('Bad alias:' + s + '/' + l)
                setAlias(l, s, self.defs, self.shortDefs)
            elif l in self.defs:
                #if alias 'l' is already known, we try setting from s->l
                s, l = l, s
            setAlias(s, l, self.shortDefs, self.defs)
            
    def getIndexName(self, index):
        #returns the flag/option/parameter with the given index (no prefixes) 
        #Note that it will be returned any of the aliases        
        for n, v in self.flags.items():
            if v == index:
                return 'flag ' + n
        for n, v in self.options.items():
            if v == index:
                return 'option ' + n
        return 'parameter ' + self.pars[index]
            
    def _describe(self):
        '''Describes the underlying method'''
        try:
            name = 'method ' + self.func.im_self.__class__.__name__ + '.'
        except AttributeError:
            name = 'function '
        return name + self.func.__name__
    
    def _getOptionsAndDefaults(self, group, defaultValue):
        #Returns from the given group (flags/options/prefixes), a map 
        #   from tuples to default values
        # The keys are tuples with all the aliases for a given option
        ret, options = {}, {}
        for name, index in group.items():
            options.setdefault(index, []).append(name)
        for index, aliases in options.items():
            ret[tuple(aliases)] = self.defaults.get(index, defaultValue)
        return ret
                                            
    def _getDecorationDefinitions(self, decoration):
        #Returns the definitions associated to a given decorator argument
        #The returned value maps names to 'as' values, if present, or to
        #  themselves, otherwise
        ret = {}
        if decoration:
            try:
                defs = self.DECORATOR_SPLIT.split(decoration.strip())
            except:
                raise OptionMatcherException('Invalid definition')
            for d in defs:
                if d:
                    match = self.DECORATOR_ASSIGN.match(d)
                    if match:
                        ret[match.group(1)] = match.group(2)
                    else:
                        ret[d] = d
        return ret

    def _getParametersInfo(self, f):
        #returns a tuple with the parameters information
        #This information includes: the list of variables, if it supports
        #   varargs, and if it supports kwargs 
        flags, varnames = f.func_code.co_flags, f.func_code.co_varnames
        varargs = flags & 0x0004
        kwargs = flags & 0x0008
        #dismiss self, *args and **kwargs as var names
        if varargs:
            varnames = varnames[:-1]
        if kwargs:
            varnames = varnames[:-1]
        if hasattr(f, 'im_self'):
            varnames = varnames[1:]
        return list(varnames), varargs, kwargs


class OptMatcherHandler(OptMatcherInfo):
    '''Internal class, representing each specific matcher handler.
    It is an OptMatcherInfo extended with operations to handle arguments
    ''' 
        
    def __init__(self, func, getoptmode):
        OptMatcherInfo.__init__(self, func, getoptmode)
        self.reset()
        
    def reset(self):
        #all prefixes are reset as provided as an empty list
        self.provided = dict([(i, []) for i in self.prefixes.values()])
        self.providedPars = []
                
    def invoke(self):
        '''Invokes the underlying function.'''
        #It is invoked using the options/parameters/defaults already setup
        status, args, kwargs = self._getInvokingPars()
        return self.func(*args, **kwargs)
    
    def checkInvokable(self):
        '''Verifies whether the underlying function can be invoked.'''
        #It can, if all the options/parameters are specified or have defaults
        return self._getInvokingPars()[0]
        
    def _getInvokingPars(self):
        #Returns the parameters required to invoke the underlying function.
        #The parameters are returned as a tuple (*args, **kwargs)
        args, parameters = [], self.providedPars[:]
        for i in range(1, self.lastArg):
            try:
                value = self.provided[i] #read first the provided value
            except KeyError:
                #otherwise, the current index could refer to a parameter,
                #which are stored separately
                if i in self.pars and parameters:
                    value = parameters.pop(0) 
                else:
                    #this argument were not provided: try the default value
                    try:
                        value = self.defaults[i]
                    except KeyError:
                        #Neither, this function cannot be invoked
                        return ('Missing required ' + self.getIndexName(i),
                                None, None)
            args.append(value)
        #if the function defined a *arg parameter, it can handle the 
        #  remaining provided parameters
        args.extend(parameters)
        return None, args, self.kwargs or {}
                        
    def handleArg(self, commandLine):
        '''Handles one argument in the command line'''
        #Returns None if ok, otherwise the reason why it cannot consume the 
        #  argument
        #An exception is raised in not recoverable situations: like flag not
        #     provided when needed, etc
        #This handling can imply, under getopt mode, consuming more 
        # than one argument in the command line, or just a portion
        # of one, if a short option was specified
        
        #Check first options (short/long)
        if commandLine.option:
            if commandLine.isShort:
                return self._handleShortArg(commandLine)
            return self._handleLongArg(commandLine)
        #If not, it is a parameter, but perhaps there are already too many...
        if not self.vararg and (len(self.providedPars) >= len(self.pars)):
            return 'Unexpected argument: ' + commandLine.arg
         
        self.providedPars.append(commandLine.arg)
        commandLine.setArgHandled()
        return None
    
    def _handleLongArg(self, cmd):
        '''Handles one long argument in the command line.'''
        name = cmd.name
        #only check the name if defined (and not defined as a short option)
        okName = name in self.defs
        if okName and self._handleOption(cmd):
            return None
        
        flag = okName and self.flags.get(name, None)
        if flag:
            if cmd.split: #flag, but user specified a value
                raise UsageException('Incorrect flag ' + name)
            self.provided[flag] = True
        else:
            prefix, name = self._splitPrefix(name)
            if prefix:
                if not name:
                    #perhaps is given as -D=value(bad) or separate (getoptmode)
                    if cmd.split or not self.getoptmode or cmd.setArgHandled():
                        raise UsageException(
                            'Incorrect prefix usage on argument ' + cmd.arg)
                    #note that cmd.value is the value of next argument now
                    name = cmd.name 
                self.provided[prefix].append((name, cmd.value))
            else: #try now the self.kwargs, if possible
                try:
                    self.kwargs[cmd.name] = cmd.value
                except TypeError:
                    #no kwargs, this argument cannot be used
                    return 'Unexpected argument: ' + cmd.arg                     
        cmd.setArgHandled()
            
    def _handleShortArg(self, cmd):
        '''Handles one short argument in the command line'''
        #This method is only called for getopt mode
        name = cmd.name
        if not name in self.shortDefs:
            #in shorts, name is just one letter, so not inclusion in 
            #shortDefs means that it is neither a prefix, no more checks needed
            return 'Unexpected flag ' + name + ' in argument ' + cmd.arg #@@@@@@@@@@@@@@@@
        flag = self.flags.get(name, None)
        if flag:
            self.provided[flag] = True
            cmd.setShortArgHandled()
        elif not self._handleOption(cmd):
            prefix = self.prefixes.get(name, None)
            #no flag, no option, but in shortDefs->is a prefix! 
            if not cmd.value:
                #given separately                    
                if cmd.setArgHandled():
                    raise UsageException('Incorrect prefix ' + name)
                cmd.value = cmd.arg
            self.provided[prefix].append(cmd.separate(cmd.value)[1:])
            cmd.setArgHandled()            
        return None
                
    def _handleOption(self, cmd):
        '''Checks if the command is a valid option, handling it if so
           Returns the option handled, or None if not handled
        '''
        #the normal case, -name=value, implies command.value
        name = cmd.name
        option = self.options.get(name, None)
        if option:
            if cmd.value:
                value = cmd.value
            else:
                #under getoptmode, this is still valid if the value is
                #provided as a separate argument (no option, no split)                
                if not self.getoptmode or cmd.setArgHandled() or cmd.split:
                    raise UsageException('Incorrect option ' + name)
                value = cmd.arg
            #If a conversion is needed (to integer/float), fo it now
            try:
                value = self.converts[option](value)
            except KeyError:
                pass #no conversion required
            except ValueError:
                raise UsageException('Incorrect value for ' + name)
            self.provided[option] = value
            cmd.setArgHandled()
        return option
    
    def _asInt(self, value):
        return int(value)
                        
    def _asFloat(self, value):
        return float(value)
                        
    def _splitPrefix(self, name):
        #Splits an existing prefix from the given name.
        #   It does not apply to short prefixes (getopt mode)
        #   It returns the tuple (prefix, rest), or (None, None) if not found
        for each in self.prefixes:
            if each in self.defs and name.startswith(each):
                return self.prefixes[each], name[len(each):]
        return None, None
                            
        
class OptionMatcherException(Exception):
    '''Exception raised when a problem happens during handling setup'''

        
class UsageException(OptionMatcherException):
    '''Exception raised while handling an argument'''
            

class OptionMatcher (object):
    ''' Class handling command line arguments by matching method parameters.
    It supports naturally the handling of mutually exclusive options.
    '''
    
    def __init__(self, matchers=None, commonMatcher=None, aliases=None,
                 option='--', delimiter='='):
        '''
        Param matchers define the methods/functions to handle the command 
            line, in specific order. 
            If not specified, all methods of current instance with 
            decorator optmatcher are used, with the specified priority
        Param common can be used to specify a matcher to handle common 
            options. If it is not specified, the method of the current 
            instance with decorator optcommon is used -if any-.
        Param aliases is a map, allowing setting option aliases. 
            In getopt mode, all aliases must be defined between a short
            (1 character length) option and a long (>1 character length)
            option
        Param option defines the prefix used to characterize an argument
            as an option. If is defined as '--', it implies 
            automatically getopt mode, which enables the usage of short 
            options with prefix -
        Param delimiter defines the character separating options' name 
            and value
        '''
        self.setMatchers(matchers, commonMatcher)
        self.setAliases(aliases)
        self.setMode(option, delimiter)
               
    def setMatchers(self, matchers, commonMatcher=None):
        '''Sets the matchers and the common matcher. See __init__'''
        self._matchers = matchers
        self._common = commonMatcher
    
    def setAliases(self, aliases):
        '''Sets the aliases. See __init__'''
        self._aliases = aliases
    
    def setMode(self, option, delimiter):
        '''Sets the working mode. See __init__'''
        self._option = option or self._option
        self._delimiter = delimiter or self._delimiter
    
    def getMatcherMethods(self, instance=None):
        '''Returns a list with all the methods defined as optmatcher
        The list is sorted by priority, then alphabetically
        '''
        return Decoration.getDecoratedMethods(instance or self, False)
        
                
    def getCommonMatcherMethod(self, instance=None):
        '''Returns the common matcher method in the given instance, if any.
        If there were multiple such methods, the method with highest 
        priority (or lower alphabetically) is returned.
        '''
        all = Decoration.getDecoratedMethods(instance or self, True)
        if all:
            return all[0]
        return None 
                                                                         
    def process(self, args, gnu=False):
        '''Processes the given command line arguments
        Param gnu determines gnu behaviour. Is True, no-option 
            arguments can be only specified latest
        '''
        matcherHandlers, commonHandler = self._createHandlers()        
        commandLine = CommandLine(args, self._option, self._delimiter, gnu)        
        highestProblem = None, 'Invalid command line input'
        
        #the method is simple: for each matcher, we verify if the arguments
        # suit it, taking in consideration the common handler, if given.
        #As soon as a matcher can handle the arguments, we invoke it, as well
        # as the common handler, if given.
        for handler in matcherHandlers:            
            problem = self._tryHandlers(commonHandler, handler, commandLine)
            if not problem:
                #handlers ok: invoke common handler, then matcher's handler
                if commonHandler:
                    commonHandler.invoke()
                return handler.invoke()
            position = commandLine.getPosition()
            if position > highestProblem[0]:
                highestProblem = position, problem 
            #prepare command line, common handler for next loop
            commandLine.reset()
            if commonHandler:
                commonHandler.reset()
        raise UsageException (highestProblem[1])        
    
    def _createHandlers(self):
        #Returns all the required handlers, as a tuple
        #the first element is the list of matchers, and the second, the
        #common matcher
        def createHandle(function):
            if not function:
                return None
            ret = OptMatcherHandler(function, self._option == '--')
            if self._aliases:
                ret.setAliases(self._aliases)                
            return ret

        return ([createHandle(f) 
                    for f in (self._matchers or self.getMatcherMethods())],
                createHandle(self._common or self.getCommonMatcherMethod()))

    
    def _tryHandlers(self, commonHandler, commandHandler, commandLine):
        #Checks if the specified handlers can process the command line.
        #If so, it returns None, letting the handlers ready to be invoked
        #Otherwise, it returns the reason why it cannot be handled 
        while not commandLine.finished():
            if commonHandler:
                if not commonHandler.handleArg(commandLine):
                    continue
            problem = commandHandler.handleArg(commandLine)
            if problem:                
                return problem
        return ((commonHandler and commonHandler.checkInvokable()) or 
                commandHandler.checkInvokable())
        

def optmatcher(flags=None, options=None, intOptions=None,
               floatOptions=None, prefixes=None, parameters=None,
               priority=None):
    '''Decorator defining a function/method as optmatcher choice'''
    
    return Decoration.decorate(False, flags, options, intOptions,
                                floatOptions, prefixes, parameters, priority)

def optcommon(flags=None, options=None, intOptions=None,
              floatOptions=None, prefixes=None, parameters=None,
              priority=None):
    '''Decorator defining a function/method as optcommon choice'''
    
    return Decoration.decorate(True, flags, options, intOptions,
                                floatOptions, prefixes, parameters, priority)
