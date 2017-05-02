
cd compile



cplus=( 5669245564223488 5688567749672960 5690574640250880 5709773144064000 5751500831719424 5765824346324992 5766201229705216 )

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

python compilegcj.py 1480487 0 Python
python compilegcj.py 1480487 1 Python
#python compilegcj.py 2449486 1 Python
python compilegcj.py 5751500831719424 0 Python
python compilegcj.py 5751500831719424 1 Python
python compilegcj.py 5644738749267968 1 Python

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


