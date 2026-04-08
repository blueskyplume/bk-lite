# Sidecar Installer Build & Release Runbook

## Artifacts

- Windows installer filename: `bklite-controller-installer.exe`
- Linux installer filename: `bklite-controller-installer`

Default object storage layout:

- Versioned path: `installer/<os>/<version>/<filename>`
- Latest alias path: `installer/<os>/<filename>`

Examples:

- `installer/windows/v1.2.3/bklite-controller-installer.exe`
- `installer/windows/bklite-controller-installer.exe`
- `installer/linux/v1.2.3/bklite-controller-installer`
- `installer/linux/bklite-controller-installer`

## Build

From `agents/sidecar-installer/`:

```bash
make build
```

Outputs:

- Windows NSIS installer: `bklite-controller-installer.exe`
- Linux installer binary: `bklite-controller-installer`

## Upload

From `server/`:

```bash
python manage.py installer_init --os windows --file_path /path/to/bklite-controller-installer.exe --version v1.2.3
python manage.py installer_init --os linux --file_path /path/to/bklite-controller-installer --version v1.2.3
```

Upload behavior:

1. Uploads to the versioned artifact path
2. Refreshes the latest alias path

## Runtime APIs

### Installer session

- `GET /api/v1/node_mgmt/open_api/installer/session?token=...`

Returns the installer session consumed by both Windows and Linux installers.

### Installer manifest

- `GET /api/proxy/node_mgmt/api/installer/manifest/`

Returns latest artifact metadata for Windows and Linux.

### Installer metadata by OS

- `GET /api/proxy/node_mgmt/api/installer/metadata/windows/`
- `GET /api/proxy/node_mgmt/api/installer/metadata/linux/`

Returns latest artifact metadata for the target OS.

## Cloud Region Variables

Recommended direct-download variables:

- `NATS_SERVERS`
- `NATS_PROTOCOL`
- `NATS_TLS_CA`
- `NATS_DOWNLOAD_USERNAME`
- `NATS_DOWNLOAD_PASSWORD`
- `NATS_INSTALLER_BUCKET`

Fallbacks still exist, but the preferred model is a dedicated download-only credential and bucket.
