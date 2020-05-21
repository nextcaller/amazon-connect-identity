# Next Caller Identity API for Amazon Connect

Cloudformation template and Python script to invoke Next Caller's Identity API function. The function can be used in conjunction with Amazon's Connect platform to resolve Name and Address Information for a given caller.

## Usage

Use `sam` to build, invoke and deploy the function.

##### SAM Build:
`sam build -b build -t aws/stack.yaml --use-container`

##### SAM Invoke:
There are a few sample events in the [events](events/) folder. You can modify them as needed to invoke this locally.

`sam local invoke -t build -t build/template.yaml -e example_events/REPLACE_ME --parameter-overrides ParameterKey=LogLevel,ParameterValue=INFO ParameterKey=IdentityAPIUsername,ParameterValue=REPLACE_ME ParameterKey=IdentityAPIPassword,ParameterValue=REPLACE_ME`

##### SAM Deploy:
`sam deploy -t build/template.yaml --s3-bucket REPLACE_ME --stack-name REPLACE_ME --parameter-overrides ParameterKey=LogLevel,ParameterValue=INFO ParameterKey=IdentityAPIUsername,ParameterValue=REPLACE_ME ParameterKey=IdentityAPIPassword,ParameterValue=REPLACE_ME --capabilities CAPABILITY_IAM`

##### Unit Tests:
Unit tests can be ran by installing this project in a virtual environment and running pytest. A helper script is located the [scripts](./scripts) directory:

* `python -m venv ve`
* `./ve/bin/pip install --upgrade pip`
* `source ve/bin/activate`
* `pip install -e .[test]`