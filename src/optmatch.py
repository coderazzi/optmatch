"""optmatch - matching command line argument by method's signatures
Support usual GNU/Unix conventions, but not exclusively

Author:  Luis M. Pena <dr.lu@coderazzi.net>
Site:    www.coderazzi.net/python/optmatch
"""

__version__ = '0.8.2'

__all__ = ['optset', 'optmatcher',
           'OptionMatcher', 'OptionMatcherException', 'UsageException']
           
__copyright__ = """
Copyright (c) Luis M. Pena <dr.lu@coderazzi.net>  All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
Redistributions in bytecode form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in
the documentation and/or other materials provided with the
distribution.

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

class Decoration(object):
    '''
    Internal namespace to define any decoration functionality
    optmatcher decorator adds an attribute 'optmatcher' that contains
        the list of parameters provided in the decorator definition, 
        like flags, options, etc, in a given order
    optset decorator behaves as the optmatcher one, but adds a 
        second attribute to the function/method: 'optset', with 
        value True
    '''
    
    @staticmethod
    def decorate(optset, *args):
        #Decoration method for optmatcher and optset decorators.
        #Param optset should be True for optset decorators
        #Param args is the ordered parameters allowed in those decorators
        
        def decorate(f, value):
            f.optmatcher = value
            if optset:
                f.optset = True          
            return f
        
        #perhaps the base decorator is called with the function to decorate
        #This happens for cases like: @optmatcher def handle(...)
        #No decorator parameter should be a function, so this case can
        # be handled as follows:
        if (args[0] and not filter(None, args[1:]) and
                type(args[0]) == type(decorate)): 
            return decorate(args[0], [])

        return lambda x: decorate(x, args)
    
    @staticmethod
    def parseDecoration(function):
        #Parses the optmatcher decoration in the given function.
        #If specified, it returns a tuple Info, priority, 
        #  or (None, None) otherwise, where Info is the ordered list
        #  of the decorator parameters
        
        def parser(flags=None, options=None, intOptions=None,
                   floatOptions=None, prefixes=None, renamePars=None,
                   priority=None):
            return (flags, options, intOptions, floatOptions, prefixes,
                    renamePars), priority
            
        try:
            return parser(*function.optmatcher)
        except:
            return None, None

    @staticmethod
    def getDecoratedMethods(instance, definedAsCommon):
        #Returns the methods decorated with optmatcher, priority sorted
        functionsAndPriorities = []
        for att in dir(instance):
            f = getattr (instance, att)
            if definedAsCommon == hasattr(f, 'optset'):
                info, priority = Decoration.parseDecoration(f)
                if info:
                    functionsAndPriorities.append((priority or 0, f))
        #sort now by inverse priority, and return just the functions
        functionsAndPriorities.sort(lambda x, y: y[0] - x[0]) 
        return [f for (p, f) in functionsAndPriorities]    


class UsageMode(object):
    '''Internal class gathering overall information, like the option prefix'''
    #Available instance attributes:
    #   option      : the option prefix ('--')
    #   assigner    : the string to be used as separator between
    #                 names and values
    #   getopt      : True if getopt mode (short is '-', long options as '--')
    #   optionsHelp : Map containing the help for each known option
    #   varNames    : Map containing the variable name for each known option.
    #                 This is only used for text representation of the options
    
    def __init__(self, option, assigner):
        self.optionsHelp, self.varNames = None, None
        self.set(option, assigner)

    def set(self, option=None, assigner=None,
            optionsHelp=None, varNames=None):
        '''Sets one or more of the mode' variables''' 
        self.option = option or self.option
        self.assigner = assigner or self.assigner
        self.optionsHelp = optionsHelp or self.optionsHelp
        self.varNames = varNames or self.varNames
        self.getopt = self.option == '--'
        
    def getOptionPrefix(self, argument):
        '''Returns the option prefix for a given argument'''
        if not self.getopt or len(argument) > 1:
            return self.option
        return '-'

    def getDelimiter(self, argument):
        '''Returns the assigner string for a given argument''' 
        if not self.getopt or len(argument) > 1:
            return self.assigner
        return ' '


class CommandLine(object):
    '''Internal class to handle the Command Line arguments
    This class is used by the handlers to iterate through the arguments in
       the command line. The iteration does not need to be argument by
       argument, as one single argument could contain multiple options
       (only in getopt mode,  where -cov could mean -c -o -v)
    '''
    #Available instance attributes:
    #   arg    : String, the whole argument, without the prefix option
    #            if the argument were '--option', arg would be 'option'
    #   name   : String, the name of the current argument
    #            if the argument were '--op=2', name would be 'op'
    #   value  : String, the value of the current argument
    #            if the argument were '--op=2', name would be '2'
    #   option : Bool, true if the current argument is an option
    #   isShort: Bool, true if the current arg is a short option
       
    def __init__(self, args, mode, gnuMode):
        '''param args: the list of arguments to handle (first dismissed)'''
        #reShort is hardcoded to '-' if the option is defined as '--'
        self.reShort = mode.getopt
        self.reOption = mode.option
        self.reSeparation = re.compile('(.+?)' + mode.assigner + '(.+)$')
        self.args = args
        self.gnuMode = gnuMode
        self.canBeOption = True #used for gnuMode  
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
        self.option, self.isShort = False, False
        option = self.arg.startswith(self.reOption)
        if self.canBeOption:
            if option:  #normal (long) option
                arg = self.arg[len(self.reOption):]
                self.option = True
            elif self.reShort and self.arg[0] == '-':
                arg = self.arg[1:]
                self.option, self.isShort, self.split = True, True, False
            else:
                self.canBeOption = not self.gnuMode
        elif option or (self.reShort and self.arg[0] == '-'):
            raise UsageException('Unexpected argument ' + self.arg + 
                                 ' after non option arguments')
        if not arg:
            raise UsageException('Unexpected argument ' + self.arg)         
        if self.isShort:         
            self.name, self.value = arg[0], arg[1:]
        else:
            self.split, self.name, self.value = self.separate(arg)
        return self.option


class ArgumentInfo(object):
    '''Class to represent arguments (options, parameters), for help matters'''
    
    def __init__(self, name, mode):
        '''All arguments have a name, and require knowing the UsageMode'''
        self.name = name
        self.mode = mode
        self.defaultProvided = False #needed, as default value could be None!
        self.defaultValue = None
        
    def __str__(self):
        if self.defaultProvided:
            format = '[%s%s%s%s]'
            if self.defaultValue is None:
                default = ''
            else:
                default = ' (' + str(self.defaultValue) + ')'
        else:
            format = '%s%s%s%s'
            default = ''
        return format % (self._getPrefix(), self.name,
                         self._getSuffix(), default)

    def setDefaultValue(self, defaultValue):
        '''Sets the default value, even if it is None'''
        self.defaultProvided = True
        self.defaultValue = defaultValue
        
    def _getPrefix(self, name=None):
        '''This is the prefix for the argument (-- for options, i.e.)'''
        return ''
        
    def _getSuffix(self, name=None):
        '''This is the prefix for the argument (=MODE, i.e.)'''
        return ''
    
    def getType(self):
        return 'Parameter'
        

class FlagInfo(ArgumentInfo):
    '''Flags are arguments with aliases, adn with a prefix (--, i.e.)'''
    
    def __init__(self, aliases, mode):
        '''The name of a flag/option is the shortest of its aliases'''
        aliases.sort(key=len)
        ArgumentInfo.__init__(self, aliases[0], mode)
        self.aliases = aliases
        
    def aliasesAsStr(self):
        '''Produces, for example: "-m MODE, --mode MODE" '''
        aliases = ['%s%s%s' % (self._getPrefix(i),
                             i,
                             self._getSuffix(i)) for i in self.aliases]
        return ', '.join(aliases)

    def getDoc(self):
        '''Returns the doc provided for the given aliases'''
        #it is enough to give the doc for one of the aliases, no check 
        # to verify if different aliases have different documentation
        if self.mode.optionsHelp:
            for a in self.aliases:
                try:
                    return self.mode.optionsHelp[a]
                except KeyError:
                    pass
            
    def _getPrefix(self, name=None):
        return self.mode.getOptionPrefix(name or self.name)
    
    def getType(self):
        return 'Flag'

    
class OptionInfo(FlagInfo):    
    '''Options are flags that add a suffix: -m MODE, instead of -m, i.e. '''

    def _getSuffix(self, name=None):
        #for a set of aliases, like 'm', 'mode', the variable name is,
        #by default, the uppercase of the longuer alias. It can be 
        #overriden if the user provided a var name for one of the aliases
        def getVariableName():
            if self.mode.varNames:
                for alias in self.aliases:
                    try:
                        return self.mode.varNames[alias]
                    except KeyError:
                        pass
            return self.aliases[-1].upper()
                                     
        return self.mode.getDelimiter(name or self.name) + getVariableName()
    
    def getType(self):
        return 'Option'

            
class PrefixInfo(OptionInfo):    
    '''Prefixes are flags that add a suffix: -m MODE, instead of -m, i.e. '''
    
    def getType(self):
        return 'Prefix'


class OptMatcherInfo(object):
    '''Internal class, holds the information associated to each matcher'''
        
    DECORATOR_SPLIT = re.compile('\\s*,\\s*')
    DECORATOR_ASSIGN = re.compile('(.+?)\\s+as\\s+(.+)')
    FLAG_PATTERN = re.compile('(.+)' + 
                              '(Flag|Option|OptionInt|OptionFloat|Prefix)$')

    def __init__(self, func, mode):
        self.mode = mode
        self._initializeParametersInformation(func)
        
        #With getoptmode, in addition to the normal definitions, users
        # can specify short options, stored in sortedDefs 
        self.defs = set()       #definitions (flags/options/prefixes)
        if mode.getopt:
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
                                                 '" in ' + self.describe())
                defSet.add(name)

    def _initializeParametersInformation(self, func):   
        #Initializes all parameter information associated to the function: 
        self.flags = {}      #maps flag name to parameter index
        self.options = {}    #maps option name to parameter index
        self.prefixes = {}   #maps prefix name to parameter index
        self.converts = {}   #maps from index (option) to convert function
        self.pars = {}       #maps parameter index to parameter name
        self.lastArg = 1     #the last available variable index plus 1
        self.orphanFlags = 0 #flags without associated variable
        
        #Note that the index number associated to the first parameter
        # is 1, not zero. This simplifies later many checks

        self.func = func
        
        vars, self.vararg, kwarg = self._getParametersInfo(func)
        #if kwargs are supported, kwargs is used as a dictinary
        self.kwargs = kwarg and not self.mode.getopt and {}
        
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

        def getDecorationDefinitions(decoration):
            #The returned value maps names to 'as' values, if present, or to
            #  themselves, otherwise, for a given decoration argument
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
                            ret[d] = None
            return ret
    
        ints, floats, used = {}, {}, []
        for att, group in [(self.flags, flags),
                           (self.options, options),
                           (self.prefixes, prefixes),
                           (self.pars, parameters),
                           (ints, intOptions),
                           (floats, floatOptions)]:
            #in the following loop, n defines each parameter name given
            #in the decorator for each group (flags, options, etc), while
            #v defines the public name (n as v)
            for n, v in getDecorationDefinitions(group).items():
                #get the index of the var: is an error if not found or reused
                if att is self.pars and (not v or n == v):
                    raise OptionMatcherException('Invalid renamePar ' + n)
                try:
                    index = vars.index(n)
                except ValueError:
                    if att is self.flags and not v:
                        #a flag could be not existing as argument, as
                        # the flag value is not really interesting. In this
                        # case, makes no sense defining it as 'var as name'
                        self.orphanFlags -= 1
                        att[n] = self.orphanFlags
                        continue                    
                    raise OptionMatcherException('Invalid argument: ' + n)
                if index in used:
                    raise OptionMatcherException(
                                    'Invalid argument redefinition: ' + n)
                used.append(index)
                att[v or n] = 1 + index
        #all groups are created as maps (name -> variable index), but for
        #params we invert the map, as the index is the important information
        self.pars = dict([(a, b) for b, a in self.pars.items()])
        #all function parameters that are not included as flags/options/
        #prefixes are definitely considered parameters
        self.pars.update(dict([(i + 1, v) for i, v in enumerate(vars) 
                                          if i not in used]))
        #intOptions and floatOptions are options with additional checks:
        self.options.update(ints)
        self.options.update(floats)
        self.converts = dict([(i, self._asFloat) for i in floats.values()])
        self.converts.update(dict([(i, self._asInt) for i in ints.values()]))
        self.lastArg = len(vars) + 1
            
    def getDoc(self):
        return self.func.__doc__
    
    def supportVargs(self):
        '''Returns whether it accepts *vars'''
        return self.vararg > 0
    
    def getVKwargsSupport(self):
        '''Returns whether it accepts *vars and **kargs argument'''
        return self.supportVargs(), isinstance(self.kwargs, dict)
    
    def getOptions(self):
        '''Returns the defined flags, options and prefixes 
        as a list of ArgumentInfo instances (FlagInfo or OptionsInfo, in fact)
        '''
        
        def getOptionsAndDefaults(group, constructor):
            ret, options = [] , {}
            #flags, options and prefixes are map name -> index
            #but with the aliases, multiple names can point to the same index
            for name, index in group.items():
                options.setdefault(index, []).append(name)
            for index, aliases in options.items():
                this = constructor(aliases, self.mode)
                try:
                    this.setDefaultValue(self.defaults[index])
                except KeyError:
                    pass
                ret.append(this)
            ret.sort(key=lambda x: x.name)
            return ret
                                                
        return getOptionsAndDefaults(self.flags, FlagInfo) + \
               getOptionsAndDefaults(self.options, OptionInfo) + \
               getOptionsAndDefaults(self.prefixes, PrefixInfo)
                                        
    def getParameters(self):
        '''Returns the defined parameters as a [ArgumentInfo instances]'''
        ret = []
        for i in range(1, self.lastArg):
            try:
                info = ArgumentInfo(self.pars[i], self.mode)
            except KeyError:
                continue
            try:
                info.setDefaultValue(self.defaults[i])
            except KeyError:
                pass
            ret.append(info)
        return ret
                                            
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
            ret = a in aSet
            if ret:
                if b in bSet:
                    raise OptionMatcherException(
                       'Bad alias:' + a + '/' + b + ' in ' + self.describe())
                bSet.add(b)
                for each in self.flags, self.options, self.prefixes:
                    try:
                        each[b] = each[a]
                    except KeyError:
                        pass
            return ret
            
        for s, l in aliases.items():
            if self.mode.getopt:
                #In getoptmode, aliases must map short and long options, 
                #   that is, options with 1 character and options with more 
                #   than 1 character
                if len(s) > len(l):
                    s, l = l, s
                if len(s) > 1 or len(l) == 1:
                    raise OptionMatcherException('Bad alias:' + s + '/' + l)
                if setAlias(l, s, self.defs, self.shortDefs):
                    continue
            elif l in self.defs:
                #if alias 'l' is already known, we try setting from s->l
                s, l = l, s
            setAlias(s, l, self.shortDefs, self.defs)
            
    def getIndexName(self, index):
        #returns the flag/option/parameter name with the given index 
        # (no prefixes) Note that it will be returned any of its aliases
        for n, v in self.flags.items():
            if v == index:
                return 'flag ' + n
        for n, v in self.options.items():
            if v == index:
                return 'option ' + n
        return 'parameter ' + self.pars[index]
            
    def describe(self):
        '''Describes the underlying method'''
        try:
            name = 'method ' + self.func.im_self.__class__.__name__ + '.'
        except AttributeError:
            name = 'function '
        return name + self.func.__name__
    
    def getDoc(self):
        '''Return the documentation of the underlying method, if any'''
        return self.func.__doc__
    
    def _getParametersInfo(self, f):
        #This information includes: the list of variables, if it supports
        #   varargs, and if it supports kwargs 
        flags, firstArg = f.func_code.co_flags, hasattr(f, 'im_self')
        varnames = f.func_code.co_varnames[firstArg:f.func_code.co_argcount]
        return list(varnames), (flags & 0x0004) != 0, (flags & 0x0008) != 0


class OptMatcherHandler(OptMatcherInfo):
    '''Internal class, representing each specific matcher handler.
    It is an OptMatcherInfo extended with operations to handle arguments
    ''' 
        
    def __init__(self, func, mode):
        OptMatcherInfo.__init__(self, func, mode)
        self.reset()
        
    def reset(self):
        #all prefixes are reset as provided as an empty list
        self.provided = dict([(i, []) for i in self.prefixes.values()])
        self.providedPars = []
                
    def invoke(self):
        '''Invokes the underlying function, unless it cannot be invoked.'''
        #It is invoked using the options/parameters/defaults already setup
        status, args, kwargs = self._getInvokingPars()
        return status==None and self.func(*args, **kwargs)
    
    def checkInvokable(self, required):
        '''Verifies whether the underlying function can be invoked.'''
        #It can, if all the options/parameters are specified or have defaults
        errorReason = self._getInvokingPars()[0]
        
        if errorReason:
            if required or self._somethingProvided():
                return errorReason
        
        return None
            
    def _somethingProvided(self):
        #just check if the user provided any value
        return self.providedPars or filter(lambda x: x != [],
                                           self.provided.values())
        
    def _getInvokingPars(self):
        #Returns the parameters required to invoke the underlying function.
        #It returns a tuple (problem, *args, **kwargs)
        provided = self.provided or self.providedPars
        args, parameters = [], self.providedPars[:]
        #we only check the indexes 1...lastArg, so the orphan flags are not
        #checked here (they are not used to invoke the method)
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
        #It must be still checked the orphan flags' variables
        #These are not passed to the method, but must have been provided to 
        #consider that the method can be invoked
        for c in range(self.orphanFlags, 0):
            if not c in self.provided:
                return 'Missing required ' + self.getIndexName(c), None, None
            
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
                    #perhaps is given as -D=value(bad) or separate (getopt)
                    if (cmd.split or not self.mode.getopt or 
                            cmd.setArgHandled()):
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
            #shortDefs means that it is neither a prefix, do no more checks
            return 'Unexpected flag ' + name + ' in argument ' + cmd.arg
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
                if not self.mode.getopt or cmd.setArgHandled() or cmd.split:
                    raise UsageException('Incorrect option ' + name)
                value = cmd.arg
            #If a conversion is needed (to integer/float), do it now
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
                            
        
class UsageAccessor(object):
    '''Class to access and to format usage info'''
    
    def __init__(self, handlers, commons, mode):
        self.mode = mode
        self.handlers = handlers
        self.commons = commons        
        self.content = []
        self.reset()
        self.commonOptions = self._getOptionsDir(self.commons, {})
        
    def getUsageString(self, width=72, column=24, ident=2):
        '''Generic method to print the usage. By default, the window
        output is limited to 72 characters, with information for each option
        positioned on the column 24.
        '''
        self.reset(width)
        if not self.handlers:
            self.add('Error, no usage configured')
        else:
            self.add('Usage:')
            options = self.getAllOptions()
            alternatives = self.getAlternatives()
            if alternatives == 1:
                #if there is one single alternative, it is shown fully
                #expanded, with options and default values
                self.add(self.getOptions(0, True) + self.getParameters(0))
            else:
                #Otherwise, getAllParameters provide the intersection of names
                #among all alternatives
                if options:
                    self.add('[common options]')
                self.add(self.getAllParameters())
            if options:
                #in any case, aliases and doc for each option is shown next
                self.addLine()
                self.addLine('options:')
                for each in options:
                    self.addLine(each.aliasesAsStr(), ident)
                    doc = each.getDoc()
                    if doc:
                        self.add(doc, column)
            if alternatives > 1:
                #finally, all the alternatives, fully expanded
                self.addLine()
                self.addLine('alternatives:')
                for i in range(alternatives):
                    content = self.getOptions(i, True) + self.getParameters(i)
                    self.addLine()
                    self.addLine('*')
                    self.add(content, ident)
                    doc = self.getDoc(i)
                    if doc:
                        self.add(doc, column)
        return self.getContent()
        
    def getAllOptions(self):
        '''Returns -as FlagInfo instances-, all the flags/options/prefixes
        that were defined for any of the provided matchers. The list
        will be sorted alphabetically, listing first the flags
        '''
        def compare(a, b):
            #first: give less weight to options than to flags
            noflag = isinstance(a, OptionInfo)
            if noflag != isinstance(b, OptionInfo):
                return (noflag and 1) or - 1
            #then: alphabetical order, case insensitive
            A = a.name.lower()    
            B = b.name.lower()
            return (A < B and - 1) or (A > B and 1) or 0
        
        #Search is done over all the matchers, with priority on the common
        return self._getOptions(self.handlers, self.commonOptions,
                                True, compare)

    def getOptions(self, alternative, includeCommon):
        '''Returns -as FlagInfo instances-, all the flags/options/prefixes
        that were defined for the given matcher, including, if required,
        those associated to the common matcher. The list
        will be sorted alphabetically, listing first the optional options
        '''
        def compare(a, b):
            #first: give less weight to instances withour default values
            if a.defaultProvided != b.defaultProvided:
                return (a.defaultProvided and - 1) or 1
            #then: alphabetical order, case insensitive
            A = a.name.lower()    
            B = b.name.lower()
            return (A < B and - 1) or (A > B and 1) or 0
        
        handlers = (alternative != -1 and [self.handlers[alternative]]) or []
                    
        return self._getOptions(handlers,
                                self.commonOptions,
                                includeCommon,
                                compare)

    def getCommonOptions(self):
        '''Returns -as FlagInfo instances-, all the flags/options/prefixes
        that were defined for the common matcher. The list
        will be sorted alphabetically, listing first the optional options
        '''
        return self.getOptions(-1, True)
    
    def _getOptions(self, handlers, base, union, compare):
        #iterate over the options of every handler, adding the option if not
        #yet there
        all = self._getOptionsDir(handlers, base)
        if union:
            all.update(base)
        ret = all.values()
        ret.sort(compare)
        return ret

    def _getOptionsDir(self, handlers, base):
        #iterate over the options of every handler, adding the option if not
        #yet there
        all = {}
        for each in handlers:
            for option in each.getOptions():
                if not option.name in all and not option.name in base:
                    all[option.name] = option
        return all

    def getAlternatives(self):
        '''Returns the number of provided matchers'''
        return len(self.handlers)
    
    def getDoc(self, alternative):
        '''Returns the documentation for the given matcher'''
        return self.handlers[alternative].getDoc()
    
    def getParameters(self, alternative):
        '''Returns the parameters (as ArgumentInfo) for the given matcher'''
        handlers = self.commons + [self.handlers[alternative]]
        ret = []
        for h in handlers: #common, first (if defined), then handlers
            ret.extend(h.getParameters())
            if h.supportVargs():
                #We break here, if a matcher defines parameters,
                #they will be never handled, as the common matcher would
                #consume them first
                ret.append(ArgumentInfo('...', self.mode))
                break
        return ret
    
    def getAllParameters(self):
        '''Returns all the expected parameters (as strings)
        The list will include the number of parameter of the matcher with
         highest number (plus the parameters in the common one)
        '''
        args, vararg = [], False
        #we get the parameters required by all the handlers.
        #By default, they are named arg1, arg2, etc
        #if all handlers define one such parameter commonly, we name it so 
        for each in self.handlers:
            pars = each.getParameters()
            for l, (a, p) in enumerate(zip(args, pars)):
                #set the name of each argument as passed to a matcher
                #if another matcher differs on the name of a common argument,
                #just name it generically as 'arg'number
                if a != p.name:
                    args[l] = 'arg%d' % (l + 1)
            args += [p.name for p in pars[len(args):]]
            if each.supportVargs():
                vararg = True
                break
        commonArgs = []
        for each in self.commons:
            commonArgs = commonArgs + [p.name for p in each.getParameters()]
            if each.supportVargs(): 
                #in this case, the parameters of no matcher will be used,
                #because the matcher would consume them first
                vararg = True
                args = []
                break
        if vararg:
            args.append('...')
        return commonArgs + args
    
    def reset(self, width=72):
        '''Format method, clears the content'''
        self.content = ['']
        self.width = width
        
    def getContent(self):
        '''Format method, returns the current content'''
        return '\n'.join(self.content)
        
    def addLine(self, content=None, column=0):
        '''
        Format method, adds a new line, and places the content on the
        given column. See add method 
        '''
        self.content.append('')
        if content:
            self.add(content, column)
        
    def add(self, content, column=0):
        '''
        Format method, adds content on the current line at the given position.
        If the current content already covers that column, a new one is 
        inserted. 
        If the content spawns multiple lines, each start at the 
        same position
        The content can be a string, or a list of objects. As a list 
        of objects, splitting on multiple lines can only happen for full
        objects; for strings, it is done at each space character.
        No care is taken for any special characters, specially '\n'
        '''
        if isinstance(content, str):
            content = content.split(' ')
        current = self.content.pop()
        if column > 0 and current and len(current) + 1 > column:
            self.content.append(current)
            current = ''
        started = not column and len(current.strip()) > 0
        current += ' ' * (column - len(current))
        for each in content:
            each = str(each)
            if started and (len(current) + len(each) >= self.width):
                self.content.append(current)
                current = ' ' * column
                started = False
            if each or started:
                if started:
                    current += ' '
                current += each
                started = True            
        self.content.append(current.rstrip())                
                
                    
class OptionMatcher (object):
    ''' Class handling command line arguments by matching method parameters.
    It supports naturally the handling of mutually exclusive options.
    '''
    
    def __init__(self, matchers=None, commons=None, aliases=None,
                 optionsHelp=None, optionVarNames=None,
                 optionPrefix='--', assigner='=', defaultHelp=True):
        '''
        Param matchers define the methods/functions to handle the command 
            line, in specific order. 
            If not specified, all methods of current instance with 
            decorator optmatcher are used, with the specified priority
        Param commons can be used to specify matchers to handle 
            common options. If it is not specified, the methods of the 
            current instance with decorator optset is used -if any-.
        Param aliases is a map, allowing setting option aliases. 
            In getopt mode, all aliases must be defined between a short
            (1 character length) option and a long (>1 character length)
            option
        Param optionsHelp defines the information associated to each
            option. It is map from option's name to its documentation.
            For aliases, it is possible to define the documentation for 
            any of the given aliases -if different info is supplied 
            for two aliases of the same option, one will be dismissed-
        Param optionsVarNames identifies, for options and prefixes, the
            variable name used during the usage output. For example, 
            option 'm' would be visualized by default as '-m M', unless
            this option is ised.
            For aliases, it is possible to define the var name for 
            any of the given aliases -if different names are supplied 
            for two aliases of the same option, one will be dismissed-
        Param optionPrefix defines the prefix used to characterize an argument
            as an option. If is defined as '--', it implies 
            automatically getopt mode, which enables the usage of short 
            options with prefix -
        Param assigner defines the character separating options' name 
            and value
        Param defaultHelp is True to automatically show the usage when the
            user requests the --help option (or -h)
        '''
        self._mode = UsageMode(optionPrefix, assigner)
        self._defaultHelp = defaultHelp
        self.setMatchers(matchers, commons)
        self.setAliases(aliases)
        self.setUsageInfo(optionsHelp, optionVarNames)
               
    def setMatchers(self, matchers, commons=None):
        '''Sets the matchers and the common matcher. See __init__'''
        self._matchers = matchers
        self._commons = commons
    
    def setAliases(self, aliases):
        '''Sets the aliases. See __init__'''
        self._aliases = aliases
    
    def setUsageInfo(self, optionsHelp, optionVarNames):
        '''Sets the usage information for each option. See __init__'''
        self._mode.set(optionsHelp=optionsHelp, varNames=optionVarNames)
    
    def setMode(self, optionPrefix, assigner):
        '''Sets the working mode. See __init__'''
        self._mode.set(option=optionPrefix, assigner=assigner)
    
    def getMatcherMethods(self, instance=None):
        '''Returns a list with all the methods defined as optmatcher
        The list is sorted by priority, then alphabetically
        '''
        return Decoration.getDecoratedMethods(instance or self, False)
                        
    def getCommonMatcherMethods(self, instance=None):
        '''Returns the common matcher method in the given instance, if any.
        If there were multiple such methods, the method with highest 
        priority (or lower alphabetically) is returned.
        '''
        return Decoration.getDecoratedMethods(instance or self, True)
                                                                         
    def getUsage(self):
        '''Returns an Usage object to handle the usage info'''
        matcherHandlers, commonHandlers = self._createHandlers()        
        return UsageAccessor(matcherHandlers, commonHandlers, self._mode)
    
    def printHelp(self):
        '''show the help message'''
        print self.getUsage().getUsageString()
        
    def process(self, args, gnu=False, handleUsageProblems=False):
        '''Processes the given command line arguments
        Param gnu determines gnu behaviour. Is True, no-option 
            arguments can be only specified latest
        '''
        matchers, commons = self._createHandlers()   
        commandLine = CommandLine(args, self._mode, gnu)        
        highestProblem = None, 'Invalid command line input'
        
        #the method is simple: for each matcher, we verify if the arguments
        # suit it, taking in consideration the common handler, if given.
        #As soon as a matcher can handle the arguments, we invoke it, as well
        # as the common handler, if given.
        try:
            for handler in matchers:            
                problem = self._tryHandlers(commons, handler, commandLine)
                if not problem:
                    #handlers ok: invoke common handler, then matcher's handler
                    for each in commons:
                        each.invoke()
                    return handler.invoke()
                position = commandLine.getPosition()
                if position > highestProblem[0]:
                    highestProblem = position, problem 
                #prepare command line, common handlers for next loop
                commandLine.reset()
                for each in commons:
                    each.reset()
            raise UsageException (highestProblem[1])       
        except UsageException, ex:
            if handleUsageProblems:
                import sys
                sys.stderr.write(str(ex) + '\n') 
            else:
                raise
    
    def _createHandlers(self):
        #Returns all the required handlers, as a tuple
        #the first element is the list of matchers, and the second, the
        #common matcher
        def createHandle(function):
            if not function:
                return None
            ret = OptMatcherHandler(function, self._mode)
            if self._aliases:
                ret.setAliases(self._aliases)                
            return ret
        
        if self._defaultHelp:
            if self._mode.getopt:
                self._aliases = self._aliases or {}
                self._aliases['h'] = 'help'
            self._mode.optionsHelp = self._mode.optionsHelp or {}
            self._mode.optionsHelp['help'] = 'shows this help message'

        matchers = [createHandle(f) 
                    for f in (self._matchers or self.getMatcherMethods())]
        
        commons = [createHandle(f) 
                   for f in (self._commons or self.getCommonMatcherMethods())]
        
        if self._defaultHelp:
            #cannot decorate directly printHelp, any instance would
            #get the decoration!
            f = lambda * a, **ch: self.printHelp()
            matchers.append(createHandle(optmatcher(flags='help')(f)))

        return matchers, commons

    
    def _tryHandlers(self, commonHandlers, commandHandler, commandLine):
        #Checks if the specified handlers can process the command line.
        #If so, it returns None, letting the handlers ready to be invoked
        #Otherwise, it returns the reason why it cannot be handled
        handlers = [commandHandler] + commonHandlers
        while not commandLine.finished():
            for each in handlers:
                problem = each.handleArg(commandLine)
                if not problem:
                    break
            else:
                if problem:
                    return problem
        for each in commonHandlers:
            problem = each.checkInvokable(False)
            if problem:
                return problem
        return commandHandler.checkInvokable(True)
        

class OptionMatcherException(Exception):
    '''Exception raised when a problem happens during handling setup'''

        
class UsageException(OptionMatcherException):
    '''Exception raised while handling an argument'''
    
    
def optmatcher(flags=None, options=None, intOptions=None,
               floatOptions=None, prefixes=None, renamePars=None,
               priority=None):
    '''Decorator defining a function / method as optmatcher choice'''
    
    return Decoration.decorate(False, flags, options, intOptions,
                                floatOptions, prefixes, renamePars, priority)

def optset(flags=None, options=None, intOptions=None,
           floatOptions=None, prefixes=None, renamePars=None,
           priority=None):
    '''Decorator defining a function / method as optset choice'''
    
    return Decoration.decorate(True, flags, options, intOptions,
                               floatOptions, prefixes, renamePars, priority)
