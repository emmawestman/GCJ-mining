
cd compile

python compilegcj.py 2751486 0 java
python compilegcj.py 2751486 1 java

python compilegcj.py 2754486 1 C#
python compilegcj.py 6377668744314880 1 C#

python compilegcj.py 5644738749267968 1 C++
python compilegcj.py 5658068650033152 1 C++
python compilegcj.py 1674486 1 C++

cplus=( 1485490 1482494 1482429 1483485 1484496 )



# C++
for i in "${cplus[@]}"
do
    if [ $i -eq 1483485]
    then
          range=(0)
    else
          range=( 0 1 )
    fi
    for r in "${range[@]}"
    do
        python compilegcj.py $i $r 'C++'
    done
done







