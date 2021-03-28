# Crons

This is a place where I keep various Lambda scripts, which I configure as scheduled events. Feel free to use/modify them as desired.

## Making updates

To update the Lambda, [create a Python deployment package](http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) containing the Python script, as well as any dependencies necessary. Then, upload this .zip file to Lambda.

### Generating the package

    rm -rf ./build
    mkdir ./build
    cp -r ./mycron/ ./build
    pip install -r ./mycron/requirements.txt -t ./build
    zip -r lambda.zip ./build
