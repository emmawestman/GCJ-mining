
cd compile
array=( 2464487 2645486 2652486 )
for i in "${array[@]}"
do
	cat <<EOF> ../p_ids.in
	i
EOF
done

