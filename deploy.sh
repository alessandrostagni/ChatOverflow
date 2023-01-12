set -euo pipefail
IFS=$'\n\t'

pip install -r lambda/indexer/requirements.txt -t .lambda/indexer/
zip -r lambda/indexer/indexer.zip ./lambda/indexer/
pip install -r lambda/search/requirements.txt -t ./lambda/search
zip -r lambda/search/search.zip ./lambda/search/
terraform apply