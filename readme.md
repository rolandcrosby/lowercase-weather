## lowercase weather gang

this is [a bot](https://twitter.com/lowercasewx) that tweets everything that [capital weather gang](https://twitter.com/capitalweather) tweets, but in lowercase.

if you are affiliated with capital weather gang and would like me to cease and/or desist, please [email](mailto:roland@rolandcrosby.com) or [dm](https://twitter.com/roooooland) me.

## tech notes

the script runs as an aws lambda function. it stores its state (currently just the high-water mark of tweets it has reposted) as a tag on the function itself. for this to work, the function's iam role needs to be granted the `lambda:listtags`, `lambda:tagresource`, and `lambda:untagresource` permissions, scoped to the function's own arn. a cloudwatch event triggers the function periodically.

## credits

profile image: [aj200224 on wikimedia commons](https://commons.wikimedia.org/wiki/File:United_States_Capital.jpg)  
header image: [roberto nickson on unsplash](https://unsplash.com/photos/z71SFYFy5dQ)