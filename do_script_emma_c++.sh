cd compile

all=( 5690574640250880_1  5695413893988352_0 5695413893988352_1 5708284669460480_0 5708284669460480_1 5708921029263360_0 5708921029263360_1 5709773144064000_0 5709773144064000_1 5738606668808192_0 5738606668808192_1 5744014401732608_0 5744014401732608_1 5751500831719424_0 5751500831719424_1 5752104073297920_0 5753053697277952_0 5753053697277952_1 5756407898963968_0 5765824346324992_0 5765824346324992_1 5766201229705216_0 5766201229705216_1 5769900270288896_0 5769900270288896_1 6377668744314880_0 6377668744314880_1 6404600001200128_0 6404600001200128_1 )
# C++
for i in "${all[@]}"
  do
    python compilegcj.py $i 'C++'
  done
