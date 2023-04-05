# Azure Storage demos

## Block blob

See more details at [Azure Storage demos](https://github.com/JanneMattila/azure-storage-demos).

Example output when uploading 512'000 KB file with two 256MB chunks:

```
>>> blob_client.stage_block(block_id=block_id, data=chunk)
Chunk 1

{'content_md5': None, 'client_request_id': '52da5626-cc81-11ed-bd22-7286e03d51bf', 'request_id': 'df4a8f52-201e-0008-778e-603246000000', 'version': '2021-12-02', 'date': datetime.datetime(2023, 3, 27, 9, 25, 33, tzinfo=datetime.timezone.utc), 'content_crc64': bytearray(b'\x19\x16\xb1\x1c\xd4\xcd\xbb#'), 'request_server_encrypted': True, 'encryption_key_sha256': None, 'encryption_scope': None}

>>> blob_client.stage_block(block_id=block_id, data=chunk)
Chunk 2

{'content_md5': None, 'client_request_id': '53ef9562-cc81-11ed-bd22-7286e03d51bf', 'request_id': 'df4a9203-201e-0008-708e-603246000000', 'version': '2021-12-02', 'date': datetime.datetime(2023, 3, 27, 9, 25, 35, tzinfo=datetime.timezone.utc), 'content_crc64': bytearray(b'\xfb\x88\xa0i\xc3W\xbbe'), 'request_server_encrypted': True, 'encryption_key_sha256': None, 'encryption_scope': None}

>>> blob_client.commit_block_list(block_list)

{'etag': '"0x8DB2EA538F3B850"', 'last_modified': datetime.datetime(2023, 3, 27, 9, 25, 36, tzinfo=datetime.timezone.utc), 'content_md5': None, 'content_crc64': bytearray(b'aOX\x9f\xa7S~\x11'), 'client_request_id': '54bb9d42-cc81-11ed-bd22-7286e03d51bf', 'request_id': 'df4a9410-201e-0008-498e-603246000000', 'version': '2021-12-02', 'version_id': None, 'date': datetime.datetime(2023, 3, 27, 9, 25, 35, tzinfo=datetime.timezone.utc), 'request_server_encrypted': True, 'encryption_key_sha256': None, 'encryption_scope': None}
```
