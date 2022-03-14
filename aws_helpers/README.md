# AWS Helpers

## Synopsis
A tool to help learn the underlying technology of the AWS API as well as to maintain environments and to learn cloud.


## Assumptions
* All AWS services can be accessed through specific API endpoints using raw requests.
* AWS requires some sort of authentication.
* Endpoints might have different versions.
* Authentication is done the same regardless of version.
* Any additional dependencies wil be met using defaults in AWS.

## Requirements
* Users will be able to list/stop/start/remove/fetch EC2 instances.
* Users will be able to list/fetch/add/remove S3 items.
* Users will be able to list/fetch/add/remove/connect to RDS instances.

## Disclaimer
Please note that this is a work-in-progress (WIP) project and should be considered incomplete.  Additional information may be added and the helpers may be restructured/reimplemented.  Also note that all requests will be done as if no SDK exists and all criticism is subject to experience and opinions on API design.

## SDK's
The simplest way to interact with AWS is an SDK.  Most languages have one, but they all might use different syntax's.  

|Language                       | SDK                                                                                                                |
|--|--| 
|Python                         | boto3                                                                                                              |
|Go                             | https://docs.aws.amazon.com/sdk-for-go/api/service/ec2/#EC2.DescribeHosts                                          |
|PHP                            | https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-ec2-2016-11-15.html#describehosts                               |
|Java                           | https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/ec2/Ec2Client.html#describeHosts--       |
|Ruby                           | https://docs.aws.amazon.com/sdk-for-ruby/v3/api/Aws/EC2/Client.html#describe_hosts-instance_method                 |


## RAW REST
In some cases, for education or for consistency with implementation, raw REST calls can also be made as long as the service (ec2), region (us-east-2), and the access/secret keys are known.  From there, you would generate the request, which consists of the Action and Version parameters along with the Host, Authorization, and X-AMZ-DATE headers.  Note that all dates should be in UTC format.

### Authorization
The API authorization is done through the Authorization header in the following format:
Authorization AWS4-HMAC-SHA256 Credential=<api-key>/<date>/<region>/<service>/aws4_request, SignedHeaders=host;x-amz-date, Signature=<signature>

The signature is a 256-encoded hmac of the canonical request.


## Retrospective
* My first note here is that clearly boto3 would have made things A LOT simpler, but if implementing a standardized API from scratch, it starts with the raw calls.
* Although most of the API calls are relatively simple, I think the way that authentication is done wasn't well thought out.
    * First off, it depends on a canonical representation of the request that's already being sent, unless the request is being published to a raw socket, there should be a better way.
    * I will say that this beats MFA and the signature can be generated through code, I just don't think it shouldn't require 7 steps to do so.
    * Another possible reason why the API was designed this way was possibly for debugging, which still shouldn't be needed if server logs are enabled.
        * A decodable hash of the full request, which includes the user's secret key by the way, should never be needed for debugging.
* The one caveat is that I'm using an older version of the API (2016) and the authentication may have changed.  
    * If this is the case, then it would have severely broken backwards compatibility and I have strong doubts that Amazon would do that.
    * The version flag should only be used if a function was implemented in a specific version or a specific implementation of an existing function is required.

## Closing thoughts
* If leveraging AWS through a single programming language, stick with the SDK.
* If leveraging AWS through multiple programming languages and want to make a standard, try to keep it as simple as possible, as with all code.
    * It may also help to break up components into separate modules

## References
* https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html 
* https://us-west-2.console.aws.amazon.com/console 
* https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Welcome.html 
* https://blog.knoldus.com/how-to-generate-aws-signature-with-postman/ 
* https://stackoverflow.com/questions/45075750/how-to-pass-access-credentials-in-request-with-aws-api 
* https://blog.scottlowe.org/2020/04/10/using-postman-to-launch-ec2-instance-via-api-calls/ 
* https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3_Authentication2.html 
* https://docs.aws.amazon.com/general/latest/gr/rande.html 

