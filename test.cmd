@echo off
echo test lexer

python lexer.py test\test_lexer.dsl > test_out\test_lexer.out

echo test parser

python parser.py test\test_parser.dsl > test_out\test_parser.out

echo test interpreter

python main.py test\test_interpreter.dsl > test_out\test_interpreter.out