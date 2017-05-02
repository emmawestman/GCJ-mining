
cd compile


python=( 1480487 24449486 5690 5709773144064000 5751500831719424 5765824346324992 )
cplus=( 5634947029139456 5669245564223488 5688567749672960 4690574640250880 5709773144064000 5751500831719424 5765824346324992 5766201229705216 )

# C
#for i in "${all[@]}"
#do
#    if [ $i -eq '5756407898963968']
#    then
#        range=( 0 )
#    elif [$i -eq '5752104073297920']
#    then
#        range=( 0 )
#      else
#        range=( 0 1 )
#    fi
#    for r in "${range[@]}"
#    do
#        python compilegcj.py $i $r 'C'
#    done
#done

# Python
for i in "${python[@]}"
do
    if [ $i -eq 2449486 ]
    then
        range=( 0 )
    else
        range=( 0 1 )
    fi
    for r in "${range[@]}"
    do
        python compilegcj.py $i $r "Python"
    done
done

# C++
for i in "${cplus[@]}"
do
    if [ $i -eq 5634947029139456]
    then
        range=( 0 )
    else
        range=( 0 1 )
    fi
    for r in "${range[@]}"
    do
        python compilegcj.py $i $r "C++"
    done
done


