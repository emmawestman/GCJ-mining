
cd compile

#all=( 5751500831719424 5658282861527040 5731331665297408 5706278382862336 5669245564223488 5658068650033152 2453486 2449486 2463486 2458486 2464487 2645486 2652486 2692487 2700486 2705486 2751486 2749486 2755486 1483485 1595491 1483488 1285485 1673486 1482494 1480492 1480487 1485488 1484496 1674486 1482492 1485490 )
#javacs=( 5751500831719424 5658282861527040 5731331665297408 5706278382862336 5669245564223488 5658068650033152 2453486 2449486 2463486 2458486 2464487 2645486 2652486 )
cplus=( 2705486 2751486 2749486 2755486 1483485 1595491 1483488 1285485 1673486 1482494 1480492 1480487 1485488 1484496 1674486 1482492 1485490 )
# 2692487 2700486
## C
#for i in "${all[@]}"
#do
#    if [ $i -eq '1483485'] 
#    then
#          range=(0)
#    else
#          range=( 0 1 )
#    fi
#    for r in "${range[@]}"
#    do
#        python compilegcj.py $i $r 'C'
#    done
#done#

## C#
#for i in "${javacs[@]}"
#do
#    if [ $i -eq '1483485']
#    then
#          range=(0)
#    else
#          range=( 0 1 )
#    fi
#    for r in "${range[@]}"
#    do
#        python compilegcj.py $i $r 'C#'
#    done
#done#

## Java
#for i in "${javacs[@]}"
#do
#    if [ $i -eq '1483485']
#    then
#          range=(0)
#    else
#          range=( 0 1 )
#    fi
#    for r in "${range[@]}"
#    do
#        python compilegcj.py $i $r 'java'
#    done
#done#

## Python
#for i in "${all[@]}"
#do
#    if [ $i -eq '1483485']
#    then
#          range=(0)
#    else
#          range=( 0 1 )
#    fi
#    for r in "${range[@]}"
#    do
#        python compilegcj.py $i $r 'Python'
#    done
#done

# C++
for i in "${cplus[@]}"
do
    if [ $i -eq '1483485']
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







