cd compile
#all=( 5652388522229760 5644738749267968 5634697451274240 5738606668808192 5636311922769920 5631989306621952 5630113748090880 5631572862566400 5648941810974720 5695413893988352 5686313294495744 5753053697277952 5744014401732608 5708921029263360 5639104758808576 5686275109552128 5670465267826688 5658571765186560 6404600001200128 5765824346324992 6377668744314880 5688567749672960 5769900270288896 5662291475300352 5640146288377856 5708284669460480 5646553574277120 5756407898963968 )
all=( 6377668744314880 5688567749672960 5769900270288896 5662291475300352 5640146288377856 5708284669460480 5646553574277120 5756407898963968 )

# C
for i in "${all[@]}"
do
    range=( 0 1 )

    for r in "${range[@]}"
    do
        python compilegcj.py $i $r 'java'
    done
done








