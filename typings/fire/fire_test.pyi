"""
This type stub file was generated by pyright.
"""

import sys
import six
from fire import testutils

"""Tests for the fire module."""
class FireTest(testutils.BaseTestCase):
  def testFire(self):
    ...
  
  def testFirePositionalCommand(self):
    ...
  
  def testFireInvalidCommandArg(self):
    ...
  
  def testFireDefaultName(self):
    ...
  
  def testFireNoArgs(self):
    ...
  
  def testFireExceptions(self):
    ...
  
  def testFireNamedArgs(self):
    ...
  
  def testFireNamedArgsSingleHyphen(self):
    ...
  
  def testFireNamedArgsWithEquals(self):
    ...
  
  def testFireNamedArgsWithEqualsSingleHyphen(self):
    ...
  
  def testFireAllNamedArgs(self):
    ...
  
  def testFireAllNamedArgsOneMissing(self):
    ...
  
  def testFirePartialNamedArgs(self):
    ...
  
  def testFirePartialNamedArgsOneMissing(self):
    ...
  
  def testFireAnnotatedArgs(self):
    ...
  
  @testutils.skipIf(six.PY2, 'Keyword-only arguments not in Python 2.')
  def testFireKeywordOnlyArgs(self):
    ...
  
  def testFireProperties(self):
    ...
  
  def testFireRecursion(self):
    ...
  
  def testFireVarArgs(self):
    ...
  
  def testFireVarArgsWithNamedArgs(self):
    ...
  
  def testFireKeywordArgs(self):
    ...
  
  def testFireKeywordArgsWithMissingPositionalArgs(self):
    ...
  
  def testFireObject(self):
    ...
  
  def testFireDict(self):
    ...
  
  def testFireObjectWithDict(self):
    ...
  
  def testFireSet(self):
    ...
  
  def testFireFrozenset(self):
    ...
  
  def testFireList(self):
    ...
  
  def testFireObjectWithList(self):
    ...
  
  def testFireObjectWithTuple(self):
    ...
  
  def testFireObjectWithListAsObject(self):
    ...
  
  def testFireObjectWithTupleAsObject(self):
    ...
  
  def testFireNoComponent(self):
    ...
  
  def testFireUnderscores(self):
    ...
  
  def testFireUnderscoresInArg(self):
    ...
  
  def testBoolParsing(self):
    ...
  
  def testBoolParsingContinued(self):
    ...
  
  def testBoolParsingSingleHyphen(self):
    ...
  
  def testBoolParsingLessExpectedCases(self):
    ...
  
  def testSingleCharFlagParsing(self):
    ...
  
  def testSingleCharFlagParsingEqualSign(self):
    ...
  
  def testSingleCharFlagParsingExactMatch(self):
    ...
  
  def testSingleCharFlagParsingCapitalLetter(self):
    ...
  
  def testBoolParsingWithNo(self):
    ...
  
  def testTraceFlag(self):
    ...
  
  def testHelpFlag(self):
    ...
  
  def testHelpFlagAndTraceFlag(self):
    ...
  
  def testTabCompletionNoName(self):
    ...
  
  def testTabCompletion(self):
    ...
  
  def testTabCompletionWithDict(self):
    ...
  
  def testBasicSeparator(self):
    ...
  
  def testNonComparable(self):
    """Fire should work with classes that disallow comparisons."""
    ...
  
  def testExtraSeparators(self):
    ...
  
  def testSeparatorForChaining(self):
    ...
  
  def testNegativeNumbers(self):
    ...
  
  def testFloatForExpectedInt(self):
    ...
  
  def testClassInstantiation(self):
    ...
  
  def testTraceErrors(self):
    ...
  
  def testClassWithDefaultMethod(self):
    ...
  
  def testClassWithInvalidProperty(self):
    ...
  
  @testutils.skipIf(sys.version_info[0: 2] <= (3, 4), 'Cannot inspect wrapped signatures in Python 2 or 3.4.')
  def testHelpKwargsDecorator(self):
    ...
  


if __name__ == '__main__':
  ...
