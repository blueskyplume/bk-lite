.PHONY: all build icons worker linux-worker nsis clean check-deps

WORKER = setup-worker.exe
INSTALLER = collector-sidecar-installer.exe
LINUX_INSTALLER = bklite-monitor-installer

all: build

build: check-deps icons worker linux-worker nsis
	@echo "Build complete: $(INSTALLER)"
	@ls -lh $(INSTALLER)
	@ls -lh $(LINUX_INSTALLER)

icons:
	@python3 gen_icon.py

worker:
	GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o $(WORKER) setup-worker.go
	@ls -lh $(WORKER)

linux-worker:
	GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o $(LINUX_INSTALLER) setup-worker.go
	@ls -lh $(LINUX_INSTALLER)

nsis:
	makensis -V2 setup.nsi

check-deps:
	@which makensis >/dev/null || (echo "NSIS not installed"; exit 1)
	@which go >/dev/null || (echo "Go not installed"; exit 1)
	@python3 -c "from PIL import Image" 2>/dev/null || (echo "Pillow not installed"; exit 1)

clean:
	rm -f $(WORKER) $(INSTALLER) $(LINUX_INSTALLER) installer.ico header.bmp wizard.bmp
