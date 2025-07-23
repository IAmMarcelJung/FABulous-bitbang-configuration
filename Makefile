MODULE = upload_bitstream
MODULES_DIR = modules
PY_FILES = $(MODULE).py $(wildcard $(MODULES_DIR)/*.py)
MPY_FILES = $(PY_FILES:.py=.mpy)
MPY_CROSS = mpy-cross


%.mpy: %.py
	$(MPY_CROSS) $<

upload: $(MPY_FILES)
	sync
	mpremote mount . exec "import $(MODULE); $(MODULE).run()"


clean:
	$(RM) $(MPY_FILES)

.PHONY: clean
