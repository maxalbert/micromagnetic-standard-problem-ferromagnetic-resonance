.PHONY: figure_clean
.PHONY: data_clean

transform_data = mxs_ft_abs.npy mys_ft_abs.npy mzs_ft_abs.npy\
	             mxs_ft_phase.npy mys_ft_phase.npy mzs_ft_phase.npy\

all: data figures

figures: ${transform_data}
	python ../postprocessing.py --figures --software OOMMF

${transform_data}:
	python ../postprocessing.py --transform --software OOMMF

data: dynamic_stage.mif relaxation_stage.mif oommf_postprocessing.py generate_data.sh
	./generate_data.sh

relax.omf: relaxation_stage.mif
	tclsh $(OOMMFTCL) boxsi +fg relaxation_stage.mif -exitondone 1
	mv relax-*omf relax.omf

figure_clean:
	rm -f *.pdf

data_clean:
	rm -f *.omf
	rm -f *.odt
	rm -f *.npy
	rm -f *.txt

clean_all:
	rm -f *.omf
	rm -f *.odt
	rm -f *.pdf
	rm -f *.npy
	rm -f *.txt
