#! /bin/bash

for (( i=1; i <= 5; i++ ))
do

    userid=$i

    curl https://api.instagram.com/v1/users/$userid/follows?access_token=XXXXXX    > followers/$userid.followers
    curl https://api.instagram.com/v1/users/$userid/followed-by?access_token=XXXXXX  > followedby/$userid.followedby

done
