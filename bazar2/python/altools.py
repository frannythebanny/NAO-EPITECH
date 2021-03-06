# -*- coding: utf-8 -*-

###########################################################
# Some usefull usage tools from aldebaran - v2.10 (penser a reporter le version number dans getVersion)
# @author The usage team - Living Labs
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

def getVersion():
    return 2.10;
# getVersion - end





#######################################
# Generic Python Tools: not related to NaoQi (formerly apputools.py)
# summary:
# - debug
# - dump: dump the contents of an object into a string
# - getFileAndLinePosition: this method return the position of caller in a string.
# - class TimeMethod: instrumentise a method/class/module/...
# - getDirectorySeparator
# - getDirectoryName: get directory name from an absolute path and filename
# - getHostFolderAndFile( strWebAddress ): separate host, directory and filename from a web address
# - isArray
# - isString
# - stringToNumber: try to convert a string to a number, return None if the string can be converted to a number
# - splitMany: split a string, accepting a list of splitters
#
# - arrayCreate: create an array of size nNewSize by inserting some value (default 0)
# - decreaseAngle: decrease an angle of some step (by making tend to zero (even if it's a neg value))
# - isNearlyEqual: is two variables quite the same?
# - limitRange: ensure that a value is in the range rMin, rMax
# - replaceWord: a string replacement, but using entire word only
#
# - chooseOneElem: Pick randomly an element in a list
# - concateneRandom: take a list of word list and concatene it
# - generatePhraseWithAdjectif: generate a sentence desbcribing an adjectif
# -
# - colorCompToHexa: take 3 floats, R,G,B and create an hexa value from them
# - colorHexaToComp: take an rgb int (24bits) and return [b,g,r]
# - rgbToHsv: take an rgb array [b,g,r] and return it in [v,s,h]
# - getColorNameFromHSV: take a hue value [h,s,v](0..255) and return the name of the nearest color with the distance to the plain color [0,1] (multilangue)"
# - darkenColor: darken one color: if rLuminosity is set to 0.0 => black; 1.0 => no change
# -
# - convertAngleToByte: convert a joint angle -3..+3 in radians to a byte 0..255
# - isFileExists
# - copyFile
# - class Const: a small class to create constant preventing to changing the value of an existant one
# - getFileContents: read a file and return it's contents, or '' if not found, empty, ...
# - getLine: extract a specific line in a multiline text, return '' if line not found, text empty or ...
# - getFileFirstLine: read a file and return it's first line, or '' if not found, empty, ...
# - getnSentences: get n random sentences from a text. there is an option to choose to keep first sentence or not
# - transformAsciiAccentForSynthesis and various work on string (remove html code, remove accent...)
# - listToRad: convert a list in degrees to a list in radians
# - getFilenameFromTime: get a string usable as a filename relative to the current datetime stamp
# - getHumanTimeStamp: get a printable timestamp than a user (even french) could understand
# - executeAndGrabOutput: execute a command in system shell and return grabbed output
# - compareVectors: Compare two vectors, return -1 if equal or the idx of the difference
# - getHtmlPage: return a web page, or "" on error (async or sync method, with optionnal timeout)
# - randomizeList: randomize/unsort the order of element in a list
# - filterList: return a part of a list with only element containing an element in listWordPart
# - substractList: remove all element in a list that are in another list
# - mySystemCall: make a system call, and choose to wait till the end or to thread
# - asyncEval: launch an evaluation in another python thread, a tricky specific manner
# - getInCache/storeInCache: object caching
# - dictionnaryToString: return a beautiful and sorted string describing a dictionnaries for debugging or printing...
# - constructFromNamedArray: construct a python object from an array of couple [attr_name,attr_value]
# - loadSound16: load a sound file and return an array of samples (16 bits) (in mono)
# - removeBlankFromFile: remove blank at begin and end of a raw sound file, a blank is a 0 byte.
# - convertSoundRaw: resample a 16 bits sound in two channels
# - normaliseSound: Analyse a raw 16 bits signed sound file, and change its volume to have peaks at 100%
# - computeEnergyBest: Compute sound energy on a mono channel sample, aSample contents signed int from -32000 to 32000 (in fact any signed value)
#
# - class NoDuplicate: a class to prevent having duplicate object in a system: it stores name and later could tell if present/or not. All is thread safe.
# - interpolateColor: interpolate a rgb color from nColorFrom to nColorTo
# - interpolateColor3: interpolate a rgb color from nColorFrom to nColorTo passing by nColorMedian at ratio of 0.5 
# - valueToPseudoColor: convert a value [0,nMax] to a pseudo color green/yellow/red
# - logToFile: add a message to the current debug log file
# - isConnectedToInternet: return True if connected to internet
# - isConnectedWithEthernet: return True if connected using ethernet cable
#
#######################################

print( "*** altools: parsing generic tools" );

import os
import re # regexp
import datetime
import string
import threading
import random
import math
import struct
import mutex
import trace
import signal
import time
import sys

global_SectionCritique = mutex.mutex(); # a global critical section to mutex some piece of code


SHRT_MIN = -32766
SHRT_MAX = 32767

global_debug_dictAlreadyOutputted = dict();
def debug( args, bIgnoreDuplicateMessage = False ):
  "output a debug message to the user"
  "bIgnoreDuplicateMessage: when set to true, won't output message if the same has been outputted"
  if( naoconfig.bDebugMode ):
    if( bIgnoreDuplicateMessage ):
        global global_debug_dictAlreadyOutputted;
        if( str( args ) in global_debugAlreadyOutputted .keys() ):
            return;
        global_debugAlreadyOutputted [str(args)] = True; # add it!
    print args;
# debug - end

def setDebugMode( bNewVal ):
  print( "altools.setDebugMode: changed from %s to %s" % ( naoconfig.bDebugMode, bNewVal ) );
  naoconfig.bDebugMode = bNewVal;
# setDebugMode - end

def dump( obj, bShowPrivate = True ):
  "dump the contents of an object into a string"
  s = "";
  for attrName in dir( obj ):
    if( not bShowPrivate and attrName[0] == '_' ):
      continue;
    s += "%s: '%s'\n" % ( attrName, str( getattr( obj, attrName ) ) );
  return s;
  
global_getNaoqiStartupTime = time.time();
def getNaoqiStartupTime():
    "return the time in seconds epoch of naoqi start (actually last altools loading)"
    global global_getNaoqiStartupTime;
    return global_getNaoqiStartupTime;
# getNaoqiStartupTime - end

global_getNaoqiStartupTimeStamp = str( datetime.datetime.now() );
global_getNaoqiStartupTimeStamp = global_getNaoqiStartupTimeStamp[0:len(global_getNaoqiStartupTimeStamp)-3]; # enleve les micro secondes!
global_getNaoqiStartupTimeStamp = global_getNaoqiStartupTimeStamp.replace( " ", "_" );
global_getNaoqiStartupTimeStamp = global_getNaoqiStartupTimeStamp.replace( ":", "m" );
  
def getNaoqiStartupTimeStamp():
    "return the time stamp of naoqi start (actually last altools loading) - human readable, printable, usable as a filename"
    global global_getNaoqiStartupTimeStamp;
    return global_getNaoqiStartupTimeStamp;
# getNaoqiStartupTimeStamp - end





  
def getFileAndLinePosition( nCallStackUp = 0 ):
    "this method return the position of caller in a string (idem __FILE__ __LINE__)"
    "purpose: debug, trace..."
    "nCallStackUp: you can ask for your caller, by adding extra higher level in the call stack"
    "0: this method"
    "1: the method that calls this method"
    "2: ..."
    co = sys._getframe(nCallStackUp+1).f_code; # return one more, call we are in a method !
    return "%s (%s @ %3d)" % (co.co_name, co.co_filename, co.co_firstlineno);
# getFileAndLinePosition - end

#~ print getFileAndLinePosition();

class TimeMethod:
    "mesure the time taken by a method"
    "Use: define an object TimeMethod in your method, and that's all!"
    def __init__(self, strOptionnalLibelle = "" ):
        "Create the object"
        self.reset( strOptionnalLibelle );
    # __init__ - end
    
    def reset( self, strOptionnalLibelle = "" ):
        "reset the object"
        self.strCaller = getFileAndLinePosition( 2 ); # callstack: reset, __init__, caller
        if( strOptionnalLibelle != "" ):
            strOptionnalLibelle = "( " + strOptionnalLibelle + " )";
        self.strOptionnalLibelle = strOptionnalLibelle;
        self.timeBegin = time.time();            
        self.intermediate = []; # optionnal pair of [time, message]
        self.bStopped = False;
    # reset - end
    
    def setIntermediate( self, strOptionnalMessageNamingFollowingPart = "" ):
        "store intermediate time and continue, the optionnal name is the name of the following part"
        if( strOptionnalMessageNamingFollowingPart != "" ):
            strOptionnalMessageNamingFollowingPart = "( " + strOptionnalMessageNamingFollowingPart + " )";
        totalTime = time.time() - self.timeBegin;
        self.intermediate.append( [ totalTime, strOptionnalMessageNamingFollowingPart ] );
        timePrev = 0;
        if( len( self.intermediate ) > 1 ):
            timePrev = self.intermediate[-2][0];
        print( "timer: %40s: intermediate time: %6.3f %s %s\n" % ( self.strCaller, totalTime-timePrev, self.strOptionnalLibelle, strOptionnalMessageNamingFollowingPart ) );
    # setIntermediate - end
    
    def getCurrentTotalTime( self ):
        return time.time() - self.timeBegin;
    # getCurrentTotalTime - end
        
    def stopAndPrint( self ):
        "stop the timer, print info, and return a string containing a printable string"
        strOut = "";
        if( self.bStopped ):
            return strOut;
        self.bStopped = True;
        totalTime = time.time() - self.timeBegin;
        if( len( self.intermediate ) < 1 ):
            strOut += "timer: %40s: executing time: %6.3f %s" % ( self.strCaller, totalTime, self.strOptionnalLibelle );
        else:
            strOut += "timer: %40s: total time: %6.3f %s\n" % ( self.strCaller, totalTime, self.strOptionnalLibelle );
            nPrev = 0.;
            for someTime in self.intermediate:
                strOut += " %57s + %6.3f %s\n" % ( "", someTime[0] - nPrev, someTime[1] );
                nPrev = someTime[0];
            strOut += " %57s + %6.3f %s" % ( "", totalTime - nPrev, "( til the end )" );
        print( strOut );
        return strOut;
    # stopAndPrint - end
    
    def __del__( self ):
        self.stopAndPrint();
    # __del__ - end
    
# class TimeMethod - end

#~ timer = TimeMethod( "coucou" );
#~ time.sleep( 1 );
#~ timer.setIntermediate( "compute" );
#~ time.sleep( 4 );
#~ timer.setIntermediate( "draw" );
#~ time.sleep( 3 );
#~ timer.stopAndPrint();


def getDirectorySeparator():
  "return / or \ relative to the os"
  if os.name == 'posix':
    return "/";
  return "\\";
# getDirectorySeparator - end

def getDirectoryName( strPathAndFile ):
    "get directory name from an absolute path and filename"
    nIndex = strPathAndFile.rfind( getDirectorySeparator() );
    
    if( nIndex == -1  ):
        return getDirectorySeparator();
    return strPathAndFile[:nIndex] + getDirectorySeparator();
# getDirectoryName - end

def getHostFolderAndFile( strWebAddress ):
    "separate host, directory and filename from a web address"
    "ie: 'http://mangedisque.com/Alma/index.html' => ['http://mangedisque.com', 'Alma', 'index.html'];"

    strHostname = "";
    strFoldersName = "";
    strFileName = "";
    
    strRemaining = strWebAddress;
    nIndex = strRemaining.find( '//' );
    if( nIndex != -1 ):
        strHostname = strRemaining[:nIndex+2];        
        strRemaining = strRemaining[nIndex+2:];
    else:
        strHostname = "http://";
        
    nIndex = strRemaining.find( '/' );
    if( nIndex != -1 ):
         strHostname += strRemaining[:nIndex];
         strRemaining = strRemaining[nIndex:];
    else:
        strHostname += strRemaining;
        strRemaining = "";

    nIndex = strRemaining.rfind( '/');
    if( nIndex != -1 ):
         strFoldersName = strRemaining[:nIndex+1];
         strFileName = strRemaining[nIndex+1:];
    else:
        strFileName = "index.php";
        
    if( strHostname[0] in ['"', "'"] ):
        strHostname = strHostname[1:];
        
    if( strFileName[-1] in ['"', "'"] ):
        strFileName = strFileName[:-1];
     
    return [ strHostname, strFoldersName, strFileName ];
# getHostFolderAndFile - end
#print( "%s" % getHostFolderAndFile( 'http://mangedisque.com/Alma/index.html' ) ); # pass
# print( "%s" % getHostFolderAndFile( 'http://google.com/index.html' ) ); # pass



# has the variable the array type ?
def isArray( aVariable ):
	try:
		aVariable[0];
	except BaseException, err:
		return False;
	return not isString( aVariable ); #car les strings aussi ont la méthode crochet

# has the variable the string type ? (bytes or unicode)
def isString( strVariable ):
  try:
    # if( type( strVariable ) == type( "some string") ):
    if isinstance( strVariable, basestring ): # True for both Unicode and byte strings
      return True;
  except BaseException, err:
    pass
  return False;
# isString - end

# has the variable the string type bytes ?
def isString_Bytes( strVariable ):
  try:
    if isinstance( strVariable, str ):
      return True;
  except BaseException, err:
    pass
  return False;
# isString_Bytes - end

# has the variable the string type unicode ?
def isString_Unicode( strVariable ):
  return isString( strVariable ) and not isString_Bytes( strVariable );
# isString_Unicode - end

def stringToNumber( strVariable ):
    "try to convert a string to a number, return None if the string can be converted to a number"
    try:
        return float( strVariable );
    except BaseException, err:
        pass
    return None;
# stringToNumber - end

def splitMany( s, aListSep ):
    "split a string, accepting a list of splitters"
    "eg: listSentence = splitMany( aBigParagraph, ['.', ',', ':' ] );"
    listOut = [];
    nFirst = 0;
    for i in range( len( s ) ):
        if( s[i] in aListSep ):
            if( i > nFirst ):
                listOut.append( s[nFirst: i] );
            nFirst = i+1;
    if( nFirst < len( s ) ):
        listOut.append( s[nFirst: i+1] );
    return listOut;
# splitMany - end
#print( ": " + str( splitMany( "salut, les gens comment ca va? Moi ca va", ['.', ',', ':', '!', '?' ] ) ) );

def arrayCreate( nNewSize, value = 0 ):
    "create an array of size nNewSize by inserting some value (default 0)"
    newArray = [];
    for i in range( nNewSize ):
        if( not isArray( value ) ):
            newArray.append( value );
        else:
            #don't want to have a pointer on the list contains in value, but a fresh new array !
            newArray.append( [] );
            newArray[len( newArray) -1].extend( value ); # TODO: .last() ???
    return newArray;
# arrayCreate - end

def arraySum( anArray ):
    "compute the sum of an array"
    "assume all element of the array could be added each others"
    sum = 0;
    for val in anArray:
        sum += val;
    return sum;
# arraySum - end

def decreaseAngle( rAngle, rStep ):
	"decrease an angle of some step (by making tend to zero (even if it's a neg value))"
	if( rAngle > 0.001 ):
		if( rAngle < rStep ):
			rAngle = 0;
		else:
			rAngle = rAngle - rStep;
	else:
		if( rAngle > rStep ):
			rAngle = 0;
		else:
			rAngle = rAngle + rStep;
	return rAngle;

def isNearlyEqual( rVal1, rVal2 ):
    "is two variables quite the same?"
    return abs( rVal1 - rVal2 ) < 0.001;

def colorCompToHexa( rR, rG, rB ):
    "take 3 floats R,G,B [0.0,1.0] and create an hexa value from them"
    nColor = ( int(rR * 255.) << 16 ) | ( int(rG * 255.) << 8 ) | int( rB * 255. );
#    debug( "colorCompToHexa: r:%f, g:%f, b:%f => 0x%x" % ( rR, rG, rB, nColor ) );
    return nColor;
# colorCompToHexa - end

def colorHexaToComp( nColor ):
    "take an rgb int (24bits) and return [b,g,r]"
    rB = ( ( nColor & 0xFF ) ) / 255.;
    rG = ( ( nColor & 0xFF00 ) >> 8  ) / 255.;
    rR = ( ( nColor & 0xFF0000 ) >> 16  ) / 255.;
    aRet = [rB, rG, rR];
#    debug( "colorHexaToComp: 0x%x => %s" % ( nColor, str( aRet ) ) );
    return aRet ;
# colorHexaToComp - end

def limitRange( rVal, rMin, rMax ):
    "ensure that a value is in the range rMin, rMax"
    if( rVal < rMin ):
        rVal = rMin;
    elif( rVal > rMax ):
        rVal = rMax;
    return rVal;
# limitRange - end

def replaceWord( src, strFrom, strTo = "" ):
    "a string replacement, but using entire word only"
    strOut = "";
    nIndex = src.find( strFrom );
    nLenSrc = len( src );
    nLenFrom = len( strFrom );
    aListSeparator=[' ', ',', '.', ';', ':', '\n', '!', '?', '<', '>', '=', "'", '"', '(', ')' ];
    nIndexBegin = 0;
    while( nIndex != -1 ):
        strOut += src[nIndexBegin:nIndex];
        # check entire wordity
        if( 
                    ( nIndex == 0 or src[nIndex-1] in aListSeparator )
            and   ( nIndex+nLenFrom == nLenSrc or src[nIndex+nLenFrom] in aListSeparator )
        ):
            # entire word
            strOut += strTo;
        else:
            # not entire => don't change it
            strOut += strFrom;

        nIndexBegin = nIndex + nLenFrom;
        nIndex = src.find( strFrom, nIndexBegin );
    # while - end
    strOut += src[nIndexBegin:]; # copy end
    return strOut;
# replaceWord - end
#print( "replaceWord: " + replaceWord( "con la petite fille est contente mais pas con\ncon! con. con abscon con (con) con>=con", "con", "trop" ) );



def chooseOneElem( aList ):
    "Pick randomly an element in a list "
    "each list contains elements, and optionnal probability ratio (default is 1)"
    "exemple of valid list:"
    "     'hello' (a non list with only one element)"
    "     ['hello', 'goodbye']"
    "     ['sometimes', ['often',10] ] often will appears 10x more often than sometimes (statistically)"
    
    # simple case
    if( not isArray( aList ) ):
        return aList;
        
    # generate statistic repartition
    listProba = [];
    nSum = 0;
    for elem in aList:
        if( isArray( elem ) and len( elem ) > 1 ):
            nVal = elem[1];        
        else:
            nVal = 1; # default value        
        listProba.append( nVal );
        nSum += nVal;
    nChoosen = random.randint( 0, nSum - 1 );
#    logToChoregraphe( "nChoosen: %d / total: %d / total different: %d (list:%s)" % ( nChoosen, nSum, len( aList ) , aList ) );
    nSum = 0;
    nIdx = 0;
    for val in listProba:
        nSum += val;
        if( nSum > nChoosen ):
            elem = aList[nIdx];
            if( isArray( elem ) ):
                return elem[0];
            return elem;
        nIdx += 1;
        
    return "not found or error";
    
# chooseOneElem - end

def concateneRandom( listlistword ):
    "take a list of word list and concatene it"
    "each list contains a word and an optionnal probability (see chooseOneElem)"
    # strSentence = chooseOneElem( 'hello' );
    # strSentence = chooseOneElem( ['hello', 'goodbye'] );
    # strSentence = chooseOneElem( ['sometimes', ['often',10] ] );    
    strSentence = "";
    for aList in listlistword:
        strSentence += chooseOneElem( aList ) + ' ';
    return strSentence;
# concateneRandom - end

def wordlist_AddOccurenceModel( listwords, nOccurenceModel = 10 ):
    "add occurence model to a word list"
    # nOccurenceModel == 10: pick always one word
    # nOccurenceModel == 3: pick nearly always one word
    # nOccurenceModel == 2: pick sometimes one word
    # nOccurenceModel == 1: pick rarely one word
    # nOccurenceModel == 0: pick never one word (no use)!    
    nbrTotalWord = len( listwords );
    if( nOccurenceModel == 10 ):
        pass # nothing to do
    elif( nOccurenceModel == 3 ):
        listwords += "";
    elif( nOccurenceModel == 2 ):
        listwords.append( ["",nbrTotalWord] );
    elif( nOccurenceModel == 1 ):
        listwords.append( ["",nbrTotalWord*10] );
    else:
        return ""; # case 0
    return listwords;
# wordlist_AddOccurenceModel

def wordlist_things( nOccurenceModel = 10 ):
    listword = ["cette chose", "ce truc", ["ce machin",5], "ce zigouigoui", "cette drole de chose", "se bidule", "se bitonio", "cet objet", "ce bazar", "cette amas bizarre", "ce binhsse", "cette cochonnerie" ];
    return wordlist_AddOccurenceModel( listword, nOccurenceModel );
# wordlist_things - end

def wordlist_interjection( nOccurenceModel = 2 ):
    "return a list word of a certain type/function, using some frequency model"
    listword  = [ "Ah mais", "oh", "ah bein ca", "je me disait bien, mais","oh la la la", "crénom", "vingt dieux", "parbleu", "ca alors", "ohlolo", "croudablou", "hey!", "ah ca donc" ];
    listword = wordlist_AddOccurenceModel( listword, nOccurenceModel );
    return listword;
# wordlist_interjection - end

def wordlist_bonus( nOccurenceModel = 2 ):
    "return a list word of a certain type/function, using some frequency model"
    listword  = ["grave", "c'est bizarre", "ne trouves tu pas",  "tro ouf",  "trop zarbi non", "plom", "mince" ];
    listword = wordlist_AddOccurenceModel( listword, nOccurenceModel );
    return listword;
# wordlist_bonus - end

def generatePhraseWithAdjectif( listAdj ):
    "generate a sentence desbcribing an adjectif"
    introduction = [ ["",10], "je trouve que", "actuellement", "oh", "ouais bein moi", "en ce moment", "aujourd'hui", "il parait que", "certains m'ont dit que", "mon petit doigt m'a dit que" ];
    subject = [ ["j'ai",3]];
    adverbe = [ ["",6], "un peu", "beaucoup", "grave", "tres", "de temps en temps"];
    # adjectif as params
    amplificateur = [ ["", 7], "trop grave", "depuis longtemps", ", si si je te jure", "beaucoup"];
    
    return concateneRandom( [introduction, subject, adverbe, adverbe, listAdj, amplificateur] );
# generatePhraseWithAdjectif - end


    
def generateQuestionAboutThings( aThingsDescriptor ):
    "generate a sentence about something"
    subject = ["quel est", "qu'est ce que c'est que", "je n'ai jamais vu", "je ne connais rien qui ressemble a", "une fois j'ai vu quelque chose qui me rappelle" ];
    adverbe = [ ["",6], ""];
    things = wordlist_things();
    amplificateur = [ ["", 50], "pourri", "moche", "dans ma vie", ", vu cette semaine", "tel qu'aujourd'hui", "disparu depuis longtemps", "en train de trainer dans le coin", "a cette place", "près de ma main", ", sauf dans un avion", "qui ressemble a ca", "qui traine", "a sa place", ", vu récemment", ", a part dans une brocante", "qui ressemble a rien qui existe"];
    
    bonus = wordlist_bonus(2);
    
    return concateneRandom( [wordlist_interjection(), subject, adverbe, things, aThingsDescriptor, amplificateur, ",", bonus, "?" ] );
# generateQuestionAboutThings - end

def generateComparison():
    "generate comparisons 'comme un nain dans un avion'"
    adj = [ ["comme",5], "autant que", "plus que", "largement plus que", "un peu comme", "légèrement plus que", "identique a" ];
    object = ["une planche", "un robot", "un avion", "une pomme", "un train", "un vélo", "une mobilette", "un couteau", "une fourchette", "un mur", "la mer", "un boulon", "un vibromasseur", "un vilebrequin", "un supermarché", "un cadavre", "une balle", "un pistolet", "un ordinateur", "une plaie"];
    name = ["Ferdinand", "Céline", "Alexandre", "Jérome", "Flora", "Manuel", "Julien", "Inetissar", "Valentin", "Bruno"];
    human = ["un nain", "un monstre", "un magicien", "un pretre", "un homme", "un bébé", "ta mère", "une ombre", "un vieillard", "un cadavre", "un fou", "une belle femme", "un bogosse", ];
    animal = ["un ver de terre", "ton chien", "une girafe", "une lionne", "un cafard"];
    star = ["la belle mère de Sarkozi", "le pape", "Zinédine Zidane", "Nao", "Jonnny Halidai" ];
    subject = object + name + animal + human + star;
    comp = [ ["qui",6] ];
    action = ["cuisinerait", "taperait", "mangerait", "fumerait", "pisserait sur", "jetterais", "irait plus vite que" , "vomirait", "aurait une relation sexuelle avec", "aurait une relation sexuelle tarifée, avec", "aurait une relation professionnelle avec", "conduirait", "piloterait", "volerait", "dévorerait", "torturait"];
    return concateneRandom( [adj, subject, comp, action, subject] );
# generateComparison - end

def generateRecognise( aThingsDescriptor ):
    "generate recognise 'ca ressembla a (mon jouet)"
    things = wordlist_things();    
    recognise = [ "à la même tête que", "ressemble a", ", ca ressemble a", "on dirait", "a le style de", "ressemble de loin a" ];
    return concateneRandom( [wordlist_interjection( 1 ), things,  recognise, aThingsDescriptor] );
# generateComparison - end


def generateBof():
    "generate a bof adulescent sentence"
    bof = [ "c'est bof", "c'est presque nul", "c'est pas chant-mé", "ca craint", "c'est pas terrible", "ca n'a rien de particulierement intéressant", "c'est limite crainiausse", "ca casse pas 3 pattes a un canard", "je trippe pas grave", "on dirait un film de Rohmére", "Ennuyeux, comme une radio qui diffuserait un film muet", "c'est quelquonque"  ];
    bonus = wordlist_bonus(2);
    return concateneRandom( [bof , "!", bonus] );
# generateComparison - end


def rgbToHsv( rgb ):
    "take an rgb array [r,g,b] (0..255) and return it in [h,s,v] (0..255)"
    "Attended value:"
    "red: [255,0,0] => [0°=>0,255,255]"
    "green: [0,255,0] => [120°=>85,255,255]"
    "blue: [0,0,255] => [240°=>170,255,255]"
    "light blue: [40,128,255] => [215°=>152, 84.3% => 214.96 , 255]"
    "grey: [128,128,128] => [0, 0, 128]"
    "light orange [255,180,80] => [34° => 24, 68.6% => 174.9, 255]"
    "light green [120,255,80] => [106° => 75, 68.6% => 174.9, 255]"
    "white [255,255,255] => [0, 0, 255]"
    "purple/magenta [255,0,255] => [-60° => 212.5, 255, 255]"
    "cyan [0,255,255] => [180° => 128, 255, 255]"
    "yellow [255,255,0] => [60° => 42.5, 255, 255]"    
    "army green [50,125,100] => [160° => 113, 153, 125]" # this one is wrong (113 instead of 98)
    "dark grey [63,64,65] => [210° => 149, 7, 63]" # this one is slightly wrong (149 instead of 164)

    """
    V = max(R,G,B)
    S = (V-min(R,G,B))/V if V<>0, 0 otherwise 
    H =

        (G - B)/6/S, if V=R; 
        1/2+(B - R)/6/S, if V=G; # en fait ca marche mieux ca avec 1/3 qu'avec 1/2, pfff...
        2/3+(R - G)/6/S, if V=B. 
    """

    r,g,b = rgb;
    
    v = max(r,g,b);
    if( v == 0 ):
        s = 0;
    else:
        s = ( v - min(r,g,b) ) * 255 / v;

    if( s == 0 ):        
        h = 0;
    else:
        if( v == r ):
            h = (g - b)*42/s; # c'est plus drole de mettre des 42!
        elif( v == g ):
#            h = 127 + ((b - r)/6)/s; # la il y a un truc de faux!
#            h = h * 255 / 360;
            h = 85 + ((b - r)*42)/s;
        else:
            h = 170 + ((r - g)*42)/s;
    if( h < 0 ):
        h += 255;
    return [h,s,v];
# def rgbToHsv - end

def getColorNameFromHSV( hsv, nIndexLang = 0, bHueIsOn360 = False ):
    "take a hue value [h,s,v](0..255) and return the name of the nearest color with the distance to the plain color [0,1] (multilangue)"
    aHueReferences256 = [
        [217, 14],      # 'Red'        
        [14, 29],       # 'Orange'
        [29, 49],       # 'Yellow'
        [49, 120],      # 'Green'
        [120, 177],     # 'Blue'
        [177, 217],     # 'Purple
    ];    
    
    aHueReferences360 = [
        [305, 20],      # 'Red'        
        [20, 41],       # 'Orange'
        [41, 69],       # 'Yellow'
        [69, 169],      # 'Green'
        [169, 249],     # 'Blue'
        [249, 305],     # 'Purple
    ];    
    
    
    aColorList = [
        [ 'Red' , 'Rouge' ],
        [ 'Orange' , 'Orange' ],
        [ 'Yellow' , 'Jaune' ],
        [ 'Green' , 'Vert' ],
        [ 'Blue', 'Bleu' ],
        [ 'Purple' , 'Violet' ],
    ];
    
    nDefaultColor = 0; # if not found => red
    
    if( bHueIsOn360 ):
        aHueReferences = aHueReferences360;
    else:
        aHueReferences = aHueReferences256;
    
    
    # handle "no color" color
    
    nSatu = hsv[1];
    if( nSatu < 40 ):
        nValue = hsv[2];
        aGreyLevel = [
            [ 'Black',  'Noir' ],
            [ 'Dark Grey',  'Gris foncé' ],
            [ 'Grey',  'Gris' ],
            [ 'Light Grey',  'Gris clair' ],
            [ 'White',  'Blanc' ],
        ];
        
        nRange = (255) / (len( aGreyLevel ) - 0);
        nIndex = nValue / nRange;
        if( nIndex >= len( aGreyLevel ) ):
            nIndex = len( aGreyLevel ) - 1;
            
        # On border area, confidence is the distance from the border. On inner area it's the difference with the median value
        if( nIndex == 0 ):
            rConfidence = nValue / float( nRange );
        elif( nIndex == len( aGreyLevel ) - 1 ):
            rConfidence = (255-nValue) / float( nRange );
        else:
            rConfidence = abs( (nValue - (nIndex*nRange) - nRange/2 ) / float( nRange ) ) * 2;
        return [aGreyLevel[nIndex][nIndexLang], rConfidence ];
        
    sColor = None
    distance = None
    nHue = hsv[0];
    # Then look up into the reference hue colors
    for i in range( len( aHueReferences ) ):
      v = aHueReferences[i];
      if v[0] <= nHue < v[1]:
          sColor = aColorList[i][nIndexLang];
          center = float(v[0]+v[1])/2.0
          distance = abs(nHue - center) / (v[1] - center)
          break;

    # If no color found here, then it's Red, since nHue is around zero
    if sColor == None:
        print( "sColor: none!!! (red?)" );
        sColor = aColorList[nDefaultColor][nIndexLang];
        v = aHueReferences[nDefaultColor];
        if nHue >= v[0]:
            nHue -= 255
        v = [v[0]-255, v[1]]        
        center = float(v[0]+v[1])/2.0
        distance = abs(nHue - center) / (v[1] - center)

    print("Hue : %d, Color : %s, variance : %s" % (nHue, sColor, str(distance)))
    return [sColor, distance];
# getColorNameFromHSV - end


def getRGBFromColorName( name, nIndexLang = 0 ):
    "take the color name and convert it to RGB value"
    if nIndexLang == 0:
      aColorDict = {'Blue':[0, 0, 255],
                    'Purple':[160, 32, 240],
                    'Green':[0, 255, 0],
                    'Yellow':[255, 255, 0],
                    'Orange':[255, 165, 0],
                    'Cyan':[0, 255, 255],
                    'Magenta':[255, 0, 255],
                    'Red':[255, 0, 0]}
    elif nIndexLang == 1:
      aColorDict = {'Bleu':[0, 0, 255],
                    'Violet':[160, 32, 240],
                    'Vert':[0, 255, 0],
                    'Jaune':[255, 255, 0],
                    'Orange':[255, 165, 0],
                    'Cyan':[0, 255, 255],
                    'Magenta':[255, 0, 255],
                    'Rouge':[255, 0, 0]}
    if aColorDict.has_key(name):
      return aColorDict[name]
    else:
      return None
    
    
def darkenColor( nColor, rLuminosity ):
    "darken one color: if rLuminosity is set to 0.0 => black; 1.0 => no change"
    if( rLuminosity > 1. ):
        rLuminosity = 1.;
    elif( rLuminosity < 0. ):
        rLuminosity = 0.;
    rB,  rG, rR = colorHexaToComp( nColor );
    rB *= rLuminosity;
    rG *= rLuminosity;
    rR *= rLuminosity;
    return colorCompToHexa( rR, rG, rB );
# darkenColor - end

def convertAngleToByte( rVal ):
  "convert a joint angle -3..+3 in radians to a byte 0..255"
  n = int( ( ( rVal + 3.0 ) * 255 ) / 6 );
  return n;
# convertAngleToByte - end

def convertByteToAngle( n ):
  "the reverse operation of convertAngleToByte"
  rVal =  ( n * 6 ) / 255.0 - 3.0;
  return rVal;
# convertByteToAngle - end


def isFileExists( strPathFilename ):
#  strPathFilename = strPathFilename.replace( "/", getDirectorySeparator() );
#  strPathFilename = strPathFilename.replace( "\\", getDirectorySeparator() );
#  strPathFilename = strPathFilename.replace( getDirectorySeparator() + getDirectorySeparator(), getDirectorySeparator() );
#  print( "isFileExists( '%s' ) =>" % strPathFilename );
  try:
    file = open( strPathFilename, 'r' );
#    print( "file: " + str( file ) );
    if( file ):
#      print( "true" );
      file.close();
      return True;
  except (IOError, os.error), err:
#    print( "err: " + str( err ) );
    pass
#  print( "false" );
  return False;
# isFileExists - end

def copyFile( strPathFilenameSrc, strPathFilenameDst ):
    "copy one file to another one"
    "return true if ok"
    print( "copyFile: %s => %s" % ( strPathFilenameSrc, strPathFilenameDst ) );
    bError = False;
    try:
        file = open( strPathFilenameSrc, "rb" );
    except BaseException, err:
        print( "ERR: copyFile: err(1): " + str( err ) );
        return False;
        
    try:
        strBuf = file.read();
    except BaseException, err:
        print( "ERR: copyFile: err(2): " + str( err ) );
        bError = True;
    file.close();        
    if( bError ):
        return False;

    try:
        file = open( strPathFilenameDst, "wb" );
        file.write( strBuf );
        file.close();
    except (IOError, os.error), err:
        print( "altools.copyFile failed: %s" % err );
        return False;
    return True;
# copyFile - end

class Const:
   """ a small class to create constant preventing to changing the value of an existant one"""
   """ to create a new constants, just type const.toto = 3;"""
   def __init__(self):
       self.__aListConstantes = {} # __aListConstantes is static to the class # seems not working ?!?

   def __getattr__(self, attr):
       try:
           return self.__aListConstantes[attr]
       except:
           return self.__dict__[attr]

   def __setattr__(self, attr, value):
#       print( "__setattr__( %s, %s )" % ( str(attr), str(value) ) );
       if( attr == "_Const__aListConstantes" ):
            if( attr in self.__dict__.keys() ):
               raise "error: other instance of same class?"; # seems not working ?!?
            self.__dict__[attr] = value; # first "classic" assignation at init
            return;
       if ( attr in self.__aListConstantes.keys() ) and self.__aListConstantes[attr] != value:
           raise( "Const: Cannot reassign constant '%s'" % attr )
       else:
           self.__aListConstantes[attr] = value;

   def __str__(self):
       return '\n'.join(['%s: %s' % (str(k), str(v)) for k,v in self.__aListConstantes.items()])

# class Const - end

const = Const();

# ressource managing constantes
const.ressource_weak = 1
const.ressource_blend = 2
const.ressource_lock = 3
const.ressource_reserve = 10
const.state_unknown = -424242;  # None # float( '-inf' ); # etat d'un capteur ou d'un extracteur inconnu


def getFileContents( szFilename ):
    "read a file and return it's contents, or '' if not found, empty, ..."
    aBuf = "";
    try:
        file = open( szFilename );
    except BaseException, err:
        print( "ERR: getFileContents: err(1): " + str( err ) );
        return "";
        
    try:
        aBuf = file.read();
    except BaseException, err:
        print( "ERR: getFileContents: err(2): " + str( err ) );
        file.close();
        return "";
        
    try:
        file.close();
    except BaseException, err:
        print( "ERR: getFileContents: err(3): " + str( err ) );
    return aBuf;
# getFileContents - end


def getLine( strText, nNumLine ):
    "extract a specific line in a multiline text, return '' if line not found, text empty or ..."
    "parameter nNumLine should be in [0,nbrline-1]"
    # trim EOL and ...
    if( len( strText ) < 1 or nNumLine < 0 ):
        return "";


    aByLine = strText.split( '\n' );

    if( nNumLine >= len( aByLine ) ):
        return "";
    return aByLine[nNumLine];
 # getLine - end

def getFileFirstLine( szFilename ):
  "read a file and return it's first line, or '' if not found, empty, ..."
  strBufferRead = getFileContents( szFilename );
  return getLine( strBufferRead, 0 );
# getFileFirstLine - end


def getnSentences ( s , n , bKeepFirstSentence = True):
    atext = string.split(s,".")
    length = len(atext)
    if n> length:
        n = length;
    if bKeepFirstSentence:
        text = atext[0]+'.';
        minimum = 1;
        n = n-1;
    else:
        text = "";
        minimum = 0;        
    x = range(minimum,length);
    random.shuffle(x);
    for i in range(n+1):
        nSentence = atext[x[i]];
        text = text + nSentence +'.';
    return(text);
#getnSentences

 # change les accents ascii en accent pour les dire correctement a la synthese
def transformAsciiAccentForSynthesis( s ):
    strOutput = "";
    nLen = len( s );
    for i in range( 0, nLen ):
        sNew = s[i];
        if(
         # equivalence hexa au cas ou, multiplateforme et ...
              s[i] == 'é' or ord( s[i] ) == 0xe9
          or s[i] == 'è' or ord( s[i] ) == 0xe8
          or s[i] == 'ê' or ord( s[i] ) == 0xea
          or s[i] == 'ë' or ord( s[i] ) == 0xeb
          ):
            sNew = 'ei';
        else:
            if( s[i] == 'ô' or ord( s[i] ) == 0xf4 or s[i] == 'ö' or ord( s[i] ) == 0xf6 ):
                sNew = 'au';
            else:
                if( sNew != s[i] and ord(s[i]) > 127 ):
                    print( "transformAsciiAccentForSynthesis: character should create problems: %s (%d) at offset %d" % ( s[i], ord( s[i] ), i ) );
#                if( ord(s[i]) < 127 ): # todo: desaccentuation !
                    pass # nothing to do!
        strOutput = strOutput + sNew;
#        debug( "transformAccentForSynthesis: %d %c 0x%x => %s 0x%x" % ( i, s[i], ord( s[i] ), sNew, ord(sNew) ) );
    return strOutput;
# transformAsciiAccentForSynthesis - end

def removeAsciiAccent( s ):
    "remove accent from a french sendence"
    #~ s = ur'Hello\u0020World !'
    #~ for i in range( 0, len( s ) ):
        #~ print( "s[i]" % str( s[i] ) );
    #~ s = unicode( s, "UTF-16" );
    #~ s = s.encode( "UTF-16" );
    #~ strOutput = "";
    #~ nLen = len( s );
    #~ for i in range( 0, nLen ):
        #~ sNew = s[i];
#~ #        print( "removeAsciiAccent: %s (0x%x)" % ( sNew, ord( sNew ) ) );
        #~ print( "removeAsciiAccent: %s" % ( sNew ) );
        
        #~ if(
         #~ # equivalence hexa au cas ou, multiplateforme et ...
              #~ sNew == 'é' or ord( sNew ) == 0xe9
          #~ or sNew == 'è' or ord( sNew ) == 0xe8
          #~ or sNew == 'ê' or ord( sNew ) == 0xea
          #~ or sNew == 'ë' or ord( sNew ) == 0xeb
          #~ True
          #~ ):
            #~ sNew = 'e';
        #~ else:
            #~ if( sNew == 'ô' or ord( sNew ) == 0xf4 or sNew == 'ö' or ord( sNew ) == 0xf6 ):
                #~ sNew = 'o';
            #~ else:
                #~ if( sNew != sNew and ord(sNew) > 127 ):
                    #~ pass # nothing to do!
        #~ strOutput = strOutput + sNew;
    #~ return strOutput;
    
    #~ nkfd_form = unicodedata.normalize('NFKD', unicode(s))
    #~ only_ascii = nkfd_form.encode('ASCII', 'ignore')
    #~ return only_ascii
    
    # return unidecode.unidecode(s)
    
    # I haven't found simpler manner to handle both unicode, ordinal and ...
    intab = "éèêëöôàù";
    outtab = "\01e\01e\01e\01e\01o\01o\01a\01u";
    trantab = string.maketrans(intab, outtab);
    s = s.translate(trantab);
    s = s.replace( "\01", "" );
    return s;
# removeAsciiAccent - end

# change les accents ascii en accent utf-8
def transformAsciiAccentToUtf8( s ):
  strOutput = "";
  nLen = len( s );
  # j'ai remarqu?u'il suffisait de prendre le char ascii plus grand que E0 et de sortir un 0xC3 0xA0+offset par rapport a E0
  for i in range( 0, nLen ):
#    print( "transformAsciiAccentToUtf8: %d %c 0x%x" % ( i, s[i], ord( s[i] ) ) );
    if( ord( s[i] ) >= 0xE0 ): # ceci marche bien, mais juste pour les accents, or des fois on a des trucs tout bizarre genre: IRREVERSIBLE a L'envers (des 0xD0 0xAF 0xC6 0x8E)
      strOutput = strOutput + chr(0xC3) + chr( 0xA0+ord( s[i] )-0xE0 );
    else:
      if( ord( s[i] ) > 127 and ord( s[i] ) != 0xC3 and ord( s[i-1] ) != 0xC3 ): # ca doit etre des caracteres pourris, on les skippe! (sauf l'accent aigu)
        pass;
      else:
        strOutput = strOutput + s[i];
  return strOutput;
# transformAsciiAccentToUtf8 - end

 # change les accents ascii en accent utf-8: %C3%A4 => 0xC30xA4
def transformWikiAccentToUtf8( s ):

  def hexToChar( match ):
    s = match.group();
#    print( 'hexToChar: %s' % s );
    if( s[0] == '%' ):
      s = s[1:]; # vire le %
    value = int( s, 16 );
#    print( "value:", value );
    s = chr( value );
#    print( "s:", s );
    return s;
    # hexToChar

  # regexp pour changer les accents wiki en utf8
  print( "transformWikiAccentToUtf8: avant: ", s );

    # ca ca marche bien, mais ca genere des "%C3%A4" => "C3A4" alors qu'on veut des %C3%A4 => chr(C3)chr(A4)
#  filter = re.compile( "%([A-F][0-9A-F])" );
#  s = filter.sub(r'\1', s);

  filter = re.compile( r'%([A-F][0-9A-F])' );
  s = filter.sub(hexToChar, s);

  print( "transformWikiAccentToUtf8: apres: ", s );
  return s;
  # transformWikiAccentToUtf8


 # enleve les accents ascii en accent utf-8: %C3%A4 => 0xC30xA4
def removeWikiAccentToUtf8( s ):
  filter = re.compile( r'%([A-F][0-9A-F])' );
  s = filter.sub("", s);
  return s;

def removeHtmlCode( s ):
#  filter = re.compile( "<([a-z]|\s)* >|<\/.>" );
#  filter = re.compile( "<\/.>" );
#  filter = re.compile( "<[a-z]|\s)+>|<\/[a-z]>" );

#  filter = re.compile( "<[\w\s=\.?\/&;\"()-]+>"    "|</[\w]+>"  );   # ajouter "|<.+[é].+>" fais qu'on perd le contenu des balises
#  s = filter.split(s);
#  s = ''.join(s);

  bInTag = False;
  strOutput = "";
  nLen = len( s );
  for i in range( 0, nLen ):
    if( s[i]  == '<' ):
      if( bInTag ):
        print( "WRN: html opening tag in already opened tag (nested open)" );
      bInTag = True;
    else: # == '<'
      if( s[i]  == '>' ):
        if( not bInTag ):
          print( "WRN: html closing tag in not open tag" );
        bInTag = False;
      else: # == '>'
        if( not bInTag ):
          strOutput = strOutput + s[i];
  return strOutput;


# passe d'un code html au resultat visuel (pour le faire lire par exemple)
def transformHtmlToRawText( s ):
#  s = s.replace( "<p>", "" );
#  s = s.replace( "<b>", "" );

#  s = "<p><a > la soeur du p? est appell?a </a> </p><coucou> < A href=tutu?titi=roro&=toto%C3%A4.html> tata </A> ";
#  s = s + "<a href=\"/wiki/Nao(robotique)\" title=\"Nao(robotique) ??ique\" class=\"mw-redirect\">";
#  s = s + " de J?me";

#  s = s.encode("utf-8");

  s = removeWikiAccentToUtf8( s );

#  s = transformWikiAccentToUtf8( s );
  s = transformAsciiAccentToUtf8( s );
#  s = s.encode("utf-8"); # marche pas quand deja de l'utf-8 et ne marche pas si ca contient de l'hexa...

  s = s.replace( "#", "" );  # car  je n'arrive pas a matcher ce charactere dans les tags regexp
  s = s.replace( "*", "" );  # car  je n'arrive pas a matcher ce charactere dans les tags regexp

  # regexp pour virer l'html
  s = removeHtmlCode( s );

#  s = transformAccentForSynthesis( s );

  return s;

# find an obj in a list, return the index in the list or -1 if not found
def find( list, obj ):
  try:
    nIdx = list.index( obj );
    debug( "find(%s,%s): found: idx: %d" % ( str(list), str(obj), nIdx ) );
    return nIdx;
  except ValueError, err:
    debug( "find(%s,%s): not found" % ( str(list),str(obj) ) );
    return -1;
# find - end

def listToRad( aList ):
  "convert a list in degrees to a list in radians"
  for val in aList:
    val = val * math.pi / 180.0;
# listToRad - end


def getFilenameFromTime():
  "get a string usable as a filename relative to the current datetime stamp"
  strTimeStamp = str( datetime.datetime.now() );
  strTimeStamp = strTimeStamp.replace( " ", "_" );
  strTimeStamp = strTimeStamp.replace( ".", "_" );
  strTimeStamp = strTimeStamp.replace( ":", "m" );  
  debug( "getFilenameFromTime: generated this string: '" + strTimeStamp + "'" );
  return strTimeStamp;
# getFilenameFromTime - end

def getHumanTimeStamp():
  "get a printable timestamp than a user (even french) could understand"
  strNow = str( datetime.datetime.now() );
  strTimeStamp = strNow[0:len(strNow)-3]; # enleve les micro secondes!
  return strTimeStamp;
# getHumanTimeStamp - end

def getDateToSay():
  "get a date and time that we could send to the tts"
  strNow = str( datetime.datetime.now().strftime("%d %B %Y, %H heure ") );
  nNbrMin = int( str( datetime.datetime.now().strftime("%M") ) );
  if( nNbrMin == 0 ):
      strNow += "pile";
  else:
      strNow += str( nNbrMin );
  return strNow;
# getDateToSay - end

def executeAndGrabOutput( strCommand, bLimitToFirstLine = False ):
  "execute a command in system shell and return grabbed output"
  strTimeStamp = getFilenameFromTime();
  strOutputFilename = getVolatilePath() + "grab_output_" + strTimeStamp+ ".tmp"; # generate a different file each call for multithreading capabilities
  mySystemCall( strCommand + " > " + strOutputFilename );
  if( bLimitToFirstLine ):
    strBufferRead = getFileFirstLine( strOutputFilename );
  else:
    strBufferRead = getFileContents( strOutputFilename );
  try:
    os.unlink( strOutputFilename );
  except BaseException, err:
    print( "ERR: executeAndGrabOutput: err(): " + str( err ) );
    pass
  debug( "executeAndGrabOutput: '%s'" % strBufferRead );
  return strBufferRead;
# executeAndGrabOutput - end

# Create a string from an array, inserting separator between each element
# It's the the reverted operation of string.split...
def join( anArray, strSeparator ):
  if( len( anArray ) < 1 ):
    return "";
  s = str( anArray[0] );
  for elem in anArray[1:]:
    s += strSeparator + str( elem );
  return s;
# join - end

# compare two array/lists, return the index corresponding to the first different value or -1 if no difference between the two array
# it's useful to see while two array are different (when == doesn't output True, and user are sure they are (but not in fact, ahaha)
def compareData( d1, d2 ):
  print( "compareData: in" );
  nLenD1 = len( d1 );
  nLenD2 = len( d2 );

  print( "compareData: p2" );

  if( nLenD1 != nLenD2 ):
    print( "compData: diff size: %d != %d" % ( nLenD1, nLenD2 ) );
    return 421;

  print( "compareData: p3" );

  for nIdx in range( 0, nLenD1 ):
    if( not d1[nIdx] == d2[nIdx] ):
      print( "compareData: out: difference at offset %d" % nIdx );
      return nIdx;

  print( "compareData: out: equal" );
  return -1;
# compareData - end

def compareVectors( a1, a2, rThreshold = 0.0001 ):
    "Compare two vectors"
    "return -1 if equal or the idx of the difference"
    "return -2 if the two vectors have different size"
    if( len( a1 ) != len( a2 ) ):
        return -2;
    for i in range( len( a1 ) ):
        rDiff = a1[i] - a2[i];
        if( rDiff > rThreshold or rDiff < -rThreshold ):
            print( "compareVectors: i:%d rDiff: %f" % ( i, rDiff ) );
            return i;
    return -1;
# compareVectors - end

def getHtmlPage( strHtmlAdress, bWaitAnswer = True, rTimeOutForAnswerInSec = 30.0 ):
    "return a web page, or "" on error (async or sync method, with optionnal timeout)"
    # this method is ok but doesn't work on adress that doesn't finished with an extension (.ext)
#  req = urllib2.Request( strHtmlAdress );
#  print req.get_full_url();
# handle = urllib2.urlopen( req );
#  res = handle.read();
#  return res;

    # use cpp !
    try:
        usage = myGetProxy( 'UsageTools' );
        # separate hostname and directories
        strHost, strFolder, strPageName = getHostFolderAndFile( strHtmlAdress );
#        print( "altools.getHtmlPage: L'ADRESSE DU SITE: -%s-%s-%s-:" % (strHost, strFolder, strPageName) );
#        strHost = strHost[len('http://'):]; # remove http: older version doesn't like it !
        strPageContents = usage.getWebPage( strHost, strFolder + strPageName, rTimeOutForAnswerInSec );
        if( strPageContents != "error" or ( rTimeOutForAnswerInSec > 0. and rTimeOutForAnswerInSec < 10.0 ) ): # if we put a short timeout, that's possible to have an empty response!
            return strPageContents; # else, we will use the normal method
        else:
            print( "WRN: getHtmlPage: CPP method error: return empty, trying other method" );
    except BaseException, err:
        print( "WRN: getHtmlPage: CPP method error: %s" % str( err ) );
        pass # use oldies version

    print( "WRN: => using old one using fork and shell!" );

    # not very efficient: should store it in var/volatile (but less os independent)
    debug( "getHtmlPage( %s, bWaitAnswer = %d, rTimeOutForAnswerInSec = %d )" % ( strHtmlAdress, bWaitAnswer, rTimeOutForAnswerInSec ) );
    strRandomFilename = getVolatilePath() + "getHtmlPage_%s.html" % getFilenameFromTime();
    # sous windows wget peut geler, donc on va l'appeller avec un timeout (qui ne fonctionne pas, c'est drole...)
#    threadWGet = mySystemCall( "wget %s --output-document=%s --tries=16 --timeout=60 --cache=off -q" % ( strHtmlAdress, strRandomFilename ), False, True ); # commenter cette ligne pour avoir toujours le meme fichier
    # en fait plein d'options n'existe pas sur Nao, donc on ne laisse que celle ci:
    threadWGet = mySystemCall( "wget \"%s\" --output-document=%s -q" % ( strHtmlAdress, strRandomFilename ), bWaitEnd = False, bStoppable = True ); # commenter cette ligne pour avoir toujours le meme fichier
    if( not bWaitAnswer ):
        debug( "getHtmlPage( %s, %d ) - direct return" % ( strHtmlAdress, bWaitAnswer ) );
        return "";

    timeBegin = time.time();
    timeElapsed = 0.0;

    time.sleep( 1.0 ); # time for the process to be created !
    
    if( isinstance( threadWGet, int ) ):
        # on est ici dans un post d'un systemCall thréadé sur un UsageRemoteTools
        try:
            usage = myGetProxy( 'UsageRemoteTools', True );
            usage.wait( threadWGet, rTimeOutForAnswerInSec*1000 ); # On a très souvent cette erreur la: "'Function wait exists but parameters are wrong'" la tache est peut etre deja fini ?
        except BaseException, err:
            print( "WRN: getHtmlPage: wait for end failed, err: " + str( err ) );
        debug( "getHtmlPage: at the end: thread is finished (naoqi id: %d)" % threadWGet );
    else:
        while( 1 ):
            debug( "getHtmlPage: thread is finished: %d" % threadWGet.isFinished()  );
            if( threadWGet.isFinished() ):
                debug( "getHtmlPage: isFinished !!!" );
                break;

            timeElapsed = time.time() - timeBegin;
            if( timeElapsed > rTimeOutForAnswerInSec ):
                debug( "getHtmlPage: %f > %f => timeout" % (timeElapsed, rTimeOutForAnswerInSec) );
                threadWGet.stop();
                break;
            time.sleep( 0.2 );
        # while - end
        debug( "getHtmlPage: at the end: thread is finished: %d" % threadWGet.isFinished()  );

#  bOnWindows = ( os.name != 'posix' );
#  if( bOnWindows ):
#      time.sleep( 8.0 ); # temps de l'appel car sur certaines plateformes (windows) le os.waitpid semble ne pas bien fonctionner ou alors c'est le wget...

    strBuf = "";

    file = False;
    try:
        file = open( strRandomFilename, 'r' );
        strBuf = file.read();
    except BaseException, err:
        print( "getHtmlPage: WRN: file '%s' is empty or not finished to be aquire... (timeElapsed: %f) err: %s" % ( strRandomFilename, timeElapsed, str( err ) ) );
    finally:
        if( file ):
            file.close();
        
    try:
        if( file ):
            os.unlink( strRandomFilename );
    except BaseException, err:
        print( "getHtmlPage: WRN: unlink of file '%s' failed... (err:%s)" % ( strRandomFilename, str( err ) ) );

#    debug( "getHtmlPage( %s, %d ) - return '%s'" % ( strHtmlAdress, bWaitAnswer, strBuf ) );
    debug( "getHtmlPage( %s, %d ) - return a page of length: '%d'" % ( strHtmlAdress, bWaitAnswer, len( strBuf ) ) );
    return strBuf;
# getHtmlPage - end

def getStandardHtmlHeader( strTitle ):
  "return the begin of a web page, until the begin of the body"
  strBuffer = "";
  strBuffer += "<html>";
  strBuffer += "  <head>";
  strBuffer += "   <title> %s </title>" % strTitle;
  strBuffer += "  </head>";
  strBuffer += "  <body>";
  return strBuffer;
# getStandardHtmlHeader - end

def randomizeList( aList ):
    "randomize/unsort the order of element in a list"
    nNumInList = len( aList );
    if( nNumInList < 2 ):
        return aList;

    # statistically if we exchange n/2 times two element of the list, it would be totally randomly sorted
    for i in xrange( nNumInList / 2 + 2 ):
        nFirst = random.randint( 0, nNumInList - 1 );
        nSecond = random.randint( 0, nNumInList - 1 );
        if( nFirst != nSecond ):
            print( "exchange %d and %d" % (nFirst,nSecond) );
            val = aList[nFirst];
            aList[nFirst] = aList[nSecond];
            aList[nSecond] = val;
        # if - end
    # for - end
    return aList;
# randomizeList - end

def filterList( aList, listWordPart ):
    "return a part of a list with only element containing an element in listWordPart"
    listOut = [];
    for word in aList:
        for wordToFind in listWordPart:
            if( wordToFind in word ): # comparison case sensitive on a part of the world
                listOut.append( word );
    # for - end
    return listOut;
# filterList - end

def substractList( aList, anotherList ):
    "remove all element in a list that are in another list"
    listOut = [];
    for word in aList:
            if( word not in anotherList ): # comparison on the exact part of an element of the list
                listOut.append( word );
    # for - end
    return listOut;
# substractList - end


import subprocess


class ASyncSystemCallThread( threading.Thread ):
    def __init__(self, strCommandAndArgs, bStoppable = False ):
        threading.Thread.__init__( self );
        self.strCommandAndArgs = strCommandAndArgs;
        self.newProcess = False;
        self.bStoppable = bStoppable;
    # init - end

    def run( self ):
        debug( "altools: asyncSystemCallThread calling '%s'" % self.strCommandAndArgs );
        # mySystemCall( self.strCommandAndArgs );
        if( self.bStoppable and isOnWin32() ):
            self.newProcess = subprocess.Popen( self.strCommandAndArgs );  # sous windows, il ne faut oas mettre shell a true si on veut pouvoir arreter une tache (genre lancer choregraphe)
        else:
            self.newProcess = subprocess.Popen( self.strCommandAndArgs, shell=True ); # , stdin=subprocess.PIPE
        try:
            sts = os.waitpid( self.newProcess.pid, 0 );
        except BaseException, err:
            print( "ERR: ASyncSystemCallThread.run: pid already finished or some erros occurs or under windows ? (err:%s)" % ( str( err ) ) );
            pass # pid already finished or some erros occurs or under windows ?
        debug( "altools: asyncSystemCallThread calling '%s' - end" % self.strCommandAndArgs );
    # run - end

    def stop( self, rTimeOut = 2.0 ):
        "stop the process"
        "return -1 if it hasn't been really stopped"
        if( self.newProcess == False ):
            return -1; # the process hasn't been launch yet !

        if( not self.isFinished() ):
        #~ if(   os.name != 'posix' ):
            #~ # Kill the process using pywin32
            #~ import win32api # install from pywin32-214.win32-py2.6.exe
            #~ print dump( win32api );
            #~ win32api.TerminateProcess( int( self.newProcess._handle ), -1)
            #~ win32api.CloseHandle(self.newProcess._handle);
            #~ import ctypes
            #~ ctypes.windll.kernel32.TerminateProcess(int(self.newProcess._handle), -1)
        #~ else:
            try:
                self.newProcess.terminate(); # warning: require python2.6 or higher # fonctionne mais shell doit etre a true dans le Popen
            except BaseException, err:
                print( "WRN: ASyncSystemCallThread.stop: terminate failed (err:%s)" % ( str( err ) ) );
        self.join( rTimeOut ); #wait with a timeout of n sec
        if( not self.isFinished() ):
            time.sleep( rTimeOut / 4.0 ); # time for things to be resfreshed (join/poll or ...) (longer)
        if( not self.isFinished() ):
            return -1;
        return self.newProcess.returncode;
    # stop - end

    def isFinished( self ):
        "is the process finished ?"
        time.sleep( 0.05 ); # time for things to be resfreshed (join/poll or ...)
#       return self.isAlive();
        if( self.newProcess == False ):
            return False; # the process hasn't been launch yet !
        self.newProcess.poll();
        return ( self.newProcess.returncode != None );
    # isFinished - end

# ASyncSystemCallThread - end

def asyncSystemCall( strCommandAndArgs, bStoppable = False ):
  "launch a system call, without waiting the end of the system call"
  "return the thread object"
  async = ASyncSystemCallThread( strCommandAndArgs, bStoppable );
  async.start();
  return async;
# asyncSystemCall - end


def mySystemCall( strCommandAndArgs, bWaitEnd = True, bStoppable = False ):
    "make a system call, and choose to wait till the end or to thread"
    "return the process status or an object of type ASyncSystemCallThread, if it's an asynccall"
    strTrace = "altools: mySystemCall( '%s', bWaitEnd=%d, bStoppable=%d)" % ( strCommandAndArgs, bWaitEnd, bStoppable );
    debug( strTrace );
    logToFile( strTrace, strSpecificFileName = "mySystemCall" );
    obj = False;
    if( naoconfig.bTryToReplacePopenByRemoteShellCall ):
        try:
            ur = myGetProxy( "UsageRemoteTools", True );
            id = None;
            if( bWaitEnd ):
                ur.systemCall( strCommandAndArgs );
            else:
                id = ur.post.systemCall( strCommandAndArgs );
            debug( "altools: mySystemCall( '%s', bWaitEnd=%d ) - remote call - end - returning id: %s" % ( strCommandAndArgs, bWaitEnd, str( id ) ) );
            logToFile( "(remoted)(end)", strSpecificFileName = "mySystemCall" );
            return id;
        except BaseException, err:
            print( "WRN: mySystemCall: UsageRemoteTools error, doing a standard call - err: %s" %  err );
            pass # in case of bug, we will use normal call (next lines)
    
    # else cas normal
    if( bWaitEnd ):
        newProcess = subprocess.Popen( strCommandAndArgs, shell=True ); # not blocking !
        try:
            sts = os.waitpid( newProcess.pid, 0 );
            obj = sts[1]; # waitpid return (pid, exitstatus)
        except BaseException, err:
            print( "WRN: mySystemCall: pid already finished or some erros occurs or under windows ? (err:%s)" % ( str( err ) ) );
            pass # pid already finished or some erros occurs or under windows ?
    else:
        obj = asyncSystemCall( strCommandAndArgs, bStoppable );
    debug( "altools: mySystemCall( '%s', bWaitEnd=%d) - end" % (strCommandAndArgs, bWaitEnd ) );
    return obj;
# mySystemCall - end


class ASyncEvalThread( threading.Thread ):
    def __init__(self, strPythonCode, globaldico = None, localdico = None, bStoppable = False ):
        threading.Thread.__init__( self );
        self.strPythonCode = str( strPythonCode );
        self.globaldico = globaldico;
        self.localdico = localdico;
        self.bStoppable = bStoppable;
        self.bMustStop = False;
    # init - end

    def run( self ):
        debug( "altools: ASyncEvalThread evaluating '%s'" % self.strPythonCode );
        self.bMustStop = False;
        sys.settrace( self.globaltrace ); # permit to kill thread, WRN: it's a debug purpose functionnality not existing or all platform and ...
        #~ self.strPythonCode = """
#~ import signal
#~ print( 'installing handler...' );
#~ def handler(signum, frame):
    #~ print 'Signal handler called with signal', signum;
    #~ exit( 42 );
#~ signal.signal(signal.SIGTERM, handler)
#~ """ + self.strPythonCode; => ERROR signal only works in main thread
        if( naoconfig.bDebugMode ):
            logToChoregraphe( "self.strPythonCode: '%s'" % self.strPythonCode );
        exec( self.strPythonCode, self.globaldico, self.localdico ); # TODO: here: do something to test bMustStop is not Set to True, if so exit
        debug( "altools: ASyncEvalThread evaluating '%s' - end" % ( self.strPythonCode ));
    # run - end

    def stop( self, rTimeOut = 3.0 ):
        "stop the process"
        #   if( not self.isFinished() ): # doesnt return a correct value!
        debug( "ASyncEvalThread.stop(): stopping..." );
        self.bMustStop = True;
        return self.join( rTimeOut ); #wait with a timeout of n sec # attention au bout de n sec, il ne kill pas le join mais juste il rend la main...
    # stop - end

    def isFinished( self ):
        "is the process finished ?"
        bAlive = self.isAlive();
        debug( "ASyncEvalThread.isFinished() => %s" % str( bAlive ) );
        return bAlive;
    # isFinished - end

    def globaltrace(self, frame, why, arg):
#        logToChoregraphe( "globaltrace( frame='%s', why='%s', arg='%s' )" % (frame, why, arg) );
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
#        logToChoregraphe( "localtrace( frame='%s', why='%s', arg='%s' )" % (frame, why, arg) );
        if self.bMustStop:
            if why == 'line':
                raise sys.exit( -9 );
        return self.localtrace;

# ASyncEvalThread - end

def asyncEval( strPythonCode, globaldico =globals(), localdico = locals() ):
  "launch an evaluation in another python thread, a tricky specific manner"
  evaluationThreadObj = ASyncEvalThread( strPythonCode, globaldico, localdico );
  evaluationThreadObj.start();
  return evaluationThreadObj;
# asyncEval

global_dictCacheObj = dict();
def getInCache( strName, typeType ):
  "get an objet from a list of cached object, return None if object not in cache"
#  debug( "altools.getInCache( %s )" % strName );
  if( isString( typeType ) ):
    strGeneratedName = strName + str( type( typeType ) );
  else:
    strGeneratedName = strName + str( typeType ); # => return the type
#  print( "altools.getInCache: strGeneratedName: '%s'" % strGeneratedName );
  global global_dictCacheObj;
  if( strGeneratedName in global_dictCacheObj ):
#    debug( "altools.getInCache: obj %s as %s caching success" % ( strName , strGeneratedName ) );
    return global_dictCacheObj[strGeneratedName];
#  debug( "altools.getInCache: obj %s as %s not in cache" % ( strName , strGeneratedName ) );
  return None;
# getInCache - end

def storeInCache( strName, obj ):
  "store an objet in a list of cached object"
  strGeneratedName = strName + str( type( obj ) );
#  print( "altools.storeInCache: strGeneratedName: '%s'" % strGeneratedName );
  global global_dictCacheObj;
  global_dictCacheObj[strGeneratedName] = obj;
#  debug( "altools.storeInCache: storing %s as %s" % ( strName , strGeneratedName ) );
# storeInCache - end

def removeFromCache( strName, typeType ):
    "remove an object from the cache, return False if the object isn't present in the cache"
    if( isString( typeType ) ):
        strGeneratedName = strName + str( type( typeType ) );
    else:
        strGeneratedName = strName + str( typeType ); # => return the type    
#    print( "altools.removeFromCache: strGeneratedName: '%s'" % strGeneratedName );        
    global global_dictCacheObj;
    try:
        del global_dictCacheObj[strGeneratedName];
        return True;
    except BaseException, err:
        print( "WRN: removeFromCache: removing failed??? (err:%s)" % ( str( err ) ) );
        pass
    return False;
# removeFromCache - end

def printCache():
    "print the cache contents"
    global global_dictCacheObj;
    print( "*** Cache contents ***" );
    print dictionnaryToString( global_dictCacheObj );
    print( "*** Cache contents - end ***" );
# removeFromCache - end

def dictionnaryToString( aDico ):
  "return a beautiful and sorted string describing a dictionnaries for debugging or printing..."
  s = "# dictionnary has %d element(s):\n" % ( len( aDico ) );
  for k, v in sorted( aDico.iteritems() ):
    s += "    '%s': %s,\n" % ( str(k), str(v) );
  return s;
# dictionnaryToString - end

def constructFromNamedArray(obj, aNamedArray ):
    "construct a python object from an array of couple [attr_name,attr_value]"
    for attr_name, attr_value in aNamedArray:
        try:
            attr = getattr( obj, attr_name );
            if( attr != None ):
                # eval( "obj." + attr_name + " = '" + attr_value + "'" );
                setattr( obj, attr_name, attr_value );
        except BaseException, err:
            print( "WRN: constructFromNamedArray: ??? (err:%s)" % ( str( err ) ) );
            pass
  # for
#   print( dump( obj ) );
    return obj;
# constructFromNamedArray - end


def loadSound16( strFileIn, nNbrChannel = 1 ):
    "load a sound file and return an array of samples (16 bits) (in mono)"
    "return [] on error"
    aSamplesMono = [];    
    try:
        file = open( strFileIn, "rb" );
    except BaseException, err:
        print( "altools::loadSound16: ERR: something wrong occurs: %s" % str( err ) );
        return [];
    try:
        aBuf = file.read();  
        file.close();
        nOffset = 0;
        lenFile = len( aBuf );
        strHeaderTag = struct.unpack_from( "4s", aBuf, 0 )[0];
        if( strHeaderTag == "RIFF" ):
            print( "altools::loadSound16: skipping wav header found in %s" % strFileIn );
            nOffset += 44; # c'est en fait un wav, on saute l'entete (bourrin)
        
        print( "altools::loadSound16: reading file '%s' of size %d interpreted as %d channel(s)" % ( strFileIn, lenFile, nNbrChannel ) );
        while( nOffset < lenFile ):
            nValSample = struct.unpack_from( "h", aBuf, nOffset )[0];
            aSamplesMono.append( nValSample ); # ici c'est lourd car on alloue un par un (pas de reserve) (des essais en initialisant le tableau  avec des [0]*n, font gagner un petit peu (5.0 sec au lieu de 5.4)
            nOffset += 2;
            if( nNbrChannel > 1 ):
                nOffset += 2; # skip right channel
        # while - end
    except BaseException, err:
        print( "altools::loadSound16: ERR: something wrong occurs: %s" % str( err ) );
        pass
        
    print( "=> %d samples" %  len( aSamplesMono ) );    
    return aSamplesMono;
# loadSound16 - end


def removeBlankFromFile( strFilename, b16Bits = True, bStereo = False ):
  "remove blank at begin and end of a raw sound file, a blank is a 0 byte."
  "bStereo: if set, it remove only by packet of 4 bytes (usefull for raw in stereo 16 bits recording)"
  try:
    file = open( strFilename, "rb" );
  except BaseException, err:
    print( "WRN: removeBlankFromFile: ??? (err:%s)" % ( str( err ) ) );

    return False;
    
  try:
    aBuf = file.read();
  finally:
    file.close();
    
  try:  
    nNumTrimAtBegin = 0;
    nNumTrimAtEnd = 0;
    nFileSize = len( aBuf );
    for i in range( nFileSize ):
  #    print( "aBuf[%d]: %d" % (i, ord( aBuf[i] )  ) );
      if( ord( aBuf[i] ) != 0 ):
  #      print( "i1:%d" % i );
        if( bStereo and b16Bits ):
          i = (i/4)*4; # don't cut between channels
        elif( bStereo or b16Bits ):
          i = (i/2)*2;
        break;
    nNumTrimAtBegin = i;

    for i in range( nFileSize - 1, 0, -1 ):
  #    print( "aBuf[%d]: %d" % (i, ord( aBuf[i] )  ) );
      if( ord( aBuf[i] ) != 0 ):
  #      print( "i2:%d" % i );
        if( bStereo ):
          i = ((i/4)*4)+4;
        elif( bStereo or b16Bits ):
          i = ((i/2)*2)+2;
        break;
    nNumTrimAtEnd = i;

  #  debug( "altools::removeBlankFromFile: nNumTrimAtBegin: %d, nNumTrimAtEnd: %d, nFileSize: %d" % (nNumTrimAtBegin, nNumTrimAtEnd, nFileSize ) );
    if( nNumTrimAtBegin > 0 or nNumTrimAtEnd < nFileSize - 1 ):
        print( "altools::removeBlankFromFile: trim at begin: %d; pos trim at end: %d (data trimmed:%d)" % ( nNumTrimAtBegin, nNumTrimAtEnd, nNumTrimAtBegin + ( nFileSize - nNumTrimAtEnd ) ) );
        aBuf = aBuf[nNumTrimAtBegin:nNumTrimAtEnd];
        try:
            file = open( strFilename, "wb" );
        except BaseException, err:
            print( "WRN: altools::removeBlankFromFile: dest file open error (2) (err:%s)" % ( str( err ) ) );
            return False;
        try:
            file.write( aBuf );
        finally:            
            file.close();
  except BaseException, err:
    print( "altools::removeBlankFromFile: ERR: something wrong occurs (file not found or ...) err: " + str( err ) );
    return False;
  return True;
# removeBlankFromFile - end

def convertSoundRaw( strFilename, nFreqIn = 22500, nFreqOut = 48000, nNbrChannelOut = 2 ):
  "resample a 16 bits sound in two channels (default: from speech synthesis) to a 4 channels (default: to send to the speech analysis)"
  " if nNbrChannelOut in_channel 0 => out_channel_0 and 2; in_channel 1 => out_channel_1 and 3"
  try:
    nNbrChannelIn = 2;
    nNbrBytesPerSamples = 2;
    nStereo = 2;
    file = open( strFilename, "rb" );
    aBuf = file.read();
    file.close();
    aBufOut = "";
    nInputFileSize = len( aBuf );
    nNbrSampleIn= nInputFileSize / ( nStereo * nNbrBytesPerSamples ); # 2: stereo and 2: 16 bits
    nNbrSampleOut = nNbrSampleIn * nFreqOut / ( nFreqIn  ); # 2: stereo and 2: 16 bits
    nNbrSampleOut -= 1; # we remove this one, because we can't interpolate the last sample !
    nTimeMicroSec = 0;
    rIncInEachOut = nFreqIn / float( nFreqOut ); # increment of sample in input when advancing one sample in output
    rPosIn = 0.0;
    print( "convertSoundRaw: nInputFileSize: %d, nNbrSampleIn: %d, nNbrSampleOut: %d" % ( nInputFileSize, nNbrSampleIn, nNbrSampleOut ) );
    for nNumSampleOut in xrange( nNbrSampleOut ):
#      print( "nNumSampleOut: %d" % nNumSampleOut );
      nPosIn = int( rPosIn ); # num of sample
      rInter = rPosIn - nPosIn; # ratio for interpolation
      for nNumChannel in xrange( nStereo ):
        nOffset = ( nPosIn * nStereo * nNbrBytesPerSamples ) + ( nNumChannel * nNbrBytesPerSamples );
#        debug( "nOffset: %d" % nOffset );
        # nValSampleFirst = ( ord( aBuf[nOffset] ) + ( ord( aBuf[nOffset+1]  ) << 8 ) ) - 0x8000; # this line is specific for a 16 bits encoding
        # nValSampleSecond = ( ord( aBuf[nOffset+nNumChannel*nStereo] ) + ord( aBuf[nOffset+nNumChannel*nStereo+1] ) << 8 ) - 0x8000; # this line is specific for a 16 bits encoding
        nValSampleFirst = struct.unpack_from( "h", aBuf, nOffset )[0]; # these lines are specific for a 16 bits encoding
        nValSampleSecond = struct.unpack_from( "h", aBuf, (nOffset+nNumChannel*nStereo) )[0];

        nValOutput = round( nValSampleFirst * ( 1 - rInter ) + nValSampleSecond * rInter );

#        print( "nValSampleFirst: %d, nValSampleSecond: %d, nValOutput: %d rInter: %f" % ( nValSampleFirst, nValSampleSecond, nValOutput, rInter ) );

#        aBufOut.append( nValOutput % 256 ); # these lines are specific for a 16 bits encoding
#        aBufOut.append( nValOutput / 256 );
        strSample = struct.pack( "h", nValOutput ); # these lines are specific for a 16 bits encoding
        if( nNbrChannelOut == 4 ):
          aBufOut += strSample+strSample; # 2 => 4 channels
        else:
          aBufOut += strSample; # 2 => 2 channels
      # for each input channels
      rPosIn += rIncInEachOut;
    # for each output sample
    file = open( strFilename, "wb" );
    file.write( aBufOut );
    file.close();
  except BaseException, err:
    print( "altools::convertSoundRaw: ERR: something wrong occurs: %s" % str( err ) );
# convertSoundRaw - end

def normaliseSound( strRawFileName, rPeakRatio = 1.0 ):
    "Analyse a raw 16 bits signed sound file, and change its volume to have peaks at 100%"
    "rPeakRatio: to specify another value for the final peak volume"
    "Return: False on write file error"
    nShortMaxValue = 32767;
    aSound = [];
    file = open( strRawFileName, "rb" );
    aBuf = file.read();
    file.close();
    nOffset = 0;
    lenFile = len( aBuf );
    print( "altools::normaliseSound: reading file of size %d" %  lenFile );
    nMax = 0;
    while( nOffset < lenFile ):
        nValSample = struct.unpack_from( "h", aBuf, nOffset )[0];
        aSound.append( nValSample ); # ici c'est lourd car on alloue un par un (pas de reserve) (des essais en initialisant le tableau  avec des [0]*n, font gagner un petit peu (5.0 sec au lieu de 5.4)
        nOffset += 2;
        # compute peak
        nValSample = abs( nValSample );
        if( nMax < nValSample ):
            nMax = nValSample;
     # while - end

    rRatio = nShortMaxValue*rPeakRatio/nMax;

    if( rRatio > 1.02 or rRatio < 0.98 ):
        # on modifie le fichier

        print( "altools::normaliseSound: applying ratio of %f" % rRatio );

        # convert
        aBufFileOut = "";
        for i in range( len( aSound ) ):
            nValSample = aSound[i];
            nValSample *= rRatio;
            if( nValSample > nShortMaxValue ):
                nValSample = nShortMaxValue;
            elif( nValSample < -nShortMaxValue ):
                nValSample = -nShortMaxValue;
            aBufFileOut += struct.pack( "h", nValSample );
         # while - end

        # write file
        try:
            file = open( strRawFileName, "wb" );
            file.write( aBufFileOut );
            file.close();
        except BaseException, err:
            print( "altools::normaliseSound: ERR: something wrong occurs (file '%s' not found or ...) (err: %s)" % ( strRawFileName, str( err ) ) );
            return False;
    # if - end
    return True;
# normaliseSound - end

def computeEnergyBest( aSample ):
	"Compute sound energy on a mono channel sample, aSample contents signed int from -32000 to 32000 (in fact any signed value)"

	# Energy(x_centered) = Energy(x) - Nsamples * (Mean(x))^2
	# Energy = Energy(x_centered)/ ( 65535.0f * sqrtf((float)nNbrSamples ) # en fait c'est mieux sans le sqrtf

	nEnergy = 0;
#	nMean = 0;
	nNumSample = len( aSample );

	for i in xrange( 1, nNumSample ):
#		nMean += aSample[i];
		nDiff = aSample[i] - aSample[i-1];
		nEnergy += nDiff*nDiff;

#	rMean = nMean / float( nNumSample );

#	print( "computeEnergyBest: nNumSample: %s, sum: %s, mean: %s, energy: %s" % ( str( nNumSample ),  str( nMean ), str( rMean ), str( nEnergy )) );
#	print( "computeEnergyBest: nNumSample: %d, sum: %d, mean: %f, energy: %d" % ( nNumSample,  nMean, rMean, nEnergy ) );
#	nEnergy -= int( rMean * rMean * nNumSample ); # on n'enleve pas la moyenne: ca n'a aucun interet (vu que c'est deja des diff)
	nEnergyFinal = int( float( nEnergy ) / nNumSample );
#	nEnergyFinal /= 32768;
	nEnergyFinal = int( math.sqrt( nEnergyFinal ) );
#	print( "computeEnergyBest: nEnergy: %f - nEnergyFinal: %s " % ( nEnergy,  str( nEnergyFinal ) ) );
	return nEnergyFinal;
# computeEnergyBest - end

def processSoundMumbled( strFileIn, strFileOut, nNbrChannelOut = 1 ):
    "Analyse a raw stereo sound file, and process it"
    "return true if all is ok"
    aMonoSound = loadSound16( strFileIn );
    if( len( aMonoSound ) < 1 ):
        return False;
    aMonoSoundBorbo = [0];
    nLenMonoSoundBorbo = -1;
    
    
    nNbrSample = len( aMonoSound );
    print( "processSoundMumbled: analysing %d sample(s)" % nNbrSample );
    nOffset = 0;
    aBufOut = "";
    nValOutputPrev = 0;
    rRatioNew = 0.001;
    rIncVolumeRange = 0.0001;
    rIncVolume = -rIncVolumeRange;
    rVolume = 1.;
    nLenRandomSound = 5000;
    nCptRandomSound = 0;
    nValOutputRandomSound = 0;
    rValOutputRandomSoundFreqDivider = 8.;
    nIdxBorbo = 0;
    nValOutputOther = 0;
    
    while( nOffset < nNbrSample ):
        nValOutput = aMonoSound[nOffset];        
        nValOutput = int( nValOutput * rRatioNew + nValOutputPrev * (1.-rRatioNew) );
        nValOutputPrev = nValOutput;
        nValOutput *=0.08/rRatioNew; # reamplify after dithering
        nValOutput = limitRange( nValOutput, SHRT_MIN, SHRT_MAX );
        if( random.random() > 0.9999 ):
            nCptRandomSound = nLenRandomSound;
            nValOutputRandomSound = nValOutput;
            rValOutputRandomSoundFreqDivider = 8. +random.randint( 0,4);
        if( nCptRandomSound > 0 ):
            nCptRandomSound -= 1;
#            nValOutput = nValOutputRandomSound;
#            nValOutput = math.sin(nOffset/rValOutputRandomSoundFreqDivider)*SHRT_MAX/10;
            nValOutputRandomSound *= 0.99; # fade out
            nLenFadeIn = 200;
            if( nCptRandomSound < 1000 ):
                # fade in
#                nValOutput = nValOutput * (1. - (nCptRandomSound/float( nLenFadeIn )));
                pass
#            nValOutput = limitRange( nValOutput, SHRT_MIN, SHRT_MAX );
            
        # nValOutput *= rVolume;
        
#        nValOutputOther = math.sin(nOffset/rValOutputRandomSoundFreqDivider)*SHRT_MAX/10;
        if( abs( nValOutput ) < 5000 or rVolume < 0.2 ):
            nValOutputOther = aMonoSoundBorbo[nIdxBorbo]*0.3;
            nIdxBorbo += 1;            
        else:
            pass
        nValOutput = nValOutput * rVolume + nValOutputOther * ( 1. - rVolume );
        if( nIdxBorbo >= nLenMonoSoundBorbo ):
            aMonoSoundBorbo = loadSound16( getApplicationSharedPath() + "wav/0_work_free/" + "borbo%d.wav" % random.randint( 1, 8 ) );
            nLenMonoSoundBorbo = len( aMonoSoundBorbo );
            nIdxBorbo = 0;            
            
        strSample = struct.pack( "h", nValOutput ); # these lines are specific for a 16 bits encoding
        if( nNbrChannelOut == 2 ):
          aBufOut += strSample+strSample; 
        else:
          aBufOut += strSample;
        nOffset += 1;
        rVolume += rIncVolume;
        if( rVolume < 0.1 ):
            rVolume = 0.1;
            rIncVolume = ( random.random()*rIncVolumeRange + 0.000001);
        elif( rVolume > 1. ):
            rVolume = 1.;
            rIncVolume = -( random.random()*rIncVolumeRange + 0.000001);
    # while - end
    
    # write file back
    try:
        file = open( strFileOut, "wb" );
        file.write( aBufOut );
        file.close();    
    except BaseException, err:
        print( "altools::processSoundMumbled: ERR: something wrong occurs: %s" % str( err ) );
        return False;
    # while - end
    
    print( "altools::processSoundMumbled: generated to file '%s'" % strFileOut );
    
    return True;
# processSoundMumbled - end

class NoDuplicate:
    "a class to prevent having duplicate object in a system: it stores name and later could tell if present/or not. All is thread safe."
    def __init__( self ):
        self.mutex = mutex.mutex();
        self.container = []; # in fact we won't write this class specifically for string...
    # __init__ - end

    def csIn( self, bMutexed = True ):
        if( bMutexed ):
            while( not self.mutex.testandset() ):
                time.sleep( 0.05 );
                debug( "NoDuplicate: csIn - wait" );
    # csIn - end

    def csOut( self, bMutexed = True ):
        if( bMutexed ):
            self.mutex.unlock();
    # csOut - end

    def add( self, newElement ):
        self.csIn();
        if( self.isPresent( newElement, False ) ): # False because we are already in the CriticalSection
            self. csOut();
            return False;

        self.container.append( newElement );
        self. csOut();
        return True;
    # add - end

    def remove( self, someElement ):
        self.csIn();
        if( not self.isPresent( someElement, False ) ): # False because we are already in the CriticalSection
            debug( "ERR: NoDuplicate.remove: element '%s' not in list." % someElement );
            self. csOut();
            return False;
        idx = find( self.container, someElement );
        if( idx == -1 ):
            debug( "ERR: NoDuplicate.remove: element '%s' not in list (2)(weird here)" % someElement );
            self. csOut();
            return False;
        del self.container[idx];
        self. csOut();
        return True;
    # remove - end

    def isPresent( self, elemToFind, bMutexed = True ):
        self.csIn( bMutexed );
        for elem in self.container:
            if( elem == elemToFind ):
                self.csOut( bMutexed );
                return True;
        self.csOut( bMutexed );
        return False;
    # isPresent - end

    def getList( self, bMutexed = True ):
        self.csIn( bMutexed );
        containerCopy = self.container;
        self.csOut( bMutexed );
        return containerCopy;
    # getList - self
# class NoDuplicate - end

# fonction de transition d'une couleur a l'autre
def interpolateColor( nColorFrom, nColorTo, rRatio ):
    "interpolate a rgb color from nColorFrom to nColorTo"
    "if rRatio tend to 0.0 if will be a color equals to nColorFrom, if it tends to 1.0 it will be nColorTo"
    rFromB,  rFromG, rFromR = colorHexaToComp( nColorFrom );
    rToB,  rToG, rToR = colorHexaToComp( nColorTo );
    rInvRatio = 1. - rRatio;
#    debug( "rRatio: %f, rinv: %f, rFromB: %f, rToB: %f" % (rRatio,rInvRatio, rFromB, rToB) );
    rToB = rFromB * rInvRatio + rToB * rRatio;
    rToG = rFromG * rInvRatio + rToG * rRatio;
    rToR = rFromR * rInvRatio + rToR * rRatio;

    return colorCompToHexa( rToR, rToG, rToB );
# interpolateColor - end

def interpolateColor3( nColorFrom, nColorMedian, nColorTo, rRatio ):
    "interpolateColor3: interpolate a rgb color from nColorFrom to nColorTo (passing by nColorMedian at ratio of 0.5)"
    if( rRatio < 0.5 ):
        nColor = interpolateColor( nColorFrom, nColorMedian, rRatio * 2. );
    else:
        nColor = interpolateColor( nColorMedian, nColorTo, ( rRatio - 0.5 ) * 2. );        
    return nColor;
# interpolateColor3 - end

def getListColorEmotion():
    "return a list of 6 eyes leds configurations" 
    import list_emotion_eyes;
    listEmo = [];
    listEmo.extend( list_emotion_eyes.listEmotionEyes ); # listEmo = list_emotion_eyes.listEmotionEyes ne ferait qu'un pointeur sur l'objet, et donc quand on append la neutralpose, ca ajoute a la liste du module, beurk.
    
    # the file can contains one light (the eyes has a plain color) or 8 lights
    # so we expand it:
    print( "listEmo: %d" % len( listEmo ) );
    for i in range( len( listEmo ) ):
        if( len( listEmo[i] ) == 1 ):
            listEmo[i] = arrayCreate( 8, listEmo[i][0] );
    print( "listEmo: %d" % len( listEmo ) );
    return listEmo;
# getListColorEmotion - end


def interpolateColorEmotion( arListRatio, rNeutral = 0. ):
    "create a position intermediary mixed from 6 emotions and a neutral"
    "arListRatio: the ratio of each emotions: [Proud, Happy, Excitement, Fear, Sadness, Anger]"
    "             if sum is greater than 1, it would be normalised"
    "             if sum is lower than 1, a neutral position would be added"
    "rNeutral:    to force an addition of a proportion of the neutral pose"
    
    debug( "interpolateColorEmotion( %s, %f )" % ( str( arListRatio ), rNeutral ) );
    
    # preparation of the ratio
    rSum = arraySum( arListRatio );
    rEpsilon = 0.001;
    
    if( rNeutral < rEpsilon and rSum < 1. ):
        rNeutral = 1. - rSum;
    rSumTotal = rSum + rNeutral;
    
    if( rSumTotal > 1. ):
        # normalisation
        for i in range( len( arListRatio ) ):
            arListRatio[i] /= rSumTotal;
        rNeutral /= rSumTotal;

    # push zeroes for others emotions:
    for i in range( len( arListRatio ), 6 ):
        arListRatio.append( 0. );
        
    anColorNeutral = arrayCreate( 8, 0x0000FF );

    listColorEmotion = getListColorEmotion();

    if( rNeutral > 0.001 ):
        listColorEmotion.append( anColorNeutral );
        arListRatio.append( rNeutral );

    

    anColor = arrayCreate( 8, [0.,0.,0.] );

    #~ print( "arListRatio: %s" % str( arListRatio ) );
    #~ print( "listColorEmotion: %s" % str( listColorEmotion ) );
    #~ print( "anColorNeutral: %s" % str( anColorNeutral ) );    
    #~ print( "anColor: %s" % str( anColor ) );
    
    # hexa to comp rgb
    arListColorEmotionRGB = [];
    for nNumEmotion in range( len( listColorEmotion ) ):
        arListColorEmotionRGB.append( [] );
        for led in listColorEmotion[nNumEmotion]:
            arListColorEmotionRGB[nNumEmotion].append( colorHexaToComp( led ) );
    
    # interpolation stuff    
    for nNumEmotion in range( len( arListColorEmotionRGB ) ):
        for nNumLed in range( len( anColor ) ):
            for nNumComposanteRGB in range( 3 ):
                anColor[nNumLed][nNumComposanteRGB] += arListRatio[nNumEmotion] * arListColorEmotionRGB[nNumEmotion][nNumLed][nNumComposanteRGB];

    print( "anColor2: %s" % str( anColor ) );
    
    # median and rgb to hexa
    for nNumLed in range( len( anColor ) ):
        # we haven't to divide in rgb space !
        #~ for nNumComposanteRGB in range( 3 ):
            #~ anColor[nNumLed][nNumComposanteRGB] = anColor[nNumLed][nNumComposanteRGB]  / len( arListColorEmotionRGB );
        anColor[nNumLed] = colorCompToHexa( anColor[nNumLed][2], anColor[nNumLed][1], anColor[nNumLed][0] );
        
    return anColor;
# interpolateColorEmotion - end

def setColorToEyes( anList8Color, rTime = 1.,  nEyesMask = 0x3 ):
    "set a list of 8 color to eyes"
    "rTime: time in sec of the fade"
    "nEyesMask: 1: left, 2: right, 3: both"
    print( "anList8Color: %s" % str( anList8Color ) );
    leds = myGetProxy( 'ALLeds' );
    for nNumSide in range( 2 ):
        nSideValMask = 1 << nNumSide;
        if( True ): # nEyesMask & nSideValMask ): TODO: bien gerer le mask
            for nNumLed in range( len( anList8Color ) ):
                strName = "FaceLed%s%d" % ( getSide(nNumSide), nNumLed );
                nColor = anList8Color[nNumLed];
                # no need of a mirror: already handled in ALLeds !
                # nIndexMirror = 7 - nNumLed;
#                print( "strName: %s, color: %x, time: %f" % ( strName, nColor, rTime ) );
                leds.post.fadeRGB( strName, nColor, rTime );
        # if - end
    # for - end
# setColorToEyes - end



def valueToPseudoColor( rValue, rMax ):
    "convert a value [0,nMax] to a pseudo color green/yellow/red"
    return interpolateColor3( 0x00FF00, 0xFFFF00, 0xFF0000, float( rValue ) / rMax );
# valueToPseudoColor - end

def valueToPseudoColor255( rValue, rMax ):
    "convert a value [0,nMax] to a pseudo color green/yellow/red (returned value are compostante [0..255]"
    "cpu optimised version"
    rRatio = float( rValue ) / rMax;
    if( rRatio < 0.5 ):
        rRatio *= 2;
        r1 = 0;
        g1 = 255;
        b1 = 0;
        r2 = 255;
        g2 = 255;
        b2 = 0;
    else:
        rRatio = ( rRatio - 0.5 ) * 2        
        r1 = 255;
        g1 = 255;
        b1 = 0;
        r2 = 255;
        g2 = 0;
        b2 = 0;
        
    rInvRatio = 1. - rRatio;
    r2 = int( r1 * rInvRatio + r2 * rRatio );
    g2 = int( g1 * rInvRatio + g2 * rRatio );
    b2 = int( b1 * rInvRatio + b2 * rRatio );
    return [b2, g2, r2];
# valueToPseudoColor255 - end

#print( "value: " + str( valueToPseudoColor255( 10, 480 ) ) );



global_strAltools_LogToFile = None;
global_mutex_LogToFile = mutex.mutex();
global_timeLogToFile_lastLog = time.time();
def logToFile( strMessage, strSpecificFileName = "" ):
    "add a message to the current debug log file"
    global global_strAltools_LogToFile;
    global global_mutex_LogToFile;
    global global_timeLogToFile_lastLog;
    timeNow = time.time();
    rDurationSec = timeNow - global_timeLogToFile_lastLog;
    global_timeLogToFile_lastLog = timeNow;
    while( global_mutex_LogToFile.testandset() == False ):
        time.sleep( 0.02 );
    if( global_strAltools_LogToFile == None ):
        try:
            os.makedirs( getCachePath() );
        except:
            pass # often the cases!
        global_strAltools_LogToFile = getCachePath() + getFilenameFromTime() + ".log";
        print( "altools.logToFile: logging to '%s'" % global_strAltools_LogToFile );
        
    if( strSpecificFileName == '' ):
        strFileName = global_strAltools_LogToFile;
    else:
        strFileName = getCachePath() + strSpecificFileName + '_' + getNaoqiStartupTimeStamp() + ".log";
#    print( "logToFile: logging to %s" % strFileName );
    try:
        file = open( strFileName, "at" );
        file.write( "%s (%5.2fs): %s\n" % ( getHumanTimeStamp(), rDurationSec, strMessage ) );
    finally:
        if( file ):
            file.close();
    global_mutex_LogToFile.unlock();
# logToFile - end

def isConnectedToInternet():
    "return True if connected to internet"
    try:
        usage = myGetProxy( 'UsageTools' );
        return usage.tryConnectTo( 'google.com' );
    except BaseException, err:
        print( "WRN: isConnectedToInternet: CPP method error: %s" % str( err ) );
        pass # use oldies version
        
    print( "WRN: => using old one using fork and shell!" );
    strInternetCmd = "LANG=en_EN.UTF-8 ping aldebaran-robotics.com -c1 | grep ' 0%' | wc -l"
    return executeAndGrabOutput( strInternetCmd, True ) != "0";
# isConnectedToInternet - end

def isConnectedWithEthernet():
    "return True if connected using ethernet cable"
    return True; # TODO !!!
# isConnectedWithEthernet - end


#######################################
# Configuration: relative to Nao but not using NaoQi
# summary:
# - getNaoqiPath, getAppuPath, and other various path
# - isLangFrench and other various language
# - isOnNao: Are we on THE real Nao ?
# - isOnWin32: Are we on a ms windows system?
# - getNaoIP: get the nao ip address (eth>wifi)
# - getSystemMusicPlayerName: get the music player name on the current machine
# - isActiveXar: centralise the list of current xar launched by loadXar or similar box
# - getEarLedNameFromIndex: get leds ears device name from index (deprecated)
# - getEarLedName: get leds ears device name from index (deprecated)
# - getBrainLedName: get the name of the led device by it's number
# - setBrainLedsIntensity: light on/off all the brain leds
# - askWatchdogToRestartNaoqi: send a signal to the watchdog to restart naoqi
#
#
#######################################

def getNaoqiPath():
  s = os.environ.get("AL_DIR");
  if( s == None ):
      s = '';
#  print( "getNaoqiPath(): " + str( s ) );
  return s;
# getNaoqiPath - end

def getAppuPath():
  s = getNaoqiPath() + getDirectorySeparator() + ".." + getDirectorySeparator() + "appu" + getDirectorySeparator();
  #  print( "getAppuPath(): " + str( s ) );
  return s;
# getAppuPath - end

print( "*** altools: parsing configuration" );

#~ strNaoToolsPath = "/opt/naoqi/extern/python/aldebaran/";
#~ if( isFileExists( getAppuPath() + "naoconfig.py" ) or isFileExists( strNaoToolsPath + "naoconfig.py" ) ):
  #~ import naoconfig
  #~ reload( naoconfig ); # reload it at every init, so we can modify it externally
#~ else:
  #~ print( "*** file %s not found" % ( getAppuPath() + "naoconfig.py" ) );
  #~ print( "*** Creating naoconfig.py from naoconfig.py.sample" );
  #~ copyFile( getAppuPath() + "naoconfig.py.sample", getAppuPath() + "naoconfig.py" );
  #~ copyFile( strNaoToolsPath + "naoconfig.py.sample", strNaoToolsPath + "naoconfig.py" );
  #~ import naoconfig

import naoconfig

# backward compatibility patch:
try:
    if( naoconfig.LANG_KO ):
        pass # dumb!
except:
    naoconfig.LANG_KO = 7; # possible case

try:
    if( naoconfig.bRemoveDirectPlay):
        pass # dumb!
except: 
    naoconfig.bRemoveDirectPlay = False;  # possible case

try:
    if( naoconfig.bTryToReplacePopenByRemoteShellCall ):
        pass # dumb!
except:
    naoconfig.bTryToReplacePopenByRemoteShellCall = False;  # possible case

print( "bDebugMode: " + str( naoconfig.bDebugMode ) );
#print( "nNumLang: " + str( getDefaultSpeakLanguage() ) );
print( "nSpeakSpeed: " + str( naoconfig.nSpeakSpeed ) );
print( "nSpeakSpeedUI: " + str( naoconfig.nSpeakSpeedUI ) );
print( "bPrecomputeText: " + str( naoconfig.bPrecomputeText ) );
print( "bRemoveDirectPlay: " + str( naoconfig.bRemoveDirectPlay ) );



def getVolatilePath():
  "get the volatile path (or temp path if on a real limited computer)"
  if( isOnNao() ):
    return "/var/volatile/";
  if( os.name == 'posix' ):
    return getDirectorySeparator() + "tmp" + getDirectorySeparator(); # /tmp
  return "c:\\temp\\"; # TODO: ? trouver le dossier temp grace a la variable d'environnement
# getVolatilePath

def getMusicPath():
  "get the music path (or temp path if on a real limited computer"
  if( isOnNao() ):
    return "/media/userdata/";
  if( os.name == 'posix' ):
    return getDirectorySeparator() + "music" + getDirectorySeparator(); # /music
  return "C:" + getDirectorySeparator() + "music" + getDirectorySeparator(); # TODO: ?
# getMusicPath - end


#### new path for 1.4.x ####

def getUserName():
    "Retourne le nom de l'utilisateur courant"
    return ""; # TODO

def getBehaviorRoot():
    "return the roots of all our tree"
    if( isOnNao() ):
        return getDirectorySeparator() + "home" + getDirectorySeparator() + "nao" + getDirectorySeparator();
    if( os.name == 'posix' ):
        return "~" + getDirectorySeparator() + "nao" + getDirectorySeparator(); # TODO: ?
    else:
        return "C:" + getDirectorySeparator() + "temp" + getDirectorySeparator();

def getApplicationsPath():
    "return a specific path"
    return getBehaviorRoot() + "Applications" + getDirectorySeparator();

global_applicationsInfos = {}; # Global HashTable, with rootBoxId for key, and only [appName] for value FTM

def setApplicationInfos(applicationRootBoxId, applicationName = ""):
  "set infos about an application : root id, application name, and path such as /home/nao/Applications/MyApp"
  global_applicationsInfos[applicationRootBoxId] = [applicationName];

def deleteApplicationInfos(boxId):
  "destroy application infos, boxId could be any box of the application"
  for id in global_applicationsInfos.keys():
    if boxId.startswith(id):
      del global_applicationsInfos[id];

def getApplicationInfos(boxId):
  "return infos about an application, boxId could be any box of the application"
  for id in global_applicationsInfos.keys():
    if boxId.startswith(id):
      return global_applicationsInfos[id];
  return None;

def getApplicationName(boxId):
  "return the name of an application, boxId could be any box of the application"
  infos = getApplicationInfos(boxId);
  if infos:
    return infos[0];
  return None;

def getApplicationPath(boxId):
  "return the name of an application, boxId could be any box of the application"
  "if the path doesn't exists, we create it"
  name = getApplicationName(boxId);
  if not name:
    return None;
  appDir = getApplicationsPath() + name + getDirectorySeparator();
  if not os.path.isdir(appDir):
    os.makedirs(appDir);
  return appDir;


def getApplicationSharedPath():
    "return a specific path"
    return getApplicationsPath() + "shared" + getDirectorySeparator();

def getUsersPath():
    "return a specific path"
    return getBehaviorRoot() + "Users" + getDirectorySeparator();


def getCachePath():
    "return a specific path"
    return getUsersPath() + "All" + getDirectorySeparator() + "Caches" + getDirectorySeparator();
    
def getHomePath():
    "return the home of current user"
    if( isOnNao() ):
        return getDirectorySeparator() + "home" + getDirectorySeparator() + "nao" + getDirectorySeparator();
    if( os.name == 'posix' ):
        return ".~/";
    return "c:" + getDirectorySeparator();
# getHomePath  - end


# ALTools.getSystemLibraryPath TODO
# ALTools.getUserPreferencesPath TODO
# ALTools.getSystemPrefrencesPath TODO
# ALTools.getDownloadPath TODO
# ALTools.getSystemCachePath TODO
# ALTools.getDocumentPath TODO
# ALTools.getPublicFolderPath TODO
# ALTools.getUserFolderPath TODO
# ALTools.getUserCacheFolderPath TODO
# ALTools.getUserApplicationSupportPath TODO
# ALTools.getSystemApplicationSupportPath TODO


def getPref( strPrefName ):
    "find a preference value in the user pref, or if not found, in the common/systeme preference"
    return "";

#### new path for 1.4.x #### - end

def isLangFrench():
  return getSpeakLanguage() == naoconfig.LANG_FR;

def isLangEnglish():
  return getSpeakLanguage() == naoconfig.LANG_EN;

def isLangSpanish():
  return getSpeakLanguage() == naoconfig.LANG_SP;

def isLangItalian():
  return getSpeakLanguage() == naoconfig.LANG_IT;

def isLangGerman():
  return getSpeakLanguage() == naoconfig.LANG_GE;

def isLangChinese():
  return getSpeakLanguage() == naoconfig.LANG_CH;

def isLangPolish():
  return getSpeakLanguage() == naoconfig.LANG_PO;

def isLangKorean():
  return getSpeakLanguage() == naoconfig.LANG_KO;

def setLangFrench():
  setSpeakLanguage( naoconfig.LANG_FR );

def setLangEnglish():
  setSpeakLanguage( naoconfig.LANG_EN );

def setLangSpanish():
  setSpeakLanguage( naoconfig.LANG_SP );

def setLangItalian():
  setSpeakLanguage( naoconfig.LANG_IT );

def setLangGerman():
  setSpeakLanguage( naoconfig.LANG_GE );

def setLangChinese():
  setSpeakLanguage( naoconfig.LANG_CH );

def setLangPolish():
  setSpeakLanguage( naoconfig.LANG_PO );
  
def setLangKorean():
  setSpeakLanguage( naoconfig.LANG_KO );



def changeLang():
#  if( naoconfig.nNumLang == naoconfig.LANG_FR ):
#    naoconfig.nNumLang = naoconfig.LANG_EN;
#  else:
#    naoconfig.nNumLang = naoconfig.LANG_FR;
    print( "altools.changeLang: TODO reécrire sans utiliser nNumLang" ); # TODO
# changeLang - end


def isOnNao():
  "Are we on THE real Nao ?"
  szCpuInfo = "/proc/cpuinfo";
#  if not isFileExists( szCpuInfo ): # already done by the getFileContents
#    return False;
  szAllFile = getFileContents( szCpuInfo );
  if( szAllFile.find( "Geode" ) == -1 ):
    return False;
  return True;
# isOnNao - end

def isOnWin32():
  "Are we on a ms windows system?"
  return not isOnNao() and os.name != 'posix';
# isOnWin32 - end

def getNaoIP():
  "get the nao ip address (eth>wifi)"
  "return '' if no ip"
  if( not isOnNao() ):
    return "";

  try:    
        import socket # under windows, we doesn't have this module
        import fcntl
        import struct
  except BaseException, err:
        print( "WRN: getNaoIP: import error (1), err: %s" % str( err ) );
        return "";
  def get_ip_address( strInterfaceName ):
    "get the ip associated to a linux network interface"
    try:
      sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
#      print( "sock: '%s'" % str( sock ) );
#      print( "strInterfaceName: " + str( strInterfaceName ) );
      strInterfaceName = strInterfaceName[:15];
#      print( "strInterfaceName: " + str( strInterfaceName ) );
      packedInterfaceName = struct.pack( '256s', strInterfaceName );
#      print( "packedInterfaceName: " + str( packedInterfaceName ) );
      ret = fcntl.ioctl(
          sock.fileno(),
          0x8915,  # SIOCGIFADDR
          packedInterfaceName
      );
#      print( "ret: '%s'" % ret );
      ret = ret[20:24];
#      print( "ret: '%s'" % ret );
      return socket.inet_ntoa( ret );
    except BaseException, err:
        print( "WRN: getNaoIP.get_ip_address: socker error (2), err: %s" % str( err ) );
        return '';
  # get_ip_address - end

  debug( "getNaoIP: getting ethernet" );
  strIP = get_ip_address( 'eth0' );
  if( strIP != '' ):
    return strIP;
  debug( "getNaoIP: getting wifi" );
  return get_ip_address( 'wlan0' );
# getNaoIP - end

# print "getNaoIP(): '%s'" % str( getNaoIP() );

def getNaoIPs():
  "get the nao ips address: [eth,wifi]"
  if( not isOnNao() ):
    return [];

  try:    
      import socket # under windows, we doesn't have this module
      import fcntl
      import struct
  except BaseException, err:
        print( "WRN: getNaoIPs: import error (1), err: %s" % str( err ) );
        return "";
  def get_ip_address( strInterfaceName ):
    "get the ip associated to a linux network interface"
    try:
      sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
#      print( "sock: '%s'" % str( sock ) );
#      print( "strInterfaceName: " + str( strInterfaceName ) );
      strInterfaceName = strInterfaceName[:15];
#      print( "strInterfaceName: " + str( strInterfaceName ) );
      packedInterfaceName = struct.pack( '256s', strInterfaceName );
#      print( "packedInterfaceName: " + str( packedInterfaceName ) );
      ret = fcntl.ioctl(
          sock.fileno(),
          0x8915,  # SIOCGIFADDR
          packedInterfaceName
      );
#      print( "ret: '%s'" % ret );
      ret = ret[20:24];
#      print( "ret: '%s'" % ret );
      return socket.inet_ntoa( ret );
    except BaseException, err:
        print( "WRN: getNaoIPs.get_ip_address: socker error (2), err: %s" % str( err ) );
        return '';
  # get_ip_address - end

  return [get_ip_address( 'eth0' ), get_ip_address( 'wlan0' )];
# getNaoIPs - end

#print "getNaoIPs(): '%s'" % str( getNaoIPs() );


def getSystemMusicPlayerName():
  "get the music player name on the current machine"
  if( isOnNao() ):
    return "mpg123";
  return "start"; # temp todo
# getSystemMusicPlayerName - end


global_listActiveXar = NoDuplicate();

def isActiveXar( strXarName ):
    nRet = global_listActiveXar.isPresent( strXarName );
    debug( "altools.isActiveXar: ret: %s" % nRet );
    return nRet;

def addActiveXar( strXarName ):
    nRet = global_listActiveXar.add( strXarName );
    debug( "altools.addActiveXar: ret: %s" % nRet );
    return nRet;

def removeActiveXar( strXarName ):
    nRet = global_listActiveXar.remove( strXarName );
    debug( "altools.removeActiveXar: ret: %s" % nRet );
    return nRet;


def getActiveXarList():
    ret = global_listActiveXar.getList();
    debug( "altools.getActiveXarList: ret: %s" % ret );
    return ret;

def getEarLedNameFromIndex( nIndex, nSideIndex = 0 ):
    return getEarLedName( nIndex, nSideIndex );
# getEarLedsNameFromIndex - end

def getEarLedName( nIndex, nSideIndex = 0 ):
    "get dcm leds ears device name from index"
    nNbrMax = 10;
    if( nIndex >= nNbrMax or nIndex < 0 ):
        print( "ERR: getEarLedName: index out of range (%d)" % nIndex );
        return "";
    nAngle = (360/nNbrMax) * nIndex;
    strName = "Ears/Led/%s/%dDeg/Actuator/Value" % ( getSide( nSideIndex ), nAngle );
    return strName;
# getEarLedName - end

def getBrainLedName( nNumLed ):
    "get the name of the dcm led device by it's number"
    "0 => front left; 1 => next in clock wise"
    if( nNumLed <= 1 ):
        return "Head/Led/Front/Right/%d/Actuator/Value" % (1-nNumLed);
    if( nNumLed >= 10 ):
        return "Head/Led/Front/Left/%d/Actuator/Value" % (nNumLed-10);

    if( nNumLed <= 2 ):
        return "Head/Led/Middle/Right/%d/Actuator/Value" % (2-nNumLed);
    if( nNumLed >= 9 ):
        return "Head/Led/Middle/Left/%d/Actuator/Value" % (nNumLed-9);

    if( nNumLed <= 5 ):
        return "Head/Led/Rear/Right/%d/Actuator/Value" % (nNumLed-3);
    if( nNumLed >= 6 ):
        return "Head/Led/Rear/Left/%d/Actuator/Value" % (8-nNumLed);

    print( "ERR: getBrainLedName: index out of range (%d)" % nNumLed );
    return "";
# getBrainLedName - end

def getTactilLedName( nNumLed ):
    "just for backward compatibility"
    return getBrainLedName( nNumLed );
# getTactilLedName - end

def setBrainLedsIntensity( rIntensity = 1.0, rTimeMs = 20, bDontWait = False ):
    "light on/off all the brain leds"
    dcm = myGetProxy( "DCM" );
    riseTime = dcm.getTime(rTimeMs);
    for i in range( 12 ):
        strDeviceName = getBrainLedName( i );
        dcm.set( [ strDeviceName, "Merge",  [[ rIntensity, riseTime ]] ] );    
    if( not bDontWait ):
        time.sleep( rTimeMs / 1000. );
# setBrainLedsIntensity - end

def setOneBrainIntensity( nLedIndex, rIntensity = 1.0, bDontWait = False ):
    "set one led beyond all the brain leds"
    "nLedIndex in [0,11]"
    dcm = myGetProxy( "DCM" );
    rTime = 0.05
    riseTime = dcm.getTime(int( rTime*1000 ));
    strDeviceName = getBrainLedName( nLedIndex );
    dcm.set( [ strDeviceName, "Merge",  [[ float( rIntensity ), riseTime ]] ] );         # le float ici est ultra important car sinon venant de chorégraphe 1.0 => 1 (depuis les sliders de params)
    if( not bDontWait ):
        time.sleep( rTime );
# setOneBrainIntensity - end

def setBrainVuMeter( nLeftLevel, nRightLevel, rIntensity = 1.0, bDontWait = False, bInverseSide = False ):
    "use the brain leds as vu meter (left and right separated)"
    "the 0 is in the front of Nao"
    "nXxxLevel in [0,6] => 0: full lightoff; 6 => full litten"
    "bInverseSide: the 0 becomes at bottom of Nao"
    dcm = myGetProxy( "DCM" );
    rTime = 0.05
    riseTime = dcm.getTime(int( rTime*1000 ));
    for i in range( 6 ):
        if( not bInverseSide ):
            strDeviceNameR = getBrainLedName( i );
            strDeviceNameL = getBrainLedName( 11-i );
        else:
            strDeviceNameR = getBrainLedName( 5-i );
            strDeviceNameL = getBrainLedName( 11-(5-i) );            
        if( i < nLeftLevel ):
            rIntL = rIntensity;
        else:
            rIntL = 0.;
        if( i < nRightLevel ):
            rIntR = rIntensity;
        else:
            rIntR = 0.;        
        dcm.set( [ strDeviceNameL, "Merge",  [[ float( rIntL ), riseTime ]] ] );         # le float ici est ultra important car sinon venant de chorégraphe 1.0 => 1 (depuis les sliders de params)
        dcm.set( [ strDeviceNameR, "Merge",  [[ float( rIntR ), riseTime ]] ] );
    if( not bDontWait ):
        time.sleep( rTime );
# setOneBrainIntensity - end
    

def askWatchdogToRestartNaoqi(): 
    "send a signal to the watchdog to restart naoqi"
    print( "WRN: ********************************************" );
    print( "WRN: altools.askWatchdogToRestartNaoqi called !!!" );
    print( "WRN: ********************************************" );
    strFilename = getVolatilePath() + 'naoqi_ask_for_reboot';
    try:
        file = open( strFilename, "wt" );
        file.write( "R" );
        file.close();
    except RuntimeError, err:
        print( "askWatchdogToRestartNaoqi: ERR: %s" % str( err ) );
# askWatchdogToRestartNaoqi - end    
    

global_strBehaviorPath = "";
def behaviorPath_set( strPath ):
    "Set the path of the current behavior (the location of the .xar currently executed)"
    global global_strBehaviorPath;
    print( "behaviorPath_set: changing current xar path from '%s' to '%s'" % ( global_strBehaviorPath, strPath ) );
    global_strBehaviorPath = strPath;
# behaviorPath_set - end

def behaviorPath_constructAbsoluteFilename( strFilename ):
    "convert a filename 'sounds/toto.wav' to an absolute filename '/home/nao/Applications/stories/sounds/toto.wav'"
    "INF: If it's an absolute filename, it won't modify it"
    global global_strBehaviorPath;
    if( not strFilename[0] == getDirectorySeparator() ):
        strDest = global_strBehaviorPath + getDirectorySeparator() + strFilename;
        if( not isFileExists( strDest ) ):
            strDest = getApplicationSharedPath() + strFilename; # TODO: portability
    else:
        strDest = strFilename;
    print( "behaviorPath_constructAbsoluteFilename: '%s' => '%s'" % ( strFilename, strDest ) );
    return strDest;
# behaviorPath_constructAbsoluteFilename - end

#######################################
# Nao and NaoQi Specific tools  (formerly appunaoqi.py)
#
#~ summary:
#~ - NaoQi constants
#~ - myGetProxy: redefinition of the basic getproxy, si it can work from choregraphe or from a python script
#~ - launchCall: launch a naoqi call with a various list of argument
#~ - postQueueOrders: launch a list of naoqi command contiguously
#~ -
#~ - logToChoregraphe: print logs in the choregraphe debug print (like box.log)
#~ -
#~ - choregrapheGetParentName: analyse box name and get the name of parent
#~ - choregrapheGetLastName: analyse box name and get the name of the last box - in the future we will juste make a self.getParent().getName()
#~ - choregrapheBoxPathNameToBoxName: transform complete choregraphe name to a boxName ALFrameManager__0xace99400__root__cascadedtemplatewhile_1 => cascadedtemplatewhile
#~ - choregrapheExplodeBoxName: analyse box name and return all the path of a box ALFrameManager__0xace99400__root__cascadedtemplatewhile_1 => ['ALFrameManager', '0xace99400', 'root', 'cascadedtemplatewhile_1']
#~ - coloriseBox_Activate: colorise the title of a box and all its parents, to show it's activity
#~ -
#~
#~ - convertEnergyToEyeColor_PseudoColor: convert energy[0,nMax] in eye color using pseudo color conversion table
#~ - convertEnergyToEyeColor_Intensity: convert energy[0,nMax] in eye color intensity
#~ - analyseSpeakSound: Analyse a raw stereo sound file, and found the light curve relative to sound (for further speaking)
#~
#~ - assumeTextHasDefaultSettings: look if text has voice default params( RSPD, VCT, Vol...) if not, add it, and return it
#~ - sayAndCache_getFilename: return the filename linked to the sentence to say (using precomputed text)
#~ - sayAndCache: generate a text in a file, then read it, next time it will be directly played from that file
#~
#~ - User Interface centralized method (uiSay, ...)
#~
#~ - class LocalizedText: multi-lang text functionnality, with caching
#~
#~ - sayAndCacheAndLight: say a cached text with light animation
#~ - sayAndEyes: say and turn eyes at the same times (deprecated?)
#~ - sayWithEyes2: do a speak with standard eyes position, blink and some emotion (deprecated?)
#~ - setSpeakLanguage: change the tts speak language
#~ - getSpeakLanguage: return the current speak language of the synthesis
#~
#~ - getJointListByChain: return all the joint name, sorted by chain: in three list: [[head_joint], [top_joint], [bottom_joint]]
#~ - getListJointSensorDCM: return all the joint name present in stm from dcm
#~ - getListJointActuatorDCM: return all the actuator joint name present in stm from dcm
#~ -
#~ - class PoseLibrary: A module to store Nao position, compare position between them and help user use them
#~
#~ - isPlugged: is nao plugged to its charger
#~ - isInPackaging: is nao in it's transport packaging box
#~ - setWifi: stop the wifi connection (si bOnOrOff is set to True reactivate it)
#~
#~ - changeAngleTimed: will change a joint from it's current position to current+inc in a certain time
#~ - lightLedsCircle: does a circle in the face led (deprecated?)
#~
#~ - playSoundHearing: play the standard appu sound before earing user command
#~ - playSoundSpeaking: play the standard appu sound before speaking to user
#~ - playSoundUnderstanding: play the standard appu sound to show a command is understood
#~
#~ - speak: say something using standard APPU interaction (leds, talk jingle...)
#~
#~ - class JointMove: record the activity of a joint and knows if it's moving or not and the side of the move
#~
#~ - isTreeContentsFileThatMatch: does the directory or subdirectory contents some file matching a mask
#~
#~ - findXar: look for behaviors in a disk tree
#~ - findFile: look for file matching the mask in a directory, if bRecursive: look into subdirectories too
#~
#~ - sendMail: send a mail from the nao mail account
#~
#~ - class MenuChoice: Launch a multimodal choice interaction, including speech recognition, Naomark and bumper
#~
#~ - storeGlobalData: store a data in the stm so everybody can acess it
#~
#~ - findPidOfChild: return the first found child of a pid
#~ - isProcessPresent: return true if the process with num nNumPid is running again
#~
#~ - getCurrentMasterVolume: get nao master sound system volume (in %)
#~ - setMasterVolume: change the master volume (in %)
#~ - volumeFadeOut: Fade out master sound system
#~ - setMasterMute: mute nao sound volume
#~ - isMasterMute: is nao sound volume muted?
#~ - setMasterPanning: change the sound master panning: 0: center -100: left +100: right
#~ - pauseMusic: pause the music player
#~ - sayInfoMusic: say the title of the song
#~
#~ - isHandPresent: Are we using a nao with hands?
#~ - describeColor: convert a [b,g,r] color to a string eg: [0,0,0] => "black" ...
#~ - getSide: get side left/right from 0..1
#~ - getColor: get color red/green/blue from 0..2
#~ - getLedsEyesDegreesFromIndex: get degrees 0..315 from 0..7
#~ - getEyeLedName: get the name of the dcm led device by it's number
#~ - getLedValueRGB: get the hexa value of a led. szLedName: the name of the led, eg 'FaceLedLeft0'
#~ - eyesRotate: rotate current configuration of eyes of one step, in one way or the others depending of nStep
#~ - circleLedsEyes: launch a leds animation using one color
#~ - circleLedsEars: launch a ears leds rotation
#~
#~ - cameraRelativePosToAbsolute: return absolute head move position from angle value in the camera angle space
#~
#~ - class Song: The representation of a song file
#~ - class NaoTunes: Manage MP3 library on Nao: list them, play them, shuffle options...
#~ -
#~ - class ExtractEvents: A python naoqi module that extract high level events so user can subscribe to exported variable in ALMemory
#~
#~ - animateEarLeds: move slightly ears leds, position is globally stored.
#~ - animateBodyLeds: animate/blink/change one body leds (0: torso; 1: left foot; 2: right foot)
#~ - animateTorsoLeds: blink torso light (idem for foot and ...)
#~ - animateEyeLeds_Attentive: animate eyes leds with an attentive style
#~ -
#~ - class LanguageProcessing: This class provides methods to process language (eg: detect lang).
#~ -
#~ - Ressource managing methods

#~ - getNaoChestName: get the nao name as stored in the rom chest
#~ - getNaoNickName: get the nao name as given by user
#~ -  getCurrentApplicationHelp: return help of current nao application
#~ -  getCurrentNotification: return current notification about something, a memo or ... (or '' if none)
#~ -  getCurrentNotification_ApplicationName: return name of application to launch
#~ -  setCurrentNotification: change the notification state ("" to reset)
#~ -  setCurrentNotification_ApplicationName: change the notification application name ("" to reset)
#~ - launchApplication: Post a launch application wish to the ALMemory
#~ - isFootPressed: return true if the foot has at least one bumper empushed
#~ - assumeStiffness: assume that stiffness is equal or greater to rValue
#~ - getNbrMoveOrder: compute current joint moving by order
#~
#~ - innerTest: altools inner test method (TODO: UPDATE)
#
#######################################

print( "*** altools: parsing specific naoqi tools" );


TRepeatType_None = 0;
TRepeatType_EveryFive = 1;
TRepeatType_EveryTen = 2;
TRepeatType_EveryQuarter = 3;
TRepeatType_EveryHalf = 4;
TRepeatType_EveryHour = 5;
TRepeatType_EveryDay = 6;
TRepeatType_EveryWeek = 7;
TRepeatType_EveryMonth = 8;
TRepeatType_EveryYear = 9;

# Vision constants
class Camera:
  def __init__(self):
    # Format of the image
    self.VGA = 2;                # 640*480
    self.QVGA =1;               # 320*240
    self.QQVGA = 0;            # 160*120
    # Standard Id
    self.BrightnessID       = 0;
    self.ContrastID         = 1;
    self.SaturationID       = 2;
    self.SID       = 2;
    self.HueID              = 3;
    self.RedChromaID        = 4;
    self.BlueChromaID       = 5;
    self.GainID             = 6;
    self.HFlipID            = 7;
    self.VFlipID            = 8;
    self.LensXID            = 9;
    self.LensYID            = 10;
    self.AutoExpositionID   = 11;
    self.AutoWhiteBalanceID = 12;
    self.AutoGainID         = 13;
    self.FormatID           = 14;
    self.FrameRateID        = 15;
    self.BufferSizeID       = 16;
    self.ExposureID         = 17;
    self.SelectID           = 18;
    self.SetDefaultParamsID = 19;
    self.ColorSpaceID       = 20;
    self.ExposureCorrectionID = 21;
    self.CameraAecAlgorithmID     = 22;
    self.CameraFastSwitchID       = 23;
    self.CameraSharpnessID        = 24; 
# class Camera - end

cameradef = Camera(); # ca fonctionne drolement pas trop ainsi...


class Motion:

  def __init__(self):
    # SPACES
    self.SPACE_BODY = 0
    self.SPACE_SUPPORT_LEG = 1

    # INTERPOLATION_TYPE
    self.INTERPOLATION_LINEAR = 0
    self.INTERPOLATION_SMOOTH = 1

    # BALANCE_MODE
    self.BALANCE_MODE_OFF = 0
    self.BALANCE_MODE_AUTO = 1
    self.BALANCE_MODE_COM_CONTROL = 2

    # SUPPORT_MODE
    self.SUPPORT_MODE_LEFT = 0
    self.SUPPORT_MODE_DOUBLE_LEFT = 1
    self.SUPPORT_MODE_RIGHT = 2
    self.SUPPORT_MODE_DOUBLE_RIGHT = 3
    self.SUPPORT_MODE_NONE = 4

    # AXIS MASK
    self.AXIS_MASK_X = 1
    self.AXIS_MASK_Y = 2
    self.AXIS_MASK_Z = 4
    self.AXIS_MASK_WX = 8
    self.AXIS_MASK_WY = 16
    self.AXIS_MASK_WZ = 32
    self.AXIS_MASK_ALL = 63
    self.AXIS_MASK_VEL = 7
    self.AXIS_MASK_ROT = 56

    # COMPUTING
    self.TO_RAD = 0.01745329;

# class Motion - end

motion = Motion();

class KnownObject:

  def __init__(self):
      
    # Types
    self.TypeUnknown = 0
    self.TypeGeneric = 1
    self.TypeBarCode = 2
    self.TypeHuman = 3
    self.TypeMax = 4
      
    # Angles
    self.AngleUnknow = 0
    self.AngleFront = 1
    self.AngleRear = 2
    self.AngleTop = 3
    self.AngleBottom = 4
    self.AngleLeft = 5
    self.AngleRight = 6
    self.AnglePers = 7
    self.AngleFace = 8
    self.AngleMax = 9

# class KnownObject - end

knownObject = KnownObject();


# configuration


# import naoqi object
import os
import sys
import time
import thread


path = `os.environ.get("AL_DIR")`
home = `os.environ.get("HOME")`

# import naoqi lib
if path == "None":
  print "the environnement variable AL_DIR is not set, aborting..."
  sys.exit(1)
else:
  #alPath = path + "/extern/python/aldebaran"
  alPath = path + "\\lib\\"
  alPath = alPath.replace("~", home)
  alPath = alPath.replace("'", "")
  sys.path.append(alPath)
  import naoqi
  from naoqi import ALBroker
  from naoqi import ALModule
  from naoqi import ALProxy
#import inaoqi_d
#from naoqi_d import * # fait crasher sous windows, ca commence bien...

# import naoqi object - end

#val = 3;
#print "unevaleur" ,  val;


def getDefaultSpeakLanguage():
  "return the default speak language"
  #return naoconfig.LANG_EN; # TODO: better things ! # CB : gets the real language
  if( not isOnNao() ):
    return 0;
  try:
    tts = myGetProxy("ALTextToSpeech");
  except:
    # no tts => anglais
    altools.debug( "WRN: altools.getDefaultSpeakLanguage: no tts found" );
    return naoconfig.LANG_EN;
  if( tts == None ):
    return naoconfig.LANG_EN;
  lang =  tts.getLanguage()
  if lang == "French":
    return naoconfig.LANG_FR;
  else:
    return naoconfig.LANG_EN;  
# getDefaultSpeakLanguage - end

def myGetProxy( strProxyName, bUseAnotherProxy = False, strHostName = 'localhost' ):
  "redefinition of the basic getproxy, so it can work from choregraphe or from a python script"
  "bUseAnotherProxy: this proxy is used to unlock another proxy, with the same name"
  "strHostName: use another hostname, WRN: using this option will recreate a new proxy at each CALL => TODO"
  if( bUseAnotherProxy ):
      return myGetProxyNoAddr( strProxyName, True );
  obj = getInCache( strProxyName+strHostName, ALProxy );
  if( obj != None ):
    return obj;
  if( strHostName != 'localhost' ):
      obj = myGetProxyWithAddr( strProxyName, strIP = strHostName );    
  else:
    obj = myGetProxyNoAddr( strProxyName );
  if( obj != None ):
    storeInCache( strProxyName+strHostName, obj );
  return obj;
# myGetProxy - end

def myGetProxyNoAddr( strProxyName, bUseAnotherProxy = False ):
    debug( "MyGetProxyNoAddr: connecting to '%s'" % (strProxyName) );
    if( naoconfig.bInChoregraphe ):
        try:
            obj = ALProxy( strProxyName, bUseAnotherProxy );
            if( not obj ):
                debug( "MyGetProxyNoAddr: couldn't connect to '%s" % (strProxyName) );
                return None;
            obj.ping(); # to validate the right construction
            debug( "MyGetProxyNoAddr: connected to '%s'" % (strProxyName) );
            return obj;
        except RuntimeError, err:
            debug(  "MyGetProxyNoAddr: Exception catched: %s" % err );
            return None;
    else:
        # print  "MyGetProxyNoAddr: method disabled";
        # return None;
        return myGetProxyWithAddr( strProxyName );
# myGetProxyNoAddr - end

def myGetProxyWithAddr( strProxyName,  strIP = naoconfig.strIP, nPort = naoconfig.nPort ):
  debug( "MyGetProxyWithAddr: connecting to '%s@%s:%d'" % (strProxyName,strIP,nPort) );
  try:
    obj = ALProxy( strProxyName, strIP, nPort );
    obj.ping(); # to validate the right construction
    if( not obj ):
      debug( "MyGetProxyWithAddr: couldn't connect to '%s@%s:%d' (1)" % (strProxyName,strIP,nPort) );
      return None;
    debug( "MyGetProxyWithAddr: connected to '%s@%s:%d' (1)" % (strProxyName,strIP,nPort) );
    return obj;
  except BaseException, err:
    debug( "MyGetProxyWithAddr: Exception catched: %s" % err );
    return None;

# various tools

def launchCall( *listArgs ):
  "launch a naoqi call with a various list of argument"
  try:
    print "LaunchCall:", listArgs;
    args = listArgs[0];
    proxy = myGetProxy( args[0] );
    strFuncName = args[1];
    params = args[2];
    print( "LaunchCall: " + strFuncName + " params: " );
    print( params );
    proxy.callPython( strFuncName, *params );
    thread.exit(); # exit thread
  except BaseException, err:
    debug( "MyPCall: Exception catched: %s" % err );
# launchCall - end

def myPCall( proxy, strFuncName, args ):
  try:
    listArgs = [ proxy, strFuncName, args ];
    thread.start_new_thread( LaunchCall, (listArgs,) );
    return;
  except BaseException, err:
    debug( "MyPCall: Exception catched: %s" % err );
# myPCall - end

def postQueueOrders( aListOrder, nDelayBetweenOrderInSec = 0. ):
    "launch a list of naoqi command contiguously"
    def implode(strString,strElem):
        if( nDelayBetweenOrderInSec > 0. ):
            return "%s;time.sleep( %f ); %s " % ( strString, nDelayBetweenOrderInSec, strElem );
        return strString + ";" + strElem;
    strConstructedCommand = reduce( implode, aListOrder )
#    print( "strConstructedCommand: %s" % strConstructedCommand );
    asyncEval( strConstructedCommand );
# postQueueOrders - end

def logToChoregraphe( strText ):
    "print logs in the choregraphe debug print (like box.log)"
    debug( "logToChoregraphe: '%s'" % strText );
    try:
        chor = myGetProxy( "ALChoregraphe" );
        chor.onPythonPrint( str( strText ) );
    except:
        pass
# logToChoregraphe - end

def choregrapheGetParentName( strBoxName ):
    "analyse box name and get the name of parent - in the future we will juste make a self.getParent().getName()"
    listBoxName = choregrapheExplodeBoxName( strBoxName );
    listBoxName.pop(); # remove last name
    strParentBoxName = "__".join( listBoxName );
#    print( "%s -> %s" % ( strBoxName, str( strParentBoxName ) ) );
    return strParentBoxName;
# choregrapheGetParentName - end

def choregrapheGetLastName( strBoxName ):
    "analyse box name and get the name of the last box - in the future we will juste make a self.getParent().getName()"
    listBoxName = choregrapheExplodeBoxName( strBoxName );
    return listBoxName.pop(); # remove last name
# choregrapheGetParentName - end

def choregrapheBoxPathNameToBoxName( strBoxName ):
    "transform complete choregraphe name to a boxName ALFrameManager__0xace99400__root__cascadedtemplatewhile_1 => cascadedtemplatewhile"
    lastName = choregrapheGetLastName( strBoxName );
    listUnderScored = lastName.split( "_" );
    listUnderScored.pop();
    lastName = "_".join( listUnderScored );

    return lastName; # remove last name
# choregrapheGetParentName - end

def choregrapheExplodeBoxName( strBoxName ):
    "analyse box name and return all the path of a box ALFrameManager__0xace99400__root__cascadedtemplatewhile_1 => ['ALFrameManager', '0xace99400', 'root', 'cascadedtemplatewhile_1']"
    listBoxName = strBoxName.split( "__" );
    return listBoxName;
# choregrapheExplodeBoxName - end

global_coloriseBox_ActivateOneBox_allBoxState = []; # will contents [ ["pathboxname", nbrActivation], ...]

def coloriseBox_ActivateOneBox_internal( strPathBoxName, bActivate = True ):
    "add an activation color to a single level box"
    global global_coloriseBox_ActivateOneBox_allBoxState;
    debug( "coloriseBox_ActivateOneBox_internal( '%s', %d )" % ( strPathBoxName, bActivate ) );

    global global_SectionCritique;
    while( global_SectionCritique.testandset() == False ):
        debug( "coloriseBox_ActivateOneBox_internal: locked" );
        time.sleep( 0.05 );

    nIdx = -1;
    for i in range( len( global_coloriseBox_ActivateOneBox_allBoxState ) ):
        if( global_coloriseBox_ActivateOneBox_allBoxState[i][0] == strPathBoxName ):
            nIdx = i;
            break;
    if( nIdx == -1 ):
        # first time
        nIdx = len( global_coloriseBox_ActivateOneBox_allBoxState );
        global_coloriseBox_ActivateOneBox_allBoxState.append( [ strPathBoxName, 0 ] );

    strBoxName = choregrapheBoxPathNameToBoxName( strPathBoxName );
    debug( "coloriseBox_ActivateOneBox_internal: '%s' last => '%s'" % ( strPathBoxName, strBoxName ) );
    if( bActivate ):
        global_coloriseBox_ActivateOneBox_allBoxState[nIdx][1] +=1;
        if( global_coloriseBox_ActivateOneBox_allBoxState[nIdx][1] == 1 ):
            # colorise it!
            controller = myGetProxy( "ALChoregrapheController" );
            try:
                controller.setBoxTitleColor( strBoxName, 0., 0., 1. );
            except BaseException, err:
                debug( "coloriseBox_ActivateOneBox_internal: Exception catched: %s" % err );
    else:
        global_coloriseBox_ActivateOneBox_allBoxState[nIdx][1] -=1;
        if( global_coloriseBox_ActivateOneBox_allBoxState[nIdx][1] == 0 ):
            # reset it!
            controller = myGetProxy( "ALChoregrapheController" );
            try:
                controller.setBoxTitleColor( strBoxName, 0., 0., 0. );
            except BaseException, err:
                debug( "coloriseBox_ActivateOneBox_internal: Exception catched: %s" % err );


    global_SectionCritique.unlock();
# coloriseBox_ActivateOneBox_internal - end

def coloriseBox_Activate( strPathBoxName, bActivate = True ):
    "colorise the title of a box and all its parents, to show it's activity"
    "we will memorise for each box, the number of child activated, so it will show the state of all child"
    try:
        controller = myGetProxy( "ALChoregrapheController" );
    except:
        return; # no controller found...

    strParentName = choregrapheGetParentName( strPathBoxName );
    if( strParentName != "root" ):
        coloriseBox_ActivateOneBox_internal( strParentName, bActivate );

    # activate this level
    coloriseBox_ActivateOneBox_internal( strPathBoxName, bActivate );
# coloriseBox_Activate - end

def coloriseBox_Desactivate( strPathBoxName ):
    return coloriseBox_Activate( strPathBoxName, False );
# coloriseBox_Desactivate - end

def convertEnergyToEyeColor_PseudoColor( nValue, nMax ):
    "convert energy[0,nMax] in eye color using pseudo color conversion table"
        # f(p) = ((Rgb-Liminf)/pi) * arctan(tan((pi/2)(Rgb + Liminf)/(Rgb - Liminf))((p/Middle)-1)) + (Rgb + Liminf)/2 => we have 2 horizontal asymptotes (Rgb, -1), and f(0) = 0
    nMaxLighten = nMax; # = 0xFFFFFF
    nValue = int( nValue * 0xFFFFFF/ nMax );
    rMiddle = nMaxLighten/16.0
    rLiminf = -nMaxLighten/3.0
    #~ p = int(p*10)
    #~ if p > 16777215:
        #~ p == 16777215
    #~ p =   ((Rgb-Liminf)/math.pi) * math.atan(math.tan((math.pi/2.0)*(Rgb + Liminf)/(Rgb - Liminf))*((p/Middle)-1.0)) + (Rgb + Liminf)/2.0
    RGPart = int(nValue/256)
    BPart = nValue - 256*RGPart
    RPart = int(RGPart/256)
    GPart = RGPart - 256*RPart
    return ( RPart << 16 ) + ( GPart << 8 ) + BPart;
# convertEnergyToEyeColor_PseudoColor - end

def convertEnergyToEyeColor_Intensity( nValue, nMax ):
    "convert energy[0,nMax] in eye color intensity"
    return ( nValue / float( nMax ) ) * 1.0 + 0.00; # +0.2 pour la possibilité de ne pas etre tout noir
# convertEnergyToEyeColor_Intensity - end

def analyseSpeakSound( strRawFile, nSampleLenMs = 50, bStereo = False ):
    "Analyse a raw stereo or mono sound file, and found the light curve relative to sound (for further speaking)"
    print( "analyseSpeakSound: analysing '%s' (time:%d)" % ( strRawFile, int( time.time() ) ) );
    nNbrChannel = 1;
    if( bStereo ):
        nNbrChannel = 2;
    aMonoSound = loadSound16( strRawFile, nNbrChannel );
    if( len( aMonoSound ) < 1 ):
        return [];

    #analyse every 50ms sound portion (because 50ms is the average latency of leds)
    anLedsColorSequency = []; # for every time step, an int corresponding to the RGB colors
    nSizeAnalyse = int( (22050*nSampleLenMs)/1000 ); # *50 => un sample chaque 50ms
    nMax = 0;
    nOffset = 0;
    nNbrSample = len( aMonoSound );
    print( "analyseSpeakSound: analysing %d sample(s)" % nNbrSample );
    while( nOffset < nNbrSample ):
        anBuf = aMonoSound[nOffset:nOffset+nSizeAnalyse];
        nOffset += nSizeAnalyse;
        nValue = computeEnergyBest( anBuf );
        if( nValue > nMax ):
            nMax = nValue;
        # storenValue to nColor
        anLedsColorSequency.append( nValue );
    # while - end

    # convert nValue to nColor (using max energy)
    nOffset = 0;
    nNbrComputed = len( anLedsColorSequency );
    print( "analyseSpeakSound: converting %d energy to leds light (max=%d)" % ( nNbrComputed, nMax) );
    while( nOffset < nNbrComputed ):
        anLedsColorSequency[nOffset] = convertEnergyToEyeColor_Intensity( anLedsColorSequency[nOffset], nMax );
        nOffset += 1;
    # while - end

    print( "analyseSpeakSound: analysing '%s' (time:%d) - end" % ( strRawFile, int( time.time() ) ) );
    return anLedsColorSequency;
# analyseSpeakSound - end

#analyseSpeakSound( "d:\\worksound\\0Power.wav" );
#analyseSpeakSound( "c:\\temp\\test.raw" );

#copyFile( "c:\\temp\\body_not_found.raw", "c:\\temp\\test.raw" );
#convertSoundRaw( "c:\\temp\\test.raw" );

def assumeTextHasDefaultSettings( strTextToSay, nUseLang = -1 ):
    "look if text has voice default params( RSPD, VCT, Vol...) if not, add it, and return it"
    if( nUseLang == -1 ):
        nUseLang = getSpeakLanguage();
        
    if( nUseLang == naoconfig.LANG_CH ):
        return strTextToSay; # current bug => don't add modifiers to this speak languages!

    if( strTextToSay.find( "\\RSPD=" ) == -1 ):
        strTextToSay = "\\RSPD=" + str( naoconfig.nSpeakSpeed ) + "\\ " + strTextToSay;
    if( strTextToSay.find( "\\VCT=" ) == -1 ):
        strTextToSay = "\\VCT=" + str( naoconfig.nSpeakPitch ) + "\\ " + strTextToSay;
    if( strTextToSay.find( "\\VOL=" ) == -1 ):
        strTextToSay = "\\VOL=" + str( naoconfig.nSpeakVolume ) + "\\ " + strTextToSay;
    return strTextToSay;
# assumeTextHasDefaultSettings - end


def sayAndCache_getFilename( strTextToSay, nUseLang = -1 ):
    "return the filename linked to the sentence to say (using precomputed text)"
    "nUseLang: if different of -1: speak with a specific languages (useful, when text are already generated: doesn't need to swap languages for nothing!"

    # we will generate a string without some specific characters
    # specific characters are all but A-Za-z0-9

    #allchars = "";
    #for i in range( 1, 256):
    #  allchars += ord( i );
    #allcharsbutalphanum = allchars.translate(None, 'abcdefghi ...)

    #  szFilename = strTextToSay.replace( " ", "_" ); # this line cut the compatybility with ALDemo
    #  szFilename = strTextToSay.replace( "\n", "__" ); # this line cut the compatybility with ALDemo
    #  szFilename = szFilename.translate( string.maketrans("",""), ' ,;.?!/\\\'"-:><=' );

    szFilename = "";
    for i in range( len( strTextToSay ) ):
        ch = strTextToSay[i];
        if( ch.isalnum() ):
            szFilename += ch;
        elif( ch == ' ' ):
            szFilename += '_';
        else:
            szFilename += "%X" % ( ord( ch )%16 );

    szFilename = szFilename[:160]; # limit filename to 160 chars
    if( nUseLang == -1 ):
        nUseLang = getSpeakLanguage();
    szFilename = str( nUseLang ) + szFilename;
    return szFilename;
# sayAndCache_getFilename - end

def sayAndCache_InformPrepare():
    "inform user we will prepare a text, and that would take sometimes"
    aListTextWait = ["Wait a little I'm preparing what I would say", "Attend un peu, je réfléchis a ce que je vais dire" ];
    if( getSpeakLanguage() <= naoconfig.LANG_FR ):
        listTextWait = aListTextWait[getSpeakLanguage()];
    else:
        listTextWait = aListTextWait[naoconfig.LANG_EN];
    sayAndCache( listTextWait, bStoreToNonVolatilePath = True, bWaitEnd = False ) # c'est récursif, mais si le texte est plus court que la limite, alors c'est ok (renderé juste la premiere fois)
# sayAndCache_InformPrepare - end
    
def sayAndCache( strTextToSay, bJustPrepare = False, bStoreToNonVolatilePath = False, bDirectPlay = False, nUseLang = -1, bWaitEnd = True, bCalledFromSayAndCacheFromLight = False ):
  "generate a text in a file, then read it, next time it will be directly played from that file"
  "bJustPrepare: render the text to a file, but don't play it now"
  "bStoreToNonVolatilePath: copy the generated file to a non volatile path (/usr/generatedvoices)"
  "nUseLang: if different of -1: speak with a specific languages (useful, when text are already generated: doesn't need to swap languages for nothing!"
  "return the length of the text in seconds, or None if impossible"
  print( "sayAndCache( '%s', bJustPrepare: %s, bStoreToNonVolatilePath: %s, bDirectPlay: %s, nUseLang: %d, bWaitEnd: %s, bCalledFromSayAndCacheFromLight: %s )" % ( strTextToSay, str( bJustPrepare ), str( bStoreToNonVolatilePath ), str( bDirectPlay ), nUseLang, str( bWaitEnd ), str( bCalledFromSayAndCacheFromLight ) ) );
  if( not naoconfig.bPrecomputeText ):
      print( "sayAndCache: disabled by configuration: bPrecomputeText is false" );
      if( bJustPrepare ):
          return None; # do nothing
      tts = myGetProxy( "ALTextToSpeech" );
      tts.say( strTextToSay );
      return None;
  if( False ):
    print( "sayAndCache: FORCING DIRECT_PLAY CAR SINON C'EST BUGGE DANS LA VERSION COURANTE!");  
    bDirectPlay = True;
  
  if( naoconfig.bRemoveDirectPlay ):
    print( "WRN: DISABLING DIRECT_PLAY SETTINGS for testing/temporary purpose" );
    bDirectPlay = False;  
  
  strTextToSay = assumeTextHasDefaultSettings( strTextToSay, nUseLang );
  szFilename = sayAndCache_getFilename( strTextToSay, nUseLang );
  
  szPathVolatile = getVolatilePath();
  
#  if( not szFilename.isalnum() ): # the underscore is not an alphanumeric, but is valid there
#    debug( "WRN: sayAndCache: some chars are not alphanumeric in filename '%s'" % szFilename );
  szPathFilename = szPathVolatile + szFilename + ".raw";
  bGenerate = not isFileExists( szPathFilename );
  
  if( bGenerate ):
    szAlternatePathFilename = getCachePath() + "generatedvoices" + getDirectorySeparator() + szFilename + ".raw"; # look in a non volatile path
    
    if( isFileExists( szAlternatePathFilename ) ):
      debug( "sayAndCache: get static precomputed text for '%s'" % ( strTextToSay ) );
      copyFile( szAlternatePathFilename, szPathFilename );
      bGenerate = not isFileExists( szPathFilename );  #update this variable
    # if alternate
  # if bGenerate
  
  if( bGenerate ):
    # generate it!
    debug( "sayAndCache: generating '%s' to file '%s'" % ( strTextToSay, szPathFilename ) );
    sayAndCache_InformProcess();
    timeBegin = time.time();
    tts = myGetProxy( "ALTextToSpeech" );
    
    if( nUseLang != -1 ):
        # change the language to the wanted one
        setSpeakLanguage( nUseLang );
    if( len( strTextToSay ) > 150 and ( not bJustPrepare or bCalledFromSayAndCacheFromLight ) ):
        # if it's a long text, we had a blabla to tell the user we will wait (if it's a just prepare from inner, we don't use it)
        sayAndCache_InformPrepare();
    
    print( "TTS TO FILE 1 - BEGIN" );
    tts.sayToFile( strTextToSay, szPathFilename );
    print( "TTS TO FILE 1 - END" );
    sayAndCache_InformProcess_end();
    
    debug( "sayAndCache: generating text to file - end (tts) - time: %fs" % ( time.time() - timeBegin ) );    
    timeBegin = time.time();
    
    removeBlankFromFile( szPathFilename );
    debug( "sayAndCache: generating text to file - end (post-process1) - time: %fs" % ( time.time() - timeBegin ) );
    timeBegin = time.time();

    if( bStoreToNonVolatilePath ):
      try:
        os.makedirs( getCachePath() + "generatedvoices" + getDirectorySeparator());
      except:
        pass
      szAlternatePathFilename = getCachePath() + "generatedvoices" + getDirectorySeparator() + szFilename + ".raw"; # a non volatile path
      copyFile( szPathFilename, szAlternatePathFilename );

    time.sleep( 0.1 ); # pour laisser la synthese souffler un peu (dans les scripts je mettais 300ms)
    debug( "sayAndCache: generating text to file - end (post-process2) - time: %fs" % ( time.time() - timeBegin ) );
    
  statinfo = os.stat( szPathFilename );
  rLength = statinfo.st_size / float(22050*1*2); # sizefile => secondes
    
  if( not bJustPrepare ):
#    debug( "altools::sayAndCache: launching sound now!" );
    if( bWaitEnd ):
        analyseSound_pause( True );
    if( bDirectPlay ):
        nLang = nUseLang;
        if( nLang == -1 ):
            nLang = getSpeakLanguage();
        nFreq = 22050;
        if( nLang == naoconfig.LANG_CH or nLang == naoconfig.LANG_KO ):
            nFreq = 17000; # parce que c'est beau, (ca fait a peu pres du speed a 72%) # todo: ca désynchronise les yeux qui se lisent trop vite ! argh !
        mySystemCall( "aplay -c1 -r%d -fS16_LE -q %s" % ( nFreq, szPathFilename ), bWaitEnd = bWaitEnd );
    else:
        leds = myGetProxy( "ALLeds", True );
        leds.post.fadeRGB( "RightFootLeds", 0xFF0000, 0.7 ); # right in red (skip)
        audioProxy = myGetProxy( "ALAudioPlayer", True );
        # read it in background and check if someone press the right feet a long times => skip text playing
        
        id = audioProxy.post.playFile(szPathFilename);
        if( not bWaitEnd ):
            # attention: no unpause of analyse dans ce cas la!
            return rLength;
        nbrFramesBumpersPushed = 0;
        nbrFramesBumpersPushedMinToSkip = 2;
        strTemplateKeyName = "Device/SubDeviceList/%sFoot/Bumper/%s/Sensor/Value";
        stm = myGetProxy( "ALMemory" );
        while( audioProxy.isRunning( id ) ):
            time.sleep( 0.1 ); # time for user to release precedent push
            listRightFeetBumpers = stm.getListData( [strTemplateKeyName % ( "R", "Left" ), strTemplateKeyName % ( "R", "Right" )] );
            if( listRightFeetBumpers[0] > 0.0 or listRightFeetBumpers[1] > 0.0 ):
                nbrFramesBumpersPushed += 1;
                if( nbrFramesBumpersPushed >= nbrFramesBumpersPushedMinToSkip ):
                    print( "sayAndCache: skipping current text reading because users press on right bumpers" );
                    audioProxy.stop( id );
        leds.post.fadeRGB( "RightFootLeds", 0x000000, 0.2 ); # turn off it
        # while - end
    #if( bDirectPlay ) - end
    analyseSound_resume( True );
  # if( not bJustPrepare ) - end
  print( "sayAndCache: End !!!");
  return rLength;
# sayAndCache - end



def sayAndCacheAndLight( strTextToSay, bJustPrepare = False, bStoreToNonVolatilePath = False, nEyesColor = 0, nUseLang = -1 ):
    "say a cached text with light animation"
    "nEyesColor: 0: white, 1: blue, 2: green; 3: red"
    "nUseLang: if different of -1: speak with a specific languages (useful, when text are already generated: doesn't need to swap languages for nothing!"
    "return the length of the text in seconds, or None if impossible"
    print( "sayAndCacheAndLight( '%s', bJustPrepare: %s, bStoreToNonVolatilePath: %s, nEyesColor: %s, nUseLang: %s )" % ( strTextToSay, str( bJustPrepare ), str( bStoreToNonVolatilePath ), str( nEyesColor ), str( nUseLang ) ) );
    if( not naoconfig.bPrecomputeText ):
        print( "sayAndCacheAndLight: disabled by configuration: bPrecomputeText is false" );
        if( bJustPrepare ):
            return None; # do nothing
        tts = myGetProxy( "ALTextToSpeech" );
        tts.say( strTextToSay );
        return None;

    rLength = sayAndCache( strTextToSay, bJustPrepare = True, bStoreToNonVolatilePath = bStoreToNonVolatilePath, nUseLang = nUseLang, bCalledFromSayAndCacheFromLight = True ); # we store it to disk, only if we must do it

    # this two lines are done too in sayAndCache...
    strTextToSay = assumeTextHasDefaultSettings( strTextToSay, nUseLang );
    szFilename = sayAndCache_getFilename( strTextToSay, nUseLang );

    szPathVolatile = getVolatilePath();
    rSampleLenSec = 0.05;
#    szPathFilenamePeak = szPathVolatile + szFilename + ("_%5.3f.egy" % rSampleLenSec);
    szPathFilenamePeak = szFilename + ("_%5.3f.egy" % rSampleLenSec);
    szPathFilenamePeakCache = getCachePath() + "generatedvoices" + getDirectorySeparator() + szPathFilenamePeak;
    szPathFilenamePeak = szPathVolatile + szPathFilenamePeak;
    anLedsColorSequency = [];
    aBufFile = "";
    bFileGenerated = False;
    if( not isFileExists( szPathFilenamePeak ) ):
        if( isFileExists( szPathFilenamePeakCache ) ):
            copyFile( szPathFilenamePeakCache, szPathFilenamePeak );
    if( not isFileExists( szPathFilenamePeak ) ):
        # generate peak file
        timeBegin = time.time();
        print( "sayAndCacheAndLight: generating peak light - begin\n" );
        szPathFilename = szPathVolatile + szFilename + ".raw";
        anLedsColorSequency = [];
        try:
            une = myGetProxy( 'UsageNoiseExtractor' );
            anLedsColorSequency = une.analyseSpeakSound( szPathFilename, int( rSampleLenSec * 1000 ), False );
        except BaseException, err:
            print( "ERR: sayAndCacheAndLight( '%s' ): err: %s" % ( strTextToSay, str( err ) ) );
            print( "ERR: sayAndCacheAndLight => trying old cpp version" );
            anLedsColorSequency = analyseSpeakSound( szPathFilename, rSampleLenSec * 1000 );
        print( "sayAndCacheAndLight: analyseSpeakSound - end - time: %fs\n" % float( time.time() - timeBegin ) );        
#        print( "anLedsColorSequency: %d samples: %s\n" % ( len( anLedsColorSequency ), str( anLedsColorSequency ) ) );
        
        print( "Writing file with %d peak samples (time: %d)\n" % ( len( anLedsColorSequency ), int( time.time() ) ) );
        #         struct.pack_into( "f"*len( anLedsColorSequency ), aBufFile, anLedsColorSequency[:] );
        for peakValue in anLedsColorSequency:
            aBufFile += struct.pack( "f", peakValue );
        try:
            file = open( szPathFilenamePeak, "wb" );
            file.write( aBufFile );
        except RuntimeError, err:
            print( "ERR: sayAndCacheAndLight( '%s' ): err: %s" % ( strTextToSay, str( err ) ) );
        print( "sayAndCacheAndLight: Written file with a size of %d in '%s'" % ( len( aBufFile ), szPathFilenamePeak ) );
        file.close();
        if( bStoreToNonVolatilePath ):
            copyFile( szPathFilenamePeak, szPathFilenamePeakCache );
        bFileGenerated = True;
        print( "sayAndCacheAndLight: generating peak light - end - time: %fs\n" % float( time.time() - timeBegin ) );
    else:
        if( not bJustPrepare ):
            # read it
            print( "Reading file containing peak samples" );
            try:
                file = open( szPathFilenamePeak, "rb" );
            except RuntimeError, err:
                print( "ERR: sayAndCacheAndLight( '%s' ): err: %s" % ( strTextToSay, str( err ) ) );
                return None;
            try:
                aBufFile = file.read();
                print( "aBufFile len: %d" % len( aBufFile ) );
                nNbrPeak = len( aBufFile ) / struct.calcsize("f");
                anLedsColorSequency = struct.unpack_from( "f"*nNbrPeak, aBufFile );
            finally:
                file.close();

    if( bJustPrepare ):
        return rLength;

#    anLedsColorSequency += (0.05,); # a la fin on laisse les leds un peu allumé (non c'est trop abrupte a voir par ailleurs)
    print( "sending leds order, len: %d" % len( anLedsColorSequency ) );

    bFirst = True;
    if( False ):
        # avec methode postQueueOrders
        strLedsGroup = 'FaceLeds';
        if( nEyesColor == 1 ):
            strLedsGroup = 'AllLedsBlue'; # 'FaceLedsBlue'; mais ca n'existe pas!
        elif( nEyesColor == 2 ):
            strLedsGroup = 'AllLedsGreen';
        elif( nEyesColor == 3 ):
            strLedsGroup = 'AllLedsRed';
        aListOrder = [];
        aListOrder.append( "ALLeds = ALProxy( 'ALLeds')" );
        for value in anLedsColorSequency:
            if( bFirst ):
                bFirst = False;
                rTime = 0.;
            else:
                rTime = 0.02;
            aListOrder.append( "ALLeds.setIntensity( '%s', %f, %f )" % ( strLedsGroup, value, rTime ) );
        aListOrder.append( "ALLeds.fadeRGB( '%s', 0x101010, 0.2 )" % strLedsGroup ); # a la fin on laisse les leds un peu allumé
        postQueueOrders( aListOrder, rSampleLenSec - 0.02 + 0.016 );
    else:
        aRGB = [];
        aTime = [];
        for value in anLedsColorSequency:
            nValue = int( 0xff * value );
            if( nEyesColor == 1 ):
                pass # nValue = nValue
            elif( nEyesColor == 2 ):
                nValue = nValue << 8;
            elif( nEyesColor == 3 ):
                nValue = nValue << 16;
            else:
                nValue = (nValue << 16) | (nValue << 8) | (nValue);
#            print( "0x%s" % nValue );
            aRGB.append( nValue );
            if( bFirst ):
                bFirst = False;
                aTime.append( 0.00 ); # En fait pour le premier coup, on le veut maintenant !
            else:
                aTime.append( rSampleLenSec - 0.00120 );
#        aRGB = [ 0xFFFFFF, 0xFF, 0xFF00, 0xFF0000 ];
#        aTime = [1.0, 1.0, 1.0,1.0];
        aRGB.append( 0x101010 ); # a la fin on laisse les leds un peu allumé
        aTime.append( 0.2 );
#        print( "aRGB: %s" % str( aRGB ) );
#        print( "aTime: %s" % str( aTime ) );
        leds = myGetProxy( 'ALLeds');
        leds.post.fadeListRGB( 'FaceLedsExternal', aRGB, aTime );
    # if test methods - end
    rLength = sayAndCache( strTextToSay, bDirectPlay = True, nUseLang = nUseLang );
    
    if( not bStoreToNonVolatilePath and bFileGenerated ):
        # cleaning file !
        #nothing to do, we don't create it in a hard place
        # os.unlink( szPathFilenamePeak );
        # os.unlink( getCachePath() + "generatedvoices" + getDirectorySeparator() + szFilename + ".raw" );
        pass
    # if - end
    
    return rLength;
    
# sayAndCacheAndLight - end

def sayAndCache_InformProcess():
    "set a peculiar color in eyes before rendering sound"
    leds = myGetProxy( "ALLeds" );
    for i in range( 4 ):
        leds.post.fadeRGB( 'FaceLed' + str( i*2 ), 0xFF00, 0.1 );
        leds.post.fadeRGB( 'FaceLed' + str( i*2+1 ), 0x00FF, 0.1 );
# sayAndCache_InformProcess - end

def sayAndCache_InformProcess_end():
    "set a peculiar color in eyes before rendering sound"
    leds = myGetProxy( "ALLeds" );
    leds.post.fadeRGB( 'FaceLeds', 0x8080FF, 0.1 );
# sayAndCache_InformProcess - end
    

def sayMumbled( strText ):
    sayAndCache( strText, bJustPrepare = True );
    strText = assumeTextHasDefaultSettings( strText );
    szFilename = sayAndCache_getFilename( strText );
    szPathFilename = getVolatilePath() + szFilename + ".raw";
    szProcessed = szPathFilename + "_mumbled.raw";
    if( not processSoundMumbled( szPathFilename, szProcessed ) ):
        return False;
    nFreq = 22050;
    mySystemCall( "aplay -c1 -r%d -fS16_LE -q %s" % ( nFreq, szProcessed ) );    
    return True;
# sayMumbled - end
    


def uiSay( strText ):
    strSpeed = "\\RSPD=%d\\ " % naoconfig.nSpeakSpeedUI;
    sayAndCache( strSpeed + strText, bJustPrepare = False, bStoreToNonVolatilePath = True ); 
#uiSay - end




def sayAndEyes( txt, bWait = True ):
  "say and turn eyes at the same times (deprecated?)"
  print( "SayAndEyes: %s %d" % ( txt, bWait ) );
  nTimeEyes = len(txt)*50; # temps de lire une lettre :)
  if( nTimeEyes < 500 ):
    nTimeEyes = 500;
  print( "nTimeEyes: %d" % nTimeEyes );
  try:
    if( bWait ):
      leds = myGetProxy( "ALLeds" );
      idEyesRandom = leds.pCall( "randomEyes", nTimeEyes / 1000.0 );
      sayAndCache( txt );
#      leds.stop( idEyesRandom );
    else:
      asyncEval( "sayAndCache( \"" + str( txt ) + "\" )" );
  except RuntimeError, err:
    print "exception catched: "
    print  err;
# sayAndEyes - end

def sayWithEyes2( strText, nEmotionType = 1, bUsePrecompute = naoconfig.bPrecomputeText ):
  """ do a speak with standard eyes position, blink and some emotion (deprecated?)"""
  print( "altools::sayWithEyes2(%s,%d)" % ( strText, nEmotionType ) );
  try:
    leds = myGetProxy( "ALLeds" );
    if( nEmotionType == 1 ):
      leds.post.fadeRGB( "FaceLeds", 0x8585ff, 0.5 );

    strText = assumeTextHasDefaultSettings( strText );
    if( bUsePrecompute ):
      sayAndCache( strText );
    else:
      tts = myGetProxy( "ALTextToSpeech" );
      tts.say( strText );

    # we set the default leds configuration
    leds.post.fadeRGB( "FaceLeds", 0x108040, 0.2 );

  except RuntimeError, err:
    print "altools::sayWithEyes2: exception catched: "
    print  err;
# sayWithEyes2 - end

class LocalizedText:
  "multi-lang text functionnality, with caching"
  "WRN: we 're accepting to have some sentence with more lang than others"

  def __init__( self ):
    self.aListSentences = [];
    self.nNbrLangMax = 0;
    self.nCurrentLanguage = 0;
    self.bPrecompute = naoconfig.bPrecomputeText;
    self.bStoreToNonVolatile = False; # if True, after generate text, it will be stored to the tmp non volatile path, so no generation at next boot
  # __init__ - end

  def setPrecompute( self, bNewState ):
    "change the precompute option, to true or false. WRN: do it before calling the add method, if you don't want to precompute them at startup"
    self.bPrecompute = bNewState
  # setPrecompute - end

  def changeCurrentLangToDefault( self ):
    "change the language to reflect the default, the text will then be prepared for the current lang"
    self.setCurrentLang( getDefaultSpeakLanguage() );
  # changeCurrentLangToDefault - end

  def setCurrentLang( self, nNumCurrentLang ):
    "change the language, the text will then be prepared for the current lang"
    print( "LocalizedText.setCurrentLang: changing to lang %d" % nNumCurrentLang );
    self.nCurrentLanguage = nNumCurrentLang;
    setSpeakLanguage( self.nCurrentLanguage );
    self.prepareTextOneLang( self.nCurrentLanguage );
  # setCurrentLang - end

  def setStoreToNonVolatile( self, bNewVal ):
    "Set or unset the StoreToNonVolatile option"
    self.bStoreToNonVolatile = bNewVal;
  # changeCurrentLangToDefault - end

  def getCurrentLang( self ):
    return self.nCurrentLanguage;
  # getCurrentLang - end

  # add a new sentence of the form ["hello", "bonjour"];
  # return the ID of the new created text
  def add( self, aMultiLangSentence ):
    # transform accent
    for i in range( 0, len( aMultiLangSentence ) ):
      aMultiLangSentence[i] = assumeTextHasDefaultSettings( transformAsciiAccentForSynthesis( aMultiLangSentence[i] ) );
    self.aListSentences.append( aMultiLangSentence );
    self.nNbrLangMax = max( self.nNbrLangMax, len( aMultiLangSentence ) );
    return len( self.aListSentences ) - 1;
  # add - end

  def say( self, nID, nStyle = 0 ):
    if nStyle == 0:
      sayWithEyes2( self.getText( nID ), 1, self.bPrecompute );
    else:
      sayAndEyes( self.getText( nID ), True );
  # say - end

  # permits to get current text for various reason
  def getText( self, nID ):
    if( nID < 0 or nID >= len( self.aListSentences ) ):
      print( "LocalizedText.getText: id %d out of bound" % nID );
    if( self.nCurrentLanguage < 0 or self.nCurrentLanguage >= len( self.aListSentences[nID] ) ):
      print( "LocalizedText.getText: self.nCurrentLanguage %d out of bound" % self.nCurrentLanguage );
    return self.aListSentences[nID][self.nCurrentLanguage];
  # getText - end

  def prepareTextOneLang( self, nNumLang ):
    #leds = myGetProxy( "ALLeds" );
    if not self.bPrecompute:
      return
    setSpeakLanguage( nNumLang );
    for sentence in self.aListSentences:
      if( nNumLang < len( sentence )  ):
        txt = sentence[nNumLang];
        print( "LocalizedText.prepareAllText: preparing this text: '%s' (lang %d)" %( txt, nNumLang ) );
#        leds.post.rasta( 0.5 );
        sayAndCache( txt, True, self.bStoreToNonVolatile );

#        leds.stop( nID );
  # prepareTextOneLang - end

  def prepareAllText( self ):
    print( "LocalizedText.prepareAllText" );
    for nNumLang in range(0, self.nNbrLangMax ): # changer de langue a la volée n'est pas immédiat, donc il faut parcourir langue par langue
      self.prepareTextOneLang( nNumLang );
    # set the default language
    setSpeakLanguage( self.nCurrentLanguage );
  # prepareAllText - end

  # return the number of different text (in each lang)
  def getNbrText( self ):
    return len( self.aListSentences );
  # getNbrText - end

# class LocalizedText - end

#def sayAndEyes_ID( id_text, bWait = True, proxyDemo = False ):
#  global global_aListMessage;
#  global global_nNumLang;
#  txt = global_aListMessage[id_text * 2 + global_nNumLang];
#  sayAndEyes( txt, bWait, proxyDemo );

def setSpeakLanguage( nNumLang = getDefaultSpeakLanguage(), proxyTts = False ):
    "change the tts speak language"
    print( "SetSpeakLanguage to: %d" % nNumLang );
    if( not proxyTts ):
        proxyTts = myGetProxy( "ALTextToSpeech" );
    if( not proxyTts ):
        debug( "ERR: setSpeakLanguage: can't connect to tts" );
        return;

    try:
        if( nNumLang == naoconfig.LANG_FR ):
            proxyTts.loadVoicePreference( "NaoOfficialVoiceFrench" );
        elif ( nNumLang == naoconfig.LANG_EN ):
            proxyTts.loadVoicePreference( "NaoOfficialVoiceEnglish" );
        elif ( nNumLang == naoconfig.LANG_SP ):
            proxyTts.loadVoicePreference( "NaoOfficialVoiceSpanish" );
        elif ( nNumLang == naoconfig.LANG_IT ):
            proxyTts.loadVoicePreference( "NaoOfficialVoiceItalian" );
        elif ( nNumLang == naoconfig.LANG_GE ):
            proxyTts.loadVoicePreference( "NaoOfficialVoiceGerman" );
        elif ( nNumLang == naoconfig.LANG_CH ):
            proxyTts.loadVoicePreference( "NaoOfficialVoiceChinese" );
        elif ( nNumLang == naoconfig.LANG_PO ):
            proxyTts.loadVoicePreference( "NaoOfficialVoicePolish" );
        elif ( nNumLang == naoconfig.LANG_KO ):
            proxyTts.loadVoicePreference( "NaoOfficialVoiceKorean" );            
        else:
            proxyTts.loadVoicePreference( "NaoOfficialVoiceEnglish" );
    except:
        print( "ERR: setSpeakLanguage: loadVoicePreference error" );
# setSpeakLanguage - end

def getSpeakLanguage():
  "return the current speak language of the synthesis"
  tts = myGetProxy( "ALTextToSpeech" );
  strLang = tts.getLanguage();
  if( strLang ==  "French" ):
    return naoconfig.LANG_FR;
  elif ( strLang ==  "English" ):
    return naoconfig.LANG_EN;
  elif ( strLang ==  "Spanish" ):
    return naoconfig.LANG_SP;
  elif ( strLang ==  "Italian" ):
    return naoconfig.LANG_IT;
  elif ( strLang ==  "German" ):
    return naoconfig.LANG_GE;
  elif ( strLang ==  "Chinese" ):
    return naoconfig.LANG_CH;
  elif ( strLang ==  "Polish" ):
    return naoconfig.LANG_PO;
  elif ( strLang ==  "Korean" ):
    return naoconfig.LANG_KO;    
  else:
    return naoconfig.LANG_EN;
# getSpeakLanguage - end

def getSpeakAbbrev( nNumLang ):
    "return the lang abbreviation from a lang number"
    if( nNumLang == naoconfig.LANG_FR ):
        return 'fr';
    if( nNumLang == naoconfig.LANG_EN ):
        return 'en';
    if( nNumLang == naoconfig.LANG_SP ):
        return 'sp';
    if( nNumLang == naoconfig.LANG_IT ):
        return 'it';
    if( nNumLang == naoconfig.LANG_GE ):
        return 'ge';
    if( nNumLang == naoconfig.LANG_CH ):
        return 'ch';
    if( nNumLang == naoconfig.LANG_PO ):
        return 'po';
    if( nNumLang == naoconfig.LANG_KO ):
        return 'ko';
    return 'en'; # default ?
# getSpeakLanguage - end


def getTextForCurrentLanguage( listText ):
    "return the good text related to the current speak language"
    "eg: getTextForCurrentLanguage( ['mouse', 'souris'] ) return the good word"
    nLangIndex = -1;
    try:
        nLangIndex = getSpeakLanguage();
        return listText[nLangIndex];
    except BaseException, err:
        print( "ERR: getTextForCurrentLanguage: idx: %d, listText: %s, err: %s" % ( nLangIndex, str( listText ), str( err ) ) );
        return "getTextForCurrentLanguage: error";
# getTextForCurrentLanguage - end    

#print getTextForCurrentLanguage( ['mouse', 'souris'] );


def translateIntoNaoLanguage( strTxt ):
    "translate a text into nao language, for example: 'je suis pret' => 'ognagnouk'"
    strTxt = removeAsciiAccent( strTxt );
    strTxt = strTxt.lower();
    aSentenceList = splitMany( strTxt, ['.', ';', ',', ':', '!', '?' ] );
    print( "sentence list: " + str( aSentenceList ) );
    strTxt = "";
    for sentence in aSentenceList:
        aWordList = splitMany( sentence, [" ", "'"] );
        # vire le 'm' et ...:
        listElision = [ 'm', 't', 's' ];
        for i in range( len( aWordList ) ):
            if( i >= len( aWordList ) ):
                break;            
            if( aWordList[i] in listElision ):
                del aWordList[i];
                i -= 1;
                
        print( "word list: " + str( aWordList ) );
        
        aFinalList = [];
        nCptWord = 0;
        for i in range( len( aWordList ) ):
            if( i >= len( aWordList ) ):
                break;
            bRemove = False;
            
            if( aWordList[i] == 'je' or aWordList[i] == 'j' ):
                # sujet
                bRemove = True;
                # verbe
                if( aWordList[i+1] == 'suis' ):
                    aFinalList.append( 'gnouke' );
                elif( aWordList[i+1] == 'ai' ):
                    aFinalList.append( 'gnike' );
                elif( aWordList[i+1] == 'appelle' ):
                    aFinalList.append( 'nomouke' );
                else:
                    bRemove = False;
                if( bRemove ):
                    del aWordList[i+1]; # vire le verbe
            elif( aWordList[i] == 'pret' ):
                # adjectif
                aFinalList.insert( nCptWord, "ognaa" );
                nCptWord += 1;
            else:
                # unknown word => generation a la volée
                strTranslatedWord = "";
                nSum = 0;
                listUnchangedWord = ['nao', 'aldebaran', 'robot' ];
                if( aWordList[i] not in listUnchangedWord ):
                    listIn = ["ba", "be", "bi", "bo", "bu", "hi", "poi", "miam" ];
                    listOut = ["ab", "eb", "ib", "ob", "ub", "ih", "glo", "plouke" ];
                    nNumLetterToSkip = 0;
                    for nNumLetter in range( len( aWordList[i] ) ):
                        if( nNumLetterToSkip > 0 ):
                            nNumLetterToSkip -= 1;
                            continue;
                        ch = aWordList[i][nNumLetter];
                        
#                        strTranslatedWord += ch.upper(); # to see results
                        #strTranslatedWord += chr( ord(ch)+1 );
                        for nNumSyllabe in range( len( listIn ) ):
                            if( aWordList[i][nNumLetter:nNumLetter+len(listIn[nNumSyllabe])] == listIn[nNumSyllabe] ):
                                strTranslatedWord += listOut[nNumSyllabe];
                                nNumLetterToSkip = len( listIn[nNumSyllabe] ) - 1;
                                break;
                        else:
                            strTranslatedWord +=  ch;
                        
                        
                        nSum += ord( ch );
                    if( ( nSum % 8 ) == 1 ):
                        strTranslatedWord += 'ouke';
                    if( ( nSum % 8 ) == 2 ):
                        strTranslatedWord += 'oque';         
                else:
                    strTranslatedWord = aWordList[i].upper();
                aFinalList.insert( nCptWord, strTranslatedWord );
                nCptWord += 1;
                
        print( "aFinalList finale: " + str( aFinalList ) );
        strTxt += ' '. join( aFinalList ) + '.';
    return strTxt;
# translateIntoNaoLanguage - end

# print( translateIntoNaoLanguage( "Je m'appelle Nao. Je suis prêt. Et hier j'ai mangé des petit pois, miam miam!" ) );



def getJointListByChain():
    "return all the joint name, sorted by chain: in three list: [[head_joint], [top_joint], [bottom_joint]]"
    motion = myGetProxy( "ALMotion" );
    listJointName = motion.getJointNames('Body');
    listJointName.remove( "RHipYawPitch" ); # when using dcm: remove this joint
    listHead = filterList( listJointName, ["Head"] );
    listUp = filterList( listJointName, ["Shoulder", "Elbow", "Wrist", "Hand"] );
    listBottom = substractList( listJointName, listHead );
    listBottom = substractList( listBottom, listUp );
    return [ listHead, listUp, listBottom ];
# getJointListByChain - end


def getListJointSensorDCM( bOnlyJointName = False ):
  "return all the sensor joint name present in stm from dcm"
  motion = myGetProxy( "ALMotion" );
  listJointName = motion.getJointNames('Body');
  listJointName.remove( "RHipYawPitch" ); # when using dcm: remove this joint
  if( bOnlyJointName ):
    return listJointName;
  listJointsDCMValue = []; # la liste des clés de chaque joint dans la stm
  for strJointName in listJointName:
      listJointsDCMValue.append( "Device/SubDeviceList/%s/Position/Sensor/Value" % strJointName );
  return listJointsDCMValue;
# getListJointSensorDCM - end

def getListJointActuatorDCM( bOnlyJointName = False ):
  "return all the actuator joint name present in stm from dcm"
  motion = myGetProxy( "ALMotion" );
  listJointName = motion.getJointNames('Body');
  listJointName.remove( "RHipYawPitch" ); # when using dcm: remove this joint
  if( bOnlyJointName ):
    return listJointName;
  listJointsDCMValue = []; # la liste des clés de chaque joint dans la stm
  for strJointName in listJointName:
      listJointsDCMValue.append( "Device/SubDeviceList/%s/Position/Actuator/Value" % strJointName );
  return listJointsDCMValue;
# getListJointActuatorDCM - end

#print( "getListJointSensorDCM: " + str( getListJointSensorDCM() ) );
#print( "getListJointSensorDCM(True): " + str( getListJointSensorDCM( True ) ) );


# fait en sorte que le robot se mette en pose init
def motionSetToPosInit( rTime = 1.0, rKneeAngleInDegrees = -100.0, proxyMotion = False ):
  if( not proxyMotion ):
    proxyMotion = myGetProxy( "ALMotion" );

  if( rKneeAngleInDegrees < 0 ):
    kneeAngle = 50.0 * motion.TO_RAD;
  else:
    kneeAngle = rKneeAngleInDegrees * motion.TO_RAD;

  # Define The Initial Position
  NumJoints = len(proxyMotion.getJointNames("Body"))
  Head     = [0.0, 0.0]
  LeftArm  = [120.0* motion.TO_RAD,  20.0* motion.TO_RAD, -80.0* motion.TO_RAD, -80.0* motion.TO_RAD]
  LeftLeg  = [0.0, 0.0, -kneeAngle/2, kneeAngle, -kneeAngle/2, 0.0]
  RightLeg = [0.0, 0.0, -kneeAngle/2, kneeAngle, -kneeAngle/2, 0.0]
  RightArm = [120.0 * motion.TO_RAD, -20.0 * motion.TO_RAD, 80.0 * motion.TO_RAD, 80.0 * motion.TO_RAD]
  if (NumJoints == 26):
    LeftArm  += [0.0, 0.0]
    RightArm += [0.0, 0.0]
  pTargetAngles = Head + LeftArm + LeftLeg + RightLeg + RightArm
  ## Set balancer Off to Allow Full control of Nao Joint
  #proxyMotion.setBalanceMode( motion.BALANCE_MODE_OFF ); # DEPRECATED
  # Send angles throw a Smooth interpolation of 1s
  proxyMotion.angleInterpolation( "Body", pTargetAngles ,rTime, True );
#MotionSetToPosInit - end

def getMotionBodyJointName():
    "return a list of all joint name used by Motion"
    motion = myGetProxy( "ALMotion" );
    return motion.getJointNames('Body');
# getMotionBodyJointName - end

def getDcmBodyJointName():
    "return a list of all joint name used by the DCM"
    listJoint = getMotionBodyJointName();
    listJoint.remove( "RHipYawPitch" ); # when using dcm: remove this joint
    return listJoint;
# getMotionBodyJointName - end

global_getBodyHigherTemperature_listKeyTemp = [];
def getBodyHigherTemperature():
    mem = myGetProxy( "ALMemory" );

    global global_getBodyHigherTemperature_listKeyTemp;

    # first time: generate key list
    if( len( global_getBodyHigherTemperature_listKeyTemp ) < 1 ):
        listJointName = getDcmBodyJointName();
        for strJointName in listJointName:
            global_getBodyHigherTemperature_listKeyTemp.append( "Device/SubDeviceList/%s/Temperature/Sensor/Value" % strJointName );

    # get all temp value
    arVal = mem.getListData( global_getBodyHigherTemperature_listKeyTemp );

    rMax = 0;
    nHigherJoint = -1;
    for rVal in arVal:
        if( rVal > rMax ):
            rMax = rVal;
#    debug( "getBodyHigherTemperature: higher: joint '%s': %5.2f" % ( strHigherJoint, rMax ) );
    return rMax;
# getBodyListTemperature - end

global_computeSampledBodyConsumption_listKey = [];
def computeSampledBodyConsumption( nNbrMeasures = 3, astrJointListToReturn = [] ):
    "sample all body consumption to compute an average, then return them"
    "nNbrMeasures: nbr of samples"
    "astrJointListToReturn: joint list to return [] => All, or name of joint"
    mem = myGetProxy( "ALMemory" );

    global global_computeSampledBodyConsumption_listKey;
    # first time: generate key list
    if( len( global_computeSampledBodyConsumption_listKey ) < 1 ):
        listJointName = getDcmBodyJointName();
        for strJointName in listJointName:
            global_computeSampledBodyConsumption_listKey.append( "Device/SubDeviceList/%s/ElectricCurrent/Sensor/Value" % strJointName );


    # get all temperature value
    arSum = [];
    for i in range( nNbrMeasures ):
        if( i == 0 ):
            arSum = mem.getListData( global_computeSampledBodyConsumption_listKey );
        else:
            arVal =  mem.getListData( global_computeSampledBodyConsumption_listKey );
            for i in range( len( arSum ) ):
                arSum[i] += arVal[i];
        if( i != nNbrMeasures - 1 ):
            time.sleep( 0.011 ); # wait til next measures
    # for - end
    # compute median
    for i in range( len( arSum ) ):
        arSum[i] /= nNbrMeasures;
        
    if( astrJointListToReturn == [] or astrJointListToReturn == 'Body' or astrJointListToReturn == 'All' ):
        return arSum;
    
    # filter only wanted value
    listJointMeasured = getDcmBodyJointName();
    aValRet = [];
    for strJointName in astrJointListToReturn:
        for i in range( len( arSum ) ):
            if( listJointMeasured[i] == strJointName ):
                aValRet.append( arSum[i] );
                break;
    return aValRet;
# computeSampledBodyConsumption - end

def getHeadTemperature():
    "return the temperature of the silicium in degrees"
    try:
        file = open( "/sys/class/i2c-adapter/i2c-1/1-004c/temp2_input" );
        if( not file ):
            return -42;
    except:
            return -42;
    try:
        strTemp = file.read();    
        nTemp = int( strTemp ) / 1000;
    finally:
        file.close();
    return nTemp;
# getHeadTemperature - end



class PoseLibrary():
  "A module to store Nao position, compare position between them and help user use them"

  @staticmethod
  def getCurrentPosition():
    "get a list of joint name and their current position value in radians ['HeadYaw'=1.0; 'HeadPitch'=1.0;... work even if no stiffness"
    motion = myGetProxy( "ALMotion" );
    listJointName = motion.getJointNames('Body');
    listJointName.remove( "RHipYawPitch" ); # when using dcm: remove this joint
    listJointsDCMValue = []; # la liste des clés de chaque joint dans la stm
    for strJointName in listJointName:
      listJointsDCMValue.append( "Device/SubDeviceList/%s/Position/Sensor/Value" % strJointName );
    # add TorsoX and Y and AccZ
    listJointsDCMValue.append( "Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value" );
    listJointsDCMValue.append( "Device/SubDeviceList/InertialSensor/AngleY/Sensor/Value" );
    listJointsDCMValue.append( "Device/SubDeviceList/InertialSensor/AccZ/Sensor/Value" );
    stm = myGetProxy( "ALMemory" );
    listJointValue = stm.getListData( listJointsDCMValue );
    dicoConstructed = dict([]);
    for i in range( len( listJointName ) ):
      dicoConstructed[listJointName[i]] = listJointValue[i];
    dicoConstructed['TorsoX'] = listJointValue[len( listJointName )];
    dicoConstructed['TorsoY'] = listJointValue[len( listJointName ) + 1];
    dicoConstructed['TorsoAccZ'] = listJointValue[len( listJointName ) + 2] * math.pi / 180;
#    debug( "altools::PoseLibrary::getCurrentPosition: " + dictionnaryToString( dicoConstructed ) );
    return dicoConstructed;
  # getJointPos - end

  @staticmethod
  def getGroupDefinition():
    "get list of group, group can contains some subgroups"
    dicoGroup = {
        'All':           ['Torsos', 'Body'],
        'Torsos':      ['TorsoX','TorsoY', 'TorsoAccZ'],
        'Body':         ['UpperBody', 'BottomBody'],
        'UpperBody': ['Head', 'Arms', 'ForeArms'],
        'BottomBody': ['Legs'],
        'Head':         ['HeadYaw', 'HeadPitch'],
        'Arms':         ['LArm', 'RArm'],
        'Legs':         ['LLeg', 'RLeg'],
        'ForeArms':   ['LForeArms', 'RForeArms'],
        'LArm':         ['LShoulderPitch','LShoulderRoll','LElbowRoll', 'LElbowYaw'],
        'RArm':         ['RShoulderPitch','RShoulderRoll','RElbowRoll', 'RElbowYaw'],
        'LLeg':         ['LHipYawPitch','LHipPitch','LHipRoll', 'LKneePitch', 'LAnkleRoll', 'LAnklePitch' ],
        'RLeg':         ['LHipYawPitch','RHipPitch','RHipRoll', 'RKneePitch', 'RAnkleRoll', 'RAnklePitch' ],
        'LForeArms': ['LWristYaw','LHand' ],
        'RForeArms': ['RWristYaw','RHand' ],
    };
    return dicoGroup;
    # getGroupDefinition - end
    
  @staticmethod
  def getListJoints( listGroup, bRemoveHipYawPitch = False ):
    "get list of joints from a group name or a list of group"
    dicoGroup = PoseLibrary.getGroupDefinition();
    bGroupExploded = True;
    while( bGroupExploded ):
        listGroupExploded = [];
        bGroupExploded = False;
        for group in listGroup:
#            debug( "group: " + str( group ) );
            if( group in dicoGroup ):
                listGroupExploded.extend( dicoGroup[group] );
#                debug( "listGroupExploded: " + str( listGroup ) );
                bGroupExploded = True; # begin another time, because there's some new group
            else:
                listGroupExploded.append( group ); # here group is just a joint name
        listGroup = listGroupExploded;
        
    if( bRemoveHipYawPitch ):        
        for i in range( len( listGroup ) ):
            if( i >= len( listGroup ) ):
                break; # la liste diminue en direct
            if( listGroup[i] in [ "RHipYawPitch", "LHipYawPitch" ] ):
                del listGroup[i];
                i -=1;

    return listGroup;
    # getListJoints - end
    
  @staticmethod
  def getGroupLimits( listGroup, rCoef = 1., bOrderedByMinMax = False ):
    "get list of limits from a group name or a list of group"
    "rCoef: you can reduce the list by a ratio (0.5, will get halt the limits)"    
    "order default: list of min,max,acc for each joint"
    "order bOrderedByMinMax: list of min of each joint, then list of max of each joint..."
    listJoints = PoseLibrary.getListJoints( listGroup );
    listLimits = [];
    if( bOrderedByMinMax ):
        listLimits = [[],[],[]];
    motion = myGetProxy( 'ALMotion' );
    for strJointName in listJoints:
        limitForThisJoint = motion.getLimits( strJointName );
        # gestion 1.7.25 et rétrocompatibilité
        if( len( limitForThisJoint ) > 1 ):
            limitForThisJoint = limitForThisJoint[1];
        limitForThisJoint = limitForThisJoint[0];
        print( "getGroupLimits: %s => %s" % ( strJointName, str( limitForThisJoint ) ) );
        if( not bOrderedByMinMax ):
            limitForThisJoint[0] *= rCoef;
            limitForThisJoint[1] *= rCoef;
            limitForThisJoint[2] *= rCoef;            
            listLimits.append( limitForThisJoint );
        else:
            listLimits[0].append( limitForThisJoint[0]*rCoef );
            listLimits[1].append( limitForThisJoint[1]*rCoef );
            listLimits[2].append( limitForThisJoint[2]*rCoef );
    return listLimits;
    # getGroupLimits - end    

  @staticmethod
  def filterPosition( aPos, listGroupToRemove ):
    "remove a group of joint from a position"
    "strGroupToRemove can contains a joint or a torso/gyro, or one of the groups in the dicoGroup: (ask for getGroupDefinition to see complete list of group)"
    # construct the list of joint with group transformed in a list of joint name
    dicoGroup = PoseLibrary.getGroupDefinition();
#    debug( "dicoGroup:" + str( dicoGroup ) );
    bGroupExploded = True;
    while( bGroupExploded ):
      listGroupExploded = [];
      bGroupExploded = False;
      for group in listGroupToRemove:
#        debug( "group: " + str( group ) );
        if( group in dicoGroup ):
            listGroupExploded.extend( dicoGroup[group] );
#            debug( "listGroupExploded: " + str( listGroupExploded ) );
            bGroupExploded = True; # begin another time, because there's some new group
        else:
            listGroupExploded.append( group ); # here group is just a joint name
      listGroupToRemove = listGroupExploded;
    debug( "altools::PoseLibrary::filterPosition: final joint list to remove: %s" % str( listGroupToRemove ) );
    for strJointName in listGroupToRemove:
      if( strJointName in aPos ):
        del aPos[strJointName];
    return aPos;
  # filterPosition - end

  @staticmethod
  def setPosition( aPosToSet, rTimeSec = 1.2, bWaitEnd = True ):
    "set a position on Nao (with optionnal time in sec to go to the position)"
    motion = myGetProxy( "ALMotion" );
    aJointName = [];
    aPos = [];
    for k, v in aPosToSet.iteritems():
        if( k.find( "Torso" ) == -1 ):
            aJointName.append( k );
            aPos.append( v );
    if( bWaitEnd ):
        motion.angleInterpolation( aJointName, aPos, rTimeSec, True );
        return -1;
    nId = motion.post.angleInterpolation( aJointName, aPos, rTimeSec, True );
    return nId;

  # setPosition - end
  
  @staticmethod
  def setPositionWithSpeed( aPosToSet, nSpeed = 30, bWaitEnd = True ):
    "set a position on Nao (with optionnal speed in % to go to the position)"
    "if not bWaitEnd return a post call threaded method id"
    motion = myGetProxy( "ALMotion" );
    aJointName = [];
    aPos = [];
    for k, v in aPosToSet.iteritems():
        if( k.find( "Torso" ) == -1 ):
            aJointName.append( k );
            aPos.append( v );
    if( bWaitEnd ):
        motion.angleInterpolationWithSpeed( aJointName, aPos, nSpeed/100. );
        return -1;
    nId = motion.post.angleInterpolationWithSpeed( aJointName, aPos, nSpeed/100. );
    return nId;
  # setPositionWithSpeed - end
  
  @staticmethod  
  def interpolatePosition( aPos1, aPos2, rRatio = 0.5 ):
    "create a position intermediary between two positions if rRatio is 0. => pos1, if at 1. => pos2"
    "rRatio in [0.,1.]"
    listPosResult = {};
    rRatio = limitRange( rRatio, 0., 1. );
    for k, v in aPos1.iteritems():
        if( k in aPos2 ):
            listPosResult[k] = v * ( 1. - rRatio ) + aPos2[k] * rRatio;
    return listPosResult;
  # interpolatePosition - end
  
  @staticmethod  
  def interpolatePositionXY( aPosTR, aPosTL, aPosBR, aPosBL, rX = 0.0, rY = 0.0 ):
    "create a position intermediary at the center of four positions"
    "rX et rY in [-1.,1.]"
    "TR: Top Right( -1,-1), aPosTL: Top Left TR: Top Right, BL: Bottom Left, BR: Bottom Right(1,1)"
    rX_Normalised = (rX+1.) /2.;
    rY_Normalised = (rY+1.) /2.;
    listPosResultTRL = PoseLibrary.interpolatePosition( aPosTR, aPosTL, rX_Normalised );
    listPosResultBRL = PoseLibrary.interpolatePosition( aPosBR, aPosBL, rX_Normalised);
    listPosResult = PoseLibrary.interpolatePosition( listPosResultBRL, listPosResultTRL, rY_Normalised );
    return listPosResult;
  # interpolatePositionXY - end    

  @staticmethod  
  def interpolatePositionXY6( aPosTR, aPosTC, aPosTL, aPosBR, aPosBC, aPosBL, rX = 0.0, rY = 0.0 ):
    "create a position intermediary at the center of 6 positions (4 corner and two center)"
    "rX et rY in [-1.,1.]"
    "TR: Top Right( -1,-1), aPosTL: Top Left TR: Top Right, BL: Bottom Left, BR: Bottom Right(1,1)"
    "aPosTC: Top Center, aPosBC: Bottom Center"
    rX_Normalised = (rX+1.) /2.;
    rY_Normalised = (rY+1.) /2.;
    if( rX_Normalised < 0.5 ):        
        rX_Normalised *= 2; # ramene sur 0..1
        listPosResultTRL = PoseLibrary.interpolatePosition( aPosTR, aPosTC, rX_Normalised );
        listPosResultBRL = PoseLibrary.interpolatePosition( aPosBR, aPosBC, rX_Normalised);
    else:
        rX_Normalised = ( rX_Normalised - 0.5 ) * 2; # ramene sur 0..1
        listPosResultTRL = PoseLibrary.interpolatePosition( aPosTC, aPosTL, rX_Normalised );
        listPosResultBRL = PoseLibrary.interpolatePosition( aPosBC, aPosBL, rX_Normalised);        
    listPosResult = PoseLibrary.interpolatePosition( listPosResultTRL, listPosResultBRL, rY_Normalised );
    return listPosResult;
  # interpolatePositionXY - end
  
  @staticmethod  
  def getEmotionPose( bAddNeutral = False ):
    "return a list of 6 dictionnary of pose"
    "if bAddNeutral: add a seven neutral pose"
    import list_emotion_poses;
    listPose = [];
    listPose.extend( list_emotion_poses.listPoses ); # listPose = list_emotion_poses.listPoses ne ferait qu'un pointeur sur l'objet, et donc quand on append la neutralpose, ca ajoute a la liste du module, beurk.
    if( bAddNeutral ):
        listPose.append( list_emotion_poses.poseNeutral );
    return listPose;
  # getEmotionPose - end
  
  @staticmethod  
  def interpolateEmotion( arListRatio, rNeutral = 0. ):
    "create a position intermediary mixed from 6 emotions and a neutral"
    "arListRatio: the ratio of each emotions: [Proud, Happy, Excitement, Fear, Sadness, Anger]"
    "             if sum is greater than 1, it would be normalised"
    "             if sum is lower than 1, a neutral position would be added"
    "rNeutral:    to force an addition of a proportion of the neutral pose"
    
    # preparatio of the ratio
    rSum = arraySum( arListRatio );
    rEpsilon = 0.001;
    if( rNeutral < rEpsilon and rSum < 1. ):
        rNeutral = 1. - rSum;
    rSumTotal = rSum + rNeutral;
    if( rSumTotal > 1. ):
        # normalisation
        for i in range( len( arListRatio ) ):
            arListRatio[i] /= rSumTotal;
        rNeutral /= rSumTotal;
    
    # push zeroes for others emotions:
    for i in range( len( arListRatio ), 6 ):
        arListRatio.append( 0. );
    
    print( "interpolateEmotion: using emotions ratio: %s and neutral ratio: %f" % ( str( arListRatio ), rNeutral ) );

    arListRatio.append( rNeutral );
    listPosEmotion = PoseLibrary.getEmotionPose( True ); # True => ajoute la neutre !
    print( "listPosEmotion has %d poses" % len( listPosEmotion ) );
    listPosResult = {};
    for k, v in listPosEmotion[0].iteritems():
        rVal = v * arListRatio[0];
        bKeyInAllPos = True;
        for i in range( 1, len( listPosEmotion ) ):
            if( k in listPosEmotion[i] ):                
                rVal += listPosEmotion[i][k] * arListRatio[i];                
            else:
                bKeyInAllPos = False;
        if( bKeyInAllPos ):
            listPosResult[k] = rVal;
    # for - end
    
    return listPosResult;
    
  # interpolateEmotion - end    
  

  @staticmethod
  def positionToString( aPos ):
    "format a position to print it"
    return dictionnaryToString( aPos );
  # positionToString - end

  @staticmethod
  def getDifferentJoints( aPosToCompare, rThreshold = 0.12 ):
    "return the list of joint that has a difference between a specific position and nao current position"
    listDiff = [];
    dicoCurrentPos = PoseLibrary.getCurrentPosition();
    for k, v in dicoCurrentPos.iteritems(): # not optimal: should iterate on aPosToCompare !
      if( k in aPosToCompare ):
        rDiff = abs( v - aPosToCompare[k] );
        if( rDiff > rThreshold ):
          debug( "difference on key %s (%f -> %f (diff:%f))" %( k, aPosToCompare[k], v, rDiff ) );
          listDiff.append( k );
    return listDiff;
  # getDifferentJoints - end
  
  
  @staticmethod
  def comparePosition( aPosToCompare, aListGroupToIgnore = [] ):
    "compare a specific position of nao with current position"
    "aPosToCompare is a dictionnary of some angles; eg: dict(  [ ('LArm', 1.32), ('HeadYaw', 0.5), ('TorsoX', 0.5) ] );"
    "aListGroupToIgnore is a mixed type list of joint or group to ignore for comparison"
    "It will return the median of absolute difference of joints in radians"
#    debug( "len( aPosToCompare ): " + str( len( aPosToCompare ) ) );
    if( len( aPosToCompare ) < 1 ):
      return 421.0; # surely some sort of error => return a big value
    dicoCurrentPos = PoseLibrary.getCurrentPosition();
    if( len( aListGroupToIgnore ) > 0 ):
        dicoCurrentPos = PoseLibrary.filterPosition( dicoCurrentPos, aListGroupToIgnore );
    rDiffSum = 0.0;
    nNbrComp = 0;
    for k, v in dicoCurrentPos.iteritems(): # not optimal: should iterate on aPosToCompare !
      if( k in aPosToCompare ):
        rDiff = abs( v - aPosToCompare[k] );
#        if( k == 'TorsoAccZ' ):
#          rDiff *= 8; # This value is important and very small compared to others
        rDiffSum += rDiff;
        nNbrComp += 1;
    debug( "altools::PoseLibrary::comparePosition:\ncurrent: %s\ncomp: %s\n=> %f/%d = %f" % ( str(dicoCurrentPos), str(aPosToCompare), rDiffSum, nNbrComp, rDiffSum / nNbrComp ) );
    return rDiffSum / nNbrComp;
  # comparePosition - end

  @staticmethod
  def getPosition_Standing():
    "get the standard standing position"
    return {
      'TorsoX': 0.0,
      'TorsoY': 0.0,
      'LAnklePitch': 0.010696,
      'LAnkleRoll': 0.058334,
      'LHipPitch': 0.010780,
      'LHipRoll': -0.050580,
      'LHipYawPitch': 0.007712,
      'LKneePitch': 0.009162,
      'RAnklePitch': 0.007712,
      'RAnkleRoll': -0.055182,
      'RHipPitch': 0.010696,
      'RHipRoll': 0.053732,
      'RKneePitch': 0.004644,
    };
  # getPosition_Standing - end
  @staticmethod
  def getPosition_Sitting():
    "get the official sitting position - without anklepitch due to ankle limitation far distant from real range"
    "now it's the new one WITH the ankle pitch"
    return {
    'HeadPitch': -0.0215179622173,
    'HeadYaw': 0.0260360389948,
    'LAnklePitch': 0.888144075871,
    'LAnkleRoll': 0.0123139619827,
    'LElbowRoll': -0.977116048336,
    'LElbowYaw': -0.733294010162,
    'LHand': 0.238207533956,
    'LHipPitch': -1.59992003441,
    'LHipRoll': 0.233209967613,
    'LHipYawPitch': -0.717870056629,
    'LKneePitch': 1.37442207336,
    'LShoulderPitch': 0.969446063042,
    'LShoulderRoll': 0.20551404357,
    'LWristYaw': -0.593699991703,
    'RAnklePitch': 0.879023969173,
    'RAnkleRoll': -0.0383080393076,
    'RElbowRoll': 0.882091999054,
    'RElbowYaw': 0.562936067581,
    'RHand': 0.314207285643,
    'RHipPitch': -1.59846997261,
    'RHipRoll': -0.162562042475,
    'RKneePitch': 1.41592395306,
    'RShoulderPitch': 0.874421954155,
    'RShoulderRoll': -0.196393966675,
    'RWristYaw': 0.860532045364,
    'TorsoAccZ': -0.994837673637,
    'TorsoX': -0.0542904734612,
    'TorsoY': -0.181328982115,
    };
  # getPosition_Sitting - end
  @staticmethod
  def getPosition_Crouching():
    "get the standard crouching position"
    return {
        'TorsoX': 0.010472,
        'TorsoY': -0.066323,
        'LAnklePitch': -1.193494,
        'LAnkleRoll': 0.093616,
        'LHipPitch': -0.774628,
        'LHipRoll': -0.091998,
        'LHipYawPitch': -0.237728,
        'LKneePitch': 2.181306,
        'RAnklePitch': -1.233294,
        'RAnkleRoll': -0.102736,
        'RHipPitch': -0.747100,
        'RHipRoll': 0.096684,
        'RKneePitch': 2.187526,
    };
  # getPosition_Crouching - end
  @staticmethod
  def getPosition_LyingBack():
    "get torsos from lying on his back"
    return {
      'TorsoX': 0.015708,
      'TorsoY': -1.548107,
    };
  # getPosition_LyingBack - end
  @staticmethod
  def getPosition_LyingFront():
    "get torsos from lying on his front"
    return {
      'TorsoX': -0.048869,
      'TorsoY': 1.338667,
    };
  # getPosition_LyingFront - end
  @staticmethod
  def getPosition_LyingLeft():
    "get Torsos from lying on his left"
    return {
    'TorsoX': -1.361357,
    'TorsoY': -0.034907,
  };
  # getPosition_LyingLeft - end
  @staticmethod
  def getPosition_LyingRight():
    "get Torsos from lying on his right"
    return {
      'TorsoX': 1.307252,
      'TorsoY': -0.050615,
    };
  # getPosition_LyingRight - end
  @staticmethod
  def getPosition_HeadDown():
    "get Torsos head down"
    return {
      'TorsoAccZ': 0.890118,
      'TorsoX': 0.0,
      'TorsoY': 0.0,
    };
  # getPosition_HeadDown - end

  # Various position - funny position
  @staticmethod
  def getPosition_Victory():
    "Nao's has win, and he is very happy !"
    return {
        'TorsoX': 0.001746,
        'TorsoY': -1.024508,
        'HeadPitch': -0.786984,
        'HeadYaw': 0.021434,
        'LAnklePitch': 0.526120,
        'LAnkleRoll': 0.325250,
        'LElbowRoll': -0.338972,
        'LElbowYaw': -0.348260,
        'LHipPitch': 0.500126,
        'LHipRoll': 0.777780,
        'LHipYawPitch': 0.779314,
        'LKneePitch': 1.998760,
        'LShoulderPitch': -0.069072,
        'LShoulderRoll': 0.635034,
        'RAnklePitch': 0.823800,
        'RAnkleRoll': -0.134950,
        'RElbowRoll': 0.572224,
        'RElbowYaw': -0.024586,
        'RHipPitch': 0.503110,
        'RHipRoll': -0.776162,
        'RKneePitch': 1.879192,
        'RShoulderPitch': -0.044444,
        'RShoulderRoll': -0.767042,
    };
  # getPosition_Victory - end
  @staticmethod
  def getPosition_ExtendedKickRight():
    "Nao's kick / sun !"
    return {
        'HeadPitch': -0.050664,
        'HeadYaw': -0.079810,
        'LAnklePitch': -0.102820,
        'LAnkleRoll': 0.168782,
        'LElbowRoll': -0.142620,
        'LElbowYaw': -0.645856,
        'LHipPitch': 0.104354,
        'LHipRoll': 0.434164,
        'LHipYawPitch': -0.170232,
        'LKneePitch': 0.009162,
        'LShoulderPitch': 1.052282,
        'LShoulderRoll': 1.570774,
        'RAnklePitch': 0.323716,
        'RAnkleRoll': -0.165630,
        'RElbowRoll': 0.010780,
        'RElbowYaw': 0.940300,
        'RHipPitch': -0.302240,
        'RHipRoll': -0.740880,
        'RKneePitch': 0.003110,
        'RShoulderPitch': 0.833004,
        'RShoulderRoll': -1.586198,
        'TorsoAccZ': -0.890118,
        'TorsoX': -0.523599,
        'TorsoY': 0.022689,
    };
  # getPosition_ExtendedKickRight - end
  @staticmethod
  def getPosition_SittingFeetUp():
    "Nao's sit with feet up !"
    return {
      'LAnklePitch': -0.661196,
      'LAnkleRoll': 0.046062,
      'LElbowRoll': -0.233126,
      'LElbowYaw': -0.748634,
      'LHipPitch': -1.464928,
      'LHipRoll': 0.245482,
      'LHipYawPitch': -0.498508,
      'LKneePitch': 0.477032,
      'LShoulderPitch': 1.576910,
      'LShoulderRoll': 0.291418,
      'RAnklePitch': -0.817580,
      'RAnkleRoll': -0.187106,
      'RElbowRoll': 0.052198,
      'RElbowYaw': 0.944902,
      'RHipPitch': -1.541712,
      'RHipRoll': -0.064386,
      'RKneePitch': 0.624380,
      'RShoulderPitch': 1.580062,
      'RShoulderRoll': -0.294570,
      'TorsoX': 0.038397,
      'TorsoY': -0.041888,
    };
  # getPosition_SittingFeetUp - end

  @staticmethod
  def getPosition_SittingFeetUpLegsJoint():
    "Nao's sit with feet up and legs joint (sage)!"
    return {
        'HeadPitch': -0.1,  # the head raise a little
        'HeadYaw': 0.0,
        'LAnklePitch': -0.251618,
        'LAnkleRoll': 0.001576,
        'LElbowRoll': -1.460326,
        'LElbowYaw': -0.710284,
        'LHipPitch': -1.463394,
        'LHipRoll': 0.012314,
        'LHipYawPitch': 0.032256,
        'LKneePitch': -0.072140,
        'LShoulderPitch': 1.533958,
        'LShoulderRoll': 0.165630,
        'RAnklePitch': -0.211650,
        'RAnkleRoll': -0.012230,
        'RElbowRoll': 1.518702,
        'RElbowYaw': 0.964844,
        'RHipPitch': -1.472682,
        'RHipRoll': -0.030638,
        'RKneePitch': -0.073590,
        'RShoulderPitch': 1.596936,
        'RShoulderRoll': -0.016916,
        'TorsoAccZ': -1.029744,
        'TorsoX': 0.043633,
        'TorsoY': -0.062832,
    };
  # getPosition_SittingFeetUpLegsJoint - end

  @staticmethod
  def getPosition_StandingPackShot():
    "Nao's nice standing (packshot)!"
    return {
      'HeadPitch': -0.108956,
      'HeadYaw': 0.240796,
      'LAnklePitch': -0.069072,
      'LAnkleRoll': -0.052114,
      'LElbowRoll': -0.915756,
      'LElbowYaw': -1.083046,
      'LHand': 0.731297,
      'LHipPitch': 0.493368,
      'LHipRoll': 0.069072,
      'LHipYawPitch': -0.213184,
      'LKneePitch': 0.009162,
      'LShoulderPitch': 1.472598,
      'LShoulderRoll': 0.214718,
      'LWristYaw': -1.578528,
      'RAnklePitch': -0.245398,
      'RAnkleRoll': 0.033790,
      'RElbowRoll': 1.073842,
      'RElbowYaw': 0.747016,
      'RHand': 0.044026,
      'RHipPitch': 0.490954,
      'RHipRoll': -0.091998,
      'RKneePitch': 0.136568,
      'RShoulderPitch': 1.630684,
      'RShoulderRoll': -0.434164,
      'RWristYaw': 0.141086,
      'TorsoAccZ': -1.064651,
      'TorsoX': 0.001746,
      'TorsoY': -0.146608,
    };
  # getPosition_StandingPackShot - end

  @staticmethod
  def getPosition_StandingWalk():
    "Nao's standing like before or after walking!"
    return {
      'LAnklePitch': -0.458708,
      'LAnkleRoll': 0.024586,
      'LElbowRoll': -0.518450,
      'LElbowYaw': -1.474216,
      'LHipPitch': -0.472430,
      'LHipRoll': 0.0,
      'LHipYawPitch': 0.001576,
      'LKneePitch': 0.885076,
      'LShoulderPitch': 1.734912,
      'LShoulderRoll': 0.256136,
      'RAnklePitch': -0.490838,
      'RAnkleRoll': -0.088930,
      'RElbowRoll': 0.518534,
      'RElbowYaw': 1.472598,
      'RHipPitch': -0.490922,
      'RHipRoll': 0.0,
      'RKneePitch': 0.908170,
      'RShoulderPitch': 1.753404,
      'RShoulderRoll': -0.250084,
      'TorsoAccZ': -0.977384,
      'TorsoX': 0.008727,
      'TorsoY': 0.155334,
    };
  # getPosition_StandingWalk - end


  @staticmethod
  def getPosition( strPosition ):
    "get a standard position"
    "eg: getPosition( 'Standing' )"
    methodName = "getPosition_" + strPosition;
    try:
      func = getattr( PoseLibrary, methodName );
    except AttributeError:
      print( "altools::PoseLibrary::isPosition(): ERR: unknown position '%s'" % strPosition );
      return {};
    return func();
  # getPosition - end

  @staticmethod
  def getListPosition():
    "get the list of position name currently in the library"
    return [
                  'Standing',
                  'Sitting',
                  'Crouching',
                  'LyingBack',
                  'LyingFront',
                  'LyingLeft',
                  'LyingRight',
                  'HeadDown',
                  'Victory',
                  'ExtendedKickRight',
                  'SittingFeetUp',
                  'SittingFeetUpLegsJoint',
                  'StandingPackShot',
                  'StandingWalk'
              ];
  # getPosition - end

  @staticmethod
  def isPosition( strPosition ):
    "are we in a specific position?"
    "eg:  isPosition( 'Standing' )"
    return PoseLibrary.comparePosition( PoseLibrary.getPosition( strPosition ) ) < 0.1;
  # isPosition - end

  @staticmethod
  def findNearestPosition( aListPosition = None, aListGroupToIgnore = [] ):
    "find nearest position between some known or specific position"
    "aListPosition is a mixed type list: eg: [ 'Sitting', 'Standing', {'TorsoX': 0.005236, 'TorsoY': 0.001745 } ]"
    "aListGroupToIgnore is a mixed type list of joint or group to ignore for comparison"
    "return an array [position, distance to this position, name of position (if this position has a name)]"
    if( aListPosition == None ):
      aListPosition = PoseLibrary.getListPosition();
    rDistMin = 1000.0;
    strNameMin = "";
    posMin = dict();
    for pos in aListPosition:
      strName = "";
      if( isString( pos ) ):
        strName = pos;
        pos = PoseLibrary.getPosition( strName );
      rDist = PoseLibrary.comparePosition( pos, aListGroupToIgnore ); # here it's not optimal, at every call we will compute the current position
#      print( "rDist: %f" % rDist );
      if( rDist < rDistMin ):
        rDistMin = rDist;
        strNameMin = strName;
        posMin = pos;
    debug( "findNearestPosition between %s:"  % aListPosition );
    debug( "posMin: %s\ndistMin: %f\nName: '%s'" % ( str( posMin), rDistMin, strNameMin ) );
    return [ posMin, rDistMin, strNameMin ];
  # findNearestPosition - end

  @staticmethod
  def exportToXar( aPos, rTime = 0.0 ):
    "Export a specifig position to a xar"
    "the name of the xar is returned"
    "eg:  exportToXar( getPosition( 'Standing' ) )"

    # On charge un sample, et on va juste poker notre liste de clés au milieu
    bError = False;
    try:
        file = open( getApplicationSharedPath() + "PoseLibrary_sample.xar", 'r' );
        strBufferSample = file.read();
    except:
        bError = True;
    finally:
        file.close();
    if( bError ):
        print( "PoseLibrary:exportToXar: read file error" );
        return None;

    strListPose = "<!-- a pose containing %d motors -->\n" % len( aPos );
    strListPose +=  "<MotionKeyframe>\n";
    strListPose +=  "  <name>keyframe%d</name>\n" % 1;
    strListPose +=  "  <index>%d</index>\n" % ( 25 + int( rTime / 25 ) );   # we act as if running at 25 fps
    strListPose +=  "  <interpolation>1</interpolation>\n";
    strListPose +=  "  <Motors>\n";
    for k, v in aPos.iteritems():
      if( k.find( "Torso" ) == -1 ):
        strListPose +=  "  <Motor>\n";
        strListPose +=  " <name>%s</name>\n" % k;
        strListPose +=  " <value>%5.6f</value>\n" % ( v * 180 / math.pi );
        strListPose +=  "  </Motor>\n";
    strListPose +=  "  </Motors>\n";
    strListPose +=  "</MotionKeyframe>\n";

    strBufferSample = strBufferSample % strListPose;
    strFilename = "/home/nao/PoseLibrary_exported_%d.xar" % time.clock();
    print( "PoseLibrary.exportToXar: outputting position to %s" % strFilename );
    try:
        file = open( strFilename, 'w' );
        file.write( strBufferSample );
        file.close();
    except:
        print( "PoseLibrary:exportToXar: write file error" );        
        return None;
    return strFilename;
  # exportToXar - end

# class PoseLibrary - end

# PoseLibrary Test Zone:
#print( PoseLibrary.getCurrentPosition() );
#print( "PoseLibrary.isPosition : %d" % PoseLibrary.isPosition( "Standing" ) );
#PoseLibrary.setPosition( PoseLibrary.getPosition( "Standing" ) );
#print( "PoseLibrary.getPos: %s" % dictionnaryToString( PoseLibrary.filterPosition( PoseLibrary.getCurrentPosition(), ["Arms"] ) ) );
#print( "PoseLibrary.getPos: %s" % dictionnaryToString( PoseLibrary.filterPosition( PoseLibrary.getCurrentPosition(), ["UpperBody", "Torsos"] ) ) ); # remove all but legs
#print( "PoseLibrary.getPos: %s" % dictionnaryToString( PoseLibrary.filterPosition( PoseLibrary.getCurrentPosition(), ["Body"] ) ) );
#PoseLibrary.exportToXar( PoseLibrary.getPosition( 'Standing' ) );
#print( PoseLibrary.positionToString( PoseLibrary.getPosition( 'Standing' ) ) );
#print( PoseLibrary.findNearestPosition( [ 'Sitting', 'Standing', {'TorsoX': 0.5, 'TorsoY': 0.5} ] ) );
#print( PoseLibrary.findNearestPosition( [ 'Standing', 'HeadDown' ]) );
#print( PoseLibrary.findNearestPosition() );
#print( "Current Pos: " + PoseLibrary.positionToString( PoseLibrary.getCurrentPosition() ) );
#PoseLibrary.getDifferentJoints( PoseLibrary.getPosition( 'Standing' ) );
#PoseLibrary.getDifferentJoints( PoseLibrary.getPosition( 'Sitting' ) );
#PoseLibrary.setPosition( PoseLibrary.getPosition( "Sitting" ) );
#print( "All joints name: " + str( PoseLibrary.getListJoints( ["Body"] ) ) );
#print( "All joints limits: " + str( PoseLibrary.getGroupLimits( ["Body"], 0.5, True ) ) );


def isPlugged():
    "is nao plugged to its charger"
    stm = myGetProxy( "ALMemory" );
    rElectricConsumption = stm.getData( "Device/SubDeviceList/Battery/Current/Sensor/Value", 0 ); # todo: ajouter un test que l'usb marche...
    nCurrentState = stm.getData( "ALSentinel/BatteryLevel", 0 );
    bPlugged = rElectricConsumption > 0.01 or nCurrentState == 5;
    return bPlugged;
# isPlugged - end

def isInPackaging():
    "is nao in it's transport packaging box"
    stm = myGetProxy( "ALMemory" );
    rAccX = abs( stm.getData( "Device/SubDeviceList/InertialSensor/AccX/Sensor/Value", 0 ) + 52 ); # on enleve - 52 ainsi le resultat doit etre proche de 0
    rAccY = abs( stm.getData( "Device/SubDeviceList/InertialSensor/AccY/Sensor/Value", 0 ) + 2 );
    rAccZ = abs( stm.getData( "Device/SubDeviceList/InertialSensor/AccZ/Sensor/Value", 0 ) + 8 );

    debug( "isInPackaging: " + str( rAccX ) );
    rLimit = 5;
    bInBox = rAccX < rLimit and rAccY < rLimit and rAccZ < rLimit;
    return bInBox;
# isInPackaging - end

def setWifi( bOnOrOff ):
  "stop the wifi connection (si bOnOrOff is set to True reactivate it)"
  strStartOrNot = "stop";
  if( bOnOrOff ):
    strStartOrNot = "start";
  try:
    mySystemCall( "/etc/init.d/wireless.sh " + strStartOrNot );
  except BaseException, err:
    debug( "setWifi: Exception catched: %s" % err );

#SetWifi - end


def changeAngleTimed( strJointName, rIncrement, rTime, bWait = True ):
	# will change a joint from it's current position to current+inc in a certain time
	motion = myGetProxy( "ALMotion" );
	rCurAngle = motion.getAngles( strJointName, True )[0];
	if( bWait ):
		motion.  call( "angleInterpolation", strJointName, rCurAngle + rIncrement, rTime, True );
	else:
		motion.pCall( "angleInterpolation", strJointName, rCurAngle + rIncrement, rTime, True );
# changeAngleTimed - end

# DEPRECATED !
def lightLedsCircle():
  "does a circle in the face led (deprecated?)"
  myLeds = myGetProxy( "ALLeds" );
  rTime = 1.0;
  for i in range( 8 ):
    myLeds.fadeRGB( "FaceLed%d" % i , 0x808080, rTime );
  time.sleep( rTime );
  myLeds.fadeRGB( "FaceLeds" , 0x0000FF, rTime );
# LightLedsCircle - end

def analyseSound_pause( bWaitForResume ):
    "pause some running sound analyse"
    "bWaitForResume: True => pause until resume call, False => pause a little times (5sec?)"
    try:
        analyser = myGetProxy( "UsageNoiseExtractor" );
        nTime = 5;
        if( bWaitForResume ):
            nTime = -1;
        analyser.inhibitSoundAnalyse( nTime );
    except BaseException, err:
        debug( "WRN: analyseSound_pause: " + str( err ) );
# analyseSound_pause - end

def analyseSound_resume( bWaitForResume ):
    "resume a previously infinite paused sound analyse"
    if( bWaitForResume ):
        try:
            analyser = myGetProxy( "UsageNoiseExtractor" );
            analyser.inhibitSoundAnalyse( 0 );
        except BaseException, err:
            debug( "WRN: analyseSound_resume: " + str( err ) );
# analyseSound_resume - end
        

# joue un son depuis appu/data/wav
def playSound( strFilename, bWait = True, bNaoqiSound = False, bDirectPlay = False, nSoundVolume = 100, bPauseSoundAnalysis = True ):
  "nSoundVolume: if bDirectPlay is on, will play the sound with a specific volume (ndev)"
  #print( "appuPlaySound: avant cnx sur audioplayer (ca lagge?)" );
  #myAP = myGetProxy( "ALAudioPlayer" );
  #print( "appuPlaySound: apres cnx sur audioplayer (ca lagge?)" );
  if( naoconfig.bRemoveDirectPlay ):
    print( "WRN: DISABLING_DIRECTPLAY SETTINGS for testing/temporary purpose" );
    bDirectPlay = False;
    
  try:
    global_proxyAudioPlayer = myGetProxy( "ALAudioPlayer" );

    # If strFilename has an absolute path, go ahead with this path !
    if strFilename.startswith( getDirectorySeparator() ):
        strSoundFile = strFilename
    else:
        if( not bNaoqiSound ):
            strSoundFile = getApplicationSharedPath() + "wav/0_work_free/" + strFilename;
            if( not isFileExists( strSoundFile ) ):
                # then try another path
                strSoundFile = getApplicationSharedPath() + "wav/1_validated/" + strFilename;
            if( not isFileExists( strSoundFile ) ):
                # and another path
                strSoundFile = getApplicationSharedPath() + "wav/0_work_copyright/" + strFilename;
            if( not isFileExists( strSoundFile ) ):
                # and another path
                strSoundFile = getApplicationSharedPath() + "wav/" + strFilename;
            if( not isFileExists( strSoundFile ) ):
                print( "appu.playSound: can't find file '%s'" % strFilename );
        else:
            strSoundFile = getNaoqiPath() + "/share/naoqi/wav/" + strFilename;

    if( bPauseSoundAnalysis ):
        analyseSound_pause( bWait );
    if( bDirectPlay ):
        mySystemCall( "aplay -q " + strSoundFile, bWait );
    else:
        if( bWait ):
            global_proxyAudioPlayer.playFile( strSoundFile );
        else:
            global_proxyAudioPlayer.post.playFile( strSoundFile );
    analyseSound_resume( bWait ); # on le remet, meme si on l'avait pas pausé!
  except BaseException, err:
    debug( "playSound: ERR: " + str( err ) );

    pass

  #if( not bNaoqiSound ):
  #  strSoundFile = getApplicationSharedPath() + "/wav/" + strFilename;
  #else:
  #  strSoundFile = getNaoqiPath() + "/data/wav/" + strFilename;
  #mySystemCall( "aplay" + " " +  strSoundFile, bWait );

# playSound - end

def playMusic( strFilename, bWait, bNaoqiSound = False ):
  print( "appuPlaySound: avant cnx sur audioplayer (ca lagge?)" );
  #myAP = myGetProxy( "ALAudioPlayer" );
  print( "appuPlaySound: apres cnx sur audioplayer (ca lagge?)" );
  ap = myGetProxy( "ALAudioPlayer" );
  if( bWait ):
    ap.playFile( getApplicationSharedPath() + "/mp3/" + strFilename );
  else:
    ap.post.playFile( getApplicationSharedPath() + "/mp3/" + strFilename );

  #if( not bNaoqiSound ):
  #  strSoundFile = getApplicationSharedPath() + "/mp3/" + strFilename;
  #else:
  #  strSoundFile = getNaoqiPath() + "/data/mp3/" + strFilename;
  #mySystemCall( getSystemMusicPlayerName() + " " +  strSoundFile, bWait );

# playMusic - end

def playSoundHearing():
  "play the standard appu sound before earing user command"
#  time.sleep( 0.4 ); # time to empty all sound buffers
  playSound( "jingle_earing.wav", bNaoqiSound = True, bDirectPlay = True );
  time.sleep( 0.05 ); # time to empty all sound buffers ?
# playSoundHearing - end

def playSoundSpeaking():
  "play the standard appu sound before speaking to user"
  playSound( "jingle_speaking.wav", bNaoqiSound = True, bDirectPlay = True );
# playSoundSpeaking - end

def playSoundUnderstanding():
  "play the standard appu sound to show a command is understood"
  playSound( "jingle_understanded.wav", bNaoqiSound = True, bDirectPlay = True );
# playSoundUnderstanding - end

# say something using standard APPU interaction (leds, talk jingle...)
# to use text from ID use the getText method from your xar file
def speak( s, bStoreToNonVolatilePath = False ):
  try:
    playSoundSpeaking();
    leds = myGetProxy( "ALLeds" );
    nTimeEyes = len( s ) *50; # temps de lire une lettre :)
    if( nTimeEyes < 500 ):
      nTimeEyes = 500;
    # leds.pCall( "eyesRandom", nTimeEyes );
  #  idEyesRandom = leds.pCall( "randomEyes", nTimeEyes / 1000.0 );
    leds.fadeRGB( "FaceLeds", 0x8585ff, 0.4 );

    s = assumeTextHasDefaultSettings( s );
    sayAndCache( s, bJustPrepare = False, bStoreToNonVolatilePath = bStoreToNonVolatilePath, bDirectPlay = False );
#  leds.stop( idEyesRandom );
    leds.fadeRGB( "FaceLeds", 0x108040, 0.4 );
  except BaseException, err:
    print( "speak: ERR: " + str( err ) );
    pass
# speak - end

global_nAppuSetSettingsSpeechRecoForMenu_alreadyDoneInLang = -1; # set to last lang initted
def appuSetSettingsSpeechRecoForMenu():
  debug( "appuSetSettingsSpeechRecoForMenu - begin" );

  global global_nAppuSetSettingsSpeechRecoForMenu_alreadyDoneInLang;

  if( global_nAppuSetSettingsSpeechRecoForMenu_alreadyDoneInLang == getDefaultSpeakLanguage() ):
    return;

  global_nAppuSetSettingsSpeechRecoForMenu_alreadyDoneInLang = getDefaultSpeakLanguage();


  myProxyAsr = myGetProxy( "ALSpeechRecognition" );

  # use default params for speech recognition
#  myProxyAsr.setParam( "NoiseCancellerEM", 0.0 );
#  myProxyAsr.setParam( 'BeamformerType', 1.0 );
  if( isLangFrench() ):
    print( "appuSetSettingsSpeechRecoForMenu: set speak reco to lang: french" );
    myProxyAsr.setLanguage( "French" );
  elif ( isLangEnglish() ):
    print( "appuSetSettingsSpeechRecoForMenu: set speak reco to lang: english" );
    myProxyAsr.setLanguage( "English" );
  elif ( isLangSpanish() ):
    print( "appuSetSettingsSpeechRecoForMenu: set speak reco to lang: spanish" );
    myProxyAsr.setLanguage( "Spanish" );
  elif ( isLangItalian() ):
    print( "appuSetSettingsSpeechRecoForMenu: set speak reco to lang: italian" );
    myProxyAsr.setLanguage( "Italian" );
  elif ( isLangGerman() ):
    print( "appuSetSettingsSpeechRecoForMenu: set speak reco to lang: german" );
    myProxyAsr.setLanguage( "German" );
  elif ( isLangPolish() ):
    print( "appuSetSettingsSpeechRecoForMenu: set speak reco to lang: polish" );
    myProxyAsr.setLanguage( "Polish" );
  elif ( isLangChinese() ):
    print( "appuSetSettingsSpeechRecoForMenu: set speak reco to lang: chinese" );
    myProxyAsr.setLanguage( "Chinese" );
  else:
    print( "appuSetSettingsSpeechRecoForMenu: set speak reco to lang: english" );
    myProxyAsr.setLanguage( "English" );

#  myProxyAsr.setParam("EarUseSpeechDetector", 2.0 );
#  myProxyAsr.setParam("EarGarbage", 0.8 );
#  myProxyAsr.setParam("EarNoiseReduction", 0.0 );
#  myProxyAsr.setParam("EarSpeed", 2.0 );
#  myProxyAsr.setParam("EarRejectionThreshold", 0.3 );    # ajout pour avoir oeil rouge
#  myProxyAsr.setParam("EarBeamWidth", 100.0 );
#  myProxyAsr.setParam( "EarSdProbabilityThreshold", 0.5 );  # de base: 0.6
#  myProxyAsr.setParam( "EarSdFramesBefore", 40.0 );
#  myProxyAsr.setParam("EarEnergyUpdate", 0.0 );
  myProxyAsr.setVisualExpression( True );

  # kill all logs
  log = myGetProxy( "ALLogger" );
  log.setVerbosity( "error" );

  myProxyAsr.setDebugMode( False );
#  myProxyAsr.setOutputToFile( False );

  debug( "appuSetSettingsSpeechRecoForMenu - end" );
# appuSetSettingsSpeechRecoForMenu - end


# record the activity of a joint and knows if it's moving or not and the side of the move
# classe qui enregistre l'activité d'une articulation et permet de savoir si elle est en train de bouger et dans quelle sens
# elle ne va sortir un info de bougé uniquement quand c'est l'utilisateur qui la bouge, et pas si c'est Nao qui decide de bouger
# compter a peu pres 1-2% de cpu pour un update toutes les 0.3sec (a verifier, c'est pas plus, mais peut etre moins...)
class JointMove:

  def __init__( self, strJointName ):
    self.strJointName = strJointName;
    self.stm = myGetProxy( "ALMemory" );
    self.strStmJointNameSensor = "Device/SubDeviceList/" + strJointName + "/Position/Sensor/Value";
    self.strStmJointNameActuator = "Device/SubDeviceList/" + strJointName + "/Position/Actuator/Value";
    self.strStmJointNameStiffness    = "Device/SubDeviceList/" + strJointName + "/Hardness/Actuator/Value";
    self.rDiffThreshold = 0.05;
    self.reset();
  # __init__ - end

  def getJointName( self ):
    return self.strJointName;
  # getJointName - end

  # assume that joint has no stiffness or that joint is not too much stiff
  def ensureJointIsSoft( self ):
    rNewValueHardness = self.stm.getData( self.strStmJointNameStiffness, 0 );
    rMin = 0.30; # below this value, arms couldn't move to the head level.
    if( rNewValueHardness > rMin ):
      dcm = myGetProxy( "DCM" );
      dcm.set( ["%s/Hardness/Actuator/Value" % self.strJointName, "Merge",  [[rMin, dcm.getTime( 20 ) ]] ] );
  # ensureJointIsSoft - end
  
  def setDiffThreshold( rNewVal ):
        "Change the diff threshold"
        self.rDiffThreshold = rNewVal;

  # start the event catching
  def start( self ):
    self.ensureJointIsSoft();
  # start - end

  # return 0 si l'articulation n'as presque pas bougé, 1 si elle a bougé dans le sens positif, et -1 si dans le sens negatif
  # don't call it too often, because snsor take some time to reach actuator value
  def update( self ):
    rNewValueSensor = self.stm.getData( self.strStmJointNameSensor, 0 ); # todo: en une passe avec un getDataList ?
    rNewValueActuator = self.stm.getData( self.strStmJointNameActuator, 0 );
    rNewValueHardness = self.stm.getData( self.strStmJointNameStiffness, 0 );
    # check if there was a new user command
    if( abs( rNewValueActuator - self.rLastActuatorValue ) < 0.005 or rNewValueHardness < 0.001 ):  # actuator is by nature very precise - actuator is copied from position when stifnness is 0
#      debug( "JointMove debug('" + self.strJointName + "'): rActu-old: %8.5f; new: %8.5f; rSensor-old: %8.5f; new: %8.5f" % ( self.rLastActuatorValue, rNewValueActuator, self.rLastSensorValue, rNewValueSensor ) );
      rDiff = rNewValueSensor - self.rLastSensorValue;
      self.rLastSensorValue = rNewValueSensor;
      if( abs( rDiff ) > self.rDiffThreshold ):
#        debug( "JointMove debug('" + self.strJointName + "'): rSensor-old: %8.5f; rDiff: %5.3f >>>" % ( self.rLastSensorValue, rDiff ) );
        if( rDiff > 0 ): return 1;
        return -1;
    else:
      # the joint has received a move order: update value
#      debug( "JointMove debug('" + self.strJointName + "'): rActu-old: %8.5f; new: %8.5f stiff: %5.3f" % ( self.rLastActuatorValue, rNewValueActuator, rNewValueHardness ) );
      # to skip the (rebond) rebound, we add small latency after having move, we put the actuator small by small to the new value
#      self.rLastActuatorValue = rNewValueActuator;
      self.rLastActuatorValue = ( self.rLastActuatorValue + rNewValueActuator ) / 2;
      # update sensor, so it won't trigger next frame
      self.rLastSensorValue = rNewValueSensor;
    return 0;
  # update - end

  # remet les valeurs a zero pour un nouveau catch d'evenement
  def reset( self ):
    self.ensureJointIsSoft();
    self.rLastSensorValue = self.stm.getData( self.strStmJointNameSensor, 0 );
    self.rLastActuatorValue = self.stm.getData( self.strStmJointNameActuator, 0 );
  # reset - end

# class JointMove - end

# does the directory or subdirectory contents some file matching a mask
def isTreeContentsFileThatMatch( strPath, mask ):
  for elem in os.listdir( strPath ):
    sFullPath = os.path.join( strPath, elem );
    if os.path.isdir(sFullPath) and not os.path.islink(sFullPath):
      if( isTreeContentsFileThatMatch( sFullPath, mask ) ):
        return True;
    if os.path.isfile( sFullPath ):
      if( elem.find( mask) != -1 ):
        return True;
  return False;
# isTreeContentsFileThatMatch - end


# look for behaviors in a disk tree
# return [[listdir containing .xar],[listxar in currentdir]]
def findXar( strPath ):
  debug( "findXar( '%s' )" % str( strPath ) );
  aBehaviorListDir = [];
  aBehaviorListFile = [];

  for elem in os.listdir( strPath ):
    sFullPath = os.path.join( strPath, elem );
    print( "fullpath: " + sFullPath );
    if os.path.isdir(sFullPath) and not os.path.islink(sFullPath):
      if( elem[0] != '.' ):
        aBehaviorListDir.append( elem );
    if os.path.isfile( sFullPath ):
      if( elem.find( ".xar" ) != -1 ):
        aBehaviorListFile.append( elem );

  # check that each of aBehaviorListDir contains at least one xar
  aBehaviorListDirContaining = [];

  for sDir in aBehaviorListDir:
    sFullPath = os.path.join( strPath, sDir );
    if( isTreeContentsFileThatMatch( sFullPath, ".xar" ) ):
      aBehaviorListDirContaining.append( sDir );

  debug( "findXar: listDir:" + str( aBehaviorListDirContaining ) );
  debug( "findXar: listFile:" + str( aBehaviorListFile ) );
  return [aBehaviorListDirContaining, aBehaviorListFile];
# findXar - end

def findFile( strPath, strFileMask, bRecursive = True ):
  "look for file matching the mask in a directory, if bRecursive: look into subdirectories too"
  debug( "findFile: entering with( %s, %s, %s )" % ( strPath, strFileMask, str( bRecursive ) ) );
  listFileFound = [];
  for elem in os.listdir( strPath ):
    sFullPath = os.path.join( strPath, elem );
    if os.path.isdir(sFullPath) and not os.path.islink(sFullPath):
      if( elem[0] != '.' and bRecursive ):
        listFileFound += findFile( sFullPath, strFileMask, bRecursive );
    if os.path.isfile( sFullPath ):
#      debug( "findFile: comparing '%s' with mask '%s'" % ( str( elem ), str( strFileMask  ) ) );
      if( elem.find( strFileMask ) != -1 ):
        listFileFound.append( sFullPath );
  debug( "findFile: exiting with this list: %s" % str( listFileFound ) );
  return listFileFound;
# findFile - end

import smtplib, email
def sendMail( strDest, strSubject, strMsg, strFileToAttach = False ):
  "send a mail from the nao mail account"
  print( "sendMail( strDest='%s'; strSubject='%s' ..." % ( strDest, strSubject ) );


#  strSmtp = "smtp.free.fr";
#  strFrom = "nao.aldebaran@free.fr";
#  strPwdFrom  = "naonaona";
#  nPort = 25

  strSmtp = "smtp.gmail.com";
  strFrom = "mynaorobot@gmail.com";
  strPwdFrom  = "NAO!nao!n40!";
  nPort = 587;

  msg = email.MIMEMultipart.MIMEMultipart();
  msg['From'] = strFrom;
  msg['To'] = strDest;
  msg['Subject'] = strSubject

  msg.attach(email.MIMEText.MIMEText(strMsg))

  if strFileToAttach:
     part = email.MIMEBase.MIMEBase('application', 'octet-stream')
     part.set_payload(open(strFileToAttach, 'rb').read())
     email.Encoders.encode_base64(part)
     part.add_header('Content-Disposition',
             'attachment; filename="%s"' % os.path.basename(strFileToAttach))
     msg.attach(part)

  mailServer = smtplib.SMTP( strSmtp, nPort )

  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(strFrom, strPwdFrom );
  mailServer.sendmail(strFrom, strDest, msg.as_string())

  mailServer.close()

# sendMail - end

# launch a multimodal choice interaction, including speech recognition, Naomark and bumper
class MenuChoice:
  def __init__(self, rConfidenceMinAcceptance ):
    debug( "MenuChoice.init( rConfidenceMinAcceptance= %5.f )" % rConfidenceMinAcceptance );
    self.rConfidenceMinAcceptance = rConfidenceMinAcceptance;
    self.listWords = [];
    self.bFeetBumperChoice = False;
    self.nBumperSubscriberID = -1;
    self.strBumperStringForLeft = "";
    self.strBumperStringForRight = "";
    self.bTorsoButton = False;
    self.strTorsoButtonString = "";
    self.bHeadChoice = False;
    self.jointMoveYes = False; # histoire de mettre un objet dedans
    self.jointMoveNo = False;
    self.bNaoMark = False;
    self.aaNaoMarkListNumber = False;
    self.bTactil = False;
    self.aaTactilCode = False;
    self.nNbrDefaultChoice = 0;          # number of choice not corresponding of .xar on disk (they are first choice in the listWords)
    self.listWordPressLeftFeetTimes = [] # if filled, use LeftFeetBumper to select choice.
    self.nPressFeetSubscriberID = -1;
    self.subscribeAsr = "MenuChoice_ASR"
    self.stm = myGetProxy( "ALMemory" );
    self.strStmKeyName_recwords = "WordRecognized";

    strTemplate = "Device/SubDeviceList/Head/Touch/%s/Sensor/Value";
    self.astrTactilStmKeyName = [ ( strTemplate % "Front" ), ( strTemplate % "Middle" ), ( strTemplate % "Rear" ) ];

    self.asr = myGetProxy( "ALSpeechRecognition" ); # if set to False: stop using recognition
    if( self.asr == None ):
      sayAndCache( "WRN: Speech Recognition not found!" );
      self.asr = False;
    else:
      self.asr.setParameter("EarUseSpeechDetector", 1.0 ) #2.0
      self.asr.setParameter("EarSdFramesBefore", 1 )
      self.asr.setParameter("EarSdFramesAfter", 1 )
      self.asr.setParameter("EarNoiseReduction", 0.0)
      self.asr.setParameter("EarSpeed", 2.0)
      self.asr.setParameter("EarUseFilter", 0.0) #1.0
    # eteint les leds des pieds, ainsi on verra celle qui s'allume ensuite
    leds = myGetProxy( "ALLeds" );
    leds.pCall( "fadeRGB", "FeetLeds", 0x000000, 0.3 );
  # __init__ - end

  #
  # Specific config and option
  #

  # change the number of default choice (normal item begins at nNbrDefaultChoice) => ne sert a rien on ne sait pas ce qu'est un defaut choix ici
#  def setNbrDefaultChoice( self, nNbrDefaultChoice ):
#    self.nNbrDefaultChoice = nNbrDefaultChoice;

  def disableAudioSpeechRecognition( self ):
    print( "WRN: MenuChoice: Disabling Audio Speech Recognition !!!" );
    self.asr = False;
  # disableAudioSpeechRecognition - end


  # permet d'ajouter un oui/non sur le pied (il sera retourner par l'update)
  def addFeetBumperChoice( self, strBumperStringForLeft = "yes", strBumperStringForRight = "no" ):
    debug( "MenuChoice.addFeetBumperChoice" );
    self.bFeetBumperChoice = True;
    self.strBumperStringForLeft = strBumperStringForLeft;
    self.strBumperStringForRight = strBumperStringForRight;
    if( self.nBumperSubscriberID == -1 ):
      self.nBumperSubscriberID = ExtractEvents.subscribe(); # effet de bord interessant, si deja en cours: remet a zero les flags stm
    else:
      ExtractEvents.resetExtractEvents( self.nBumperSubscriberID ); # just reset
    # visual return for user
    leds = myGetProxy( "ALLeds" );
    leds.pCall( "fadeRGB", "LeftFootLeds", 0x00FF00, 0.4 ); # left en vert (yes)
    leds.pCall( "fadeRGB", "RightFootLeds", 0xFF0000, 0.4 ); # right en rouge (no)
  # addFeetBumperChoice - end

  # permet d'ajouter un oui/non en bougeant la tete de nao (il sera retourner par l'update)
  def addHeadChoice( self, strHeadStringForYes = "yes", strHeadStringForNo = "no" ):
    debug( "MenuChoice.addHeadChoice" );
    self.bHeadChoice = True;
    self.strHeadStringForYes = strHeadStringForYes;
    self.strHeadStringForNo = strHeadStringForNo;
    self.jointMoveYes = JointMove( "HeadPitch" );
    self.jointMoveNo = JointMove( "HeadYaw" );
  # addHeadChoice - end

  # permet d'ajouter des choix du ieme item en cliquant i fois sur le pied gauche de Nao
  # le choix commence au ieme item de la liste courante
  def addItemByPressLeftFeetTimes( self, listWordPressLeftFeetTimes ):
    debug( "MenuChoice.addItemByPressLeftFeetTimes( %s )" % listWordPressLeftFeetTimes );
    self.listWordPressLeftFeetTimes = listWordPressLeftFeetTimes;
    if( self.nPressFeetSubscriberID == -1 ):
      self.nPressFeetSubscriberID = ExtractEvents.subscribe(); # effet de bord interessant, si deja en cours: remet a zero les flags stm
    else:
      ExtractEvents.resetExtractEvents( self.nPressFeetSubscriberID ); # just reset
    # visual return for user
    leds = myGetProxy( "ALLeds" );
    leds.pCall( "fadeRGB", "LeftFootLeds", 0x0000FF, 0.4 ); # left en bleu (count)
  # addItemByPressLeftFeetTimes - end

  # permet d'ajouter un message (par exemple l'aide) quand on appuie sur le bouton du torse
  def addTorsoButtonWord( self, strTorsoButtonString = "help" ):
    debug( "MenuChoice.addTorsoButtonWord" );
    self.bTorsoButton = True;
    self.strTorsoButtonString = strTorsoButtonString;

    sentinel = myGetProxy( "ALSentinel" );
    stmDataName = "ALSentinel/SimpleClickOccured";
    sentinel.enableDefaultActionSimpleClick( False );
    self.stm.insertData( stmDataName, False );

    # visual return for user
    leds = myGetProxy( "ALLeds" );
    leds.post.fadeRGB( "ChestLeds", 0x0000FF, 0.4 );
  # addTorsoButtonWord - end

  # permet d'ajouter une liste de numero de NaoMark avec son mot associé, qui vont chacune déclencher un certain choix
  # [ [64, "oui"], [68, "non"] ...
  def addNaoMark( self, aaNaoMarkListNumber ):
    debug( "MenuChoice.addNaoMark" );
    self.bNaoMark = True;
    if( self.aaNaoMarkListNumber == False ):
      # first time
      self.aaNaoMarkListNumber = aaNaoMarkListNumber;
      # init naomark
      self.ALMarkDetection = myGetProxy( "ALLandMarkDetection" );
      self.ALMarkDetection.subscribe( str( self ), 1200, 0.0 );
    else:
      self.aaNaoMarkListNumber = self.aaNaoMarkListNumber + aaNaoMarkListNumber; # add new mark to current one
  # addNaoMark - end

  # permet d'ajouter une liste de mot associé a une touche de capteur tactile
  # [ ["Tap", "exit"], ... ]
  def addTactilCode( self, aaTactilCode ):
    debug( "MenuChoice.addTactilCode" );
    self.bTactil = True;
    if( self.aaTactilCode == False ):
      # first time
      self.aaTactilCode = aaTactilCode;
      # init tactil
      # nothing
    else:
      self.aaTactilCode = self.aaTactilCode + aaTactilCode; # add new code to current one
  # addTactilCode - end


  # list of word can contains specific "virtual" word link to interaction with robot
  # this method will add correct interaction code to link to them
  #
  # here is THE exhaustive list of virtual word (numeroted by type):
  #
  # 1: MARK_xxx => the nao mark with number xxx
  # 2: MVT_chain => movement detected on the chain (chain is a motion named chain LArm, RArm...)
  # 3: MVT_joint => movement detected on the joint (joint is a motion named joint LHipYaw, LShoulderRoll, ...)
  # 4: MVT_joint_UP => movement detected on the joint (joint is a motion named joint LHipYaw, LShoulderRoll, ...)  in the positive direction
  # 5: MVT_joint_DOWN => movement detected on the joint (joint is a motion named joint LHipYaw, LShoulderRoll, ...)  in the positive direction
  # 6: BUMP_LFOOT|RFOOT|CHEST|LSOLE|RSOLE => bumper pressed

  def interpretVirtualWord( self, strWord ):
    nType = self.getVirtualWordType( strWord );

  def isVirtualWordType( self, strWord ):
    return self.getVirtualWordType( strWord ) == 0;

  # getVirtualWordType: return -1, or the type
  def getVirtualWordType( self, strWord ):
    strBeginWord = strWord[:3];
    if( strBeginWord == "MARK" ):
      return 1;
    if( strBeginWord == "MVT_" ):
      strChain = strWord[4:];
      if( strChain.find( ( "Head", "LArm", "RArm", "LLeg", "RLeg" ) )  ):
        return 2;
      if( strWord.endswith( "UP" ) ):
        return 4;
      if( strWord.endswith( "DOWN" ) ):
        return 5;
      return 3;
    if( strBeginWord == "BUMP" ):
      return 6;

  def informHearing( self ):
    "play the hearing sound, after cutting audioin acquisition"
    if( self.asr ):
        try:
            self.asr.unsubscribe(self.subscribeAsr);
        except:
            print( "ERR: IGNORE ALL AUDIO IN NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" );

    #playSoundHearing();
    if( self.asr ):
        try:
            self.asr.subscribe(self.subscribeAsr);
        except:
            print( "ERR: IGNORE ALL AUDIO IN NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" );
    # informHearing - end

  #
  # Process
  #

  # launch the stuff !
  def start( self, listWords = [] ):
    debug( "MenuChoice.start" );

    debug( "listWords:" + str( listWords ) );
    self.listWords = listWords;

    # preparation for Asr
    if( self.asr ):
      appuSetSettingsSpeechRecoForMenu();
      self.asr.setDebugMode( False ); # option to add verbose message
      self.asr.setWordListAsVocabulary( self.listWords );
      self.asr.setVisualExpression( True );
    #self.informHearing();

    # code couleur
    leds = myGetProxy( "ALLeds" );
    leds.pCall( "fadeRGB", "FaceLeds", 0x123180, 0.1 );


    self.stm.insertData( self.strStmKeyName_recwords, ["",0.0] ); # ca traine trop a etre mis a jour sinon
    if( self.asr ):
      self.asr.subscribe(self.subscribeAsr);
    debug( "MenuChoice.start - end" );
  # start - end

  # a appeller régulierement, va retourner une matrice ["word", rConfidence] ou ["",] si rien encore de reconnu ou breaké
  def update( self ):
    debug( "MenuChoice.update" );
    # pour l'instant nous n'utilisons pas le subscribe data car il ne marches plus dans chorégraphe.
    if( self.bFeetBumperChoice ):
      bTouched = ExtractEvents.retrieveEvent_FeetBumper( self.nBumperSubscriberID, 'L' );
      if( bTouched ):
        s = self.strBumperStringForLeft;
        print( "MenuChoice::update: FeetBumperChoice: emulating: %s" % s );
        return [s, 2.0];
      bTouched = ExtractEvents.retrieveEvent_FeetBumper( self.nBumperSubscriberID, 'R' );
      if( bTouched ):
        s = self.strBumperStringForRight;
        print( "MenuChoice::update: FeetBumperChoice: emulating: %s" % s );
        return [s, 2.0];
    # if self.bFeetBumperChoice

    if( self.bHeadChoice ):
      bTouched = self.jointMoveYes.update() != 0;
      if( bTouched ):
        s = self.strHeadStringForYes;
        print( "MenuChoice::update: HeadChoice: emulating: %s" % s );
        return [s, 4.0];
      bTouched = self.jointMoveNo.update() != 0;
      if( bTouched ):
        s = self.strHeadStringForNo;
        print( "MenuChoice::update: HeadChoice: emulating: %s" % s );
        return [s, 4.0];
    # if self.bHeadChoice

    if( self.bTorsoButton ):
      animateTorsoLeds( 0x0000FF );
      bTouched = self.stm.getData( "ALSentinel/SimpleClickOccured", 0 );
      if( bTouched ):
        s = self.strTorsoButtonString;
        print( "MenuChoice::update: torsobutton: emulating: %s" % s );
        return [s, 3.0];
    # if self.bTorsoButton

    if( self.bNaoMark ):
      aMark = self.stm.getData( "LandmarkDetected", 0 );
      if( len( aMark ) > 0 ):
        anTimeStamp = aMark[0]; # an array of two ints
        nNbrDetected = len( aMark[1] );
        if( nNbrDetected > 0 ):
            playSound( "cnx_choregraphe.wav", bNaoqiSound = True );
            firstMarkInfo = aMark[1][0];
            nNumNaoMark = int( firstMarkInfo[1][0] );
            print( "MenuChoice::update: receiving nNumNaoMark: " + str( nNumNaoMark ) );
            s = "";
            for target in self.aaNaoMarkListNumber:
                if( nNumNaoMark == target[0] ):
                   s = target[1];
                   break;
            if( s != "" ):
              print( "MenuChoice::update: naomark: emulating: %s" % s );
              return [s, 3.0];
    # if self.bNaoMark

    if( self.bTactil ):
      actualState = self.stm.getListData( self.astrTactilStmKeyName );
      s = "";
      for target in self.aaTactilCode:
        if( target[0] == "Tap" and actualState[0] == 1 and actualState[1] == 1 and actualState[2] == 1 ):
          s = target[1];
          break;
      if( s != "" ):
        print( "MenuChoice::update: tactil: emulating: %s" % s );
        return [s, 3.0];
    # if self.bTactil

    if( len( self.listWordPressLeftFeetTimes ) > 0 ):
      animateLeftFootLeds( 0x0000FF );
      strKeyname = ExtractEvents.getEventALMemoryKeyName_FeetMultiPress() + "L";
      nNumPress = ExtractEvents.retrieveEvent_FeetMultiPress( self.nPressFeetSubscriberID, 'L' );
      if( nNumPress > 0 ):
        nNumPress = nNumPress - 1; # we want it from 0 to len - 1
        if( nNumPress < len( self.listWordPressLeftFeetTimes ) ):
          s = self.listWordPressLeftFeetTimes[nNumPress];
          print( "MenuChoice::update: PressFeet %d: emulating: %s" % (nNumPress, s ) );
          return [s, 3.0];
        else:
          playSound( "bip_error.wav", True, True );
    # if self.listWordPressLeftFeetTimes

    if( not self.asr ):
      # add a slow ear movement
      animateEarLeds();
    animateEyeLeds_Attentive();

    aRecognised = self.stm.getData( self.strStmKeyName_recwords, 0 );
    if( aRecognised[0] != "" ):
      strWordFound = aRecognised[0];
      rConfidence = aRecognised[1];
      print( "MenuChoice::update: received: %s with %5.2f" % ( strWordFound, rConfidence ) );
      self.stm.insertData( self.strStmKeyName_recwords, ["",0.0] ); # ca traine trop a etre mis a jour sinon
      if( rConfidence > self.rConfidenceMinAcceptance ):
        return aRecognised;
    return ["", 0.0];
  # update - end


  def stopAsrAndSay( self, s ):
    "This is the method to call before talking while Speech Recognition is running"
    if( self.asr ):
        try:
            self.asr.unsubscribe(self.subscribeAsr);
        except:
            print( "ERR: IGNORE ALL AUDIO IN NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" );
    speak( s );
    if( self.asr ):
        try:
            self.asr.subscribe(self.subscribeAsr);
        except:
            print( "ERR: IGNORE ALL AUDIO IN NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" );

  # relance la reco, car parfois on s'est fait stopper (si on a voulu faire une confirmation ou ...)
  def restart( self ):
    debug( "MenuChoice::restart" );
    if( self.asr ):
      debug( "MenuChoice::asr.stopDetection" );
      try:
        self.asr.unsubscribe(self.subscribeAsr);
      except:
        print("cannot unsubscribe")
      self.asr.setWordListAsVocabulary( self.listWords );
      self.stm.insertData( self.strStmKeyName_recwords, ["",0.0] ); # ca traine trop a etre mis a jour sinon
      debug( "MenuChoice::asr.startDetection" );
      self.asr.subscribe(self.subscribeAsr);
    if( self.bFeetBumperChoice ):
      self.addFeetBumperChoice( self.strBumperStringForLeft, self.strBumperStringForRight ); # histoire de remettre les bonnes couleurs et de reinit les états
    if( self.bHeadChoice ):
      self.addHeadChoice( self.strHeadStringForYes, self.strHeadStringForNo ); # histoire de remettre les bonnes couleurs et de reinit les états
    if( self.bTorsoButton ):
      self.addTorsoButtonWord( self.strTorsoButtonString ); # histoire de remettre les bonnes couleurs et de reinit les états
    if( self.bNaoMark ):
      self.addNaoMark( self.aaNaoMarkListNumber );
    if( self.bTactil ):
      self.addTactilCode( self.aaTactilCode  );
    if( len( self.listWordPressLeftFeetTimes ) > 0 ):
      self.addItemByPressLeftFeetTimes( self.listWordPressLeftFeetTimes ); # histoire de remettre les bonnes couleurs et de reinit les états
    #self.informHearing();
  # restart - end

  # stoppe la reconnaissance vocale et l'interaction
  def stop( self ):
    debug( "MenuChoice.stop" );
    # reset leds
    leds = myGetProxy( "ALLeds" );
    leds.post.off( "FeetLeds" );
    leds.post.off( "ChestLeds" );
    if( self.asr ):
      try:
        self.asr.unsubscribe(self.subscribeAsr);
      except:
        print("stop : cannot unsubscribe")
    if( self.bFeetBumperChoice ):
      ExtractEvents.unSubscribe( self.nBumperSubscriberID );
      # rallume les leds en blanc (pour dire: pas d'interactions)
      leds.on( "FeetLeds" );
    if( self.bTorsoButton ):
      sentinel = myGetProxy( "ALSentinel" );
      sentinel.enableDefaultActionSimpleClick( True );
    if( self.bNaoMark ):
      self.ALMarkDetection.unsubscribe( str( self ) );
    if( self.bTactil ):
      # nothing to do...
      pass
    if( self.nPressFeetSubscriberID != -1 ):
      ExtractEvents.unSubscribe( self.nPressFeetSubscriberID );

  # stop - end

# class MenuChoice - end

def storeGlobalData( strDataName, val ):
  "store a data in the stm so everybody can acess it"
  try:
    mem = myGetProxy( "ALMemory" );
    strDataName = getGlobalDataStmName( strDataName );
    mem.insertData( strDataName, val );
  except RuntimeError, err:
    debug( "ERR: storeGlobalData: can't set '%s'" % strDataName );
# storeGlobalData - end

def getGlobalData( strDataName ):
  try:
    mem = myGetProxy( "ALMemory" );
    strDataName = getGlobalDataStmName( strDataName );
    return mem.getData( strDataName, 0 );
  except RuntimeError, err:
    debug(  "WRN: getGlobalData: can't access '%s' => returning 0" % strDataName );
    return 0;
# getGlobalData - end


def getGlobalDataStmName( strDataName ):
  return "ALTools_Globals_" + strDataName;
# getGlobalDataStmName - end

# pidof c'est pas mal aussi...
def findPidOfChild( nParentPid ):
    "return the first found child of a pid"
#  nSonPid = nParentPid + 1; # TODO: get the real handler, because, mpg123 is the son of the shell it's often the +1 after the one returned, but find the good one sill be better!
    # look for the son of the subprocess ID: (the top would be a getSonPid...)

# works fine if getppid( pid ) exists...
#    self.nPidCurrentPlay = newProcess.pid + 1;
#    while( os.getppid( self.nPidCurrentPlay ) != newProcess.pid and self.nPidCurrentPlay < newProcess.pid + 1000 ):
#        self.nPidCurrentPlay += 1;
    strRet = executeAndGrabOutput( "top -n 1 | grep %d" % nParentPid ); # not optimal !!!
    listSplit = strRet.split();
    if( len( listSplit ) < 1 ):
        return -1;
    nSonPid = int( listSplit[0] ); # le premier entier est le pid ! (le parent n'est lui pas retourné)
    return nSonPid;
# findPidOfChild - end


def isProcessPresent( nNumPid ):
    "return true if the process with num nNumPid is running again"
    bRet = False;
    try:
        strFilename = "/proc/%d/cmdline" % nNumPid;
        file = open( strFilename, "rb" );
    except:
        return False;
    try:
        aBuf = file.read();
        bRet = len( aBuf ) > 0;
    except:
        pass
    finally:
        file.close();
    return bRet;
# isProcessPresent - end

# sound volume (premisse of the robot's class)

def getCurrentMasterVolume():
    "get nao master sound system volume (in %)"
    try:
        ad = myGetProxy( 'ALAudioDevice' );
        nVal = ad.getOutputVolume();
        debug( "getCurrentMasterVolume: %d" % ( nVal ) );
        return nVal;
    except BaseException, err:
        print( "getCurrentMasterVolume: error '%s'" % str( err ) );
        
    print( "WRN: => using old one using fork and shell!" );
  
    strOutput = executeAndGrabOutput( "amixer sget Master | grep 'Front Right: Playback' | cut -d[ -f2 | cut -d% -f1", True );
    nValR = int( strOutput );
    strOutput = executeAndGrabOutput( "amixer sget Master | grep 'Front Left: Playback' | cut -d[ -f2 | cut -d% -f1", True );
    nValL = int( strOutput );
    nVal = ( nValR + nValL ) / 2;
    debug( "getCurrentMasterVolume: %d (%d,%d)" % ( nVal, nValL, nValR ) );
    return nVal;
# getCurrentMasterVolume - end

def setMasterVolume( nVolPercent ):
    "change the master volume (in %)"
    if( nVolPercent < 0 ):
        nVolPercent = 0;
    if( nVolPercent > 100 ):
        nVolPercent = 100;
    debug( "setMasterVolume to %d%%" % nVolPercent );
    
    try:
        ad = myGetProxy( 'ALAudioDevice' );
        ad.setOutputVolume( nVolPercent );
        return;
    except BaseException, err:
        print( "getCurrentMasterVolume: error '%s'" % str( err ) );
        
    print( "WRN: => using old one using fork and shell!" );
        
    strCommand = "amixer -q sset Master " + str( nVolPercent * 32 / 100 );
    strCommand += "; amixer  -q sset \"Master Mono\" 32";
    strCommand += "; amixer  -q sset PCM 25";    
    mySystemCall( strCommand );
# setMasterVolume - end


def volumeFadeOut():
    "Fade out master sound system"
    nVol = getCurrentMasterVolume();
    print( "volumeFadeOut: %d -----> 0" % nVol );
    nCpt = 0;
    while( nVol > 0 and nCpt < 30 ): # when concurrent calls are made with other fade type, it could go to a dead lock. because getCurrentMasterVolume take some time, we prefere to add some counter
        ++nCpt;
        # ramping
        if( nVol > 55 ):
            nVol -= 3;
        else:
            nVol -= 9;
        setMasterVolume(nVol);
#        print( "volout: %d" % nVol );

def volumeFadeIn( nFinalVolume ):
    "Fade in master sound system"
    nVol = getCurrentMasterVolume();
    print( "volumeFadeIn: %d -----> %d" % ( nVol, nFinalVolume ) );
    nCpt = 0;
    while( nVol < nFinalVolume and nCpt < 30 ): # when concurrent calls are made with other fade type, it could go to a dead lock. because getCurrentMasterVolume take some time, we prefere to add some counter
        ++nCpt;
        if( nVol > 55 ):
            nVol += 3;
        else:
            nVol += 9;
        setMasterVolume(nVol);
#        print( "volin: %d" % nVol );

def setMasterMute( bMute ):
  "mute nao sound volume"
  if( bMute ):
    strVal = "off";
  else:
    strVal = "on";
  debug( "setMasterMute: %s" % strVal );
  mySystemCall( "amixer -q sset Master " + strVal );
# setMasterMute - end

def isMasterMute():
  "is nao sound volume muted?"
  strOutput = executeAndGrabOutput( "amixer sget Master | grep 'Front Right: Playback' | cut -d[ -f4 | cut -d] -f1", True );
  strOutput = strOutput.strip();
  bMute = ( strOutput == "off" );
  debug( "isMasterMute: %d (strOutput='%s')" % ( bMute, strOutput ) );
  return bMute;
# isMasterMute - end

def setMasterPanning( nPanning = 0 ):
    "change the sound master panning: 0: center -100: left +100: right"
    "current bug: currently volume is louder when at border, than at center, sorry"
    try:
        debug( "setMasterPanning to %d" % nPanning );
        nVol = getCurrentMasterVolume();
        nCoefR = nVol + nVol*nPanning/100;
        nCoefL = nVol - nVol*nPanning/100;
        nCoefR = nCoefR * 32 / 100;
        nCoefL = nCoefL * 32 / 100;
        mySystemCall( "amixer -q sset Master %d,%d" % ( nCoefL, nCoefR ) );
        mySystemCall( "amixer -q sset PCM 25" );
        mySystemCall( "amixer -q sset \"Master Mono\" 32" );
    except BaseException, err:
        print( "setMasterPanning: error '%s'" % str( err ) );
# setMasterPanning - end

 # pause music
def pauseMusic():
  "pause the music player"
  debug( "pauseMusic" );
  mySystemCall( "killall -STOP mpg321b" );

# restart music
def unPauseMusic():
  debug( "unPauseMusic" );
  mySystemCall( "killall -CONT mpg321b" );

def sayInfoMusic():
  "say the title of the song"
  debug( "sayInfoMusic" );
  strOutput = NaoTunes.static_getCurrentPlaying().toString( False );
  print( "sayInfoMusic: " + str( strOutput ) );
  # second try: analyse current process (pourritos)
#  if( strOutput == "" ):
#    strOutput = executeAndGrabOutput( "ps | grep mpg321b | cut -d/ -f2-", True );
#    strOutput = strOutput.strip();
  strOutput = Song.cleanField( strOutput );
  if( strOutput != "" ):
    speak( strOutput );
# sayInfoMusic - end

def isHandPresent():
  """Are we using a nao with hands?"""
  # return len( ALMotion.getJointNames('Body') ) == 25;
  # plus efficace
  return ALMotion.getJointNames('Body').find( "RHand" ) != -1;


def describeColor( anBGR, nLangIndex ):
  """ convert a [b,g,r] color to a string eg: [0,0,0] => "black" ... """
  # a bit tricky: we imagine each base color as a bit set or not, and we will have a color list indexed to the resulting nibble
  aListColor = [
    [
      "black",         # 000
      "red",      # 001
      "green",         # 010
      "yellow",      # 011
      "blue",        # 100
      "pink",        # 101
      "turquoise", # 110
      "white"       # 111
    ],
    [
      "noir",         # 000
      "rouge",      # 001
      "vert",         # 010
      "jaune",      # 011
      "bleu",        # 100
      "rose",        # 101
      "turquoise", # 110
      "blanc"       # 111
    ]
  ];

  # settings to reduce to plain colors
  nMinThreshold = 40;
  nMaxThreshold = 110;

  nValBit = 0;
  for i in range( 3 ):
    if( anBGR[i] > nMaxThreshold ):
      nValBit += 1 << i;
    elif( anBGR[i] > nMinThreshold ):
      # one component is too much average => leaving
      return "";

  # if we reached this point, then we've got a plain color!
  return aListColor[nLangIndex][nValBit];
# describeColor - end

def getSide( nIndex ):
  """ get side left/right from 0..1 """
  aSide = [ "Left", "Right" ];
  if( nIndex < 0 or nIndex > 1 ):
    print( "ERR: getSide: index %d out of range" % nIndex );
    nIndex = 0;
  return aSide[nIndex];
# getSide - end

def getColor( nIndex ):
  """ get color red/green/blue from 0..2 """
  aColor = [ "Red", "Green", "Blue" ];
  if( nIndex < 0 or nIndex > 2 ):
    print( "ERR: getColor: index %d out of range" % nIndex );
    nIndex = 0;
  return aColor[nIndex];
# getColor - end

def getLedsEyesDegreesFromIndex( nIndex ):
  """ get degrees 0..315 from 0..7 """
  aEyeLedsAngle = [ 0, 45, 90, 135, 180, 225, 270, 315 ];
  if( nIndex < 0 or nIndex > 7 ):
    print( "ERR: getLedsEyesDegreesFromIndex: index %d out of range" % nIndex );
    nIndex = 0;
  return aEyeLedsAngle[nIndex];
# getLedsEyesDegreesFromIndex - end

def getEyeLedName( nIndex, nSideIndex = 0 ):
    "get the name of the dcm led device by it's number"
    # TODO !!!
    return "";
#def getEyeLedName - end

def getLedValueRGB( szLedName ):
  #  """ get the hexa value of a led. szLedName: the name of the led, eg 'FaceLedLeft0' """
  szSide = szLedName[7:];
  szSide = szSide.strip( "01234567");
  nNum = int( szLedName[len(szLedName ) -1:] );
#  print( "szSide: %s" % szSide ); print( "nNum: %d" % nNum );
  szTemplateStmKeyName = "Device/SubDeviceList/Face/Led/%s/%s/%dDeg/Actuator/Value";
  if( szSide == "Right" ):
    nNum = 7 - nNum;
  stm = myGetProxy( "ALMemory" );
  aVal = stm.getListData(  [
                                                   szTemplateStmKeyName % ( "Red", szSide, getLedsEyesDegreesFromIndex( nNum ) ),
                                                   szTemplateStmKeyName % ( "Green", szSide, getLedsEyesDegreesFromIndex( nNum ) ),
                                                   szTemplateStmKeyName % ( "Blue", szSide, getLedsEyesDegreesFromIndex( nNum ) )
                                                ] );
#  print( str(aVal) );
  nVal = (int(min(1.0,aVal[0])*255) << 16) + (int(min(1.0,aVal[1])*255) << 8) + int(min(1.0,aVal[2])*255);
#  print str( nVal );
  return nVal
# getLedValueRGB - end

def eyesRotate( nStep = 1 ):
  # rotate current configuration of eyes of one step, in one way or the others depending of nStep
  nNbrEyesLedsSide = 2;
  nNbrEyesLeds = 8;
  rDuration = 0.05;
  leds = myGetProxy( "ALLeds" );
  for nSide in range( nNbrEyesLedsSide ):
    # copy all leds, then poke it
    anVal = [];
    for i in range( nNbrEyesLeds ):
      anVal.append( getLedValueRGB( "FaceLed%s%d" % ( getSide( nSide ), i ) ) );
    for i in range( nNbrEyesLeds ):
      nNumDest = ( i + nStep + nNbrEyesLeds ) % nNbrEyesLeds; # put there nStep to -1 or +1 to change rotation CCW/CW
      leds.post.fadeRGB( "FaceLed%s%d" %( getSide( nSide ), nNumDest ), anVal[i], rDuration );
  time.sleep( rDuration );
# eyesRotate - end

def circleLedsEyes( nColor, rTime, nNbrTurn ):
  # launch a leds animation using one color
  leds = myGetProxy( "ALLeds" );
  nNbrSegment = 8;
  for i in range( nNbrSegment*nNbrTurn ):
    leds.post.fadeRGB( "FaceLed%d" % (i%nNbrSegment) , nColor, rTime );
    leds.post.fadeRGB( "FaceLed%d" % (i%nNbrSegment) , 0x000000, rTime*1.25 );
    time.sleep( rTime*0.25 );
  time.sleep( rTime*0.5 ); # wait last time
# circleLedsEyes - end

def circleLedsEars( rTime, nNbrTurn ):
  "launch a ears leds rotation"
  leds = myGetProxy( "ALLeds" );
  aNames = [[],[]]; # left/right
  rColor = 1.0;
  nNbrSegment = 10;
  for i in range( nNbrSegment ):
    aNames[0].append( "Ears/Led/%s/%dDeg/Actuator/Value" % ( "Left", i * 36 ) );
    aNames[1].append( "Ears/Led/%s/%dDeg/Actuator/Value" % ( "Right", i * 36 ) );
  for i in range( nNbrSegment*nNbrTurn ):
    for j in range( 2 ):
      leds.post.fade( aNames[j][(i%nNbrSegment)] , rColor, rTime );
      leds.post.fade( aNames[j][(i%nNbrSegment)] , 0.0, rTime*1.25 );    
      time.sleep( rTime / 4 );
# circleLedsEars

def cameraRelativePosToAbsolute( rYaw, rPitch ):
    "return absolute head move position from angle value in the camera angle space"
    motion = myGetProxy( "ALMotion" );
    rAngleY = motion.getAngles( 'HeadYaw', True )[0];
    rAngleP = motion.getAngles( 'HeadPitch', True )[0];
    aVal = [];
    aVal.append( rAngleY - rYaw * 0.6 );
    aVal.append( rAngleP + rPitch * 0.6 );
    return aVal;
# cameraRelativePosToAbsolute - end


class Song():
  "The representation of a song file"
  def __init__(self, strFilename = "", strLocalPath = "", strStyle = "", strArtist = "", strTitle = "", strExtra = "" ):
    self.strFilename = strFilename;
    self.strLocalPath = strLocalPath; # local path in the library, without filename eg: rock/metal/
    self.strStyle = strStyle;
    self.strArtist = strArtist;
    self.strTitle = strTitle;
    self.strExtra = strExtra; # some extra information ("featuring Alex" / "radio mix" / "acapella version") ...
    # optionnal field:
    self.rUserNotation = -1;
    self.rGlobalNotation = -1;

    # extract info from song
    if( strArtist == "" and strTitle == "" ):
      aField = strFilename.split( "_-_" );
      if( len( aField ) > 1 ):
        self.strArtist = Song.cleanField( aField[0] );
        self.strTitle = Song.cleanField( aField[1] );
        aFieldExt = aField[1].split( "__" );
        if( len( aFieldExt ) > 1 ):
          if( self.strExtra == "" ):
            self.strExtra = Song.cleanField( aFieldExt[1] );
          self.strTitle = Song.cleanField( aFieldExt[0] );

  @staticmethod
  def cleanField( strFieldContents ):
    """clean a field extracted from a file name eg: "_" => " " and ... """
    strFieldContents = strFieldContents.replace( "_", " " );
    strFieldContents = strFieldContents.replace( ".mp3", "" );
    return strFieldContents;

  def toString( self, bFull = True ):
    "convert the value in a clean string, ready to print"
    if( bFull ):
      strOutput = "\n";
      strOutput += "---------------------\n";
      strOutput += "Filename: " + self.strFilename + "\n";
      strOutput += "LocalPath: " + self.strLocalPath+ "\n";
      strOutput += "Style: " + self.strStyle+ "\n";
      strOutput += "Artist: " + self.strArtist+ "\n";
      strOutput += "Title: " + self.strTitle+ "\n";
      strOutput += "Extra Info: " + self.strExtra+ "\n";
      strOutput += "User Notation: " + str( self.rUserNotation ) + "\n";
      strOutput += "Global Notation: " + str( self.rGlobalNotation ) + "\n";
      strOutput += "---------------------\n";
    else:
      strOutput = self.strArtist + ": " + self.strTitle;
    return strOutput;
  # toString - end

  def toArray( self ):
    "convert the value in a song to an array"
    output = [];
    output.append( self.strFilename );
    output.append( self.strLocalPath );
    output.append( self.strStyle );
    output.append( self.strArtist );
    output.append( self.strTitle );
    output.append( self.strExtra );
    output.append( self.rUserNotation );
    output.append( self.rGlobalNotation );
    return output;
  # toArray - end

  def toNamedArray( self ):
    "convert the value in a song to an array of couple [attr_name,attr_value] "
    output = [];
    output.append( ["strFilename", self.strFilename] );
    output.append( ["strLocalPath", self.strLocalPath] );
    output.append( ["strStyle", self.strStyle] );
    output.append( ["strArtist", self.strArtist] );
    output.append( ["strTitle", self.strTitle] );
    output.append( ["strExtra", self.strExtra] );
    output.append( ["rUserNotation", self.rUserNotation] );
    output.append( ["rGlobalNotation", self.rGlobalNotation] );
    return output;
  # toNamedArray - end

  def fromNamedArray( self, aNamedArray ):
    "construct a song from an array of couple [attr_name,attr_value]"
    self = constructFromNamedArray( self, aNamedArray );
  # fromNamedArray - end

  def toDict( self ):
    "convert a song to a dict array"
    dictOutput = dict();
    for attrName in dir( self ):
      dictOutput[attrName] = getattr( self, attrName );
    return dictOutput;
  # toDict - end

# class Song - end

class NaoTunes():
  "Manage MP3 library on Nao: list them, play them, shuffle options..."
  def __init__(self ):
    self.strRootPath = "";
    self.listMusic = []; # the list of music of the library (array of Song)
    self.bShuffle = True;
    # current/last search
    self.filteredList = []; # a temporary playlist of music (array of [Song, bAlreadyPlayed])
    self.filteredParams = ["",""];  # [styleparams, filenameparams]
    self.filteredCurrentPlaying = -1; # the index of the current playing song in filteredList
    self.ids = [] #ids of audioplayer methods
  # init - end

#  def setRootPath( self, strPath ):
#    "set the root path of our song library"
#    self.strRootPath = strPath;
#  # setRootPath - end

  def setMusicPathByStyle( self, strPath ):
    "Add music to the base: add a lookup path to find mp3 sorted by style, the first directory name is the music style"
    listSong = findFile( strPath, ".mp3" );
    #print( str( listSong ) );
#    strRootPath = self.strRootPath;
    strRootPath = strPath;
    for song in listSong:
      song = song[len(strPath):];
      listField = song.split( getDirectorySeparator() );
      if( len( listField ) > 1 ):
        strStyle = listField[0];
      else:
        strStyle = "";
      strFilename = listField[len( listField)-1];
#      print( str( listField ) );
      self.listMusic.append( Song( strFilename, strPath + strStyle + getDirectorySeparator(), strStyle ) );
#    print( "NaoTunes: found music: " + str( self.listMusic ) );
    print( "NaoTunes: found %d tunes" % len( self.listMusic ) );
  # setMusicPathByStyle - end

  def toString( self, bFull = False ):
    "return the image of tha library in a string"
    s = "";
    for song in self.listMusic:
      if( bFull ):
        s += dump( song, False );
      else:
        s += "%s: %s - %s (%s)\n" % ( song.strStyle, song.strArtist, song.strTitle , song.strFilename);
    s += "%d songs" % len( self.listMusic );
    return s;

  def getListSong( self ):
    "return the present songin the library"
    return self.listMusic;
  # getListSong - end

  def getListStyle( self ):
    "return the present style in the library"
    listStyle = [];
    for song in self.listMusic:
      if( song.strStyle != "" ):
        if( find( listStyle, song.strStyle ) == -1 ):
          listStyle.append( song.strStyle );
    return listStyle;
  # getListStyle - end

  # construct an array of song to play
  def find( self, strStyleMask,  strFileMask = ""):
    if( self.filteredParams[0] == strStyleMask and self.filteredParams[1] == strFileMask and len( self.filteredList ) > 0):
      return; # do nothing
    print( "NaoTunes: filtering on ('%s','%s')" % (strStyleMask,  strFileMask) );
    self.filteredParams[0] = strStyleMask;
    self.filteredParams[1] = strFileMask;
    self.filteredList = [];
    for song in self.listMusic:
      if( song.strStyle.find( strStyleMask )  != -1 ):
        self.filteredList.append( [song, False] );
    print( "NaoTunes: filtering found %d tunes" % len( self.filteredList ) );
    return self.filteredList;
  # findByStyle - end

  def playByStyle( self, strStyleMask = "", bWait = True ):
    "play a song, filtered on a specific style"
    self.find( strStyleMask );
    stm = myGetProxy( "ALMemory" );

    if( len( self.filteredList ) < 1 ):
      return False;
    #
    if( not self.bShuffle ):
      self.filteredCurrentPlaying += 1;
      if( self.filteredCurrentPlaying >= len( self.filteredList ) ):
        return False; # playing finished
    else:
      # random in list
      # detect if all played
      bAllPlayed = True;
      for songAndPlayed in self.filteredList :
        if( not songAndPlayed[1] ):
          bAllPlayed = False;
          break;
      if( bAllPlayed ):
        # clean list
        for i in range( 0, len( self.filteredList ) ):
          self.filteredList[i][1] = False;

      nNumFile = random.randint( 0, len( self.filteredList ) - 1 );
      while( self.filteredList[nNumFile][1] ):
        nNumFile = random.randint( 0, len( self.filteredList ) - 1 );
      self.filteredList[nNumFile][1] = True;
      self.filteredCurrentPlaying = nNumFile;
    # else shuffle - end
    songAndPlayed = self.filteredList[self.filteredCurrentPlaying];
    strSoundFile = self.strRootPath + songAndPlayed[0].strLocalPath + songAndPlayed[0].strFilename;
    print( "NaoTunes: playing '%s'" % strSoundFile );
    try:
      #stm = myGetProxy( "ALMemory" );
      debug( "NaoTunes: inserting song: " + str( songAndPlayed[0].toNamedArray() ) );
      stm.insertData( NaoTunes.static_getALMemoryKeyName_SongName(), songAndPlayed[0].toNamedArray() ); # insert current song
    except:
      pass
    #mySystemCall( getSystemMusicPlayerName() + " " +  strSoundFile, bWait );
    audioProxy = myGetProxy("ALAudioPlayer")
    id = audioProxy.post.playFile(strSoundFile)
    self.ids.append(id)
    #self.ids.remove(id)
    if( bWait ):
      # we know that we've finished playing
      try:
        audioProxy.wait(id, 0);
        debug( "NaoTunes: erasing current playing song... " );
        stm.insertData( NaoTunes.static_getALMemoryKeyName_SongName(), [] ); # erase current song
        #audioProxy.wait(id, 0)
      except:
        pass
    try:
      self.ids.remove(id)
    except:
      pass
    return True;
  # playByStyle - end

  def getCurrentPlaying( self ):
    "return the current song playing / last music played"
    if( self.filteredCurrentPlaying == -1 ):
      return "";
    return self.filteredList[self.filteredCurrentPlaying][0];
  # getCurrentPlaying - end

  def stopPlaying( self ):
    "stop playing current song"
    try:
      stm = myGetProxy( "ALMemory" );
      debug( "NaoTunes: erasing current playing song... (2)" );
      stm.insertData( NaoTunes.static_getALMemoryKeyName_SongName(), [] );
    except:
      pass
    playerStop = myGetProxy('ALAudioPlayer', True)
    for id in self.ids:
      playerStop.stop(id)
    #self.ids = []
    #mySystemCall( "killall mpg321b" ); # Crado (TODO)
  # stopPlaying - end

  @staticmethod
  def static_getALMemoryKeyName_SongName():
    return "NaoTunes/CurrentSongPlaying";
  # static_getALMemoryKeyName_SongName - end

  @staticmethod
  def static_getCurrentPlaying():
    "return the currenlty playing song object, from the stm"
    stm = myGetProxy( "ALMemory" );
    songInfo = stm.getData( NaoTunes.static_getALMemoryKeyName_SongName(), 0 );
    temp = Song();
    temp.fromNamedArray( songInfo );
    return temp;
  # static_getCurrentPlaying - end

#class NaoTunes - end

extractEvents = False; # Ne pas changer le nom de cet objet (probleme de bind python...)
class ExtractEvents( ALModule ):
  "A python naoqi module that extract high level events so user can subscribe to exported variable in ALMemory"
  def __init__( self, strName ):
    ALModule.__init__( self, strName );
    nNow = time.time() * 1000;
    self.aMultiPressFeetTimeLastPressed = [ nNow, nNow ];
    self.anMultiPressFeetNbrConsecutifPress = [0,0];
    self.bMultiPressFeetStarted = False;
    self.bMustStop = False;
    self.strLeftID = "L";
    self.strRightID = "R";
    self.nMultiPressTimeRepetMs = 700;
    self.nNbrFeet = 2;
    self.stm = myGetProxy( "ALMemory" );
    self.nNextUserID = 1; # next ID to give to an user
    self.anListRegisteredID = [];
  # __init__ - end

  def myDataChanged(self, strKeyName, value, strMsg ):
    debug( "ExtractEvents::myDataChanged(%s,%s,%s)" % ( str( strKeyName ), str( value ), str( strMsg ) ) );
  # myDataChanged - end

  def onBumpers(self, strKeyName, value, strMsg ):
    debug( "ExtractEvents::onBumpers(%s,%s,%s)" % ( str( strKeyName ), str( value ), str( strMsg ) ) );

    bPushed = value > 0.1;
    nIndexFeet = 0;
    if( strMsg == self.strRightID ):
      nIndexFeet = 1;

    if( bPushed ):
      self.insertFeetBumper( strMsg );

      # gestion multi press feet

      nNow = time.time() * 1000;
      nDurationSinceLastMs = nNow - self.aMultiPressFeetTimeLastPressed[nIndexFeet];
      debug( "nDurationSinceLastMs: %d; now: %s" % ( nDurationSinceLastMs, str( nNow ) ) );
      self.aMultiPressFeetTimeLastPressed[nIndexFeet] = nNow;
      if( nDurationSinceLastMs < self.nMultiPressTimeRepetMs and nDurationSinceLastMs > 0 ): # Alma 08-04-02: adding > 0 because sometimes if > 35 minutes ca boucle dans les negatifs
        if( nDurationSinceLastMs < 60 ):
          # on vient de recevoir l'autre bumper, on skippe celui ci!
          debug( "ExtractEvents::onBumpers: skipping this event (%dms)" % nDurationSinceLastMs );
          pass
        else:
          # multipress detected
          self.anMultiPressFeetNbrConsecutifPress[nIndexFeet] += 1;
          debug( "ExtractEvents::onBumpers: increasing temporary press counter to [%d]=>%d\n" %( nIndexFeet, self.anMultiPressFeetNbrConsecutifPress[nIndexFeet] ) );
      else:
        self.anMultiPressFeetNbrConsecutifPress[nIndexFeet] = 1;
    # if( bPushed ) - end
  # onBumpers - end

  def loopUpdateMultiPressFeet( self ):
    if( self.bMultiPressFeetStarted ):
      debug( "INF: ExtractEvents.loopUpdateMultiPressFeet: already started! (ignoring)\n" );
      return;
    debug( "INF: ExtractEvents.loopUpdateMultiPressFeet: starting...\n" );

    self.bMultiPressFeetStarted = True;

    while( not self.bMustStop ):
      time.sleep( self.nMultiPressTimeRepetMs * 1.5 / 1000.0 );
      nNow = time.time() * 1000;
      for i in range( 0, self.nNbrFeet ):
        if( self.anMultiPressFeetNbrConsecutifPress[i] > 0 ):
          nDurationSinceLastMs = nNow - self.aMultiPressFeetTimeLastPressed[i];
          debug( "ExtractEvents.loopUpdateMultiPressFeet: time since nbr%d: %d\n" % ( int(self.aMultiPressFeetTimeLastPressed[i] ), int(nDurationSinceLastMs ) ) );
          if( nDurationSinceLastMs > self.nMultiPressTimeRepetMs * 1.1 ):
            # we have an end of multi press, insert it in almemory
            if( i == 0 ):
              strFeetLetter = self.strLeftID;
            else:
              strFeetLetter = self.strRightID;
            self.insertFeetMultiPressEvent( strFeetLetter, int( self.anMultiPressFeetNbrConsecutifPress[i] ) );
            self.anMultiPressFeetNbrConsecutifPress[i] = 0;
      # for - end

    # never ending while, unless exit modules

    debug( "INF: ExtractEvents.loopUpdateMultiPressFeet: stopped...\n" );
    self.bMultiPressFeetStarted = False;
  # loopUpdateMultiPressFeet - end

  def insertFeetBumper( self, strFeetLetter = 'L' ):
    "insert an instant bumper press in ALMemory"
    debug( "ExtractEvents.insertFeetBumper: set %s to True\n" % strFeetLetter );

    for nUserID in self.anListRegisteredID:
      strKeyName = ExtractEvents.getEventALMemoryKeyName_FeetBumper( nUserID ) + strFeetLetter;
      self.stm.insertData( strKeyName, True );
  # insertFeetBumper - end

  def insertFeetMultiPressEvent( self, strFeetLetter = 'L', nNbrPress = 1 ):
    "insert a multi bumper press in ALMemory"
    debug( "ExtractEvents.insertFeetMultiPressEvent: set %s to %d\n" % ( strFeetLetter, nNbrPress ) );

    for nUserID in self.anListRegisteredID:
      strKeyName = ExtractEvents.getEventALMemoryKeyName_FeetMultiPress( nUserID ) + strFeetLetter;
      self.stm.insertData( strKeyName, nNbrPress );
  # insertFeetMultiPressEvent - end

  def addSubscriber( self ):
    "add a subscriber to this object"
    nUserID = self.nNextUserID;
    ++self.nNextUserID;
    debug( "ExtractEvents::addSubscriber: new subscriber: %d" % nUserID );
    # create empty keys
    ExtractEvents.resetExtractEvents( nUserID );
    self.anListRegisteredID.append( nUserID );

    return nUserID;
  # addSubscriber - end

  def delSubscriber( self, nSubscriberID ):
    "remove a subscriber to this object"
    debug( "ExtractEvents::delSubscriber: remove subscriber %d" % nSubscriberID );
    if( not nSubscriberID in self.anListRegisteredID ):
      print( "WRN: ExtractEvents.delSubscriber: nSubscriberID %d has already subscribe" % nSubscriberID );
      return;
    self.anListRegisteredID.remove( nSubscriberID );
  # delSubscriber - end

  def getNbrSubscriber( self ):
    nNbrSubscriber = len( self.anListRegisteredID );
    debug( "ExtractEvents::getNbrSubscriber: nNbrSubscriber: %d" % nNbrSubscriber );
    return nNbrSubscriber;
  # getNbrSubscriber - end

  #
  # Static zone for simpler user access
  #

  @staticmethod
  def subscribe():
    "an user want to subscribe to this extractors"
    "return an ID of subscribers: nSubscriberID"
    global extractEvents;

    while( extractEvents != False and extractEvents.bMustStop ):
      time.sleep( 0.2 ); # a previous version is about to shutdown, wait it finished its closing

    if( extractEvents == False ):
      # create the first object (it's a singleton du pauvre like)
      extractEvents = ExtractEvents( "altools.extractEvents" );
      debug( "binding python data changed method" );
      extractEvents.BIND_PYTHON( extractEvents.getName(), "myDataChanged" );
      extractEvents.BIND_PYTHON( extractEvents.getName(), "onBumpers" );

      # register
      stm = myGetProxy( "ALMemory" );
      strLeftID = "L";
      strRightID = "R";
      strTemplateKeyName = "%sBumperPressed"
      stm.subscribeToMicroEvent( strTemplateKeyName % ( "Left" ), extractEvents.getName(), strLeftID, "onBumpers" );
      stm.subscribeToMicroEvent( strTemplateKeyName % ( "Right" ), extractEvents.getName(), strLeftID, "onBumpers" );
      stm.subscribeToMicroEvent( strTemplateKeyName % ( "Left" ), extractEvents.getName(), strRightID, "onBumpers" );
      stm.subscribeToMicroEvent( strTemplateKeyName % ( "Right" ), extractEvents.getName(), strRightID, "onBumpers" );

      #extractEvents.loopUpdateMultiPressFeet();
      asyncEval( "extractEvents.loopUpdateMultiPressFeet();", globals(), locals() );

    return extractEvents.addSubscriber();
  # subscribe - end

  @staticmethod
  def unSubscribe( nSubscriberID, bDontDeleteObjectForTimeOptimisationPurpose = False ):
    global extractEvents;
    if( extractEvents == False ):
      print( "WRN: altools.unSubscribe: no more subscriber" );
      return;
    extractEvents.delSubscriber( nSubscriberID );
    if( extractEvents.getNbrSubscriber() < 1 and not bDontDeleteObjectForTimeOptimisationPurpose ):
      debug( "ExtractEvents::unSubscribe(static): exiting module extractEvents" );
      stm = myGetProxy( "ALMemory" );
      strLeftID = "L";
      strRightID = "R";
      strTemplateKeyName = "%sBumperPressed"
      stm.unsubscribeToMicroEvent( strTemplateKeyName % ( "Left" ), extractEvents.getName() );
      stm.unsubscribeToMicroEvent( strTemplateKeyName % ( "Right" ), extractEvents.getName() );
      stm.unsubscribeToMicroEvent( strTemplateKeyName % ( "Left" ), extractEvents.getName() );
      stm.unsubscribeToMicroEvent( strTemplateKeyName % ( "Right" ), extractEvents.getName() );

      extractEvents.bMustStop = True; # stop the loopUpdateMultiPressFeet
      while( extractEvents.bMultiPressFeetStarted ):
        time.sleep( 0.2 ); # time for loopUpdateMultiPressFeet to stop
      if( extractEvents != False ):
        extractEvents.exit(); # close the module at naoqi level
        # time.sleep( 2.0 ); no wait!
      extractEvents = False; # will delete the object / called the gc

  # unSubscribe - end

  @staticmethod
  def resetExtractEvents( nSubscriberID, bResetLeft = True, bResetRight = True ):
    stm = myGetProxy( "ALMemory" );
    strLeftID = "L";
    strRightID = "R";
    if( bResetLeft ):
      stm.insertData( ExtractEvents.getEventALMemoryKeyName_FeetBumper( nSubscriberID ) + strLeftID, False );
      stm.insertData( ExtractEvents.getEventALMemoryKeyName_FeetMultiPress( nSubscriberID ) + strLeftID, 0 );
    if( bResetRight ):
      stm.insertData( ExtractEvents.getEventALMemoryKeyName_FeetBumper( nSubscriberID ) + strRightID, False );
      stm.insertData( ExtractEvents.getEventALMemoryKeyName_FeetMultiPress( nSubscriberID ) + strRightID, 0 );
  # resetExtractEvents - end

  @staticmethod
  def getEventALMemoryKeyName_FeetBumper( nSubscriberID = 0 ):
    "get the almemory's key of a type of event"
    return "ExtractEvents/ShortEvent/Bumper_" + str( nSubscriberID ) + "_";
  # getEventALMemoryKeyName_FeetBumper - end

  @staticmethod
  def getEventALMemoryKeyName_FeetMultiPress(  nSubscriberID = 0 ):
    "get the almemory's key of a type of event"
    return "ExtractEvents/ShortEvent/MultiPressFeet_" + str( nSubscriberID ) + "_";
  # getEventALMemoryKeyName_FeetMultiPress - end


  @staticmethod
  def retrieveEvent_FeetBumper( nSubscriberID = 0, strFeetLetter = 'L' ):
    "retrieve the value of a type of event"
    stm = myGetProxy( "ALMemory" );
    strKeyName = ExtractEvents.getEventALMemoryKeyName_FeetBumper( nSubscriberID ) + strFeetLetter;
    bTouched = stm.getData( strKeyName, 0 );
    if( not bTouched ):
      return False;
    stm.insertData( strKeyName, False );
    return True;
  # retrieveEvent_FeetBumper - end

  @staticmethod
  def retrieveEvent_FeetMultiPress( nSubscriberID = 0, strFeetLetter = 'L' ):
    "retrieve the value of a type of event"
    stm = myGetProxy( "ALMemory" );
    strKeyName = ExtractEvents.getEventALMemoryKeyName_FeetMultiPress( nSubscriberID ) + strFeetLetter;
    nPress = stm.getData( strKeyName, 0 );
    if( nPress == 0 ):
      return 0;
    stm.insertData( strKeyName, False );
    return nPress;
  # retrieveEvent_FeetMultiPress - end

  @staticmethod
  def innerTest():
    broker = ALBroker( "pythonBroker_ExtractEvents_innerTest", "127.0.0.1", 9999, naoconfig.strIP, naoconfig.nPort )
    print("ok broker")
    nSubscriberID  = ExtractEvents.subscribe();
    for i in range( 10 ):
      nMulti = ExtractEvents.retrieveEvent_FeetMultiPress( nSubscriberID, 'L' );
      if( nMulti > 0 ):
        output_MultiPressFeet_Left( nMulti );
      nMulti = ExtractEvents.retrieveEvent_FeetMultiPress( nSubscriberID, 'R' );
      if( nMulti > 0 ):
        output_MultiPressFeet_Right( nMulti );

      bPress = ExtractEvents.retrieveEvent_FeetBumper( nSubscriberID, 'L' );
      if( bPress > 0 ):
        output_FeetEventOccured_Left();
      bPress = ExtractEvents.retrieveEvent_FeetBumper( nSubscriberID, 'R' );
      if( bPress > 0 ):
        output_FeetEventOccured_Right( nSubscriberID );

      time.sleep( 0.4 );
    # for - end
    ExtractEvents.unSubscribe( nSubscriberID );
  # innerTest - end

# Class ExtractEvents - end

#ExtractEvents.innerTest();



animateEarLeds_nNextIndex = 0;
def animateEarLeds():
  "move slightly ears leds, position is globally stored. If someone move ears independantly of this method, it won't work fine (but not crash)"
  nNbrLedByEars = 10;
  leds = myGetProxy( "ALLeds" );
  strTemplate = "Ears/Led/%s/%dDeg/Actuator/Value";
  global animateEarLeds_nNextIndex;
  nAngle = (360/nNbrLedByEars) * animateEarLeds_nNextIndex;
  # update index before sending movement in case of a fast/concurrent call of animateEarLeds
  animateEarLeds_nNextIndex -= 1;   # more beautiful to turn in this way
  if( animateEarLeds_nNextIndex < 0 ):
    animateEarLeds_nNextIndex = nNbrLedByEars-1;
  leds.post.off( "EarLeds" );
  leds.post.on( strTemplate % ( "Left", nAngle ) );
  leds.on( strTemplate % ( "Right", nAngle ) );  # wait the end of action
# animateEarLeds - end

aAnimateBodyLedsTick = [0,0,0]; # animation ticks of body leds
def animateBodyLeds( nNumLed, nColorParams = 0xFFFFFF ):
  "animate/blink/change one body leds (0: torso; 1: left foot; 2: right foot)"
  leds = myGetProxy( "ALLeds" );
  nColor = 0;
  if( aAnimateBodyLedsTick[nNumLed] == 1 ):
    nColor = nColorParams;
    aAnimateBodyLedsTick[nNumLed] = 0;
  else:
    aAnimateBodyLedsTick[nNumLed] += 1;

  astrLedsName = [ "ChestLeds", "LeftFootLeds", "RightFootLeds" ];

  leds.post.fadeRGB( astrLedsName[nNumLed], nColor, 0.2 );
# animateBodyLeds - end

def animateTorsoLeds( nColor = 0xFFFFFF ):
  "blink torso light"
  animateBodyLeds( 0, nColor );

def animateLeftFootLeds( nColor = 0xFFFFFF ):
  "blink left foot"
  animateBodyLeds( 1, nColor );

def animateRightFootLeds( nColor = 0xFFFFFF ):
  "blink right foot"
  animateBodyLeds( 2, nColor );

animateEyeLeds_AttentiveTick = 0;
def animateEyeLeds_Attentive():
  "animate eyes leds with an attentive style"
  leds = myGetProxy( "ALLeds" );
  nColor = 0;
  rDuration = 0.3
  global animateEyeLeds_AttentiveTick;
  if( animateEyeLeds_AttentiveTick == 1 ):
    animateEyeLeds_AttentiveTick = 0;
    leds.post.fadeRGB( "FaceLedRight6", 0x001000, rDuration );
    leds.post.fadeRGB( "FaceLedLeft6", 0x001000, rDuration );
  else:
    animateEyeLeds_AttentiveTick = 1;
    leds.post.fadeRGB( "FaceLeds",  0x00FF80, rDuration );
# animateEyeLeds_Attentive - end


import re, sys, pickle, os
from os.path import join

class LanguageProcessing:
  "This class provides methods to process language (eg: detect lang)."
  def __init__(self, sDictionaryPath = "/opt/appu/data/pkl"):
    "The path where the data are stored/to be stored."
    self.sDictionaryPath = sDictionaryPath # TODO : throw an exception if it's not a real path

  def setDictionaryPath(self, sNewDictionaryPath):
    "If the data path has to be changed."
    self.sDictionaryPath = sNewDictionaryPath # TODO : throw an exception and keep the old value
    if not os.path.isdir(sNewDictionaryPath):
      print(sNewDictionaryPath+" is not a repository")

  def getDictionaryPath(self):
    "Returns the data path."
    return self.sDictionaryPath

  def __sortValues(self, eElem1, eElem2):
    "This private method is a tool for some language processing functions."
    return -cmp(eElem1[1],eElem2[1])

  def createDictionary(self, sStringToProcess):
    "This function creates the trigram dictionary from the input string."
    # Remove uppercase letters and punctuation. Each punctuation character is replaced by a \n.
    sOldCleanString = sStringToProcess.lower()
    sCleanString = re.sub('[ \t\v\f\r]|\d|[!-/:-@[-`{-~]','\n',sOldCleanString)
    #Get all the words
    aString = sCleanString.split('\n')
    dTrigrams = {}
    for sWord in aString:
      if len(sWord) < 4:
        if len(sWord) > 0:
          # The word is a trigram (<= 3 char). Its frequency in the trigram dict is increased.
          try:
            nFreq = dTrigrams[sWord]
          except KeyError:
            dTrigrams[sWord] = 1
          else:
            dTrigrams[sWord] = nFreq + 1
      else:
        # The word contains many trigrams
        nLength = len(sWord)
        nCnt = 0
        while nCnt < nLength - 2:
          sNewTrig = sWord[nCnt:nCnt+3]
          # The frequency of the trigram is increased.
          try:
            nFreq = dTrigrams[sNewTrig]
          except KeyError:
            dTrigrams[sNewTrig] = 1
          else:
            dTrigrams[sNewTrig] = nFreq + 1
          nCnt += 1
    # precomputes the total weight
    rNbrTrigramsCorpus = 0.0
    for nValue in dTrigrams.itervalues():
      rNbrTrigramsCorpus += float(nValue)
    # Store this weight in the trigram dictionary
    dTrigrams["TOTAL_WEIGHT"] = rNbrTrigramsCorpus
    # Returns the trigram dictionary.
    return dTrigrams

  def computeLanguageProbabilities(self, sStringToProcess):
    "Computes the language probabilities for the input string."
    # TODO : optimize the dictionary opening/access

    # Creates the trigram dictionary from the input string.
    dDictionary = self.createDictionary(sStringToProcess)
    if not os.path.isdir(self.sDictionaryPath):
      print(self.sDictionaryPath+" is not a repository!") # TODO : throw error ?
      return
    aDir = os.listdir(self.sDictionaryPath)
    dProb = {}
    # compute the frequency sum of the input trigrams (to normalize)
    rNbrTrigramsInput = dDictionary["TOTAL_WEIGHT"]
    # traversal of the dictionaries
    for sElem in aDir:
      rProba = 0.0
      sFullPath = os.path.join(self.sDictionaryPath, sElem)
      if os.path.isfile(sFullPath):
        fPklFile = open(sFullPath, 'rb')
        try:
          dTrigramCorpus = pickle.load(fPklFile)
        except:
          pass
        else:
          # computes the frequency sum of the learnt trigram dictionary (to normalize)
          rNbrTrigramsCorpus = dTrigramCorpus["TOTAL_WEIGHT"]
          fPklFile.close()
          # computes the probability of the current language
          for k, v in dDictionary.iteritems():
            try:
              rCorpusFreq = float(dTrigramCorpus[k])
            except KeyError:
              rCorpusFreq = 0.0
            rProba = rProba + ((rCorpusFreq/rNbrTrigramsCorpus) * (v/ rNbrTrigramsInput))
        dProb[sElem[:len(sElem)-4]]=rProba
    iDic = dProb.items()
    return(iDic)

  def findLanguage(self, sStringToProcess):
    "Returns the name of the most probable language."
    iDic = self.computeLanguageProbabilities(sStringToProcess)
    iDic.sort(self.__sortValues)
    return iDic[0]

  def findEnglishOrFrench(self, sStringToProcess):
    "Returns the name of the most probable language, between English and French."
    # TODO : use only English and French dictionaries.
    iDic = self.computeLanguageProbabilities(sStringToProcess)
    iDic.sort(self.__sortValues)
    for aElem in iDic:
      if aElem[0] == "french" or aElem[0] == "english":
        return(aElem[0][0].upper() +aElem[0][1:] )

# class LanguageProcessing - end

# Ressource managing methods


def ressourceTypeToString( nNumRessource ):
    if( nNumRessource == const.ressource_weak ):
        return "weak";
    if( nNumRessource == const.ressource_blend ):
        return "blend";
    if( nNumRessource == const.ressource_lock ):
        return "lock";
    if( nNumRessource == const.ressource_reserve ):
        return "reserve (for child)";
# ressourceTypeToString - end

def ressourceCreateNaoRessource():
    try:
        rm = myGetProxy( "ALRessourceManager" );
    except:
        logToChoregraphe( "ERR: Ressource Manager not found, ressource managing disabled" );
        return;
        
    if( rm == None ): # when called from exterior of choregraphe, when a constructor on a proxy fail it doesn't throw an exception.
        return;

    # Person
    rm.addChilds( "All", [ "Body", "Talk", "Me", "Leds", "Sensors", "Camera" ] );

    # Body
    rm.addChilds( "Body", [ "Head", "Arms", "Legs" ] );
    rm.addChilds( "Head", [ "HeadYaw", "HeadPitch" ] );
    rm.addChilds( "Arms", [ "LArm", "RArm", "ForeArms" ] );
    rm.addChilds( "ForeArms", [ "LForearm", "RForearm" ] );
    rm.addChilds( "LForearm", [ "LWristYaw", "LHand" ] );
    rm.addChilds( "RForearm", [ "RWristYaw", "RHand" ] );
    rm.addChilds( "Legs", [ "Hips", "Knees", "Ankle" ] );
    rm.addChilds( "Knees", [ "LKnee", "RKnee" ] );
    rm.addChilds( "Ankle", [ "LAnkle", "RAnkle" ] );

    # Sound
    rm.addChilds( "Talk", [ "AudioIn", "AudioOut" ] );

    # Leds
    rm.addChilds( "Leds", [ "EyeLeds", "EarLeds", "ChestLeds", "FeetLeds", "BrainLeds" ] );

    # Sensors
    rm.addChilds( "Sensors", [ "Brain", "Chest", "Feet" ] );
    rm.addChilds( "Feet", [ "LFoot", "RFoot" ] );

# ressourceCreateNaoRessource - end


def getNaoChestName():
    "get the nao name as stored in the rom chest"
    stm = myGetProxy( "ALMemory" );
    strNum = stm.getData( "Device/DeviceList/ChestBoard/BodyNickName" );
    if( strNum == 'Nao336' and getNaoNickName() == 'Astroboy' ):
        strNum = 'Nao332';    
    return strNum;
# getNaoChestName - end

def getNaoNickName():
    "get the nao name as given by user"
    # return executeAndGrabOutput( "hostname", True );
    return getFileFirstLine( '/etc/hostname' );
# getNaoNickName - end

global_listNaoOwner = {
    '316': ['Valentin','Nanimator'],
    '327': ['Alex','NaoAlex'],  
    '302': ['Flora','NaoFlop'],
    '471': ['Céline','Lestate'],
    '488': ['Jérome','NaoIntissar'],
    '492': ['Julien','Nao2Jams'],
    
    '340': ['JmPomies','Tifouite'],
    '337': ['Jerome Laplace',''],
    '329': ['Locki','Noah'],
    '340': ['Troopa',''],
    '351': ['Mlecyloj',''],
    '317': ['Scoobi','Nao'],
    '379': ['Ksan','Timmy'],
    '387': ['Richard Seltrecht','Isaac'],
    '341': ['Zelig','Sonny'],
    '339': ['Rodriguez','Andrew'],
    '305': ['Tibot','Zoé'],
    '314': ['Laurent','Nao'],
    '409': ['Drack','Igor'],
    '319': ['Oxman','R2'],
    '342': ['Jfiger',''],
    '321': ['Bothari','Tchoggi'],
    '307': ['Alexan','Cybot'],
    '407': ['Olleke','Domo'],
    '412': ['Hadrien',''],
    '312': ['Bilbo','Nao'],
    '334': ['Nameluas','Nao'],
    '338': ['DavidRPT','Nao'],
    '332': ['Clayde','AstroBoy'],  # 332 renamed in 336
    '336': ['Harkanork','Tao'],
    '330': ['Antoine','Naodadi'],
    '367': ['Mataweh','Junior'],
    '358': ['Lexa','Zirup'],
    '306': ['Gwjsan','Naomi'],
};

def getUserNameFromChestBody():
    "get the user name from the chest number"
    "WRN: valid only for appu, and beta30!"
    global global_listNaoOwner;
    strNum = getNaoChestName(); 
    strNum = strNum[3:];
    strName = global_listNaoOwner[strNum][0];
    return strName;
# getUserNameFromChestBody - end

def getNaoNicknameFromChestBody():
    "get the user name from the chest number"
    "WRN: valid only for appu, and beta30!"
    global global_listNaoOwner;
    strNum = getNaoChestName(); 
    strNum = strNum[3:];
    strName = global_listNaoOwner[strNum][1];
    if( strName == '' ):
        return 'Nao';
    return strName;
# getUserNameFromChestBody - end

#print( "Le robot de %s, c'est %s." % ( getUserNameFromChestBody(), getNaoNicknameFromChestBody() ) );

def getCurrentApplicationHelp():
    "return help of current nao application"
    return ""; # TODO
# getCurrentApplicationHelp - end

global_strNotificationVarName = "ALTools/NotificationMessage";
def getCurrentNotification():
    "return current notification about something, a memo or ... (or '' if none)"
    global global_strNotificationVarName;
    stm = myGetProxy( "ALMemory" );
    try:
        return stm.getData( global_strNotificationVarName, 0 );
    except:
        return "";
# getCurrentNotification - end

def getCurrentNotification_ApplicationName():
    global global_strNotificationVarName;
    stm = myGetProxy( "ALMemory" );
    try:
        return stm.getData( global_strNotificationVarName + "_application_name", 0 );
    except:
        return "";
# getCurrentNotification_ApplicationName - end


def setCurrentNotification( strMessage = "" ):
    "change the notification state ("" to reset)"
    global global_strNotificationVarName;
    stm = myGetProxy( "ALMemory" );
    stm.insertData( global_strNotificationVarName, strMessage );
    debug( "altools.setCurrentNotification to '%s'" % strMessage );
# setCurrentNotification - end

def setCurrentNotification_ApplicationName( strApplicationName = "" ):
    "change the notification application name ("" to reset)"
    global global_strNotificationVarName;
    stm = myGetProxy( "ALMemory" );
    stm.insertData( global_strNotificationVarName + "_application_name", strApplicationName );
    debug( "altools.setCurrentNotification_ApplicationName to '%s'" % strApplicationName );
# setCurrentNotification_ApplicationName - end
    
def getLaunchApplicationALMemoryKeyName():
    "return the name of the ALMemory key name where 'launch application' order are posted"
    return "ALTools/LaunchNow";
# getLaunchApplicationALMemoryKeyName - end

def launchApplication( strApplicationName ):
    "Post a launch application wish to the ALMemory"
    print( "altools.launchApplication: sending launch order of '%s'" % strApplicationName );
    stm = myGetProxy( "ALMemory" );
    stm.insertData( getLaunchApplicationALMemoryKeyName(), strApplicationName );
# launchApplication - end

    


def getCpuLoad():
    "get the current cpu load/usage (as a integer percent) (the second value from uptime)"
    "in fact the first value it's better: it represents 1min, so it's more interesting"
    # strRet = executeAndGrabOutput( "uptime | cut -dg -f2 | cut -d: -f2" );
    #~ try:
        #~ strText = executeAndGrabOutput( "uptime" );
        #~ aAnalysed = strText.split( 'load average:' );
        #~ aAnalysed = aAnalysed[1].split( ',' );
        #~ return int(float( aAnalysed[1] ) * 100);
    #~ except:
        #~ return 0;
  
    try:
        szCpuLoad = "/proc/loadavg";
        strAllFile = getFileContents( szCpuLoad );
        listVar = strAllFile.split( ' ' );
        if( len( listVar ) > 1 ):
            return int( float( listVar[0] ) * 100 ); # change listVar[1] to [0] to have the time on 1 min
    except BaseException, err:
        debug( "ERR: altools.getCpuLoad: %s" % str( err ) );
    return 0;
# getCpuLoad - end


def isFootPressed( strFeetLetter = 'L' ):
    "return true if the foot has at least one bumper empushed"
    strTemplateKeyName = "Device/SubDeviceList/%sFoot/Bumper/%s/Sensor/Value";  
    stm = myGetProxy( "ALMemory" );
    listRightFeetBumpers = stm.getListData( [strTemplateKeyName % ( strFeetLetter, "Left" ), strTemplateKeyName % ( strFeetLetter, "Right" )] );
    return listRightFeetBumpers[0] or listRightFeetBumpers[1];
# isFootPressed - end

def assumeStiffness( strChainName, rValue, bDontWait = False ):
    "assume that stiffness is equal or greater to rValue"
    "Chain can be a motion chain or 'Body'"
    # Whole body case
    if( strChainName == 'Body' ):
        for strJoint in ['Head', 'LArm', 'RArm', 'LLeg', 'RLeg' ]:
            assumeStiffness( strJoint, rValue, ( strJoint != 'RLeg' or bDontWait ) ); # si dontwait: tous vont etre en dontwait, sinon seul le dernier sera en wait
        return;

    motion = myGetProxy( 'ALMotion' );
    listStiff = motion.getStiffnesses( strChainName );
    bDoStiff = False;
    for rStiff in listStiff:
        if( rStiff < rValue ):
            bDoStiff = True;
            break;
    if( bDoStiff ):
        rTime = 0.7;
        if( bDontWait ):
            motion.post.stiffnessInterpolation( strChainName, rValue, rTime );
        else:
            motion.stiffnessInterpolation( strChainName, rValue, rTime );
# assumeStiffness - end

def assumeStiffnessBelow( strChainName, rValue, bDontWait = False ):
    "assume that stiffness is below or equal than rValue"
    "Chain can be a motion chain or 'Body'"
    # Whole body case
    if( strChainName == 'Body' ):
        for strJoint in ['Head', 'LArm', 'RArm', 'LLeg', 'RLeg' ]:
            assumeStiffnessBelow( strJoint, rValue, ( strJoint != 'RLeg' or bDontWait ) ); # si dontwait: tous vont etre en dontwait, sinon seul le dernier sera en wait
        return;
        
    motion = myGetProxy( 'ALMotion' );
    listStiff = motion.getStiffnesses( strChainName );
    bDoStiff = False;
    for rStiff in listStiff:
        if( rStiff > rValue ):
            bDoStiff = True;
            break;
    
    if( bDoStiff ):
        rTime = 0.7;
        if( bDontWait ):
            motion.post.stiffnessInterpolation( strChainName, rValue, rTime );
        else:
            motion.stiffnessInterpolation( strChainName, rValue, rTime );
# assumeStiffness - end

global_getNbrMoveOrder_listKeyOrder = [];
global_getNbrMoveOrder_listKeyValue = [];
global_getNbrMoveOrder_listKeyStiffness = [];
global_getNbrMoveOrder_listOrder_prev = [];

def getNbrMoveOrder( nThreshold = 0.06 ):
    "compute current joint moving by order"
    mem = myGetProxy( "ALMemory" );
    global global_getNbrMoveOrder_listKeyOrder;
    global global_getNbrMoveOrder_listKeyValue;
    global global_getNbrMoveOrder_listKeyStiffness;
    global global_getNbrMoveOrder_listOrder_prev;

    # first time: generate key list
    if( len( global_getNbrMoveOrder_listKeyOrder ) < 1 ):
        listJointName = getDcmBodyJointName();
        for strJointName in listJointName:
            global_getNbrMoveOrder_listKeyOrder.append( "Device/SubDeviceList/%s/Position/Actuator/Value" % strJointName );
            global_getNbrMoveOrder_listKeyValue.append( "Device/SubDeviceList/%s/Position/Sensor/Value" % strJointName );
            global_getNbrMoveOrder_listKeyStiffness.append( "Device/SubDeviceList/%s/Hardness/Actuator/Value" % strJointName );
            global_getNbrMoveOrder_listOrder_prev = mem.getListData( global_getNbrMoveOrder_listKeyOrder ); # init first time

    # get all values
    arOrder = mem.getListData( global_getNbrMoveOrder_listKeyOrder );
    arValue = mem.getListData( global_getNbrMoveOrder_listKeyValue );
    arStiffness= mem.getListData( global_getNbrMoveOrder_listKeyStiffness );

    nNbr = 0;
    for i in range( len( arOrder ) ):
        # a joint is moving if: pos is different from order, if order changed and if stiffness
        # we can have a big difference between order and value when no stiffness (position is out of range)
        if( ( abs( arOrder[i] - arValue[i] ) > nThreshold or abs( global_getNbrMoveOrder_listOrder_prev[i] - arOrder[i] ) > 0.01 ) and arStiffness[i] > 0.01 ):
            nNbr += 1;
            debug( "getNbrMoveOrder: difference on %s: order: %f; sensor: %f; stiffness: %f" % ( global_getNbrMoveOrder_listKeyValue[i], arOrder[i], arValue[i], arStiffness[i] ) );
    global_getNbrMoveOrder_listOrder_prev = arOrder;
    return nNbr;
# getNbrMoveOrder - end    


global_animations_FrameNumber = dict();
def animations_resetFrameNumber( strBoxName ):
    print( "********* animations_resetFrameNumber( '%s' )" % strBoxName );    
    global global_animations_FrameNumber;
    global_animations_FrameNumber[strBoxName] = 0;
    
def animations_increaseFrameNumber( strBoxName, nbr ):
    "called from children"
    print( "********* animations_increaseFrameNumber( '%s', %d )" % ( strBoxName, nbr ) );
    global global_animations_FrameNumber;
    strBoxName = choregrapheGetParentName( strBoxName );
    try:
        global_animations_FrameNumber[strBoxName] += nbr;
    except:
        # not existing        
        global_animations_FrameNumber[strBoxName] = nbr;
    
def animations_getFrameNumber( strBoxName ):
    print( "********* animations_getFrameNumber( '%s' )" % strBoxName );    
    global global_animations_FrameNumber;
    try:
        return global_animations_FrameNumber[strBoxName];
    except:
        return 0;

#animations_resetFrameNumber( "toto" );
#animations_increaseFrameNumber( "toto__tutu", 5 );
#print( "gfn: " + str(  animations_getFrameNumber( "toto" ) ) );




def innerTest():
  "altools inner test method (TODO: UPDATE)"
  SayAndEyes( "InnerTest" );
# innerTest

print( "*** altools: parsing finished" );

# to know end of loading
global_bIsLoaded = True;


# globals

if( naoconfig.bDebugMode ):
  if( isOnNao() ):
    print( "altools: enabling Heat Monitoring and stuffs..." );
    try:
        sentinel = myGetProxy( "ALSentinel" );
        sentinel.enableHeatMonitoring( True ); # pour tout de suite voir les problemes !
        sentinel.enableCheckRemainingRam( True );
        motion = myGetProxy( "ALMotion" );
        motion.setMotionConfig( [["ACTIVATE_DEBUG_OF_FALL_MANAGER", True]] );
    except:
        debug( "enableHeatMonitoring at startup: foiring" );

import gc
if( naoconfig.bDebugMode ):
	pass
#  gc.set_debug(gc.DEBUG_LEAK);
#  gc.set_debug(gc.DEBUG_STATS);
#  gc.set_debug(gc.DEBUG_SAVEALL);

# set the standard voice of this Nao
# setSpeakLanguage( getDefaultSpeakLanguage() ); # TODO: refaire pour la bonne gestion.
# en attendant, pour passer le robot en francais par défaut, 
# mettre a la fin de l'autolaunch.py, la ligne suivante:
# LaunchThread( "ALTextToSpeech", "loadVoicePreference",  "NaoOfficialVoiceFrench" );


# create nao ressources
if( isOnNao() ):
    ressourceCreateNaoRessource();


##############################################
# test zone
##############################################

#InnerTest();

#a = [1,2];
#print find(a, 0);

#import threading
#print threading.enumerate();

# RecognizeWords( ["hello", "bye"], True, 0.2 );

# sayAndCache( "coucou" );

#'read this short text'.translate( None, 'aeiou') # None comme argument n'existe pas avant python 2.6
#'read this short text'.translate( string.maketrans("",""), 'aeiou') # ceci fonctionne !

#import commands
#print( str( commands.getoutput("dir") ) ); # fonctionne pas sous windows: => '{' n'est pas reconnu en tant que commande interne

# print( "isOnNao: " + str( isOnNao() ) );
# executeAndGrabOutput( "time /t" );

#print( datetime.datetime.today().strftime("%Y_%m_%d") )
#print( datetime.datetime.today().strftime("%H:%M") )

# findFile( "c:\\temp", ".xar" );

# print( "toto.html".rstrip( ".html" ) );

#print( "eval - before" );
#asyncSystemCall( "sleep 3" );
#asyncEval( "time.sleep( 2 )" );
#print( "eval - after" );

#import time
#global_nValue = 1;
#print( "global_nValue: %d" % global_nValue );
#asyncEval( "global_nValue = 2" );
#time.sleep( 2 );
#print( "global_nValue: %d" % global_nValue );

#tunes = NaoTunes();
#tunes.setMusicPathByStyle( getMusicPath() );
#print( tunes.toString() );
#print( "liststyles: " + str( tunes.getListStyle() ) );
#tunes.playByStyle( "", True );
#tunes.playByStyle( "rock", False );
#tunes.playByStyle( "rock" );
#tunes.playByStyle( "rock" );
#print( "current playing: " + tunes.getCurrentPlaying().toString( True ) );
#print( "current playing: " + tunes.getCurrentPlaying().toString( False ) );
#print( "current static: " + tunes.static_getCurrentPlaying().toString( True ) );
#sayInfoMusic();

#getInCache( "toto", int );
#storeInCache( "toto", 3 );
#print( getInCache( "toto", int ) );
#print( "ALMemory: " + str( myGetProxy( "ALMemory" ) ) );
#print( "ALMemory: " + str( myGetProxy( "ALMemory" ) ) );
#print( "ALMemory: " + str( myGetProxy( "ALMemory" ) ) );

#setSpeakLanguage( 0 );
#sayAndCache( "hello" );
#setSpeakLanguage( 1 );
#sayAndCache( "hello" );

#import py_compile
#py_compile.compile( 'altools.py' )

#subprocess.Popen( "aplay /opt/naoqi/data/wav/warning.wav", shell=True );

# sayAndCache( "coco" );

#const.toto = 3;

#strPage = getHtmlPage( "http://fr.wikipedia.org/wiki/Special:Page_au_hasard" );
#print( strPage );

#print( "const.ressource_weak before print" );
#print( "const.ressource_weak value: %d" % const.ressource_weak );
#print( "const.ressource_weak after print" );

#getHtmlPage( '"http://mangedisque.com/index.php"' );

