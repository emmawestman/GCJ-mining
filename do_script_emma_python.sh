cd compile
#all=( 5652388522229760 5644738749267968 5634697451274240 5738606668808192 5636311922769920 5631989306621952 5630113748090880 5631572862566400 5648941810974720 5695413893988352 5686313294495744 5753053697277952 5744014401732608 5708921029263360 5639104758808576 5686275109552128 5670465267826688 5658571765186560 6404600001200128 5765824346324992 6377668744314880 5688567749672960 5769900270288896 5662291475300352 5640146288377856 5708284669460480 5646553574277120 5756407898963968 )
all=( 5634947029139456_1 5636311922769920_0 5636311922769920_1 5639104758808576_0 5639104758808576_1 5640146288377856_0 5640146288377856_1 5644738749267968_0 5644738749267968_1 5646553574277120_0 5646553574277120_1 5648941810974720_0 5648941810974720_1 5652388522229760_0 5652388522229760_1 5658068650033152_0 5658068650033152_1 5658282861527040_0 5658282861527040_1 5658571765186560_0 5658571765186560_1 5662291475300352_0 5662291475300352_1 5669245564223488_0 5669245564223488_1 5670465267826688_0 5670465267826688_1 5686275109552128_0 5686275109552128_1 5686313294495744_0 5686313294495744_1 5688567749672960_0 5688567749672960_1 5690574640250880_0 5690574640250880_1 5695413893988352_0 5695413893988352_1 5706278382862336_0 5706278382862336_1 5708284669460480_0 5708284669460480_1 5708921029263360_0 5708921029263360_1 5709773144064000_0 5709773144064000_1 5731331665297408_0 5731331665297408_1 5738606668808192_0 5738606668808192_1 5744014401732608_0 5744014401732608_1 5751500831719424_0 5751500831719424_1 5752104073297920_0 5753053697277952_0 5753053697277952_1 5765824346324992_0 5765824346324992_1 5766201229705216_0 5766201229705216_1 5769900270288896_0 5769900270288896_1 6377668744314880_0 6377668744314880_1 6404600001200128_1 )

# C
for i in "${all[@]}"
  do
    python compilegcj.py $i 'Python'
  done
