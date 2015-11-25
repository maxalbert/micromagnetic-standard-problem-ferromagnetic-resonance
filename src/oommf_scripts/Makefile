.PHONY: figure_clean
.PHONY: data_clean

transform_data = mxs_ft_abs.npy mys_ft_abs.npy mzs_ft_abs.npy\
                 mxs_ft_phase.npy mys_ft_phase.npy mzs_ft_phase.npy\

all: data figures

figures: ${transform_data}
	python ../postprocessing.py --figures --software OOMMF

${transform_data}:
	python ../transform_data.py --software OOMMF

data:
	./generate_data.sh

figure_clean:
	rm -f *.pdf
