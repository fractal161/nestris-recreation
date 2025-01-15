build/nestris.nes: nestris.cfg config.fab src/*.fab src/*.macrofab | buildDir
	./nesfab/nesfab nestris.cfg

run: build/nestris.nes
	mesen build/nestris.nes

release: | releaseDir
	cp build/nestris.nes release/nestris.nes
	zip release/nestris.zip build/nestris.nes

buildDir:
	mkdir -p build

releaseDir:
	mkdir -p release

clean:
	rm build/*
