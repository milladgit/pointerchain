
FONT = -fCourier14

all:
	enscript -Ecpp $(FONT) ../simple/uvm/source.c --color=1 -o - | ps2pdf - lvl0-uvm.pdf
	enscript -Ecpp $(FONT) ../simple/pointerchain/source.c --color=1 -o - | ps2pdf - lvl0-pointerchain.pdf
	enscript -Ecpp $(FONT) ../struct_level_1/uvm/source.c --color=1 -o - | ps2pdf - lvl1-uvm.pdf
	enscript -Ecpp $(FONT) ../struct_level_1/pointerchain/source.c --color=1 -o - | ps2pdf - lvl1-pointerchain.pdf
	enscript -Ecpp $(FONT) ../struct_level_2/uvm/source.c --color=1 -o - | ps2pdf - lvl2-uvm.pdf
	enscript -Ecpp $(FONT) ../struct_level_2/pointerchain/source.c --color=1 -o - | ps2pdf - lvl2-pointerchain.pdf
	enscript -Ecpp $(FONT) ../struct_level_3/uvm/source.c --color=1 -o - | ps2pdf - lvl3-uvm.pdf
	enscript -Ecpp $(FONT) ../struct_level_3/pointerchain/source.c --color=1 -o - | ps2pdf - lvl3-pointerchain.pdf

