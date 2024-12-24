echo ==============================
echo        Testing Lexer
echo ==============================

for ((i=1; i<=3; i++))
do
    echo testing test$i lexer
    python lexer.py test/test$i.dsl 1> test_out/lexer/test$i.out 2>test_out/lexer/test${i}_error.out

    shasum -a 256 "test_out/lexer/test$i.out" | awk '{ print $1 }' > "test_out/lexer/test$i.ans"
    shasum -a 256 "test_out/lexer/test${i}_error.out" | awk '{ print $1 }' > "test_out/lexer/test${i}_error.ans"

    diff "test_out/lexer/test$i.ans" "test_out/lexer/test$i.hash"
    diff "test_out/lexer/test${i}_error.ans" "test_out/lexer/test${i}_error.hash"

    echo finish testing test$i lexer
done

echo finish test correct lexer
echo 
for ((i=1; i<=3; i++))
do
    echo testing error_test$i lexer
    python lexer.py test/test_error_lexer$i.dsl 1> test_out/lexer/error_test$i.out 2>test_out/lexer/error_test${i}_error.out

    shasum -a 256 "test_out/lexer/error_test$i.out" | awk '{ print $1 }' > "test_out/lexer/error_test$i.ans"
    shasum -a 256 "test_out/lexer/error_test${i}_error.out" | awk '{ print $1 }' > "test_out/lexer/error_test${i}_error.ans"

    diff "test_out/lexer/error_test$i.hash" "test_out/lexer/error_test$i.ans"
    diff "test_out/lexer/error_test${i}_error.ans" "test_out/lexer/error_test${i}_error.hash"

    echo finish testing test$i lexer
done

echo finish test wrong lexer
echo

echo ==============================
echo        Testing Parser
echo ==============================

for ((i=1; i<=3; i++))
do
    echo testing test$i parser
    python parser.py test/test$i.dsl 1> test_out/parser/test$i.out 2>test_out/parser/test${i}_error.out

    shasum -a 256 "test_out/parser/test$i.out" | awk '{ print $1 }' > "test_out/parser/test$i.ans"
    shasum -a 256 "test_out/parser/test${i}_error.out" | awk '{ print $1 }' > "test_out/parser/test${i}_error.ans"

    diff "test_out/parser/test$i.hash" "test_out/parser/test$i.ans"
    diff "test_out/parser/test${i}_error.hash" "test_out/parser/test${i}_error.ans"
    
    echo finish testing test$i parser
done

echo finish test correct parser
echo 

for ((i=1; i<=4; i++))
do
    echo testing error_test$i parser
    python parser.py test/test_error_parser$i.dsl 1> test_out/parser/error_test$i.out 2>test_out/parser/error_test${i}_error.out

    shasum -a 256 "test_out/parser/error_test$i.out" | awk '{ print $1 }' > "test_out/parser/error_test$i.ans"
    shasum -a 256 "test_out/parser/error_test${i}_error.out" | awk '{ print $1 }' > "test_out/parser/error_test${i}_error.ans"

    diff "test_out/parser/error_test$i.hash" "test_out/parser/error_test$i.ans"
    diff "test_out/parser/error_test${i}_error.hash" "test_out/parser/error_test${i}_error.ans"
    echo finish testing test$i parser
done

for ((i=1; i<=5; i++))
do
    python parser.py test/test_error_interpreter$i.dsl 1> test_out/parser/error_interpreter$i.out
done

echo finish test wrong parser
echo

echo ==============================
echo        Testing Interpreter
echo ==============================

for ((i=1; i<=3; i++))
do
    echo testing test$i interpreter
    python interpreter.py test_out/parser/test$i.out 1> test_out/interpreter/test$i.out 2>test_out/interpreter/test${i}_error.out

    shasum -a 256 "test_out/interpreter/test$i.out" | awk '{ print $1 }' > "test_out/interpreter/test$i.ans"
    shasum -a 256 "test_out/interpreter/test${i}_error.out" | awk '{ print $1 }' > "test_out/interpreter/test${i}_error.ans"

    diff "test_out/interpreter/test$i.hash" "test_out/interpreter/test$i.ans"
    diff "test_out/interpreter/test${i}_error.hash" "test_out/interpreter/test${i}_error.ans"

    echo finish testing test$i interpreter
done
echo finish test correct interpreter
echo 

for ((i=1; i<=5; i++))
do
    echo testing error_test$i interpreter
    python interpreter.py test_out/parser/error_interpreter$i.out 1> test_out/interpreter/error_test$i.out 2>test_out/interpreter/error_test${i}_error.out

    shasum -a 256 "test_out/interpreter/error_test$i.out" | awk '{ print $1 }' > "test_out/interpreter/error_test$i.ans"
    shasum -a 256 "test_out/interpreter/error_test${i}_error.out" | awk '{ print $1 }' > "test_out/interpreter/error_test${i}_error.ans"

    diff "test_out/interpreter/error_test$i.hash" "test_out/interpreter/error_test$i.ans"
    diff "test_out/interpreter/error_test${i}_error.hash" "test_out/interpreter/error_test${i}_error.ans"

    echo finish testing test$i interpreter
done

echo finish test wrong interpreter
echo

for ((i=1; i<=5; i++))
do
    rm test_out/parser/error_interpreter$i.out
done

echo finish