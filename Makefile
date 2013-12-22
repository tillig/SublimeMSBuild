
all: build

build: clean
	zip MSBuild.sublime-package *

clean:
	rm -rf MSBuild.sublime-package

deploy: build
	cp MSBuild.sublime-package ~/.config/sublime-text-3/Installed\ Packages/