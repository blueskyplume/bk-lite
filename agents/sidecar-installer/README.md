# Sidecar Installer Build & Release Runbook

## Artifacts

- Windows installer filename: `bklite-monitor-installer.exe`
- Linux installer filename: `bklite-monitor-installer`

Default object storage layout:

- Versioned path: `installer/<os>/<version>/<filename>`
- Latest alias path: `installer/<os>/<filename>`

Examples:

- `installer/windows/v1.2.3/bklite-monitor-installer.exe`
- `installer/windows/bklite-monitor-installer.exe`
- `installer/linux/v1.2.3/bklite-monitor-installer`
- `installer/linux/bklite-monitor-installer`

## Build

From `agents/sidecar-installer/`:

```bash
make build
```

Outputs:

- Windows NSIS installer: `collector-sidecar-installer.exe`
- Linux installer binary: `bklite-monitor-installer`

## Upload

From `server/`:

```bash
python manage.py installer_init --os windows --file_path /path/to/collector-sidecar-installer.exe --version v1.2.3
python manage.py installer_init --os linux --file_path /path/to/bklite-monitor-installer --version v1.2.3
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
