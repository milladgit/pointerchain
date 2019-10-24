
COMPILER=pgcc

# For PGI
C_FLAGS=-c99 -Mkeepasm -O0 -g

# Device
TARGET_DEV=tesla:cc50

# For OpenACC
OPENACC=-acc -ta=$(TARGET_DEV),keepptx
OPENACC_MANAGED=-acc -ta=$(TARGET_DEV),keepptx,managed


BIN_FOLDER=./bin
ASM_FOLDER=./asm


# all: makebin sourceobjdump sourceasm

all: makebin uvm pointerchain


makebin:
	mkdir -p $(BIN_FOLDER)
	mkdir -p $(ASM_FOLDER)



uvm: makebin
	$(COMPILER) $(C_FLAGS) $(OPENACC_MANAGED) source.c -o $(BIN_FOLDER)/source_mananged
	mv source.s $(ASM_FOLDER)/source_mananged.s
	mv source.n001.ptx ./asm/source_managed_ptx.ptx
	objdump -S --disassemble $(BIN_FOLDER)/source_mananged > $(ASM_FOLDER)/source_objdump_managed.s
	$(COMPILER) $(C_FLAGS) -S $(OPENACC_MANAGED) source.c -o $(ASM_FOLDER)/source_asm_managed.s
	rm -rf *.ptx *.s

pointerchain: makebin 
	$(COMPILER) $(C_FLAGS) $(OPENACC) source.c -o $(BIN_FOLDER)/source
	mv source.s $(ASM_FOLDER)/source.s
	mv source.n001.ptx ./asm/source_ptx.ptx
	objdump -S --disassemble $(BIN_FOLDER)/source > $(ASM_FOLDER)/source_objdump.s
	$(COMPILER) $(C_FLAGS) -S $(OPENACC) source.c -o $(ASM_FOLDER)/source_asm.s
	rm -rf *.ptx *.s



#########################################################################################################
#########################################################################################################
#########################################################################################################



source: source.c
	$(COMPILER) $(C_FLAGS) $(OPENACC) source.c -o $(BIN_FOLDER)/source
	mv source.s $(ASM_FOLDER)/source.s
	mv source.n001.ptx ./asm/source_ptx.ptx
	$(COMPILER) $(C_FLAGS) $(OPENACC_MANAGED) source.c -o $(BIN_FOLDER)/source_mananged
	mv source.s $(ASM_FOLDER)/source_mananged.s
	mv source.n001.ptx ./asm/source_managed_ptx.ptx

sourceobjdump: source
	objdump -S --disassemble $(BIN_FOLDER)/source > $(ASM_FOLDER)/source_objdump.s
	objdump -S --disassemble $(BIN_FOLDER)/source_mananged > $(ASM_FOLDER)/source_objdump_managed.s

sourceasm: source.c
	$(COMPILER) $(C_FLAGS) -S $(OPENACC) source.c -o $(ASM_FOLDER)/source_asm.s
	$(COMPILER) $(C_FLAGS) -S $(OPENACC_MANAGED) source.c -o $(ASM_FOLDER)/source_asm_managed.s
	rm -rf *.ptx *.s



#########################################################################################################
#########################################################################################################
#########################################################################################################



clean:
	rm -rf $(BIN_FOLDER) *.o $(ASM_FOLDER) *.ptx *.s
	rm -rf */$(BIN_FOLDER) */*.o */$(ASM_FOLDER) */*.ptx */*.s
	rm -rf */*/$(BIN_FOLDER) */*/*.o */*/$(ASM_FOLDER) */*/*.ptx */*/*.s

