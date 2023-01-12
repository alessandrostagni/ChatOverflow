set -euo pipefail
IFS=$'\n\t'

# Deploy indexer lambda
rm -f lambda/indexer/indexer.zip
pip install -r lambda/indexer/requirements.txt -t ./lambda/indexer/
(cd lambda/indexer/ && zip -r indexer.zip .)

# Deploy search lambda
rm -f lambda/search/search.zip
pip install -r lambda/search/requirements.txt -t ./lambda/search
(cd lambda/search/ && zip -r search.zip .)
terraform apply