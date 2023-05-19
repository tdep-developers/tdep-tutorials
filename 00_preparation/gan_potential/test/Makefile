test: predictions.nc
	sokrates_plot_predictions predictions.nc trajectory_test.nc --outfile plot_test.png
	python verify_predictions.py predictions.nc

predictions.nc:
	sokrates_compute --float32 --folder-model ../module/ samples/*/*/*/geometry.in

clean:
	rm -rf predictions.nc plot_test.png
