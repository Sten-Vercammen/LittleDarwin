import sys
from JavaParser import JavaParser
from JavaParse import JavaParse
import copy
from antlr4.tree.Tree import TerminalNodeImpl

sys.setrecursionlimit(50000)



class JavaMutate(object):
    def __init__(self, javaParseObjectInput=None, verbose=False):
        self.verbose = verbose

        if javaParseObjectInput is not None:
            self.javaParseObject = javaParseObjectInput
        else:
            self.javaParseObject = JavaParse(self.verbose)

    def applyMutators(self, tree, type):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTrees = list()
        mutationTypeCount = dict()

        # mutatedTrees.extend(self.arithmeticOperatorDeletionShortcut(tree))
        # mutatedTrees.extend(self.arithmeticOperatorDeletionUnary(tree))
        # mutatedTrees.extend(self.arithmeticOperatorInsertionShortcut(tree))
        # mutatedTrees.extend(self.arithmeticOperatorInsertionUnary(tree))
        # mutatedTrees.extend(self.conditionalOperatorInsertion(tree))
        # mutatedTrees.extend(self.logicalOperatorDeletion(tree))
        # mutatedTrees.extend(self.logicalOperatorInsertion(tree))

        if type == "classical" or type == "all":
            resultArithmeticOperatorReplacementBinary = self.arithmeticOperatorReplacementBinary(tree)
            mutatedTrees.extend(resultArithmeticOperatorReplacementBinary)
            mutationTypeCount["ArithmeticOperatorReplacementBinary"] = len(resultArithmeticOperatorReplacementBinary)

            resultArithmeticOperatorReplacementShortcut = self.arithmeticOperatorReplacementShortcut(tree)
            mutatedTrees.extend(resultArithmeticOperatorReplacementShortcut)
            mutationTypeCount["ArithmeticOperatorReplacementShortcut"] = len(
                resultArithmeticOperatorReplacementShortcut)

            resultArithmeticOperatorReplacementUnary = self.arithmeticOperatorReplacementUnary(tree)
            mutatedTrees.extend(resultArithmeticOperatorReplacementUnary)
            mutationTypeCount["ArithmeticOperatorReplacementUnary"] = len(resultArithmeticOperatorReplacementUnary)

            # currently generating too many mutations
            # resultNegateConditionalsMutator = self.negateConditionalsMutator(tree)
            # mutatedTrees.extend(resultNegateConditionalsMutator)
            # mutationTypeCount["NegateConditionalsMutator"] = len(resultNegateConditionalsMutator)

            resultLogicalOperatorReplacement = self.logicalOperatorReplacement(tree)
            mutatedTrees.extend(resultLogicalOperatorReplacement)
            mutationTypeCount["LogicalOperatorReplacement"] = len(resultLogicalOperatorReplacement)

            resultShiftOperatorReplacement = self.shiftOperatorReplacement(tree)
            mutatedTrees.extend(resultShiftOperatorReplacement)
            mutationTypeCount["ShiftOperatorReplacement"] = len(resultShiftOperatorReplacement)

            resultRelationalOperatorReplacement = self.relationalOperatorReplacement(tree)
            mutatedTrees.extend(resultRelationalOperatorReplacement)
            mutationTypeCount["RelationalOperatorReplacement"] = len(resultRelationalOperatorReplacement)

            resultConditionalOperatorReplacement = self.conditionalOperatorReplacement(tree)
            mutatedTrees.extend(resultConditionalOperatorReplacement)
            mutationTypeCount["ConditionalOperatorReplacement"] = len(resultConditionalOperatorReplacement)

            resultConditionalOperatorDeletion = self.conditionalOperatorDeletion(tree)
            mutatedTrees.extend(resultConditionalOperatorDeletion)
            mutationTypeCount["ConditionalOperatorDeletion"] = len(resultConditionalOperatorDeletion)

            resultAssignmentOperatorReplacementShortcut = self.assignmentOperatorReplacementShortcut(tree)
            mutatedTrees.extend(resultAssignmentOperatorReplacementShortcut)
            mutationTypeCount["AssignmentOperatorReplacementShortcut"] = len(
                resultAssignmentOperatorReplacementShortcut)

        elif type == "object-oriented" or type == "all":
            pass

        return (mutatedTrees, mutationTypeCount)

    def negateConditionalsMutator(self, tree):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ParExpressionContext)

        while len(expressionList) > 0:
            # tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ParExpressionContext)
            assert isinstance(node.children[0], TerminalNodeImpl)
            assert isinstance(node.children[2], TerminalNodeImpl)
            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore
            originalText0 = copy.deepcopy(node.children[0].symbol.text)
            node.children[0].symbol.text = u"(!("
            originalText2 = copy.deepcopy(node.children[2].symbol.text)
            node.children[2].symbol.text = u"))"
            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter
            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: negateConditionalsMutator\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))
            # mutatedTreesTexts.append(tree.getText())
            node.children[0].symbol.text = copy.deepcopy(originalText0)
            node.children[2].symbol.text = copy.deepcopy(originalText2)

        return mutatedTreesTexts


    # Method Level Mutants """

    def arithmeticOperatorReplacementBinary(self, tree):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            # tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if not (isinstance(node.children[0], JavaParser.ExpressionContext) and isinstance(node.children[1],
                                                                                                  TerminalNodeImpl) and isinstance(
                        node.children[2], JavaParser.ExpressionContext)):
                    continue  # not a binary expression
            except Exception, e:
                continue

            if not (node.children[1].symbol.text == u"+" or node.children[1].symbol.text == u"-" or node.children[
                1].symbol.text == u"*" or node.children[1].symbol.text == u"/" or node.children[1].symbol.text == u"%"):
                continue  # not an arithmetic operator

            if node.children[0].getText()[0] == '\"' or node.children[2].getText()[0] == '\"':
                continue  # string concatenation, don't change

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore
            originalText = copy.deepcopy(node.children[1].symbol.text)

            if originalText == u"+":
                node.children[1].symbol.text = u"-"
            elif originalText == u"-":
                node.children[1].symbol.text = u"+"
            elif originalText == u"/":
                node.children[1].symbol.text = u"*"
            elif originalText == u"*":
                node.children[1].symbol.text = u"/"
            elif originalText == u"%":
                node.children[1].symbol.text = u"/"
            else:
                assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter
            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: arithmeticOperatorReplacementBinary\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))  # create compilable, readable code

            node.children[1].symbol.text = copy.deepcopy(originalText)

        return mutatedTreesTexts


    def arithmeticOperatorReplacementUnary(self, tree):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            # tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if not (isinstance(node.children[0], TerminalNodeImpl) and isinstance(node.children[1],
                                                                                      JavaParser.ExpressionContext)):
                    continue  # not a unary expression
            except Exception, e:
                continue

            if not (node.children[0].symbol.text == u"+" or node.children[0].symbol.text == u"-"):
                continue  # not an arithmetic operator

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore
            originalText = copy.deepcopy(node.children[0].symbol.text)

            if originalText == u"+":
                node.children[0].symbol.text = u"-"
            elif originalText == u"-":
                node.children[0].symbol.text = u"+"
            else:
                assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter
            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: arithmeticOperatorReplacementUnary\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))  # create compilable, readable code

            node.children[0].symbol.text = copy.deepcopy(originalText)

        return mutatedTreesTexts

    def arithmeticOperatorReplacementShortcut(self, tree):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            # tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if isinstance(node.children[0], TerminalNodeImpl) and isinstance(node.children[1],
                                                                                 JavaParser.ExpressionContext):
                    terminalChild = 0
                elif isinstance(node.children[1], TerminalNodeImpl) and isinstance(node.children[0],
                                                                                   JavaParser.ExpressionContext):
                    terminalChild = 1
                else:
                    continue  # not a shortcut expression
            except Exception, e:
                continue

            if not (node.children[terminalChild].symbol.text == u"++" or node.children[
                terminalChild].symbol.text == u"--"):
                continue  # not an arithmetic operator

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore
            originalText = copy.deepcopy(node.children[terminalChild].symbol.text)

            if originalText == u"++":
                node.children[terminalChild].symbol.text = u"--"
            elif originalText == u"--":
                node.children[terminalChild].symbol.text = u"++"
            else:
                assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter

            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: arithmeticOperatorReplacementShortcut\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))  # create compilable, readable code

            node.children[terminalChild].symbol.text = copy.deepcopy(originalText)

        return mutatedTreesTexts

    def arithmeticOperatorInsertionUnary(self, tree):
        pass

    def arithmeticOperatorInsertionShortcut(self, tree):
        pass

    def arithmeticOperatorDeletionUnary(self, tree):
        pass

    def arithmeticOperatorDeletionShortcut(self, tree):
        pass

    def relationalOperatorReplacement(self, tree):  # covered by negateConditionals
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            # tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if not (isinstance(node.children[0], JavaParser.ExpressionContext) and isinstance(node.children[1],
                                                                                                  TerminalNodeImpl) and isinstance(
                        node.children[2], JavaParser.ExpressionContext)):
                    continue  # not a binary expression
            except Exception, e:
                continue

            if not (node.children[1].symbol.text == u">" or node.children[1].symbol.text == u"<" or node.children[
                1].symbol.text == u">=" or node.children[1].symbol.text == u"<=" or node.children[
                1].symbol.text == u"==" or node.children[1].symbol.text == u"!="):
                continue  # not a relation operator

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore

            originalText = copy.deepcopy(node.children[1].symbol.text)

            if originalText == u">":
                node.children[1].symbol.text = u"<="
            elif originalText == u"<":
                node.children[1].symbol.text = u">="
            elif originalText == u"<=":
                node.children[1].symbol.text = u">"
            elif originalText == u">=":
                node.children[1].symbol.text = u"<"
            elif originalText == u"!=":
                node.children[1].symbol.text = u"=="
            elif originalText == u"==":
                node.children[1].symbol.text = u"!="
            else:
                assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter

            mutatedTreesTexts.append((
                (
                    "/* LittleDarwin generated mutant\n mutant type: relationalOperatorReplacement\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                        " ".join(tree.getText().rsplit("<EOF>", 1))))))  # create compilable, readable code

            node.children[1].symbol.text = copy.deepcopy(originalText)

        return mutatedTreesTexts

    def conditionalOperatorReplacement(self, tree):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            # tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if not (isinstance(node.children[0], JavaParser.ExpressionContext) and isinstance(node.children[1],
                                                                                                  TerminalNodeImpl) and isinstance(
                        node.children[2], JavaParser.ExpressionContext)):
                    continue  # not a binary expression
            except Exception, e:
                continue

            if not (node.children[1].symbol.text == u"&&" or node.children[1].symbol.text == u"||"):
                continue  # not a conditional operator (non-lazy ones covered in logical operators)

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore

            originalText = copy.deepcopy(node.children[1].symbol.text)

            if originalText == u"&&":
                node.children[1].symbol.text = u"||"
            elif originalText == u"||":
                node.children[1].symbol.text = u"&&"
            else:
                assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter
            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: conditionalOperatorReplacement\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))  # create compilable, readable code

            node.children[1].symbol.text = copy.deepcopy(originalText)

        return mutatedTreesTexts


    def conditionalOperatorDeletion(self, tree):  # covered by negateConditionals
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            # tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if not (isinstance(node.children[0], TerminalNodeImpl) and isinstance(node.children[1],
                                                                                      JavaParser.ExpressionContext)):
                    continue  # not a unary expression
            except Exception, e:
                continue

            if not (node.children[0].symbol.text == u"!"):
                continue  # not a unary conditional operator

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore
            originalText = copy.deepcopy(node.children[0].symbol.text)

            if originalText == u"!":
                node.children[0].symbol.text = u" "
            else:
                assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter
            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: conditionalOperatorDeletion\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))  # create compilable, readable code

            node.children[0].symbol.text = copy.deepcopy(originalText)

        return mutatedTreesTexts


    # def conditionalOperatorInsertion(self, tree): # covered by negateConditionals, both generate too many mutations
    # pass

    def shiftOperatorReplacement(self, tree):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            #tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if (isinstance(node.children[0], JavaParser.ExpressionContext) and isinstance(node.children[1],
                                                                                              TerminalNodeImpl) and isinstance(
                        node.children[2], TerminalNodeImpl) and isinstance(node.children[3],
                                                                           JavaParser.ExpressionContext)):
                    threeTerminals = False
                elif (isinstance(node.children[0], JavaParser.ExpressionContext) and isinstance(node.children[1],
                                                                                                TerminalNodeImpl) and isinstance(
                        node.children[2], TerminalNodeImpl) and isinstance(node.children[3],
                                                                           TerminalNodeImpl) and isinstance(
                        node.children[4], JavaParser.ExpressionContext)):
                    threeTerminals = True
                else:
                    continue  # not a binary shift expression
            except Exception, e:
                continue

            try:
                if (threeTerminals is False) and (
                            (node.children[1].symbol.text == u"<" and node.children[2].symbol.text == u"<") or (
                                        node.children[1].symbol.text == u">" and node.children[2].symbol.text == u">")):
                    pass
                elif (threeTerminals is True) and (
                                    node.children[1].symbol.text == u">" and node.children[2].symbol.text == u">" and
                                node.children[3].symbol.text == u">"):
                    pass
                else:
                    continue  # not a shift operator
            except Exception, e:
                continue

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore

            if threeTerminals:
                originalText1 = copy.deepcopy(node.children[1].symbol.text)
                originalText2 = copy.deepcopy(node.children[2].symbol.text)
                originalText3 = copy.deepcopy(node.children[3].symbol.text)

                if originalText1 == u">" and originalText2 == u">" and originalText3 == u">":
                    node.children[3].symbol.text = u" "
                else:
                    assert False

            else:
                originalText1 = copy.deepcopy(node.children[1].symbol.text)
                originalText2 = copy.deepcopy(node.children[2].symbol.text)

                if originalText1 == u">" and originalText2 == u">":
                    node.children[1].symbol.text = u"<"
                    node.children[2].symbol.text = u"<"
                elif originalText1 == u"<" and originalText2 == u"<":
                    node.children[1].symbol.text = u">"
                    node.children[2].symbol.text = u">"
                else:
                    assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter

            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: shiftOperatorReplacement\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))  # create compilable, readable code

            node.children[1].symbol.text = copy.deepcopy(originalText1)
            node.children[2].symbol.text = copy.deepcopy(originalText2)
            if threeTerminals:
                node.children[3].symbol.text = copy.deepcopy(originalText3)

        return mutatedTreesTexts

    def logicalOperatorReplacement(self, tree):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            #tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if not (isinstance(node.children[0], JavaParser.ExpressionContext) and isinstance(node.children[1],
                                                                                                  TerminalNodeImpl) and isinstance(
                        node.children[2], JavaParser.ExpressionContext)):
                    continue  # not a binary expression
            except Exception, e:
                continue

            if not (node.children[1].symbol.text == u"&" or node.children[1].symbol.text == u"|" or node.children[
                1].symbol.text == u"^"):
                continue  # not a logical operator

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore

            originalText = copy.deepcopy(node.children[1].symbol.text)

            if originalText == u"&":
                node.children[1].symbol.text = u"|"
            elif originalText == u"|":
                node.children[1].symbol.text = u"^"
            elif originalText == u"^":
                node.children[1].symbol.text = u"&"
            else:
                assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter
            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: logicalOperatorReplacement\n " + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))  # create compilable, readable code

            node.children[1].symbol.text = copy.deepcopy(originalText)

        return mutatedTreesTexts

    def logicalOperatorInsertion(self, tree):
        pass

    def logicalOperatorDeletion(self, tree):
        pass

    def assignmentOperatorReplacementShortcut(self, tree):
        assert isinstance(tree, JavaParser.CompilationUnitContext)
        mutatedTreesTexts = list()
        expressionList = self.javaParseObject.seek(tree, JavaParser.ExpressionContext)

        while len(expressionList) > 0:
            #tmpTree = copy.deepcopy(tree)
            expressionIndex = expressionList.pop()

            node = self.javaParseObject.getNode(tree, expressionIndex)
            assert isinstance(node, JavaParser.ExpressionContext)

            try:
                if not (isinstance(node.children[0], JavaParser.ExpressionContext) and isinstance(node.children[1],
                                                                                                  TerminalNodeImpl) and isinstance(
                        node.children[2], JavaParser.ExpressionContext)):
                    continue  # not a binary expression
            except Exception, e:
                continue

            if not (node.children[1].symbol.text == u"+=" or node.children[1].symbol.text == u"-=" or node.children[
                1].symbol.text == u"*=" or node.children[1].symbol.text == u"/=" or node.children[
                1].symbol.text == u"%=" or node.children[1].symbol.text == u"&=" or node.children[
                1].symbol.text == u"|=" or node.children[1].symbol.text == u"^=" or node.children[
                1].symbol.text == u"<<=" or node.children[1].symbol.text == u">>=" or node.children[
                1].symbol.text == u">>>="):
                continue  # not an assignment operator

            mutationBefore = "----> before: " + node.getText()
            if self.verbose:
                print mutationBefore

            originalText = copy.deepcopy(node.children[1].symbol.text)

            if originalText == u"+=":
                node.children[1].symbol.text = u"-="
            elif originalText == u"-=":
                node.children[1].symbol.text = u"+="
            elif originalText == u"/=":
                node.children[1].symbol.text = u"*="
            elif originalText == u"*=":
                node.children[1].symbol.text = u"/="
            elif originalText == u"%=":
                node.children[1].symbol.text = u"/="
            elif originalText == u"&=":
                node.children[1].symbol.text = u"|="
            elif originalText == u"|=":
                node.children[1].symbol.text = u"^="
            elif originalText == u"^=":
                node.children[1].symbol.text = u"&="
            elif originalText == u">>=":
                node.children[1].symbol.text = u">>>="
            elif originalText == u"<<=":
                node.children[1].symbol.text = u">>="
            elif originalText == u">>>=":
                node.children[1].symbol.text = u">>="
            else:
                assert False

            mutationAfter = "----> after: " + node.getText()
            if self.verbose:
                print mutationAfter
            mutatedTreesTexts.append((
                "/* LittleDarwin generated mutant\n mutant type: assignmentOperatorReplacementShortcut\n" + mutationBefore + "\n" + mutationAfter + "\n----> line number in original file: " + str(node.start.line) + "\n*/ \n\n" + (
                    " ".join(tree.getText().rsplit("<EOF>", 1)))))  # create compilable, readable code

            node.children[1].symbol.text = copy.deepcopy(originalText)

        return mutatedTreesTexts