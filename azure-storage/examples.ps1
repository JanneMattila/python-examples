$storage = "<your storage account name>"
$tenantId = "<your tenant id>"

Login-AzAccount
Login-AzAccount -Tenant $tenantId

$accessToken = Get-AzAccessToken -ResourceUrl "https://$storage.blob.core.windows.net/"
$secureAccessToken = ConvertTo-SecureString -AsPlainText -String $accessToken.Token

Invoke-RestMethod `
    -Method "GET" `
    -Headers @{ "x-ms-version" = "2022-11-02" } `
    -Authentication Bearer `
    -Token $secureAccessToken `
    -Uri "https://$storage.blob.core.windows.net/block-blobs/demo.bin?comp=blocklist&blocklisttype=all" 

# Example output (formatted):
# ---------------------------
# <?xml version="1.0" encoding="utf-8"?>
# <BlockList>
#   <CommittedBlocks>
#     <Block>
#       <Name>NGM0MjI4YjMtNWM5Mi00YzEwLWEyN2QtYzk4YTcyMzZkOWEy</Name>
#       <Size>268435456</Size>
#     </Block>
#     <Block>
#       <Name>NmUzM2JkNTQtOGIxNi00NDBhLTk2ZDctMTE5ZWYyYjQyYWM5</Name>
#       <Size>255852544</Size>
#     </Block>
#   </CommittedBlocks>
#   <UncommittedBlocks />
# </BlockList>
