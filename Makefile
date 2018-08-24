PKG_PATH=./pkg
PKG_ZIP=enlightenme.zip
LIB_PATH=./enlightenme_lambda

LAMBDA_FUNC_NAME=enlightenme_lambda
AWS_S3_BUCKET_NAME=enlighten-me-bucket
AWS_PROFILE_NAME=enlightenme-lambda

clean:
	echo "cleaning $(PKG_PATH)"
	rm -rf $(PKG_PATH)
	rm -rf $(PKG_ZIP)
	rm -rf requirements.txt

prepare:
	mkdir $(PKG_PATH)
	pipenv lock --requirements > requirements.txt
	pipenv run pip install -r requirements.txt -t $(PKG_PATH)
	cp $(LIB_PATH)/* $(PKG_PATH)
	cd $(PKG_PATH) && zip -r -D ../$(PKG_ZIP) *

deploy:
	aws s3 cp $(PKG_ZIP) s3://$(AWS_S3_BUCKET_NAME) --profile $(AWS_PROFILE_NAME)
	aws lambda get-function --function-name $(LAMBDA_FUNC_NAME)
	aws lambda update-function-code --function-name $(LAMBDA_FUNC_NAME) --s3-bucket $(AWS_S3_BUCKET_NAME) --s3-key $(PKG_ZIP) --publish
