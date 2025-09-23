BUILD_DIR := build
RELEASE_DIR := release
SKIN_DIR := skins
ROM := nestris
BUILD_PATH := $(BUILD_DIR)/$(ROM).nes
SRC_FILES := $(shell find src -name "*.fab" -or -name '*.macrofab')

SKIN := $(shell ./scripts/get_skin.sh)
SKIN_PATH := $(SKIN_DIR)/$(SKIN)
SKIN_FILES := $(shell find ${SKIN_PATH} -type f)

$(BUILD_PATH): $(ROM).cfg config.fab $(SRC_FILES) $(SKIN_FILES) | buildDir
	./nesfab/nesfab $(ROM).cfg
	python scripts/patch_mmc1.py

.PHONY: clean run release buildDir releaseDir

run: $(BUILD_PATH)
	mesen $(BUILD_PATH)

release: | releaseDir
	cp $(BUILD_PATH) $(RELEASE_DIR)/$(ROM).nes
	zip $(RELEASE_DIR)/$(ROM).zip $(BUILD_PATH).nes

buildDir:
	@mkdir -p $(BUILD_DIR)

releaseDir:
	@mkdir -p $(RELEASE_DIR)

clean:
	rm -f $(BUILD_DIR)/*
	rm -f $(RELEASE_DIR)/*
