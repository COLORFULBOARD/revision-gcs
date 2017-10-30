# Revision GCS Client

Google Cloud Storage client for [Revision](https://github.com/COLORFULBOARD/revision).

## Before you begin

1. Enable API

Enable the Google Cloud Storage API.

2. Create service account

Set up authentication with a service account for your project so you can access the API from your machine.

3. Install `Revision GCS`

Install the client library.

```sh
$ pip install revision-gcs
```

## Options

You must configure in `.revision.json` as follow:

```javascript
{
  "clients": [
    {
      "key": "YOUR_KEY", // Dataset unique key
      "module": "revision_gcs.GCSClient",
      "local_path": "PATH/TO/LOCAL_PATH",
      "remote_path": "PATH/TO/REMOTE_STORAGE_PATH", // Required: Specify your storage bucket uri
      "revision_file": "CHANGELOG.md", // Optional: Default: CHANGELOG.md
      "options": {
        "key_file": "PATH/TO/KEY_FILE" // Required: Specify the path for service account keyfile
      }
    }
  ]
}
```

## Sample

Samples are in the [sample/](https://github.com/COLORFULBOARD/revision-gcs/tree/master/sample) directory.

```sh
$ cd sample/cli
$ revision sample commit
$ revision sample push
$ revision sample pull
```

## License

Revision is licensed under MIT License. See [LICENSE](https://github.com/COLORFULBOARD/revision-gcs/blob/master/LICENSE) for more information.
