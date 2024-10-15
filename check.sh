function checkSolution() {
    for i in {1..2}; do
        if diff <(python3 $1 < data/secret/subtask$i/1.in) data/secret/subtask$i/1.ans; then
            echo "$i - OK"
        else
            echo "FAIL"
            return
        fi
    done
}