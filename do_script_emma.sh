
cd compile

#2749486

all=( 2749486 5709773144064000 5690574640250880 5634947029139456 5766201229705216 5752104073297920 5751500831719424 5658282861527040 5731331665297408 5706278382862336 5669245564223488 5658068650033152 2453486 2449486 2463486 2458486 2464487 2645486 2652486 2692487 2700486 2705486 2751486 2755486 1483485 1595491 1483488 1285485 1673486 1482494 1480492 1480487 1485488 1484496 1674486 1482492 1485490  )

# C
for i in "${all[@]}"
do
    range=( 0 1 )

    for r in "${range[@]}"
    do
        python compilegcj.py $i $r 'C'
    done
done




