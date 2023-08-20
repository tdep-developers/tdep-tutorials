for folder in stride_*
do
	pushd $folder
	make
	popd
done

