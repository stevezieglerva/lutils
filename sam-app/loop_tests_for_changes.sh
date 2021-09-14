#!/bin/bash
source venv/bin/activate


chsum1=""
export test_pattern="test*unit*.*"

while [[ true ]]
do
    chsum2=`find . -type f -mtime -2s -prune -exec md5 {} \;`
    if [[ $chsum1 != $chsum2 ]] ; then
            echo ""
            echo "$(date) Starting ..."
            python3 test_and_format.py tests/ "$test_pattern" | grep -E "✅|❗|❌|👍|😡" 
        chsum1=$chsum2
    fi
    sleep 2
done  





